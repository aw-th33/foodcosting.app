# Design Spec: KOT Brand Design System for foodcosting.app

**Date:** 2026-04-24
**Status:** Draft

---

## Problem

The current visual identity (Instrument Serif + Inter, warm off-white, terracotta accent) reads as generic AI-generated SaaS branding. It's well-built but indistinguishable from dozens of other content brands. foodcosting.app needs a visual identity that is instantly recognizable, industry-native, and ownable.

## Decision

Adopt the KOT (Kitchen Order Ticket) / receipt aesthetic as the brand's visual foundation. This borrows the visual language food business owners encounter daily — POS receipts, kitchen tickets, register displays — and applies it across all touchpoints from social content to the landing page.

## Key Design Decisions

### Logo
- **Mark:** Lowercase monospace "f" in a bordered box (register key aesthetic)
- **Wordmark:** "foodcosting" in IBM Plex Mono bold, ".app" as a smaller suffix
- **Variants:** Light (ink on paper) and dark (paper on ink), icon-only for small sizes
- **Replaces:** The current geometric skewed-F SVG mark + Inter wordmark

### Color
- **Core:** ink (#111111), paper (#F8F6F0), receipt (#FFFFFF), faded (#6B6B66), divider (#DDD8CC)
- **Signal:** alert (#C0392B), healthy (#2E7D32), caution (#E68A00) — data-adjacent only
- **Replaces:** The current terracotta accent (#C44A2A), teal (#328589), and warm off-white (#FAFAF7)

### Typography
- **Primary:** IBM Plex Mono — numbers, labels, data, wordmark, receipt elements
- **Secondary:** Inter — headlines, body copy, editorial text
- **Dropped:** Instrument Serif (the main source of "Claude branding" feel), JetBrains Mono
- **Key shift:** Monospace is now the default voice, not the accent

### Layout Patterns
Six receipt-grammar patterns shared across all formats:
1. Line item (label left, value right, dashed dividers)
2. Dashed divider (always dashed, never solid)
3. Receipt header (centered brand between dashed rules)
4. Highlight stamp (inverted monospace block, replaces italic accent)
5. Receipt footer (centered CTA with asterisk decorators)
6. Dark mode (inverted palette for video/CTA)

### Expression Spectrum
- Social content: most literal receipt metaphor
- Video: receipt elements animate like a ticket printing
- Blog/OG: receipt as illustration element
- Landing page: receipt DNA in data cards, abstracted into clean layout
- App UI: monospace numbers, dashed separators, receipt-style summaries

## Artifacts

| File | Purpose | Audience |
|---|---|---|
| `docs/brand/brand-book.md` | Visual brand guide with rationale | Human (Ahmed, designers, collaborators) |
| `docs/brand/brand-tokens.md` | Structured token reference with exact values and constraints | Agents (carousel-writer, short-form-writer, blog-writer, remotion-renderer) |

## What Changes

### Immediate
- Brand guidelines established in `docs/brand/`
- Existing brand constitution at `.claude/skills/foodcosting-carousel-skill/references/brand-constitution.md` to be replaced with a pointer to the new shared reference

### Follow-up (separate implementation plan)
- Update Remotion carousel components (tokens.ts, primitives, slides) to use new design system
- Update Remotion short-form video scenes to align with KOT palette
- Update carousel-writer agent to reference new brand tokens
- Update short-form-writer agent to reference new brand tokens
- Update LogoMark.tsx to render the new monospace boxed F
- Test render a carousel and short-form video with the new system
- Eventually: apply KOT DNA to the landing page and app UI

## Out of Scope

- Landing page redesign (future project)
- App UI changes (future project)
- Remotion component implementation (separate plan)
- Image model prompt templates (separate plan, after tokens are proven in Remotion)
