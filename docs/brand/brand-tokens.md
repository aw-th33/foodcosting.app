# foodcosting.app — Brand Tokens (Agent Reference)

This file is the single source of truth for all visual decisions. Agents must follow these tokens exactly. No interpretation, no creative liberty on values.

---

## Identity

- brand_name: foodcosting.app
- brand_concept: KOT / receipt aesthetic — the visual language of POS receipts and kitchen order tickets
- audience: Restaurant owners, F&B managers, dark kitchen operators, food truck operators, caterers, home bakers

## Logo

- mark: lowercase monospace "f" inside a bordered box
- mark_font: IBM Plex Mono, bold
- mark_border: 2px solid, border-radius 3px
- mark_letter: always lowercase
- wordmark_text: "foodcosting"
- wordmark_font: IBM Plex Mono, 700
- wordmark_spacing: 0.05em
- suffix_text: ".app"
- suffix_style: separate element, smaller, faded color
- variants: light (ink on paper), dark (paper-text on ink)
- icon_only: boxed f without wordmark (favicon, watermark)

## Colors

### Core

| Token | Hex | RGB | Usage |
|---|---|---|---|
| ink | #111111 | 17, 17, 17 | Headlines, borders, CTA backgrounds, primary text |
| paper | #F8F6F0 | 248, 246, 240 | Canvas background |
| receipt | #FFFFFF | 255, 255, 255 | Card surfaces, data card backgrounds |
| faded | #6B6B66 | 107, 107, 102 | Secondary text, labels, timestamps |
| divider | #DDD8CC | 221, 216, 204 | Dashed rules, separators |

### Signal (data-adjacent only)

| Token | Hex | RGB | Usage |
|---|---|---|---|
| alert | #C0392B | 192, 57, 43 | High food cost, losses, danger numbers |
| healthy | #2E7D32 | 46, 125, 50 | Good margins, target hit, profit |
| caution | #E68A00 | 230, 138, 0 | Borderline numbers, warnings |

### Dark Mode (video / CTA)

| Token | Hex | Usage |
|---|---|---|
| dark_bg | #111111 | Background |
| dark_text | #F0ECE4 | Primary text |
| dark_faded | #888888 | Secondary text |
| dark_divider | #333333 | Dashed rules |

### Color Constraints

- signal_colors_data_only: true
- signal_colors_never_decorative: true
- gradient: never
- shadow: never
- blur: never
- glow: never
- surface_ratio: "95% ink + paper + receipt"

## Typography

### Families

| Role | Family | Fallback | Usage |
|---|---|---|---|
| mono | IBM Plex Mono | 'Courier New', monospace | Numbers, labels, data, wordmark, counters, footers |
| sans | Inter | system-ui, sans-serif | Headlines, body copy, editorial, CTA text |

### Prohibited

- serif: never (no Instrument Serif, no Georgia, no Times)

### Type Scale (carousel context, 1080px wide)

| Role | Family | Size | Weight | Letter Spacing | Line Height | Notes |
|---|---|---|---|---|---|---|
| hero | sans | 120-150px | 800 | -0.025em | 0.98 | Cover slide headline |
| headline_l | sans | 96-108px | 700 | -0.02em | 1.04 | Large editorial headline |
| headline_m | sans | 80-96px | 700 | -0.02em | 1.00 | Mid editorial headline |
| headline_s | sans | 72-88px | 700 | -0.02em | 1.04 | Small headline, lists |
| body_l | sans | 32px | 400 | normal | 1.40 | Large body text |
| body_m | sans | 28px | 400 | normal | 1.45 | Standard body text |
| data_xl | mono | 80-120px | 700 | normal | 1.00 | Hero numbers, key stats |
| data_l | mono | 48-64px | 700 | normal | 1.00 | Calculation results |
| data_m | mono | 32-40px | 700 | normal | 1.00 | Line item values |
| label | mono | 22-24px | 500 | 0.14em | 1.00 | Uppercase kickers, labels |
| counter | mono | 22-24px | 400 | 0.10em | 1.00 | Slide counter (01 / 06) |
| caption | mono | 20-22px | 400 | 0.10em | 1.30 | Footer, meta, timestamps |
| stamp | mono | 28-36px | 700 | 0.05em | 1.00 | Highlight stamps (inverted bg) |

### Type Scale (web context, base sizes)

| Role | Family | Size | Weight | Letter Spacing | Line Height |
|---|---|---|---|---|---|
| hero | sans | 48px | 800 | -0.03em | 1.05 |
| headline | sans | 28-32px | 700 | -0.02em | 1.15 |
| subheading | sans | 16-18px | 400 | normal | 1.40 |
| body | sans | 15px | 400 | normal | 1.60 |
| label | mono | 11px | 500 | 0.1em | 1.00 |
| cta | sans | 14px | 600 | normal | 1.00 |
| data | mono | context | 700 | normal | 1.00 |
| watermark | mono | 10px | 500 | 0.05em | 1.00 |

### Typography Constraints

- numbers_always_mono: true
- default_family: mono (use sans only when readability of longer text demands it)
- case: sentence case always
- title_case: never
- all_caps: only for label role
- max_body_width: 780px (carousel), 65ch (web)

## Layout

### Canvas Sizes

| Format | Width | Height | Ratio |
|---|---|---|---|
| carousel | 1080px | 1350px | 4:5 |
| short_video | 1080px | 1920px | 9:16 |
| single_post | 1080px | 1080px | 1:1 |
| og_image | 1200px | 630px | ~1.9:1 |
| story | 1080px | 1920px | 9:16 |

### Spacing

- base_unit: 8px
- scale: 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 128
- canvas_padding: 96px (carousel), 40px minimum (web)
- border_radius: 0 everywhere except logo box (3px) and CTA pill (999px)

### Layout Patterns

#### line_item
```
structure: label (left) — value (right)
divider: 1px dashed {divider}
total_divider: 2px dashed {ink}
total_style: bold, ink color
alignment: space-between
```

#### dashed_divider
```
style: always dashed, never solid
light: 1px dashed {divider} — between items
heavy: 2px dashed {ink} — before totals
```

#### receipt_header
```
structure: dashed rule — centered monospace brand name — dashed rule
font: mono, label size, faded color
use: slide headers, section openers, watermarks
```

#### highlight_stamp
```
structure: inverted monospace text block
background: ink (neutral), alert/healthy/caution (with data)
text: paper color on dark bg, white on signal bg
font: mono, stamp size, bold
max_per_slide: 1
replaces: italic accent pattern
```

#### receipt_footer
```
structure: dashed rule — centered CTA — brand name
cta_decorator: asterisk (* * * text * * *)
font: mono, caption size, faded color
```

#### dark_mode
```
use: video scenes, CTA slides
bg: {dark_bg}
text: {dark_text}
secondary: {dark_faded}
dividers: 1px dashed {dark_divider}
same patterns as light, inverted palette
```

### Layout Constraints

- solid_lines: never (always dashed)
- colored_backgrounds: never (except dark_mode)
- decorative_elements: never
- illustrations: never
- emoji: never
- one_primary_visual_per_slide: true
- max_slides_carousel: 10

## Voice

- tone: direct, operator-minded, number-first
- specificity: "34% food cost" not "high food cost"
- banned: food puns, startup hype, buzzwords
- case: sentence case everywhere including headlines
- formulas:
  - hook: "[Bold claim] + [The number that proves it]"
  - education: "[Problem] + [Why it happens] + [Fix]"
  - data: "[One number, huge] + [What it means] + [CTA]"
