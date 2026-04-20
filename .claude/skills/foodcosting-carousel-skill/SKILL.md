---
name: foodcosting-carousel
description: Create Instagram/LinkedIn carousel posts for foodcosting.app. Use this skill whenever asked to create a carousel, multi-slide post, swipe post, or content series for foodcosting.app social media. Also trigger when asked to create educational content, data posts, or thought leadership posts for foodcosting.app even if the word "carousel" is not used. Always use this skill for foodcosting.app social content creation.
---

# foodcosting.app Carousel Skill

Read `references/brand-constitution.md` before starting. All color, type, and voice rules live there. This skill adds carousel-specific structure and precise canvas specs on top of those foundations.

---

## Canvas specification

Every slide is **1080 x 1080px** (Instagram square format). All measurements below are in pixels at this canvas size. Do not scale down. Do not use document-scale font sizes.

```
Canvas:       1080 x 1080px
Background:   #FFFFFF always (except final CTA slide)
Safe zone:    80px margin all four sides
Content area: 920px wide, starts at x=80, ends at x=1000
```

**The single most common mistake is treating this like a document.** It is a social post viewed on a phone. Everything must be larger than feels comfortable in a document context.

---

## Typography at 1080x1080

These are the only permitted font sizes. Do not use any other sizes.

| Role | Size | Weight | Color | Tracking |
|---|---|---|---|---|
| Hook headline | 72-96px | 800 | #111111 | -0.03em |
| Content headline | 52-64px | 700 | #111111 | -0.02em |
| Phase label | 28px | 500 | #999999 | 0.08em uppercase |
| Body / detail | 32-36px | 400 | #666666 | normal |
| Chart label | 28px | 500 | contextual | normal |
| Hero number (data slide) | 180-220px | 800 | #111111 | -0.04em |
| Ghost number (decorative) | 320-400px | 800 | #F0F0F0 | -0.06em |
| CTA headline | 56-64px | 700 | #FFFFFF | -0.02em |
| CTA link | 32px | 400 | #FFFFFF | normal |
| Wordmark | 24px | 500 | #444444 | 0.04em |

Line height: 1.1 for headlines, 1.5 for body text.

---

## Vertical layout: the bottom-third rule

Content on every slide (except data slides) anchors to the **bottom third** of the canvas, not the top or center.

```
Top zone     (y=0 to y=360):    EMPTY. White space only.
Middle zone  (y=360 to y=620):  Ghost number or decorative element only.
Content zone (y=620 to y=920):  All text and charts live here.
Footer zone  (y=920 to y=1000): Wordmark (last slide only).
```

The generous empty space at the top is intentional. It is what makes the posts feel clean and minimal. Do not fill it.

**Exception — Hook slide**: Headline sits vertically centered between y=400 and y=680. Subtext sits 40px below the headline baseline. Nothing else.

**Exception — Data slide**: Hero number is centered vertically and horizontally on the full canvas.

**Exception — CTA slide**: All content vertically centered on black canvas.

---

## Carousel structure

Every foodcosting.app carousel follows this exact sequence:

### Slide 1: Hook

Purpose: Stop the scroll. One idea only.

Layout:
- Canvas: white, no charts, no bars
- Headline: vertically centered around y=500, horizontally centered, x=540
- Font: 72-96px / 800 / #111111 / -0.03em tracking
- Subtext (optional): 36px / 400 / #999999 / 40px below headline baseline / centered
- Ghost number (optional): 320-400px / #F0F0F0 / centered behind headline

Rules:
- Maximum 12 words in headline
- No wordmark on this slide
- No data visualization on this slide
- The headline must work as a standalone sentence someone would screenshot and share

Good examples:
- "Most restaurants think they know their food cost. They don't."
- "Your chef knows the recipe. Does anyone know the cost?"
- "The number that separates a good restaurant from a great one."

### Slides 2-N: Content slides

Purpose: Deliver the value. One point per slide.

Layout:
- Phase label: x=80, y=640 — 28px / 500 / #999999 / uppercase (e.g. "01 /")
- Content headline: x=80, y=700 — 52-64px / 700 / #111111 / line-height 1.1
- Body text: x=80, y=780 (or 40px below headline baseline) — 32px / 400 / #666666 / max-width 920px
- Chart (if present): below body text, minimum 48px gap, never above body text
- Content headline must not exceed 2 lines at 52-64px within 920px width
- Body text must not exceed 3 lines at 32px

