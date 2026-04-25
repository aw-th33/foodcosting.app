POST TOPIC: Ideal food cost percentage by business type — benchmarks for restaurants, food trucks, and caterers
POST FORMAT: Data story
SLIDE COUNT: 6

---

SLIDE 1 - COVER
Type: cover
Kicker: KNOW YOUR NUMBER
Title: Your food cost target depends on how you cook, not just what you sell
Accent: depends
Subtitle: The "keep it low" advice is not a target. Here are the real benchmarks by business type.
Issue label: Field Notes / 02
Design notes: 1080x1350, warm off-white background. Instrument Serif for the headline. "depends" italicized in accent color (#C44A2A). Kicker mono label top-left. Subtitle muted below headline. Swipe cue at bottom.

---

SLIDE 2 - THE COMMON BELIEF
Type: quote
Kicker: THE COMMON BELIEF
Preface: Every operator hears this early on —
Quote: "Keep your food cost low and the margins take care of themselves."
Attribution: — said without specifying what "low" means for your format
Design notes: Large display quote centered in the editorial field. Kicker mono label top. Attribution muted and small at bottom. Preface sits above the quote in muted body type. No decorative elements.

---

SLIDE 3 - THE BENCHMARKS
Type: math
Kicker: THE REAL TARGETS
Headline: Five formats, five different numbers. Which one is yours?
Lines:
  - { label: "Full-service restaurant", value: "28-35%", accent: false }
  - { label: "Quick-service / fast casual", value: "32-35%", accent: false }
  - { label: "Food truck", value: "28-32%", accent: false }
  - { label: "Caterer", value: "25-35%", accent: false }
  - { label: "Home baker", value: "30-40%", accent: true }
Footnote: Home bakers run highest because they buy ingredients at retail, not wholesale.
Design notes: Mono receipt-style line items. Each row: label left, value right, hairline divider between rows. Accent row (home baker) value in accent color. Footnote muted caption at bottom. Kicker mono label top.

---

SLIDE 4 - WHERE EACH FORMAT LEAKS
Type: list
Kicker: WHERE IT BREAKS
Headline: Each format has one leak that shows up most often.
Items:
  - { term: "Restaurant", description: "Pricing a dish from memory. Costs shift; the card you wrote in January does not match April's invoices." }
  - { term: "Food truck", description: "Holding prices steady while portion sizes quietly drift heavier each week." }
  - { term: "Caterer", description: "Ignoring buffer prep. Cooking for 90 when 80 people show up is a cost whether the food gets eaten or not." }
  - { term: "Home baker", description: "Leaving packaging out of the cost calculation. Boxes, labels, and ribbon are part of the product." }
Design notes: Mono counters 01-04 left of each term. Dashed dividers between items. Term in display/bold, description in muted body below. Kicker mono label top.

---

SLIDE 5 - THE FIX
Type: pullquote
Kicker: START HERE
Quote: Before you raise prices, check whether your portions have crept up.
Meta:
  - { label: "Then check", value: "supplier invoices vs. six months ago", accent: false }
  - { label: "Then reprice", value: "if portions are right and costs are market rate", accent: true }
Design notes: Large display quote center. Two meta rows below in mono label/value pairs, hairline above the meta block. "Then reprice" row value in accent color. Kicker mono label top.

---

SLIDE 6 - CTA
Type: cta
Kicker: CALCULATE YOURS
Headline: Find your food cost in two minutes.
Body: Enter your ingredients and menu price at foodcosting.app. No spreadsheet, no formula — just your number.
Pill: link in bio
Meta: Save this for the next time a dish feels off.
Design notes: Always-dark final slide. Wordmark bottom-right. Pill as ghost button. Meta as small muted cue below the pill.

---

CAPTION:
Food cost targets are not universal. A food truck running 33% has a real problem. A caterer at 33% might be doing fine.

The number that matters is your number — the one that leaves room for labour, rent, and something left over after you pay yourself.

Swipe through for the real benchmarks by format, plus the single most common mistake that blows up each one.

Then check your actual food cost at foodcosting.app. Takes two minutes.

HASHTAGS:
#restaurantbusiness #foodcost #restaurantmanagement #fandbbusiness #foodcosting

---

## Remotion props

Slides 1-3 (merge with part 2 to form the complete CarouselProps object):

```json
{"slides_part1":[{"type":"cover","kicker":"KNOW YOUR NUMBER","title":"Your food cost target depends on how you cook, not just what you sell","accent":"depends","subtitle":"The keep it low advice is not a target. Here are the real benchmarks by business type.","issueLabel":"Field Notes / 02"},{"type":"quote","kicker":"THE COMMON BELIEF","preface":"Every operator hears this early on","quote":"Keep your food cost low and the margins take care of themselves.","attribution":"said without specifying what low means for your format"},{"type":"math","kicker":"THE REAL TARGETS","headline":"Five formats, five different numbers. Which one is yours?","lines":[{"label":"Full-service restaurant","value":"28-35%","accent":false},{"label":"Quick-service / fast casual","value":"32-35%","accent":false},{"label":"Food truck","value":"28-32%","accent":false},{"label":"Caterer","value":"25-35%","accent":false},{"label":"Home baker","value":"30-40%","accent":true}],"footnote":"Home bakers run highest because they buy ingredients at retail, not wholesale."}]}
```

Slides 4-6:

```json
{"slides_part2":[{"type":"list","kicker":"WHERE IT BREAKS","headline":"Each format has one leak that shows up most often.","items":[{"term":"Restaurant","description":"Pricing a dish from memory. Costs shift; the card you wrote in January does not match April's invoices."},{"term":"Food truck","description":"Holding prices steady while portion sizes quietly drift heavier each week."},{"term":"Caterer","description":"Ignoring buffer prep. Cooking for 90 when 80 people show up is a cost whether the food gets eaten or not."},{"term":"Home baker","description":"Leaving packaging out of the cost calculation. Boxes, labels, and ribbon are part of the product."}]},{"type":"pullquote","kicker":"START HERE","quote":"Before you raise prices, check whether your portions have crept up.","meta":[{"label":"Then check","value":"supplier invoices vs. six months ago","accent":false},{"label":"Then reprice","value":"if portions are right and costs are market rate","accent":true}]},{"type":"cta","kicker":"CALCULATE YOURS","headline":"Find your food cost in two minutes.","body":"Enter your ingredients and menu price at foodcosting.app. No spreadsheet, no formula — just your number.","pill":"link in bio","meta":"Save this for the next time a dish feels off."}]}
```

Full props are in pipeline/context/carousel-props.json.
