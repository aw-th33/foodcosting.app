"""
Create Buffer draft posts from an approved social manifest.

Usage:
    python scripts/buffer/create_drafts.py \
        --manifest pipeline/social/ready/example-video.json \
        --output pipeline/context/buffer-drafts-created.json

Dry run:
    python scripts/buffer/create_drafts.py --manifest <manifest> --dry-run

The script intentionally creates Buffer drafts, not scheduled/published posts.
Ahmed reviews and schedules the drafts inside Buffer.
"""

import argparse
import hashlib
import json
import mimetypes
import os
import struct
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPO_ROOT / "pipeline" / "context" / "buffer-drafts-created.json"
BUFFER_API_URL = "https://api.buffer.com"
CLOUDINARY_UPLOAD_URL = "https://api.cloudinary.com/v1_1/{cloud_name}/{resource_type}/upload"

POST_TYPES = {"video", "carousel", "still"}
DEFAULT_CHANNELS = {
    "video": ["instagram", "youtube", "facebook"],
    "carousel": ["instagram", "facebook"],
    "still": ["instagram", "facebook"],
}
CHANNEL_ENVS = {
    "instagram": "BUFFER_CHANNEL_INSTAGRAM",
    "youtube": "BUFFER_CHANNEL_YOUTUBE",
    "facebook": "BUFFER_CHANNEL_FACEBOOK",
    "linkedin": "BUFFER_CHANNEL_LINKEDIN",
}
VIDEO_EXTENSIONS = {".mp4"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
MAX_FREE_VIDEO_BYTES = 100 * 1024 * 1024
WARN_VIDEO_BYTES = 25 * 1024 * 1024
WARN_IMAGE_BYTES = 5 * 1024 * 1024


class ValidationError(Exception):
    """Raised when the manifest or environment is unsafe to process."""


def load_env():
    """Load .env from repo root into os.environ without overriding existing vars."""
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key and value and key not in os.environ:
            os.environ[key] = value


def write_json(data, output_path=None):
    serialized = json.dumps(data, indent=2, ensure_ascii=False)
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(serialized, encoding="utf-8")
        print(f"Written to {path}", file=sys.stderr)
    else:
        print(serialized)


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path} is not valid JSON: {exc}") from exc


def resolve_asset_path(asset, manifest_path):
    path = Path(asset)
    if path.is_absolute():
        return path

    repo_relative = REPO_ROOT / path
    if repo_relative.exists():
        return repo_relative

    manifest_relative = manifest_path.parent / path
    return manifest_relative


def default_channels_for(post_type):
    return list(DEFAULT_CHANNELS[post_type])


def load_manifest(manifest_path):
    manifest_path = Path(manifest_path).resolve()
    manifest = read_json(manifest_path)
    post_type = manifest.get("post_type")
    if post_type not in POST_TYPES:
        raise ValidationError("manifest.post_type must be one of: video, carousel, still")

    manifest.setdefault("channels", default_channels_for(post_type))
    manifest["_manifest_path"] = str(manifest_path)
    manifest["_manifest_dir"] = str(manifest_path.parent)
    return manifest