Rules:
- One chart or data bar maximum per slide
- No ghost numbers on content slides (ghost numbers are for data slides only)
- Body text states the specific cost or consequence, not a general principle

### Data slides (insert between content slides as needed)

Purpose: Make the number the hero. The number IS the slide.

Layout:
- Hero number: fully centered, x=540 (center), y=540 (center) — 180-220px / 800 / #111111
- Unit suffix: same baseline as hero number, immediately right — 80px / 400 / #999999
- Label above: y=340 — 28px / 500 / #999999 / uppercase / centered
- Context line below: y=700 — 32px / 400 / #666666 / centered / 1 line max
- Ghost number behind: 320-400px / #F0F0F0 / same center as hero number

Rules:
- One number only. Never two statistics on a data slide.
- The ghost number is always the same value as the hero number, the decorative underlay.

### Second-to-last slide: Tension

Purpose: Name the cost of inaction. Create urgency before the CTA.

Layout: Same as content slides.

This slide must contain either:
- A before/after two-column comparison with specific numbers (e.g. estimated vs actual)
- A single sentence naming the monthly or annual cost of the problem
- A direct question the reader must answer honestly ("Do you know yours?")

### Last slide: CTA

Purpose: One action only.

Layout:
- Background: #111111 (the ONLY black-background slide in the entire carousel)
- All content vertically and horizontally centered
- CTA headline: 56-64px / 700 / #FFFFFF / centered / 1-2 lines max
- CTA link line: "foodcosting.app →" — 32px / 400 / #FFFFFF / centered / 40px below headline baseline
- Social proof (optional): 24px / 400 / #555555 / centered / 60px below CTA link
- Wordmark: x=960 (right-aligned to safe zone edge), y=1048 — 24px / 500 / #444444

Rules:
- Black background reserved exclusively for this slide. Never use it elsewhere.
- Wordmark appears on this slide only.
- No charts, no bars, no ghost numbers.

---

## Chart specifications at 1080x1080

All charts anchor inside the content zone (y=620 to y=920), below the body text with minimum 48px gap.

### Horizontal comparison bar

Use for: target vs actual, before vs after, profitable vs average.

```
Bar height:       48px per bar (minimum — never thinner)
Bar width:        840px max (x=80 to x=920)
Gap between bars: 32px
Label above bar:  28px / 500 / #999999, 12px above bar top, x=80
Value label:      32px / 700 / color-matched to bar, right-aligned at x=1000
Bar border-radius: 4px
```

Color rules:
- Target / profitable / under budget: fill #328589
- Actual / over budget / at risk: fill #E05252
- Industry average / neutral benchmark: fill #111111

### Zone spectrum bar

Use for: showing where a number sits on a spectrum (e.g. food cost % zones).

```
Bar height:   16px
Bar width:    840px (x=80 to x=920)
Zone colors:  #328589 (good) | #111111 (average) | #E05252 (danger)
Marker dot:   12px circle / #111111 / positioned above bar at correct % position
Marker line:  1px vertical / 24px tall / from dot down to bar top
Zone labels:  28px / 500 / color-matched / below bar / 16px gap
```

### Two-column stat comparison

Use for: side-by-side number contrast (28% estimated vs 34% actual).

```
Left column:    x=80 to x=460, center-aligned within column
Right column:   x=540 to x=920, center-aligned within column
Divider:        1px / #E5E5E5 / x=500 / spanning y=660 to y=880
Number size:    120px / 800
Label:          28px / 400 / #999999 / 20px below number baseline
Number color:   left = #111111 (estimated/target) / right = #E05252 (actual/over)
```

---

## Slide count guidelines

| Post type | Slide count | Structure |
|---|---|---|
| Quick tip | 4 | Hook + 2 content + CTA |
| Educational explainer | 6 | Hook + 3 content + tension + CTA |
| Data story | 7 | Hook + 2 content + 2 data + tension + CTA |
| Deep dive | 9-10 max | Hook + 4-5 content + data + tension + CTA |

Never exceed 10 slides.

---

## Caption (post body text)

Structure:
1. Line 1: Restate the hook as a punchy standalone sentence
2. Lines 2-4: One sentence per content slide summarising the key point
3. Blank line
4. CTA: "Know your number. foodcosting.app"
5. Blank line
6. Hashtags: #restaurantbusiness #foodcost #restaurantmanagement #fandbbusiness #foodcosting

