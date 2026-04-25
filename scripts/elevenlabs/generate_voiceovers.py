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

SCRIPTS = {
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

OUTPUT_DIR = pathlib.Path("remotion/public/audio")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
HEADERS = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json",
    "Accept": "audio/mpeg",
}

for name, text in SCRIPTS.items():
    print(f"Generating {name}...")
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
    }
    response = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()

    out_path = OUTPUT_DIR / f"{name}-voice.mp3"
    out_path.write_bytes(response.content)
    size_kb = len(response.content) / 1024
    print(f"  Saved {out_path} ({size_kb:.1f} KB)")

print("Done.")