def validate_manifest(manifest):
    warnings = []
    status = manifest.get("status")
    if status != "ready_for_buffer":
        raise ValidationError("manifest.status must be ready_for_buffer")

    for field in ("post_type", "assets", "title", "caption_base", "channels"):
        if field not in manifest:
            raise ValidationError(f"manifest.{field} is required")

    post_type = manifest["post_type"]
    assets = manifest["assets"]
    channels = manifest["channels"]

    if not isinstance(assets, list) or not assets:
        raise ValidationError("manifest.assets must be a non-empty array")
    if not isinstance(channels, list) or not channels:
        raise ValidationError("manifest.channels must be a non-empty array")

    unknown_channels = [c for c in channels if c not in CHANNEL_ENVS]
    if unknown_channels:
        raise ValidationError(f"unsupported channel(s): {', '.join(unknown_channels)}")
    if post_type != "video" and "youtube" in channels:
        raise ValidationError("YouTube drafts are only supported for video posts")

    if post_type == "video" and len(assets) != 1:
        raise ValidationError("video manifests must contain exactly one asset")
    if post_type == "still" and len(assets) != 1:
        raise ValidationError("still manifests must contain exactly one asset")
    if post_type == "carousel" and not (2 <= len(assets) <= 10):
        raise ValidationError("carousel manifests must contain 2 to 10 image assets")

    captions = manifest.get("captions", {})
    if captions is not None and not isinstance(captions, dict):
        raise ValidationError("manifest.captions must be an object when provided")
    for channel in channels:
        caption = caption_for_channel(manifest, channel)
        if not caption:
            raise ValidationError(f"missing caption for {channel}; add captions.{channel} or caption_base")
        if channel not in (captions or {}):
            warnings.append(f"{channel} will use caption_base because captions.{channel} is missing")
        if "foodcosting.app" not in caption.lower():
            warnings.append(f"{channel} caption does not mention foodcosting.app")

    manifest_path = Path(manifest["_manifest_path"])
    resolved_assets = []
    for asset in assets:
        path = resolve_asset_path(asset, manifest_path)
        if not path.exists():
            raise ValidationError(f"asset does not exist: {asset}")
        if not path.is_file():
            raise ValidationError(f"asset is not a file: {asset}")
        suffix = path.suffix.lower()
        if post_type == "video":
            if suffix not in VIDEO_EXTENSIONS:
                raise ValidationError(f"video asset must be an MP4 file: {asset}")
            warnings.extend(validate_video_asset(path))
        else:
            if suffix not in IMAGE_EXTENSIONS:
                raise ValidationError(f"image asset must be PNG/JPG/JPEG: {asset}")
            warnings.extend(validate_image_asset(path))
        resolved_assets.append(path)

    manifest["_resolved_assets"] = [str(path) for path in resolved_assets]
    return warnings


