# Short-Form Video 15-Second Cap — Design Spec

**Date:** 2026-04-25
**Branch:** feat/kot-content-templates (or new branch from main)
**Status:** Approved for implementation

---

## Problem

All three short-form Remotion compositions are far too long for YouTube Shorts and Facebook Reels:

| Composition | Current | Overage |
|---|---|---|
| FoodCostTip | 1650f / 55s | +40s |
| MythBusting | 1500f / 50s | +35s |
| QuickMath | 1050f / 35s | +20s |

Platform guidance for Shorts/Reels favours under 15 seconds for maximum completion rate. Attention drop-off begins within the first 3 seconds.

---

## Hard Constraint

**All short-form compositions must be ≤ 450 frames at 30fps (15 seconds).** This is a non-negotiable cap. The `durationInFrames` default prop in `Root.tsx` for each composition must be set to exactly 450.

---

## Approach Per Composition

### FoodCostTip — Scene Cut + Fast Punch

Drop the Problem scene entirely. It is the least essential scene for short-form — the Hook already sets up the tension, and the Tip delivers the payoff. The composition becomes 3 scenes.

| Scene | Frames | Seconds | Notes |
|---|---|---|---|
| Hook | 90 | 3s | 0–20% |
| Tip | 270 | 9s | 20–80% |
| CTA | 90 | 3s | 80–100% |

**Stagger rule:** Tip line reveal delay reduced from 25 frames → 8 frames per line. Up to 4 lines still animate cleanly within the 270-frame budget.

**Sequence timing in FoodCostTip.tsx:**
- `hookEnd = Math.floor(durationInFrames * 0.20)` → 90f
- `tipEnd = Math.floor(durationInFrames * 0.80)` → 360f
- CTA runs from `tipEnd` to `durationInFrames`

The `problemEnd` calculation and Problem `<Sequence>` block are removed entirely.

---

### MythBusting — Receipt Reveal (compressed stagger)

Drop the Proof scene — too data-heavy for 15s. The myth/reality contrast is the core content and must be preserved. The composition becomes 3 scenes.

| Scene | Frames | Seconds | Notes |
|---|---|---|---|
| Myth | 135 | 4.5s | 0–30% |
| Reality | 135 | 4.5s | 30–60% |
| CTA | 180 | 6s | 60–100% |

**Sequence timing in MythBusting.tsx:**
- `mythEnd = Math.floor(durationInFrames * 0.30)` → 135f
- `realityEnd = Math.floor(durationInFrames * 0.60)` → 270f
- CTA runs from `realityEnd` to `durationInFrames`

The `proofEnd` calculation and Proof `<Sequence>` block are removed entirely.

---

### QuickMath — Fast Punch

Drop the ingredient stagger. The single menu price result is the hero number — show it fast. The composition keeps 3 scenes but the Calculation scene is redesigned to skip staggered ingredient reveal.

| Scene | Frames | Seconds | Notes |
|---|---|---|---|
| Setup | 90 | 3s | 0–20% |
| Calculation | 225 | 7.5s | 20–70% |
| CTA | 135 | 4.5s | 70–100% |

**Sequence timing in QuickMath.tsx:**
- `setupEnd = Math.floor(durationInFrames * 0.20)` → 90f
- `calcEnd = Math.floor(durationInFrames * 0.70)` → 315f
- CTA runs from `calcEnd` to `durationInFrames`

**Calculation scene change:** The ingredient list stagger delay is removed. Ingredients render at full opacity immediately. Only the result value (`result`) gets a spring-in animation, triggered at frame 0 of the scene (no delay offset needed). The `resultDelay` variable and its `Math.max(0, frame - resultDelay)` offset are removed.

---

## Stagger Delay Rule (Global)

Any scene that uses per-line stagger animations must use a maximum delay of **8 frames per item** (down from 25). This applies to:

- `Tip.tsx` — line reveal delay: `const delay = i * 8`
- `Calculation.tsx` — ingredient reveal: removed entirely (immediate render)
- `Proof.tsx` — not used in 15s format (scene dropped from MythBusting)

---

## Root.tsx Changes

Update `durationInFrames` for all three short-form compositions to 450:

```tsx
// FoodCostTip
durationInFrames={450}

// MythBusting  
durationInFrames={450}

// QuickMath
durationInFrames={450}
```

The `defaultProps.durationInFrames` value inside each composition's `defaultProps` object must also be updated to 450 to match.

---

## Files to Change

| File | Change |
|---|---|
| `remotion/src/Root.tsx` | Set `durationInFrames={450}` and `defaultProps.durationInFrames: 450` for FoodCostTip, MythBusting, QuickMath |
| `remotion/src/FoodCostTip.tsx` | Remove Problem scene and sequence; update timing ratios |
| `remotion/src/MythBusting.tsx` | Remove Proof scene and sequence; update timing ratios |
| `remotion/src/QuickMath.tsx` | Update `calcEnd` ratio to 0.70; update timing |
| `remotion/src/scenes/Tip.tsx` | Change stagger delay from `i * 25` to `i * 8` |
| `remotion/src/scenes/Calculation.tsx` | Remove ingredient stagger; remove `resultDelay` offset |

---

## Out of Scope

- The Carousel composition is unaffected — it is not a short-form video.
- Scene component visual design is unchanged — only timing and scene selection change.
- No new props are added. `durationInFrames` is already a prop on all three composition types.
- The Problem, Proof scenes are not deleted — they remain available if a longer-form format is ever needed.
