# Carousel Design System Redesign — Spec

**Date:** 2026-04-22
**Status:** Approved
**Approach:** Full replacement (Option A)

---

## Overview

Replace the existing Remotion carousel system with the Minimal Editorial design system from the Claude Design handoff bundle. This is a full replacement — old slide types, tokens, and components are deleted and rebuilt from scratch.

---

## Canvas

| Property | Old | New |
| -------- | --- | --- |
| Size | 1080×1080 (1:1) | **1080×1350 (4:5)** |
| Padding | 80px | **96px all sides** |
| Background | `#FFFFFF` | **`#FAFAF7`** (warm off-white) |
| FPS | 30 | 30 |

Root.tsx Carousel composition: `width={1080}` `height={1350}` `fps={30}` `durationInFrames={slides.length}`

---

## Color Tokens

```ts
export const color = {
  bg:     '#FAFAF7',   // warm off-white — every slide background
  fg:     '#0E0E0E',   // near-black — all primary text
  muted:  '#6B6B66',   // secondary text, labels, captions
  line:   '#0E0E0E',   // hairline rules (same as fg)
  paper:  '#F4F1EA',   // card insets (used sparingly)
  accent: '#C44A2A',   // terracotta — ONE use per slide max
  ok:     '#3E9B57',   // healthy green (comparison slides only)
  warn:   '#D99A3B',   // borderline amber (comparison slides only)
} as const;
```

Rules:

- 95% of every slide is `bg` + `fg`
- `muted` for labels, subtitles, captions — never body
- `accent` appears once per slide max — the punchline, not the voice
- No pure `#000000` or `#FFFFFF`. No drop shadows. No gradients. No blur.

---

## Typography

```ts
export const font = {
  display: "'Instrument Serif', Georgia, serif",
  body:    "'Inter', system-ui, sans-serif",
  mono:    "'JetBrains Mono', ui-monospace, monospace",
} as const;

export const type = {
  hero:    { fontSize: 150, lineHeight: 0.98, letterSpacing: '-0.025em', fontFamily: font.display },
  xl:      { fontSize: 128, lineHeight: 0.98, letterSpacing: '-0.03em',  fontFamily: font.display },
  l:       { fontSize: 108, lineHeight: 1.04, letterSpacing: '-0.02em',  fontFamily: font.display },
  m:       { fontSize:  96, lineHeight: 1.00, letterSpacing: '-0.02em',  fontFamily: font.display },
  s:       { fontSize:  88, lineHeight: 1.04, letterSpacing: '-0.02em',  fontFamily: font.display },
  bodyL:   { fontSize:  32, lineHeight: 1.40, fontFamily: font.body },
  bodyM:   { fontSize:  28, lineHeight: 1.45, fontFamily: font.body },
  label:   { fontSize:  24, letterSpacing: '0.14em', textTransform: 'uppercase', fontFamily: font.mono },
  count:   { fontSize:  24, letterSpacing: '0.10em', fontFamily: font.mono },
  caption: { fontSize:  22, letterSpacing: '0.10em', fontFamily: font.mono },
} as const;
```

`fonts.ts` is imported at the top of `Root.tsx` (side-effect import: `import './carousel/fonts'`) so fonts load before any composition renders.

Fonts loaded via `@remotion/google-fonts`:

- Instrument Serif — weights 400 regular + 400 italic
- Inter — weights 400, 500, 600
- JetBrains Mono — weights 400, 500

Rules:

- Display sizes always use `fontWeight: 400` — never bold
- Italics are meaningful: exactly one `<em>` per slide max, always in `accent` color
- Body copy max width: 780px

---

## Spacing Scale

Only these values: `8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 128` px.

---

## File Structure

```text
remotion/src/carousel/
  tokens.ts              ← full replacement
  fonts.ts               ← NEW
  types.ts               ← full replacement
  Carousel.tsx           ← updated imports only
  primitives/
    LogoMark.tsx         ← NEW
    SlideFrame.tsx       ← NEW
    SlideCount.tsx       ← NEW
    Rule.tsx             ← NEW
    SwipeCue.tsx         ← NEW
  slides/
    Cover.tsx            ← NEW (replaces HookSlide.tsx)
    QuoteRule.tsx        ← NEW
    Math.tsx             ← NEW
    List.tsx             ← NEW (replaces ContentSlide.tsx)
    Pullquote.tsx        ← NEW (replaces DataSlide.tsx)
    CTA.tsx              ← NEW (replaces CTASlide.tsx)
```