def validate_env(channels):
    missing = []
    placeholders = []
    for key in ("BUFFER_API_TOKEN", "CLOUDINARY_CLOUD_NAME", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET"):
        if not os.environ.get(key):
            missing.append(key)
    for channel in channels:
        env_key = CHANNEL_ENVS[channel]
        value = os.environ.get(env_key)
        if not value:
            missing.append(env_key)
        elif looks_like_placeholder(value):
            placeholders.append(env_key)
    if missing:
        raise ValidationError("missing required environment variable(s): " + ", ".join(sorted(set(missing))))
    if placeholders:
        raise ValidationError("placeholder environment value(s) must be replaced: " + ", ".join(sorted(set(placeholders))))


def looks_like_placeholder(value):
    normalized = value.strip().lower()
    return (
        normalized.startswith("your_")
        or normalized.startswith("<")
        or normalized.endswith("_here")
        or "replace_me" in normalized
        or "placeholder" in normalized
    )


def validate_duplicate(output_path, manifest_path, force):
    path = Path(output_path)
    if force or not path.exists():
        return
    try:
        existing = read_json(path)
    except ValidationError:
        return
    same_manifest = Path(existing.get("source_manifest", "")).resolve() == Path(manifest_path).resolve()
    has_posts = bool(existing.get("buffer_posts"))
    if same_manifest and has_posts:
        raise ValidationError(f"{path} already contains Buffer drafts for this manifest; pass --force to create again")


def validate_video_asset(path):
    warnings = []
    size = path.stat().st_size
    if size > MAX_FREE_VIDEO_BYTES:
        raise ValidationError(f"video exceeds Cloudinary free-plan 100 MB file limit: {path}")
    if size > WARN_VIDEO_BYTES:
        warnings.append(f"video is above 25 MB free-tier comfort threshold: {path.name}")

    metadata = ffprobe_video(path)
    if not metadata:
        warnings.append(f"could not inspect video dimensions/duration with ffprobe: {path.name}")
        return warnings

    duration = metadata.get("duration")
    width = metadata.get("width")
    height = metadata.get("height")
    if duration and duration > 60:
        warnings.append(f"video is over 60 seconds: {duration:.1f}s")
    if width and height and not is_close_ratio(width, height, 9, 16):
        warnings.append(f"video is not close to 9:16: {width}x{height}")
    return warnings


def validate_image_asset(path):
    warnings = []
    size = path.stat().st_size
    if size > WARN_IMAGE_BYTES:
        warnings.append(f"image is above 5 MB free-tier comfort threshold: {path.name}")
    dimensions = image_dimensions(path)
    if not dimensions:
        warnings.append(f"could not inspect image dimensions: {path.name}")
        return warnings
    width, height = dimensions
    aspect = width / height if height else 0
    if aspect < 0.75 or aspect > 1.95:
        warnings.append(f"image dimensions may not be social-friendly: {path.name} ({width}x{height})")
    return warnings


def ffprobe_video(path):
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(path),
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    data = json.loads(result.stdout)
    stream = (data.get("streams") or [{}])[0]
    fmt = data.get("format") or {}
    duration = None
    try:
        duration = float(fmt.get("duration")) if fmt.get("duration") is not None else None
    except ValueError:
        pass
    return {
        "width": stream.get("width"),
        "height": stream.get("height"),
        "duration": duration,
    }


def image_dimensions(path):
    with open(path, "rb") as f:
        header = f.read(32)

    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        width, height = struct.unpack(">II", header[16:24])
        return width, height

    if header.startswith(b"\xff\xd8"):
        return jpeg_dimensions(path)

    return None


def jpeg_dimensions(path):
    with open(path, "rb") as f:
        f.read(2)
        while True:
            marker_start = f.read(1)
            if not marker_start:
                return None
            if marker_start != b"\xff":
                continue
            marker = f.read(1)
            while marker == b"\xff":
                marker = f.read(1)
            if marker in (b"\xd8", b"\xd9"):
                continue
            length_bytes = f.read(2)
            if len(length_bytes) != 2:
                return None
            length = struct.unpack(">H", length_bytes)[0]
            if marker in {b"\xc0", b"\xc1", b"\xc2", b"\xc3", b"\xc5", b"\xc6", b"\xc7", b"\xc9", b"\xca", b"\xcb", b"\xcd", b"\xce", b"\xcf"}:
                data = f.read(5)
                if len(data) != 5:
                    return None
                height, width = struct.unpack(">HH", data[1:5])
                return width, height
            f.seek(length - 2, os.SEEK_CUR)


def is_close_ratio(width, height, target_width, target_height, tolerance=0.04):
    if not width or not height:
        return False
    ratio = width / height
    target = target_width / target_height
    return abs(ratio - target) <= tolerance


def caption_for_channel(manifest, channel):
    captions = manifest.get("captions") or {}
    return captions.get(channel) or manifest.get("caption_base", "")


def cloudinary_signature(params, api_secret):
    signable = {k: v for k, v in params.items() if v is not None and k not in {"file", "api_key", "resource_type", "cloud_name", "signature"}}
    payload = "&".join(f"{key}={signable[key]}" for key in sorted(signable))
    return hashlib.sha1(f"{payload}{api_secret}".encode("utf-8")).hexdigest()


def multipart_form_data(fields, files):
    boundary = f"----foodcosting-{uuid.uuid4().hex}"
    chunks = []
    for name, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        chunks.append(str(value).encode())
        chunks.append(b"\r\n")

    for name, path in files.items():
        path = Path(path)
        mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"; filename="{path.name}"\r\n'.encode())
        chunks.append(f"Content-Type: {mime_type}\r\n\r\n".encode())
        chunks.append(path.read_bytes())
        chunks.append(b"\r\n")

    chunks.append(f"--{boundary}--\r\n".encode())
    return boundary, b"".join(chunks)


def upload_to_cloudinary(path, resource_type, slug):
    cloud_name = os.environ["CLOUDINARY_CLOUD_NAME"]
    api_key = os.environ["CLOUDINARY_API_KEY"]
    api_secret = os.environ["CLOUDINARY_API_SECRET"]
    timestamp = int(time.time())
    public_id = Path(path).stem
    params = {
        "timestamp": timestamp,
        "folder": f"foodcosting/social/{slug}",
        "public_id": public_id,
        "overwrite": "true",
    }
    signature = cloudinary_signature(params, api_secret)
    fields = {
        **params,
        "api_key": api_key,
        "signature": signature,
    }
    boundary, body = multipart_form_data(fields, {"file": path})
    url = CLOUDINARY_UPLOAD_URL.format(cloud_name=cloud_name, resource_type=resource_type)
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    result = request_json(url, method="POST", body=body, headers=headers)
    if not result.get("secure_url"):
        raise RuntimeError(f"Cloudinary upload did not return a secure_url for {path}: {result}")
    return {
        "asset_path": str(path),
        "resource_type": resource_type,
        "public_id": result.get("public_id"),
        "secure_url": result.get("secure_url"),
        "bytes": result.get("bytes"),
        "format": result.get("format"),
        "width": result.get("width"),
        "height": result.get("height"),
        "duration": result.get("duration"),
    }


def request_json(url, method="GET", body=None, headers=None):
    request_headers = {
        "User-Agent": "foodcosting-buffer-drafts/0.1 (+https://foodcosting.app)",
        "Accept": "application/json",
    }
    request_headers.update(headers or {})
    request = Request(url, data=body, headers=request_headers, method=method)
    try:
        with urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        raise RuntimeError(f"HTTP {exc.code} from {url}: {error_body}") from exc
    except URLError as exc:
        raise RuntimeError(f"request failed for {url}: {exc}") from exc


def graphql_string(value):
    return json.dumps(str(value))


def graphql_assets(assets):
    if "videos" in assets:
        videos = ", ".join("{ url: " + graphql_string(video["url"]) + " }" for video in assets["videos"])
        return "videos: [" + videos + "]"
    images = ", ".join("{ url: " + graphql_string(image["url"]) + " }" for image in assets["images"])
    return "images: [" + images + "]"


def graphql_metadata(metadata):
    if not metadata:
        return ""
    return "metadata: " + graphql_input(metadata)


def graphql_input(value):
    if isinstance(value, dict):
        items = []
        for key, item in value.items():
            items.append(f"{key}: {graphql_input(item)}")
        return "{ " + ", ".join(items) + " }"
    if isinstance(value, list):
        return "[" + ", ".join(graphql_input(item) for item in value) + "]"
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, GraphQLEnum):
        return value.value
    return graphql_string(value)


