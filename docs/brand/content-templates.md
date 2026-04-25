# Design Spec: Content Templates — Shorts & Carousel KOT Reskin

**Date:** 2026-04-24
**Status:** Draft
**Depends on:** [KOT Brand Design System](2026-04-24-kot-brand-design-system.md)

---

## Problem

The current Remotion system produces visually identical content — one short-form layout (Hook → Problem → Tip → CTA) and one carousel style (editorial serif). Every post looks the same, which causes audience fatigue and reduces feed engagement.

## Decision

Define a template system with multiple content types for shorts and a dual-palette KOT reskin for carousels. Templates are visual layout specs — the building blocks agents and Remotion use to produce varied, on-brand content.

---

## Short-Form Video Templates (1080×1920, 9:16)

### Design direction

**Receipt DNA on dark** as primary palette, **literal receipt on paper** as light variant. Same layouts, inverted colors. Alternate between dark and light across posts for feed variety.

Both palettes share:
- Dashed dividers (never solid)
- IBM Plex Mono for numbers, labels, stamps
- Inter for headlines and body
- Signal colors (alert, healthy, caution) only on data values
- Receipt header/footer patterns
- Boxed-F logo mark

### Content type 1: Educational tip (4 scenes)

Existing flow, redesigned with KOT tokens.

| Scene | Layout | Key elements |
|---|---|---|
| Hook | Centered, receipt-framed | Receipt header (brand between dashed rules), bold headline (Inter 800), hero number (Plex Mono 700, signal color), supporting mono caption |
| Problem | Left-aligned with stamp | Highlight stamp ("THE PROBLEM", alert bg), headline (Inter 700), dashed divider, body text (Inter 400, faded) |
| Tip | Full receipt line-items | Receipt header as section title, label/value pairs (Plex Mono) with dashed dividers between, heavy dashed rule before total, total row in bold with healthy color |
| CTA | Centered, shared | Boxed-F logo + wordmark, headline (Inter 700), dashed divider, pill button (inverted bg, 999px radius), asterisk footer |

**Animation patterns:**
- Hook: Spring scale-in + fade (existing pattern, retuned)
- Problem: Slide up + fade
- Tip: Staggered line-item entrance (each line 25 frames apart, slide from left + fade)
- CTA: Spring scale-in + fade

### Content type 2: Myth-busting (4 scenes, new)

| Scene | Layout | Key elements |
|---|---|---|
| Myth | Centered, receipt-framed | Dashed rules framing content, highlight stamp ("MYTH", ink bg / inverted on light), italic quote (Inter 700), "swipe for the truth →" mono caption |
| Reality | Left-aligned with stamp | Highlight stamp ("REALITY", healthy bg), headline (Inter 700), dashed divider, body text, hero number (Plex Mono 700, healthy color), mono caption |
| Proof | Comparison line-items | Receipt header ("THE MATH"), two receipt blocks stacked (e.g. Steakhouse vs Sandwich Shop), each with label/value line items, heavy dashed rule before gross profit total, signal colors on values |
| CTA | Shared CTA scene | Same as educational tip |

**Animation patterns:**
- Myth: Fade-in with stamp appearing first (scale spring)
- Reality: Slide up + fade, number counting up
- Proof: Two receipt blocks stagger in (top block first, bottom block 15 frames later), line items within each block stagger
- CTA: Same as educational tip

### Content type 3: Quick math (3 scenes, new)

| Scene | Layout | Key elements |
|---|---|---|
| Setup | Centered, receipt-framed | Receipt header (brand between dashed rules), bold question headline (Inter 800), oversized "$?" (Plex Mono 700), "let's do the math →" mono caption |
| Calculation | Full receipt | Receipt header as section title, ingredient line items (label/value with dashed dividers), heavy dashed rule before total cost, spacing gap, target % line, heavy dashed rule, result number (Plex Mono 700, healthy color, large), "minimum menu price" mono caption |
| CTA | Shared CTA scene | Same as educational tip |

**Animation patterns:**
- Setup: Spring scale-in, "$?" pulses once
- Calculation: Line items stagger in top-to-bottom (25 frames apart), total slides in after all items, pause, then result number scales in with spring
- CTA: Same as educational tip

### Palette definitions

**Dark palette (primary):**
| Element | Value |
|---|---|
| Background | #111111 |
| Primary text | #F0ECE4 |
| Secondary text | #888888 |
| Dividers | 1px dashed #333333 |
| Heavy dividers | 2px dashed #F0ECE4 |
| Stamp (neutral) | bg: #F0ECE4, text: #111111 |

**Light palette (variant):**
| Element | Value |
|---|---|
| Background | #F8F6F0 |
| Primary text | #111111 |
| Secondary text | #6B6B66 |
| Dividers | 1px dashed #DDD8CC |
| Heavy dividers | 2px dashed #111111 |
| Stamp (neutral) | bg: #111111, text: #F8F6F0 |

**Signal colors (both palettes):**
| Token | Hex | Usage |
|---|---|---|
| alert | #C0392B | Stamp bg for problems, danger numbers |
| healthy | #2E7D32 | Stamp bg for reality, good numbers, totals |
| caution | #E68A00 | Borderline numbers, warnings |

### Short-form timing