**Deleted:** `HookSlide.tsx`, `ContentSlide.tsx`, `DataSlide.tsx`, `CTASlide.tsx`

---

## Type Schemas

```ts
export interface CoverSlide {
  type: 'cover';
  kicker: string;      // "HOT TAKE" — mono uppercase, 1–3 words
  title: string;       // 8–14 words, main headline
  accent?: string;     // ONE word within title to italicize in accent color
  subtitle: string;    // ≤ 2 sentences, muted
}

export interface QuoteSlide {
  type: 'quote';
  kicker: string;
  preface?: string;    // lead-in above quote, muted uppercase
  quote: string;       // large serif quote body
  attribution?: string;
}

export interface MathSlide {
  type: 'math';
  kicker: string;
  headline: string;    // display/s serif
  lines: { label: string; value: string; accent?: boolean }[];
  footnote?: string;
}

export interface ListSlide {
  type: 'list';
  kicker: string;
  headline: string;    // display/m serif
  items: { term: string; description: string }[]; // 3–5 items
}

export interface PullquoteSlide {
  type: 'pullquote';
  kicker: string;
  quote: string;       // ≤ 24 words
  meta: { label: string; value: string }[]; // 1–2 formula/example pairs
}

export interface CTASlide {
  type: 'cta';
  kicker: string;      // "PRICE SMARTER"
  headline: string;    // display/xl serif, ≤ 8 words
  body: string;        // 1 sentence, muted
  pill?: string;       // default: "🔗 link in bio"
}

export type Slide = CoverSlide | QuoteSlide | MathSlide | ListSlide | PullquoteSlide | CTASlide;

export interface CarouselProps {
  slides: Slide[];
}
```

Slide counter (`n / total`) derived from slide index and `slides.length` — not stored in props.

---

## Primitives

### LogoMark

Abstract F-mark inline SVG + "foodcosting" wordmark in Inter 600. Accepts `size` and `color` props. No external asset dependency.

### SlideFrame

`AbsoluteFill` with `background: color.bg`, `color: color.fg`, `padding: 96px`, `display: flex`, `flexDirection: column`. Accepts optional `bg`/`fg` overrides.

### SlideCount

`n / total` in JetBrains Mono, `count` type scale, `color.muted`. Zero-padded: `01 / 06`.

### Rule

`1px solid color.line` at `opacity: 0.8`. No `rgba`. Full width.

### SwipeCue

Mono uppercase "SWIPE" + inline arrow SVG. `color.muted`. Cover slide only.

---

## Slide Layout Rules

Every slide uses three zones:

```text
[HEADER]  — SlideCount left, kicker right  (except Cover + CTA)
[CONTENT] — flex: 1, centered vertically
[FOOTER]  — attribution or swipe cue
```

- **Cover:** logo + issue label top, kicker + hero headline mid, subtitle + SwipeCue bottom
- **Quote:** Header top, large serif quote centered, mono attribution bottom
- **Math:** Header top, serif headline + Rule + mono grid centered, optional footnote bottom
- **List:** Header top, serif headline, numbered rows with hairline Rules, each row = `SlideCount · italic serif term · body description`
- **Pullquote:** Header top, oversized `"` in accent, serif quote, mono meta pairs bottom
- **CTA:** LogoMark top, mono kicker, display/xl headline, body line, pill + share-meta bottom

Border radius: `0` everywhere except CTA pill (`999px`). No mid-size radii.

---

## remotion-renderer Agent Update

The agent's `## Remotion props` extraction logic in Path B (carousel rendering) must be updated to expect the new schema. The existing example shape in the agent instructions references `hook`, `content`, `data`, `cta` types — replace with the 6 new types above.

The Notion carousel page body format changes from:

```json
{ "slides": [ { "type": "hook", ... }, { "type": "cta", ... } ] }
```

to:

```json
{ "slides": [ { "type": "cover", ... }, { "type": "cta", ... } ] }
```

---

## Out of Scope (Phase 2)

- Motion: word-stagger headline entry, count-up numbers, 12-frame fade transitions
- `@remotion/transitions` cross-cut between slides

---

## Constraints

- No colors outside `tokens.ts`
- No fonts outside the three families
- No drop shadows, gradients, blur, or emoji (except `🔗` on CTA pill)
- No chart colors, no additional border-radius values
- Spacing values must be from the scale only