class GraphQLEnum:
    def __init__(self, value):
        self.value = value


def metadata_for_channel(channel, post_type, manifest):
    title = manifest.get("title") or "FoodCosting.app"
    if channel == "instagram":
        instagram_type = "reel" if post_type == "video" else "carousel" if post_type == "carousel" else "post"
        return {"instagram": {"type": GraphQLEnum(instagram_type), "shouldShareToFeed": True}}
    if channel == "facebook":
        facebook_type = "reel" if post_type == "video" else "post"
        return {"facebook": {"type": GraphQLEnum(facebook_type)}}
    if channel == "youtube":
        return {
            "youtube": {
                "title": title[:100],
                "privacy": GraphQLEnum("public"),
                "categoryId": "27",
                "license": GraphQLEnum("youtube"),
                "notifySubscribers": False,
                "embeddable": True,
                "madeForKids": False,
            }
        }
    return {}


def buffer_create_post(channel, channel_id, text, assets, metadata):
    query = """
    mutation CreatePost {
      createPost(input: {
        text: __TEXT__
        channelId: __CHANNEL_ID__
        schedulingType: automatic
        mode: addToQueue
        saveToDraft: true
        assets: {
          __ASSETS__
        }
        __METADATA__
      }) {
        ... on PostActionSuccess {
          post {
            id
            text
            status
            dueAt
            channelId
            assets {
              id
              mimeType
              source
            }
          }
        }
        ... on MutationError {
          message
        }
      }
    }
    """
    query = (
        query
        .replace("__TEXT__", graphql_string(text))
        .replace("__CHANNEL_ID__", graphql_string(channel_id))
        .replace("__ASSETS__", graphql_assets(assets))
        .replace("__METADATA__", graphql_metadata(metadata))
    )
    body = json.dumps({"query": query}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {os.environ['BUFFER_API_TOKEN']}",
        "Content-Type": "application/json",
    }
    response = request_json(BUFFER_API_URL, method="POST", body=body, headers=headers)
    if response.get("errors"):
        raise RuntimeError(f"Buffer GraphQL error for {channel}: {response['errors']}")
    result = response.get("data", {}).get("createPost")
    if not result:
        raise RuntimeError(f"Buffer did not return createPost data for {channel}: {response}")
    if result.get("message"):
        raise RuntimeError(f"Buffer rejected {channel} draft: {result['message']}")
    return result["post"]


