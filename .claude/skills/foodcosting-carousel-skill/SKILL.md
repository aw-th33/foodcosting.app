---
name: foodcosting-carousel
description: Create Instagram/LinkedIn carousel posts for foodcosting.app. Use this skill whenever asked to create a carousel, multi-slide post, swipe post, or content series for foodcosting.app social media. Also trigger when asked to create educational content, data posts, or thought leadership posts for foodcosting.app even if the word "carousel" is not used. Always use this skill for foodcosting.app social content creation.
---

# foodcosting.app Carousel Skill

Read `references/brand-constitution.md` before starting. All color, type, and voice rules live there. This skill defines the current Minimal Editorial carousel system used by the Remotion `Carousel` composition.

---

## Canvas

Every slide is **1080 x 1350px** (Instagram 4:5 format).

```text
Canvas:     1080 x 1350px
Padding:    96px all sides
Background: #FAFAF7
FPS:        30
```

Use warm off-white editorial space, serif display type, hairline rules, and restrained accents. Do not use the legacy square canvas, legacy vertical layout, chart bars, or black CTA slide.

---

## Tokens

Use only the colors and spacing from the Remotion carousel design system.

```ts
color.bg = '#FAFAF7'
color.fg = '#0E0E0E'
color.muted = '#6B6B66'
color.line = '#0E0E0E'
color.paper = '#F4F1EA'
color.accent = '#C44A2A'
color.ok = '#3E9B57'
color.warn = '#D99A3B'
```

Rules:

- 95% of every slide is `bg` and `fg`.
- `muted` is for labels, subtitles, captions, and secondary text.
- `accent` appears once per slide max, usually as one italicized word or phrase.
- Do not use pure black, pure white, gradients, shadows, blur, emoji, or decorative food illustrations.
- Spacing values must come from this scale: `8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 128`.

---

## Typography

Use the current Remotion font families:

- Display: Instrument Serif, Georgia, serif
- Body: Inter, system-ui, sans-serif
- Mono: JetBrains Mono, ui-monospace, monospace

Display type uses font weight 400. Italics are meaningful and should be used at most once per slide, in the accent color.

Approved type roles:

| Role | Size | Notes |
|---|---:|---|
| hero | 150px | Cover headline |
| xl | 128px | CTA headline |
| l | 108px | Large editorial headline |
| m | 96px | Mid editorial headline |
| s | 88px | Pullquote/list emphasis |
| bodyL | 32px | Large body |
| bodyM | 28px | Body and descriptions |
| label | 24px | Mono uppercase labels |
| count | 24px | Slide count |
| caption | 22px | Footer/meta copy |

Body copy max width is 780px.

---

## Slide Families

Only these slide types are valid. They must match `remotion/src/carousel/types.ts`.

### `cover`

Use for the opening slide.

Required props:

- `type: "cover"`
- `kicker`: 1-3 word mono label, e.g. `HOT TAKE`
- `title`: 8-14 word headline
- `subtitle`: one or two muted sentences

Optional props:

- `accent`: one word or short phrase from the title to italicize in accent color
- `issueLabel`: e.g. `Field Notes / 01`

### `quote`

Use for the old rule, flawed belief, or customer/operator quote the post will challenge.

Required props:

- `type: "quote"`
- `kicker`
- `quote`

Optional props:

- `preface`
- `attribution`

### `math`

Use for simple food-cost arithmetic, formulas, or line-by-line margin logic.

Required props:

- `type: "math"`
- `kicker`
- `headline`
- `lines`: array of `{ "label": "string", "value": "string", "accent": boolean optional }`

Optional props:

- `footnote`

### `list`

Use for 3-5 concrete misses, leaks, reasons, or steps.

Required props:

- `type: "list"`
- `kicker`
- `headline`
- `items`: array of `{ "term": "string", "description": "string" }`

### `pullquote`

Use for the core takeaway or second-to-last tension/shift slide.

Required props:

- `type: "pullquote"`
- `kicker`
- `quote`: 24 words max
- `meta`: array of one or two `{ "label": "string", "value": "string", "accent": boolean optional }`

### `cta`

Use for the final slide only.

Required props:

- `type: "cta"`
- `kicker`
- `headline`: 8 words max
- `body`: one muted sentence

Optional props:

- `pill`: defaults conceptually to `link in bio` if omitted
- `meta`: short share/save cue

---

## Structure

Default sequence:

```text
cover -> quote -> math -> list -> pullquote -> cta
```

Variable-length carousels may add or omit middle slides, but every slide must use one of the six valid slide families and the final slide must be `cta`.

Recommended structures:

| Format | Slide count | Structure |
|---|---:|---|
| Quick tip | 4 | cover + math/list + pullquote + cta |
| Educational | 6 | cover + quote + math + list + pullquote + cta |
| Data story | 6-7 | cover + quote + math + list/math + pullquote + cta |
| Deep dive | 8-10 max | cover + quote + 4-6 math/list/pullquote slides + cta |

Never exceed 10 slides.

---

## Output Format

Produce a complete carousel brief followed by exactly one complete Remotion props block.

````markdown
POST TOPIC: [topic]
POST FORMAT: [Quick tip / Educational / Data story / Deep dive]
SLIDE COUNT: [n]

---

SLIDE 1 - COVER
Type: cover
Kicker: [copy]
Title: [copy]
Accent: [one title word/phrase or NONE]
Subtitle: [copy]
Issue label: [copy or NONE]
Design notes: 1080x1350, warm off-white background, logo/issue label top, editorial headline mid, subtitle and swipe cue bottom.

---

SLIDE 2 - [LABEL]
Type: quote | math | list | pullquote
[List every prop value required by that slide type.]
Design notes: [Brief layout note using Minimal Editorial zones, type roles, and accent usage.]

---

LAST SLIDE - CTA
Type: cta
Kicker: [copy]
Headline: [copy]
Body: [copy]
Pill: [copy or NONE]
Meta: [copy or NONE]

---

CAPTION:
[full caption text]

HASHTAGS:
#restaurantbusiness #foodcost #restaurantmanagement #fandbbusiness #foodcosting

---

## Remotion props

```json
{
  "slides": [
    {
      "type": "cover",
      "kicker": "HOT TAKE",
      "title": "Your ideal food cost means nothing if actual keeps drifting.",
      "accent": "nothing",
      "subtitle": "Most operators are managing the wrong number. The gap between target and reality is where profit disappears.",
      "issueLabel": "Field Notes / 01"
    },
    {
      "type": "quote",
      "kicker": "THE OLD BELIEF",
      "preface": "You've heard it in every menu meeting -",
      "quote": "\"If the target says 28%, the menu is healthy.\"",
      "attribution": "- said before the prep bin hit the trash"
    },
    {
      "type": "math",
      "kicker": "FAST MATH",
      "headline": "A 28% target becomes 35% fast when the kitchen gets real.",
      "lines": [
        { "label": "Ideal", "value": "28% planned food cost" },
        { "label": "Waste", "value": "+3% trim, spoilage, over-prep" },
        { "label": "Actual", "value": "35% after service", "accent": true }
      ],
      "footnote": "Seven points of drift can wipe out the margin you thought the menu had."
    },
    {
      "type": "list",
      "kicker": "WHAT IT MISSES",
      "headline": "Four leaks hiding behind one clean percentage.",
      "items": [
        { "term": "Waste", "description": "Prep loss eats margin before service starts." },
        { "term": "Yield", "description": "A 10 lb case is not 10 lb of usable food." },
        { "term": "Updates", "description": "Supplier prices move faster than old recipe cards." }
      ]
    },
    {
      "type": "pullquote",
      "kicker": "DO THIS INSTEAD",
      "quote": "Track ideal and actual side by side, then fix the gap before it becomes the month.",
      "meta": [
        { "label": "The question", "value": "What changed?" },
        { "label": "The target", "value": "price, portion, or prep", "accent": true }
      ]
    },
    {
      "type": "cta",
      "kicker": "PRICE SMARTER",
      "headline": "Get the free dish costing calculator.",
      "body": "Enter ingredients, yields, and your target food cost. Get a price that leaves room for profit.",
      "pill": "link in bio"
    }
  ]
}
```
````

The `## Remotion props` section must contain one complete JSON object. Do not split slides across multiple JSON blocks.

---

## Guardrails

- Never emit `hook`, `content`, or `data` slide types.
- Never use the legacy square canvas or black CTA system.
- Never invent props outside `remotion/src/carousel/types.ts`.
- Do not abbreviate slides with "same as previous" or "similar to slide N".
- Every slide needs specific food business language, a number, a concrete consequence, or a named operator scenario.
- Keep the CTA to one action: visit foodcosting.app or use the free calculator.
