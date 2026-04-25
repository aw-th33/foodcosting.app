# Voiceover + Background Music — Design Spec

**Date:** 2026-04-25
**Branch:** new branch from `feat/kot-content-templates` or from `main` after merge
**Status:** Approved for implementation

---

## Goal

Add AI voiceover (ElevenLabs) and a subtle background music bed to all three short-form Remotion compositions. Voice explains the screen without reading it (friendly practitioner tone). Music sits at ~15% volume and never competes with voice.

---

## Approach

**Approach A — Fixed transcript, manual timing fit.**

Write one transcript per composition. Generate one MP3 per composition via ElevenLabs API. Drop MP3s into `remotion/public/audio/`. Add a royalty-free background music file to the same directory. Each composition mixes voice + music via two `<Audio>` components. The 15s hard cap is preserved — the transcript is written to fit within the voiceover window (~11s), leaving 2s each for Hook and CTA to play out.

No frame-sync machinery. No `@remotion/media-utils`. No dynamic duration. Simple.

---

## Transcripts

Each transcript is written for ~11s of speaking time at a relaxed friendly pace (~130 wpm, ~24 words). Voice runs during Hook + Tip/middle scenes; CTA closes visually.

### FoodCostTip
> "Most operators check food cost after the week's done — but by then the margin's already gone. The fix is simple: cost the plate before you price it, and update it every time your supplier invoice changes. That's it."

### MythBusting
> "Everyone says keep food cost under 30% — but a steakhouse running 38% can be more profitable than a sandwich shop at 28. The number that actually matters is how much gross profit lands per plate, not the percentage."

### QuickMath
> "If you're pricing a burger at whatever feels right, you're guessing. Take your ingredient cost, divide by your target food cost percentage — that gives you the floor. Anything below it and you're paying customers to eat."

---

## ElevenLabs Configuration

**Voice character:** Friendly practitioner — warm, direct, no filler. Like a fellow operator sharing a tip.

**Recommended ElevenLabs settings:**
- Model: `eleven_turbo_v2_5` (fast, high quality)
- Voice: `Adam` or `Josh` (warm male) — or equivalent female voice if preferred
- Stability: `0.5`
- Similarity boost: `0.75`
- Style: `0.3` (slight personality, not dramatic)
- Speed: `0.95` (slightly relaxed pace, not rushed)

**Output format:** MP3, 44.1kHz

**Output filenames:**
- `remotion/public/audio/foodcosttip-voice.mp3`
- `remotion/public/audio/mythbusting-voice.mp3`
- `remotion/public/audio/quickmath-voice.mp3`

---

## Background Music

**Deferred to a separate implementation step.** Music sourcing and integration will be handled after voiceover is verified working. The `musicSrc` prop and `<Audio>` wiring for music are out of scope for the current plan.

---

## Remotion Audio Integration

Each composition already has one `<Audio>` component conditionally rendered for `audioSrc` — no changes needed to the composition files themselves. The existing pattern handles voice:

```tsx
{audioSrc && <Audio src={audioSrc} />}
```

### Voice prop

`audioSrc` already exists on all three types and compositions. No type changes needed.

### Voice prop

`audioSrc` already exists on all three types and compositions. No type changes needed for voice. Update `Root.tsx` defaultProps once MP3s are generated:
- FoodCostTip: `audioSrc: '/audio/foodcosttip-voice.mp3'`
- MythBusting: `audioSrc: '/audio/mythbusting-voice.mp3'`
- QuickMath: `audioSrc: '/audio/quickmath-voice.mp3'`

**Voice:** ElevenLabs Adam (`pNInz6obpgDQGcFmaJgB`)

---

## ElevenLabs Generation Script

A Python script at `scripts/elevenlabs/generate_voiceovers.py` handles the API calls.

### Script responsibilities
1. Read `ELEVENLABS_API_KEY` from environment
2. For each of the three transcripts, call the ElevenLabs `/v1/text-to-speech/{voice_id}` endpoint
3. Save the returned audio bytes to the correct path under `remotion/public/audio/`
4. Print confirmation with file size and path for each

### Script inputs (hardcoded in script, not CLI args)
```python
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam — replace with chosen voice ID
MODEL_ID = "eleven_turbo_v2_5"
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.3,
    "use_speaker_boost": True,
    "speed": 0.95,
}

SCRIPTS = {
    "foodcosttip": "Most operators check food cost after the week's done — but by then the margin's already gone. The fix is simple: cost the plate before you price it, and update it every time your supplier invoice changes. That's it.",
    "mythbusting": "Everyone says keep food cost under 30% — but a steakhouse running 38% can be more profitable than a sandwich shop at 28. The number that actually matters is how much gross profit lands per plate, not the percentage.",
    "quickmath": "If you're pricing a burger at whatever feels right, you're guessing. Take your ingredient cost, divide by your target food cost percentage — that gives you the floor. Anything below it and you're paying customers to eat.",
}

OUTPUT_DIR = "remotion/public/audio"
```

### Script dependencies
- `requests` (standard, no special install needed beyond `pip install requests`)
- `python-dotenv` to load `.env` file

### `.env` update
Add to `.env` (not `.env.example` — that already has the slot):
```
ELEVENLABS_API_KEY=your_key_here
```

---

## File Structure After Implementation

```
remotion/
  public/
    audio/
      foodcosttip-voice.mp3      ← generated by script
      mythbusting-voice.mp3      ← generated by script
      quickmath-voice.mp3        ← generated by script
      (bg-music.mp3 — deferred)
scripts/
  elevenlabs/
    generate_voiceovers.py       ← new script
```

---

## Verification

1. Run `generate_voiceovers.py` → confirm 3 MP3 files appear in `remotion/public/audio/`
2. Manually source `bg-music.mp3` and drop it into `remotion/public/audio/`
3. Update Root.tsx defaultProps with actual paths
4. Open Remotion Studio → scrub each composition → confirm voice audible, music barely audible underneath
5. Confirm total composition duration remains 450 frames (audio does not extend it)
6. TypeScript compiles clean

---

## Out of Scope

- Background music integration — deferred to separate step
- Scene-level audio sync (Approach B/C) — deferred
- Subtitle/caption overlay — deferred
- Female voice variant — can be swapped by changing `VOICE_ID` constant