def slug_for_manifest(manifest):
    title = manifest.get("title", "social-post").lower()
    chars = []
    for char in title:
        if char.isalnum():
            chars.append(char)
        elif chars and chars[-1] != "-":
            chars.append("-")
    slug = "".join(chars).strip("-")
    return slug or f"social-post-{int(time.time())}"


def build_buffer_assets(post_type, uploaded_assets):
    if post_type == "video":
        return {"videos": [{"url": uploaded_assets[0]["secure_url"]}]}
    return {"images": [{"url": asset["secure_url"]} for asset in uploaded_assets]}


def create_drafts(manifest, dry_run=False):
    post_type = manifest["post_type"]
    channels = manifest["channels"]
    slug = slug_for_manifest(manifest)
    resolved_assets = [Path(path) for path in manifest["_resolved_assets"]]
    uploaded_assets = []

    if dry_run:
        for path in resolved_assets:
            resource_type = "video" if post_type == "video" else "image"
            uploaded_assets.append({
                "asset_path": str(path),
                "resource_type": resource_type,
                "secure_url": f"dry-run://cloudinary/{slug}/{path.name}",
            })
    else:
        for path in resolved_assets:
            resource_type = "video" if post_type == "video" else "image"
            uploaded_assets.append(upload_to_cloudinary(path, resource_type, slug))

    buffer_assets = build_buffer_assets(post_type, uploaded_assets)
    buffer_posts = {}
    for channel in channels:
        channel_id = os.environ[CHANNEL_ENVS[channel]]
        caption = caption_for_channel(manifest, channel)
        metadata = metadata_for_channel(channel, post_type, manifest)
        if dry_run:
            buffer_posts[channel] = {
                "id": f"dry-run-{channel}",
                "status": "draft",
                "channelId": channel_id,
                "text": caption,
                "assets": buffer_assets,
                "metadata": metadata_to_plain(metadata),
            }
        else:
            buffer_posts[channel] = buffer_create_post(channel, channel_id, caption, buffer_assets, metadata)

    return uploaded_assets, buffer_posts


def metadata_to_plain(value):
    if isinstance(value, dict):
        return {key: metadata_to_plain(item) for key, item in value.items()}
    if isinstance(value, list):
        return [metadata_to_plain(item) for item in value]
    if isinstance(value, GraphQLEnum):
        return value.value
    return value


def build_audit(manifest, warnings, uploaded_assets, buffer_posts, dry_run):
    return {
        "dry_run": dry_run,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_manifest": manifest["_manifest_path"],
        "post_type": manifest["post_type"],
        "channels": manifest["channels"],
        "uploaded_assets": uploaded_assets,
        "buffer_posts": buffer_posts,
        "warnings": warnings,
        "skipped_channels": [],
    }


def main():
    parser = argparse.ArgumentParser(description="Create Buffer draft posts from a social manifest")
    parser.add_argument("--manifest", required=True, help="Path to pipeline/social/ready/<slug>.json")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Audit JSON output path")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print intended work without uploading or creating drafts")
    parser.add_argument("--force", action="store_true", help="Allow creating drafts again for the same manifest/output")
    args = parser.parse_args()

    load_env()

    try:
        manifest = load_manifest(args.manifest)
        warnings = validate_manifest(manifest)
        validate_env(manifest["channels"])
        validate_duplicate(args.output, manifest["_manifest_path"], args.force)
        uploaded_assets, buffer_posts = create_drafts(manifest, dry_run=args.dry_run)
        audit = build_audit(manifest, warnings, uploaded_assets, buffer_posts, args.dry_run)
    except (ValidationError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        write_json(audit, None)
    else:
        write_json(audit, args.output)


if __name__ == "__main__":
    main()