| Content type | Scenes | Approx duration |
|---|---|---|
| Educational tip | 4 | 45-55s |
| Myth-busting | 4 | 45-55s |
| Quick math | 3 | 30-40s |

---

## Carousel Slide Templates (1080×1350, 4:5)

### Design direction

KOT reskin of existing 6 slide types. Light (paper) as primary palette, dark (ink) as variant. CTA slide is always dark regardless of carousel palette. Same layout structures, updated with KOT tokens.

### Slide type changes from current system

| Element | Current | KOT reskin |
|---|---|---|
| Display font | Instrument Serif | Inter 800 (headlines), IBM Plex Mono 700 (data) |
| Body font | Inter | Inter (unchanged) |
| Mono font | JetBrains Mono | IBM Plex Mono |
| Accent highlight | Italic + terracotta color | Monospace highlight stamp (inverted bg block) |
| Dividers | 1px solid, 0.8 opacity | 1px dashed #DDD8CC (light) or #333 (dark) |
| Heavy dividers | None | 2px dashed #111 (light) or #F0ECE4 (dark) — before totals |
| Colors | bg #FAFAF7, accent #C44A2A, ok #3E9B57, warn #D99A3B | bg #F8F6F0, alert #C0392B, healthy #2E7D32, caution #E68A00 |
| Logo | Geometric skewed-F SVG | Boxed monospace F |
| Slide counter | Monospace NN/NN | Unchanged format, IBM Plex Mono |
| Receipt header | N/A | Centered brand name between dashed rules (slide headers) |
| Receipt footer | N/A | Asterisk-decorated CTA text (CTA slide) |

### Slide templates

**Cover**
- Top: Logo mark + issue label
- Middle: Dashed rule, mono kicker (uppercase, label size), headline (Inter 800, large), accent word wrapped in highlight stamp instead of italic+color, dashed rule, subtitle (Inter 400, faded)
- Bottom: Swipe cue (mono, uppercase, with arrow)

**Math**
- Header: Slide count + kicker
- Headline: Inter 700
- Body: Dashed rule, line-item grid (Plex Mono labels left, values right), dashed dividers between rows, heavy dashed rule before total, total in bold with signal color
- Footer: Optional footnote (Inter 400, faded)

**List**
- Header: Slide count + kicker
- Headline: Inter 700
- Items: Mono counter (01, 02, 03...) + term (Inter 700) + description (Inter 400, faded), dashed divider between items

**Quote**
- Header: Slide count + kicker
- Body: Framed between dashed rules, large italic quote (Inter 700), dashed rule below, attribution (Plex Mono, faded)

**Pullquote**
- Header: Slide count + kicker
- Body: Centered headline text, hero stat word (Plex Mono 700, large), dashed rule, comparison data columns below (label in mono uppercase, value in mono with signal color)

**CTA (always dark)**
- Logo mark + wordmark
- Dashed rule
- Mono kicker
- Headline (Inter 800)
- Body text (Inter 400, faded)
- Dashed rule
- Pill button (inverted bg, 999px radius)
- Asterisk footer: `* * * save · share · price right * * *`

### Carousel palette definitions

Same as short-form palettes. Light is default, dark is variant. CTA always uses dark palette.

---

## Variation Strategy

Content stays on-brand while avoiding repetition through two mechanisms:

1. **Content type rotation** (shorts) — Rotate between educational tip, myth-busting, and quick math. Different scene counts and layouts create natural variety.

2. **Palette alternation** (both formats) — Alternate dark and light posts in the feed. Same layouts, different feel. Suggested pattern: dark → light → dark, or by content type (e.g. myth-busting always dark, quick math always light).

---

## Template Inventory

### Short-form scenes (9 total)

| Scene | Used by | Palette |
|---|---|---|
| Hook | Educational tip | Dark / Light |
| Problem | Educational tip | Dark / Light |
| Tip | Educational tip | Dark / Light |
| Myth | Myth-busting | Dark / Light |
| Reality | Myth-busting | Dark / Light |
| Proof | Myth-busting | Dark / Light |
| Setup | Quick math | Dark / Light |
| Calculation | Quick math | Dark / Light |
| CTA | All (shared) | Dark / Light |

### Carousel slides (6 types)

| Slide type | Palette |
|---|---|
| Cover | Light / Dark |
| Math | Light / Dark |
| List | Light / Dark |
| Quote | Light / Dark |
| Pullquote | Light / Dark |
| CTA | Dark only |

---

## What Changes

### Remotion implementation (separate plan)
- Update `tokens.ts` with KOT color, typography, and spacing tokens
- Add palette system (dark/light toggle) to tokens
- Update all carousel slide components to use new tokens and dashed dividers
- Update `LogoMark.tsx` to render boxed-F
- Create 5 new short-form scene components (Myth, Reality, Proof, Setup, Calculation)
- Redesign existing 4 short-form scenes (Hook, Problem, Tip, CTA) with KOT tokens
- Register new compositions in `Root.tsx` (MythBusting, QuickMath)

### Agent updates (separate plan)
- Update `short-form-writer` agent to output content for all 3 content types
- Update `carousel-writer` agent to reference new slide type specs
- Update `remotion-renderer` agent to handle new compositions and palette prop

## Out of Scope

- New carousel content types (checklist, comparison, myth series) — future v2
- Landing page or app UI updates
- Image/video AI model prompt templates
- Audio/voiceover integration