---

## Output format

Produce a structured brief in this exact format. Every measurement must be explicit. This brief is handed directly to a designer or code renderer.

```
POST TOPIC: [topic]
POST FORMAT: [Educational / Data story / Quick tip / Deep dive]
SLIDE COUNT: [n]

---

SLIDE 1 - HOOK
Canvas: 1080x1080px / background #FFFFFF
Headline: "[copy]"
  Position: centered, y-center ~500
  Font: Inter 800, [72-96]px, #111111, -0.03em tracking, line-height 1.1
Subtext: "[copy]" or NONE
  Position: centered, y=[headline baseline + 40px]
  Font: Inter 400, 36px, #999999
Ghost number: "[value]" or NONE
  Position: centered behind headline
  Font: Inter 800, 360px, #F0F0F0, -0.06em tracking

---

SLIDE [n] - [DESCRIPTIVE LABEL]
Canvas: 1080x1080px / background #FFFFFF
Phase label: "[e.g. 01 /]"
  Position: x=80, y=640
  Font: Inter 500, 28px, #999999, uppercase, 0.08em tracking
Headline: "[copy]"
  Position: x=80, y=700
  Font: Inter 700, [52-64]px, #111111, -0.02em tracking, line-height 1.1
Body: "[copy]"
  Position: x=80, y=[headline baseline + 40px], max-width 920px
  Font: Inter 400, 32px, #666666, line-height 1.5
Chart: [NONE] or [chart type below]
  [If horizontal bar:]
  Bar 1 label: "[label]" / value: [n]% / fill: [color] / height: 48px / width: [n]px
  Bar 2 label: "[label]" / value: [n]% / fill: [color] / height: 48px / width: [n]px
  [If two-column stat:]
  Left number: "[value]" / label: "[label]" / color: #111111
  Right number: "[value]" / label: "[label]" / color: #E05252

---

SLIDE [n] - DATA
Canvas: 1080x1080px / background #FFFFFF
Ghost number: "[value]"
  Position: centered, x=540, y=540
  Font: Inter 800, 360px, #F0F0F0, -0.06em tracking
Hero number: "[value]"
  Position: centered, x=540, y=540
  Font: Inter 800, 200px, #111111, -0.04em tracking
Unit: "[e.g. %]"
  Position: same baseline as hero number, immediately right
  Font: Inter 400, 80px, #999999
Label above: "[copy]"
  Position: centered, y=340
  Font: Inter 500, 28px, #999999, uppercase
Context line: "[copy]"
  Position: centered, y=720
  Font: Inter 400, 32px, #666666

---

LAST SLIDE - CTA
Canvas: 1080x1080px / background #111111
Headline: "[copy]"
  Position: centered, y-center ~480
  Font: Inter 700, 60px, #FFFFFF, -0.02em tracking, line-height 1.1
CTA line: "foodcosting.app →"
  Position: centered, y=[headline baseline + 40px]
  Font: Inter 400, 32px, #FFFFFF
Social proof: "[copy]" or NONE
  Position: centered, y=[CTA baseline + 60px]
  Font: Inter 400, 24px, #555555
Wordmark: "foodcosting.app"
  Position: x=960 (right-align), y=1048
  Font: Inter 500, 24px, #444444

---

CAPTION:
[full caption text]

HASHTAGS:
[hashtags]
```

---

## Common mistakes to avoid

- **Font sizes from document world are wrong here.** 14px, 16px, 18px are invisible at social scale. Minimum body size is 32px. Minimum headline size is 52px on content slides, 72px on the hook.
- **Content must anchor to the bottom third (y=620+).** Text starting at y=200 looks like a document page, not a social post.
- **The top half of every content slide should be mostly empty.** This is intentional. Do not fill it.
- **Wordmark on last slide only**, bottom-right at 24px.
- **Black background on CTA slide only.** Nowhere else.
- **No decorative food illustrations or icons.** Data and typography are the only visuals.
- **Sentence case everywhere.** Never Title Case or ALL CAPS.
- **Every chart bar must be 48px tall minimum.** Thinner bars disappear on mobile screens.
- **One chart per slide maximum.**
- **GP Teal (#328589) is a data color only.** It indicates a positive/profitable state in charts. Never use it as a decorative brand color.
- **Every slide must contain a specific number or named scenario.** If a slide has no number and no named operator scenario, rewrite it before output.
