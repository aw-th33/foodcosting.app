# Voiceover Generation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate ElevenLabs AI voiceover MP3s for all three short-form Remotion compositions and wire them into Root.tsx so Remotion Studio plays voice audio during preview.

**Architecture:** A Python script calls the ElevenLabs TTS API for each of three hardcoded transcripts and saves the resulting MP3s to `remotion/public/audio/`. Root.tsx defaultProps are updated to point at the generated files. No composition code changes — the `<Audio src={audioSrc} />` wiring already exists in all three compositions.

**Tech Stack:** Python 3, ElevenLabs REST API (`/v1/text-to-speech`), `requests`, `python-dotenv`, Remotion `<Audio>` component (already wired)

---

## File Map

| File | Change |
|---|---|
| `scripts/elevenlabs/generate_voiceovers.py` | Create — calls ElevenLabs API, saves 3 MP3s |
| `remotion/public/audio/` | Create directory, receive generated MP3s |
| `remotion/src/Root.tsx` | Update `audioSrc` in defaultProps for all 3 compositions |
| `.env` | Add `ELEVENLABS_API_KEY=` value (manual step, not automated) |

---

### Task 1: Create the ElevenLabs voiceover script

**Files:**
- Create: `scripts/elevenlabs/generate_voiceovers.py`

- [ ] **Step 1: Create the scripts/elevenlabs directory**

```bash
mkdir -p scripts/elevenlabs
```

- [ ] **Step 2: Create generate_voiceovers.py**

Create `scripts/elevenlabs/generate_voiceovers.py` with this exact content:

```python
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
```

- [ ] **Step 3: Verify the script has no syntax errors**

```bash
python -c "import ast; ast.parse(open('scripts/elevenlabs/generate_voiceovers.py').read()); print('syntax OK')"
```

Expected output: `syntax OK`

- [ ] **Step 4: Commit**

```bash
git add scripts/elevenlabs/generate_voiceovers.py
git commit -m "feat: add ElevenLabs voiceover generation script"
```

---

### Task 2: Add ELEVENLABS_API_KEY to .env and run the script

**Files:**
- Modify: `.env` (manual — not committed)
- Create: `remotion/public/audio/foodcosttip-voice.mp3`
- Create: `remotion/public/audio/mythbusting-voice.mp3`
- Create: `remotion/public/audio/quickmath-voice.mp3`

- [ ] **Step 1: Check .env exists and has the key slot**

```bash
grep ELEVENLABS_API_KEY .env || echo "key not found"
```

If the key is missing from `.env`, add it:

```bash
echo "ELEVENLABS_API_KEY=your_actual_key_here" >> .env
```

Replace `your_actual_key_here` with the real key from the ElevenLabs dashboard at https://elevenlabs.io — Settings → API Keys.

- [ ] **Step 2: Install dependencies if needed**

```bash
pip install requests python-dotenv
```

Expected: installs cleanly or reports "already satisfied".

- [ ] **Step 3: Run the script from the project root**

```bash
python scripts/elevenlabs/generate_voiceovers.py
```

Expected output:
```
Generating foodcosttip...
  Saved remotion/public/audio/foodcosttip-voice.mp3 (XX.X KB)
Generating mythbusting...
  Saved remotion/public/audio/mythbusting-voice.mp3 (XX.X KB)
Generating quickmath...
  Saved remotion/public/audio/quickmath-voice.mp3 (XX.X KB)
Done.
```

If the script raises `RuntimeError: ELEVENLABS_API_KEY not set`, the `.env` file is not being found — ensure you're running from the project root (`c:/Users/admin/Documents/Foodcosting.app`).

If the script raises `requests.exceptions.HTTPError: 401`, the API key is invalid — check the key in the ElevenLabs dashboard.

- [ ] **Step 4: Verify files exist and are non-empty**

```bash
ls -lh remotion/public/audio/
```

Expected: three `.mp3` files, each between 50KB and 300KB. A file smaller than 10KB indicates an error response was saved instead of audio.

- [ ] **Step 5: Add audio directory to git but ignore MP3 files**

The `remotion/public/audio/` directory should be tracked, but the generated MP3 binaries should not be committed (they are reproducible via the script).

Check whether `.gitignore` already covers this:

```bash
grep -n "audio" .gitignore || echo "not present"
```

If not present, add:

```bash
echo "remotion/public/audio/*.mp3" >> .gitignore
```

Then commit the `.gitignore` change and a `.gitkeep` to preserve the directory:

```bash
touch remotion/public/audio/.gitkeep
git add .gitignore remotion/public/audio/.gitkeep
git commit -m "chore: track audio directory, gitignore generated MP3s"
```

---

### Task 3: Wire audioSrc paths into Root.tsx defaultProps

**Files:**
- Modify: `remotion/src/Root.tsx`

- [ ] **Step 1: Update FoodCostTip defaultProps audioSrc**

In `remotion/src/Root.tsx`, find the FoodCostTip `defaultProps` block. Change:

```tsx
audioSrc: null,
```

to:

```tsx
audioSrc: '/audio/foodcosttip-voice.mp3',
```

- [ ] **Step 2: Update MythBusting defaultProps audioSrc**

Find the MythBusting `defaultProps` block. Change:

```tsx
audioSrc: null,
```

to:

```tsx
audioSrc: '/audio/mythbusting-voice.mp3',
```

- [ ] **Step 3: Update QuickMath defaultProps audioSrc**

Find the QuickMath `defaultProps` block. Change:

```tsx
audioSrc: null,
```

to:

```tsx
audioSrc: '/audio/quickmath-voice.mp3',
```

- [ ] **Step 4: Verify TypeScript compiles**

```bash
cd remotion && npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add remotion/src/Root.tsx
git commit -m "feat: wire ElevenLabs voiceover paths into composition defaultProps"
```

---

### Task 4: Verify audio playback in Remotion Studio

- [ ] **Step 1: Start Remotion Studio (or confirm it's already running)**

```bash
cd remotion && npx remotion studio
```

Open [http://localhost:3900](http://localhost:3900).

- [ ] **Step 2: Verify FoodCostTip voice**

Select the `FoodCostTip` composition. Press play. Confirm:
- Voice audio plays from the start
- Voice is audible throughout — "Most operators check food cost after the week's done…"
- Audio does not cut off before the CTA scene (voice should finish within ~11s)
- Total duration is still **450 frames / 15.0s** (audio does not extend it)

- [ ] **Step 3: Verify MythBusting voice**

Select `MythBusting`. Press play. Confirm:
- Voice plays — "Everyone says keep food cost under 30%…"
- Audible throughout middle scenes
- Duration unchanged at 450 frames

- [ ] **Step 4: Verify QuickMath voice**

Select `QuickMath`. Press play. Confirm:
- Voice plays — "If you're pricing a burger at whatever feels right…"
- Audible and fits within 15s
- Duration unchanged at 450 frames

- [ ] **Step 5: Commit note**

No code changes expected in this task. If a path was wrong and you had to fix it in Root.tsx, commit the fix:

```bash
git add remotion/src/Root.tsx
git commit -m "fix: correct audio path for <composition name>"
```
