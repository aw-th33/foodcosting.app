# Humanizer Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the humanizer anti-AI writing rules into all three content-producing agents so carousel copy, captions, short-form scripts, and blog posts go through a mandatory quality pass before saving to Notion.

**Architecture:** Create a local reference copy of the humanizer rules at `.claude/skills/humanizer-reference.md`. Each content agent reads this file at startup and applies a two-pass audit (identify AI patterns, revise, check remaining tells, revise again) before saving content. Medium-specific rules stay inline in each agent.

**Tech Stack:** Markdown agent definitions, no code changes.

**Spec:** `docs/superpowers/specs/2026-04-24-humanizer-integration-design.md`

---

### Task 1: Create the local humanizer reference file

**Files:**
- Create: `.claude/skills/humanizer-reference.md`

This file is a curated extract of the humanizer skill's pattern library and audit process, formatted for agent consumption. It is NOT the full skill file (which includes interactive process instructions for human use). It contains only the patterns and the two-pass audit process that agents need.

- [ ] **Step 1: Create the humanizer reference file**

Write the following to `.claude/skills/humanizer-reference.md`:

```markdown
# Humanizer: Anti-AI writing patterns

This is a reference file for content agents. Read it in full before writing any content. Apply these rules during your humanizer pass.

## Two-pass audit process

After writing your content and before saving to Notion:

1. Scan all written copy for the patterns listed below. Rewrite any flagged text.
2. Ask yourself: "What makes this obviously AI generated?" List the remaining tells briefly.
3. Revise to fix them.
4. Only then proceed to save.

## Personality and soul

Avoiding AI patterns is half the job. Sterile, voiceless writing is just as obvious.

Signs of soulless writing:
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty
- Reads like a Wikipedia article or press release

How to add voice:
- Have opinions. React to what you are writing. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.
- Vary your rhythm. Short punchy sentences. Then longer ones that take their time.
- Acknowledge complexity. Real humans have mixed feelings.
- Be specific about feelings. Not "this is concerning" but "there's something unsettling about watching margins erode while sales look fine."

## Content patterns to eliminate

### 1. Significance inflation
Words to watch: stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance, reflects broader, symbolizing, contributing to the, setting the stage for, marking/shaping the, represents a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

### 2. Promotional language
Words to watch: boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking, renowned, breathtaking, must-visit, stunning

### 3. Superficial -ing analyses
Words to watch: highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

Tacking present participle phrases onto sentences to add fake depth. Remove them.

### 4. Vague attributions
Words to watch: Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications

Replace with specific sources or remove entirely.

### 5. Overused AI vocabulary
High-frequency AI words: additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant

### 6. Copula avoidance
Replace "serves as", "functions as", "stands as", "marks", "represents" with plain "is" or "are" where appropriate.

### 7. Negative parallelisms and tailing negations
"Not only...but..." and "It's not just about X, it's about Y" are overused. So are clipped fragments like "no guessing" or "no wasted motion" tacked onto sentence ends. Write real clauses instead.

### 8. Rule of three overuse
Do not force ideas into groups of three to appear comprehensive. If you have two points, say two. If you have four, say four.

### 9. Elegant variation (synonym cycling)
Do not substitute synonyms for the same concept across consecutive sentences. If you said "the owner", say "the owner" again, not "the operator", "the entrepreneur", "the business leader".

### 10. Em dash overuse
Rewrite em dashes with commas, periods, or parentheses. Most em dashes can be eliminated entirely.

### 11. Passive voice and subjectless fragments
"No configuration needed" should be "You do not need a configuration file." Name the actor.

### 12. Boldface overuse
Do not mechanically bold phrases. Use bold sparingly for genuinely critical terms only.

### 13. Inline-header vertical lists
Avoid bullet points that start with **Bold label:** followed by description. Convert to prose or plain list items.

### 14. Title case in headings
Use sentence case only. Not "Strategic Negotiations And Global Partnerships" but "Strategic negotiations and global partnerships".

### 15. Filler phrases
Remove: "In order to" (use "To"), "Due to the fact that" (use "Because"), "At this point in time" (use "Now"), "It is important to note that" (just state the fact), "has the ability to" (use "can").

### 16. Signposting and announcements
Remove: "Let's dive in", "Let's explore", "Let's break this down", "Here's what you need to know", "Without further ado". Just start the content.

### 17. Persuasive authority tropes
Remove: "The real question is", "At its core", "In reality", "What really matters", "Fundamentally", "The heart of the matter". These add ceremony to ordinary points.

### 18. Generic positive conclusions
Remove: "The future looks bright", "Exciting times lie ahead", "A major step forward", "Continues to thrive". End with something specific instead.

### 19. Sycophantic tone
Remove: "Great question!", "You're absolutely right!", "That's an excellent point!". Just respond directly.

### 20. Excessive hedging
Remove: "could potentially possibly", "it might be argued that", "it is worth considering whether". State the point or qualify it once.

### 21. Fragmented headers
Do not follow a heading with a one-line paragraph that restates the heading. Start with real content.

### 22. False ranges
Do not use "from X to Y" constructions where X and Y are not on a meaningful scale.

### 23. Curly quotation marks
Use straight quotes ("...") not curly quotes.

### 24. Collaborative communication artifacts
Never include: "I hope this helps", "Let me know if", "Here is a", "Of course!", "Certainly!". These are chatbot artifacts, not content.
```

