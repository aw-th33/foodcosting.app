import argparse
import os
import pathlib
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise RuntimeError("ELEVENLABS_API_KEY not set in environment or .env file")

VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam
MODEL_ID = "eleven_turbo_v2_5"
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.3,
    "use_speaker_boost": True,
    "speed": 0.95,
}

BATCH_SCRIPTS = {
    "foodcosttip": (
        "Most operators check food cost after the week's done — but by then the margin's already gone. "
        "The fix is simple: cost the plate before you price it, and update it every time your supplier "
        "invoice changes. That's it."
    ),
    "mythbusting": (
        "Everyone says keep food cost under 30% — but a steakhouse running 38% can be more profitable "
        "than a sandwich shop at 28. The number that actually matters is how much gross profit lands "
        "per plate, not the percentage."
    ),
    "quickmath": (
        "If you're pricing a burger at whatever feels right, you're guessing. Take your ingredient cost, "
        "divide by your target food cost percentage — that gives you the floor. Anything below it and "
        "you're paying customers to eat."
    ),
}

URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
HEADERS = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json",
    "Accept": "audio/mpeg",
}


def generate(text: str, out_path: pathlib.Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
    }
    response = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    out_path.write_bytes(response.content)
    size_kb = len(response.content) / 1024
    print(f"  Saved {out_path} ({size_kb:.1f} KB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ElevenLabs voiceover MP3s")
    parser.add_argument("--text", help="Transcript text for a single voiceover")
    parser.add_argument("--output", help="Output path for single voiceover (e.g. remotion/public/audio/my-video-voice.mp3)")
    args = parser.parse_args()

    if args.text and args.output:
        # Single-shot mode: called by remotion-renderer for a specific script
        print(f"Generating single voiceover -> {args.output}")
        generate(args.text, pathlib.Path(args.output))
        print("Done.")
    else:
        # Batch mode: regenerate all three template voiceovers
        output_dir = pathlib.Path("remotion/public/audio")
        for name, text in BATCH_SCRIPTS.items():
            print(f"Generating {name}...")
            generate(text, output_dir / f"{name}-voice.mp3")
        print("Done.")


if __name__ == "__main__":
    main()
