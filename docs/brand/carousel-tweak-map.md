# Carousel Tweak Map

This note is the fastest way to orient a future local or remote agent before making carousel design changes.

## Where the live carousel lives

- `remotion/src/carousel/Carousel.tsx`
  - Slide dispatcher. If the tweak is "which component renders which slide type" or "how palette gets passed", start here.
- `remotion/src/carousel/types.ts`
  - Slide schema. Change this when the content shape itself changes, such as adding a field like `eyebrow`, `footerNote`, or a new slide type.
- `remotion/src/carousel/tokens.ts`
  - Global design control center. Update this for palette, typography, spacing, canvas padding, or other system-wide look-and-feel changes.

## Shared chrome and layout primitives

- `remotion/src/carousel/primitives/SlideFrame.tsx`
  - Base 1080x1350 slide frame behavior: background, foreground, padding, flex layout.
- `remotion/src/carousel/primitives/Header.tsx`
  - Top row pattern used by interior slides: slide count plus kicker/label.
- `remotion/src/carousel/primitives/SlideCount.tsx`
  - Numbering treatment such as `01 / 06`.
- `remotion/src/carousel/primitives/Rule.tsx`
  - Dashed divider behavior. If the separators need to feel lighter, heavier, tighter, or more branded, edit here first.
- `remotion/src/carousel/primitives/LogoMark.tsx`
  - Brand mark and optional wordmark.
- `remotion/src/carousel/primitives/SwipeCue.tsx`
  - "Swipe" affordance on cover-style slides.

## Slide-specific files

- `remotion/src/carousel/slides/Cover.tsx`
  - Cover hierarchy, top branding row, hero title, subtitle, issue label, swipe cue.
- `remotion/src/carousel/slides/QuoteRule.tsx`
  - Quote/opinion slide treatment.
- `remotion/src/carousel/slides/Math.tsx`
  - Number-heavy line-item slide.
- `remotion/src/carousel/slides/List.tsx`
  - Ranked or multi-point explanation slide.
- `remotion/src/carousel/slides/Pullquote.tsx`
  - Key takeaway plus supporting meta values.
- `remotion/src/carousel/slides/CTA.tsx`
  - Final call-to-action slide. This one is intentionally forced to dark mode.
- `remotion/src/carousel/slides/AccentText.tsx`
  - Highlighted word treatment inside large headlines.

## Composition and preview entrypoints

- `remotion/src/Root.tsx`
  - Default sample carousel content and the registered `Carousel` composition used in preview/render flows.
- `remotion/package.json`
  - Preview command: `npm run preview`
  - Current render example: `npm run render`

## Source-of-truth design docs

- `docs/brand/brand-tokens.md`
  - Canonical visual rules: color, typography, spacing, layout constraints.
- `docs/brand/content-templates.md`
  - Content and slide-family intent.
- `docs/superpowers/specs/2026-04-22-carousel-design-system-redesign.md`
  - Original redesign architecture and file map.
- `docs/superpowers/plans/2026-04-24-kot-content-templates.md`
  - Implementation plan for the current KOT/receipt-style system.

## Quick decision guide

- If every slide should change in the same way, start in `tokens.ts` or a primitive.
- If only one slide family feels off, go straight to that file under `slides/`.
- If the copy structure needs new fields, update `types.ts` first, then the slide component, then the sample props in `Root.tsx`.
- If the change is "make the preview reflect a new design direction", update the sample `Carousel` props in `Root.tsx` so future sessions see the intended baseline immediately.

## Notes worth knowing before editing

- The carousel composition currently uses one frame per slide in `Root.tsx`. That is a simple preview setup, not a timed animation system.
- Several files contain mojibake characters such as `â€”` and `Â·`. If we touch copy-heavy files next, it would be worth normalizing encoding as part of the design pass.
- The CTA slide is hard-coded to use the dark palette in `remotion/src/carousel/slides/CTA.tsx`.
- There are existing uncommitted changes elsewhere in the repo. Avoid broad cleanup and keep carousel edits scoped.

## Approved defaults from current tuning pass

- Cover slide headline default is `128px / 800` via `type.hero` in `remotion/src/carousel/tokens.ts`.
- List slide rows use a wider label column and gutter to protect term/description separation in `remotion/src/carousel/slides/List.tsx`.
- List slide rows also use tighter vertical spacing and slightly smaller description copy to avoid bottom clipping in dense 4-item layouts.
- CTA footer in `remotion/src/carousel/slides/CTA.tsx` treats the pill as non-shrinking and allows the meta text to wrap separately.
- CTA footer decoration uses an opening `* * *` prefix only, not both opening and closing markers, because long meta copy wraps more cleanly that way.

## Suggested workflow for future tweak sessions

1. Open `docs/brand/carousel-tweak-map.md`.
2. Preview with `cd remotion && npm run preview`.
3. Decide whether the change is token-level, primitive-level, or slide-level.
4. Make the smallest edit in the lowest shared layer that solves the problem.
5. If the tweak changes the intended baseline, update the sample carousel props in `remotion/src/Root.tsx`.