- [ ] **Step 2: Verify the file exists and is readable**

Run:
```bash
wc -l ".claude/skills/humanizer-reference.md"
```

Expected: approximately 110-120 lines.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/humanizer-reference.md
git commit -m "feat: add local humanizer reference for content agents

Curated extract of anti-AI writing patterns and two-pass audit
process. Content agents read this file at startup since they cannot
invoke the Skill tool directly."
```

---

### Task 2: Update carousel-writer with humanizer integration

**Files:**
- Modify: `.claude/agents/carousel-writer.md:13-22` (Before you start section)
- Modify: `.claude/agents/carousel-writer.md:86-106` (after Step 4, before Step 4.5)

- [ ] **Step 1: Add humanizer read to the "Before you start" section**

In `.claude/agents/carousel-writer.md`, find the "Before you start" section (line 13). Add the humanizer reference read after the existing two `cat` commands. Change this:

```markdown
## Before you start

Read the brand constitution and carousel skill in full:

```bash
cat "c:/Users/admin/Documents/Foodcosting.app/.claude/skills/foodcosting-carousel-skill/references/brand-constitution.md"
cat "c:/Users/admin/Documents/Foodcosting.app/.claude/skills/foodcosting-carousel-skill/SKILL.md"
```

Do not skip this. The skill contains the current 1080x1350 canvas, typography, slide families, structure rules, and output format.
```

To this:

```markdown
## Before you start

Read the brand constitution, carousel skill, and humanizer reference in full:

```bash
cat "c:/Users/admin/Documents/Foodcosting.app/.claude/skills/foodcosting-carousel-skill/references/brand-constitution.md"
cat "c:/Users/admin/Documents/Foodcosting.app/.claude/skills/foodcosting-carousel-skill/SKILL.md"
cat "c:/Users/admin/Documents/Foodcosting.app/.claude/skills/humanizer-reference.md"
```

Do not skip this. The carousel skill contains the current 1080x1350 canvas, typography, slide families, structure rules, and output format. The humanizer reference contains anti-AI writing patterns you must apply to all slide copy and captions.
```

- [ ] **Step 2: Insert Step 4.1 between Step 4 and Step 4.5**

In `.claude/agents/carousel-writer.md`, find the line `### Step 4.5 - Produce the Remotion props JSON` (line 108). Insert the following new section immediately before it:

```markdown
### Step 4.1 - Humanizer pass

Before producing Remotion props, apply the humanizer reference's full two-pass audit to all written copy in the brief:

1. Scan every slide's text fields (title, subtitle, headline, quote, items, body) and the caption for the AI patterns listed in the humanizer reference
2. Rewrite any flagged copy
3. Ask: "What makes this obviously AI generated?" List the remaining tells briefly.
4. Revise to fix them
5. Only then proceed to Step 4.5

Medium-specific rules for carousel copy:

- Slide headlines: max 12 words, must land without context from other slides
- Caption: write like an operator sharing a lesson, not a brand posting content. No hashtag-stuffing tone.
- Avoid rule-of-three groupings in list slides unless the source material genuinely has three items
- Quote slides: must sound like something a real person would say, not a manufactured pull-quote
- Kickers are exempt from the humanizer pass (they are label tokens, not prose)

```

- [ ] **Step 3: Verify the file is well-formed**

Run:
```bash
head -30 ".claude/agents/carousel-writer.md"
grep -n "Step 4.1" ".claude/agents/carousel-writer.md"
grep -n "humanizer" ".claude/agents/carousel-writer.md"
```

Expected: "Step 4.1" appears once. "humanizer" appears at least 3 times (in "Before you start", in Step 4.1 heading, and in Step 4.1 body).

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/carousel-writer.md
git commit -m "feat: add humanizer pass to carousel-writer agent

Reads humanizer reference at startup. New Step 4.1 applies two-pass
anti-AI audit to all slide copy and captions before Remotion props
generation. Includes carousel-specific rules for headlines, quotes,
and list slides."
```

---

### Task 3: Update short-form-writer with humanizer integration

**Files:**
- Modify: `.claude/agents/short-form-writer.md:6-9` (after frontmatter, before "Platform context")
- Modify: `.claude/agents/short-form-writer.md:66-78` (after Step 3, before Step 4)

- [ ] **Step 1: Add "Before you start" section**

In `.claude/agents/short-form-writer.md`, find the line `## Platform context` (line 11). Insert the following new section immediately before it:

```markdown
## Before you start

Read the humanizer reference in full:

```bash
cat "c:/Users/admin/Documents/Foodcosting.app/.claude/skills/humanizer-reference.md"
```

Do not skip this. You will apply these anti-AI writing rules to every script you write.

```

- [ ] **Step 2: Insert Step 3.1 between Step 3 and Step 4**

In `.claude/agents/short-form-writer.md`, find the line `### Step 4 - Write the Remotion props` (line 77). Insert the following new section immediately before it:

```markdown
### Step 3.1 - Humanizer pass

Before writing Remotion props, apply the humanizer reference's full two-pass audit to both script variants:

1. Scan all HOOK, PROBLEM, TIP, and CTA lines for AI patterns listed in the humanizer reference
2. Rewrite any flagged lines
3. Ask: "What makes this obviously AI generated?" List the remaining tells briefly.
4. Revise to fix them
5. Only then proceed to Step 4

Medium-specific rules for short-form scripts:

- Every line must be speakable in one breath at normal pace
- No textbook definitions. Rephrase as if explaining to someone standing next to you in a kitchen.
- Hook line: conversational surprise, not a headline
- Remotion prop text (hook, problem, cta) gets the same pass. These appear on screen.

```

- [ ] **Step 3: Verify the file is well-formed**

Run:
```bash
head -20 ".claude/agents/short-form-writer.md"
grep -n "Step 3.1" ".claude/agents/short-form-writer.md"
grep -n "humanizer" ".claude/agents/short-form-writer.md"
```

Expected: "Step 3.1" appears once. "humanizer" appears at least 3 times.

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/short-form-writer.md
git commit -m "feat: add humanizer pass to short-form-writer agent

New 'Before you start' section reads humanizer reference. New Step 3.1
applies two-pass anti-AI audit to all script lines before Remotion
props generation. Includes medium-specific rules for speakability
and conversational tone."
```

---

### Task 4: Update blog-writer to use shared humanizer reference

**Files:**
- Modify: `.claude/agents/blog-writer.md:13-22` (before "Before you start" / before process section)
- Modify: `.claude/agents/blog-writer.md:21-54` (replace "Human writing standards" section)

- [ ] **Step 1: Add humanizer read to the process startup**

In `.claude/agents/blog-writer.md`, find the line `## Your process` (line 55). Insert the following new section immediately before it:

```markdown
## Before you start

Read the humanizer reference in full:

```bash
cat "c:/Users/admin/Documents/Foodcosting.app/.claude/skills/humanizer-reference.md"
```

Do not skip this. You will apply these anti-AI writing rules during the self-audit before publishing.

```

- [ ] **Step 2: Replace the "Human writing standards" section**

In `.claude/agents/blog-writer.md`, replace the entire section from `## Human writing standards (anti-AI pass)` (line 21) through the self-audit process ending at `4. Only then publish to Notion` (line 53) with the following:

```markdown
## Human writing standards (anti-AI pass)

Before finalising the post, apply the humanizer reference (loaded at startup) using its full two-pass audit process:

1. Scan the draft for all AI patterns in the humanizer reference
2. Ask: "What makes this sound AI-generated?" Identify the remaining tells.
3. Revise to fix them
4. Only then proceed to publishing

In addition to the humanizer reference's rules, these blog-specific standards always apply:

- No em dashes. Rewrite with a comma, period, or parentheses.
- Sentence case in all headings
- No inline-header bullet lists (avoid **Bold label:** description format)
- Have an opinion. React to the numbers. "Food cost above 35% on a burger? You're working for free."
- Vary sentence length. Short punchy ones. Then a longer one that earns its length.
- Be specific about the reader's situation, not generic about "food businesses"
- Use "you" directly. Talk to the owner, not about them.
```

This removes: the banned words list, the banned constructions list, the "What good writing looks like instead" subsection, and the inline self-audit process. All of these are now covered by the shared humanizer reference file.

- [ ] **Step 3: Verify the file is well-formed**

Run:
```bash
grep -n "humanizer" ".claude/agents/blog-writer.md"
grep -c "delve" ".claude/agents/blog-writer.md"
grep -c "tapestry" ".claude/agents/blog-writer.md"
```

Expected: "humanizer" appears at least 3 times. "delve" count is 0. "tapestry" count is 0. (The banned words are now in the shared reference, not in this file.)

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/blog-writer.md
git commit -m "refactor: replace inline anti-AI rules with shared humanizer reference

Removes duplicated banned-words list and self-audit process. Blog-writer
now reads the shared humanizer-reference.md at startup. Blog-specific
standards (em dashes, sentence case, opinion-driven voice) remain inline."
```

---

### Task 5: Verification — dry-run all three agents

**Files:** None modified. Read-only verification.

- [ ] **Step 1: Verify humanizer reference is readable from agent working directory**

Run:
```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && cat ".claude/skills/humanizer-reference.md" | head -5
```

Expected output starts with `# Humanizer: Anti-AI writing patterns`.

- [ ] **Step 2: Verify carousel-writer agent structure**

Run:
```bash
grep -n "^## \|^### " ".claude/agents/carousel-writer.md"
```

Expected: section headings should include "Before you start", then Steps 1 through 8, with Step 4.1 appearing between Step 4 and Step 4.5.

- [ ] **Step 3: Verify short-form-writer agent structure**

Run:
```bash
grep -n "^## \|^### " ".claude/agents/short-form-writer.md"
```

Expected: section headings should include "Before you start", "Platform context", then Steps 1 through 7, with Step 3.1 appearing between Step 3 and Step 4.

- [ ] **Step 4: Verify blog-writer agent structure**

Run:
```bash
grep -n "^## \|^### " ".claude/agents/blog-writer.md"
```

Expected: section headings should include "Before you start", "Voice and tone rules", "Human writing standards (anti-AI pass)", "Your process", then Steps 1 through 6. No "Banned words" or "Banned constructions" subsections should appear.

- [ ] **Step 5: Verify no broken references**

Run:
```bash
grep -rn "humanizer" ".claude/agents/" ".claude/skills/humanizer-reference.md" | wc -l
```

Expected: at least 10 matches across all files (reference file + 3 agents).
