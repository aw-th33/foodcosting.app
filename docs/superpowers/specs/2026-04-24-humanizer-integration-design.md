# Humanizer integration into content agents

**Date:** 2026-04-24
**Status:** Approved
**Approach:** B — shared skill reference with medium-specific inline rules

## Problem

The carousel-writer and short-form-writer agents produce content that reads as obviously AI-generated. The blog-writer already has comprehensive inline anti-AI rules, but these are duplicated and not shared. The carousel copy and captions are the worst offenders. Short-form scripts have a secondary issue where lines sound like textbook definitions rather than spoken word.

The humanizer skill exists as a superpowers plugin skill (loaded at runtime via the Skill tool) with 29 pattern categories and a two-pass audit process, but no agent currently references it. Importantly, the humanizer is NOT a local file — it is loaded dynamically. Agents run as subagents with only Bash, Read, and Write tools and cannot invoke the Skill tool.

## Solution

Create a local reference copy of the humanizer rules at `.claude/skills/humanizer-reference.md` that agents can read with `cat`. Add a mandatory humanizer pass to all three content-producing agents (carousel-writer, short-form-writer, blog-writer) by reading this local reference file at startup and applying the two-pass audit before saving content to Notion.

Medium-specific rules stay inline in each agent. The shared humanizer reference file is the single source of truth for anti-AI pattern detection.

**Why a local copy instead of a symlink or plugin path:** The plugin cache path (`C:/Users/admin/.claude/plugins/cache/...`) is version-stamped and changes on plugin updates. A local reference file in the project repo is stable, version-controlled, and accessible to agents and remote triggers alike.

## Changes by agent

### carousel-writer.md

**Startup addition — "Before you start" section:**

Add the humanizer skill to the list of required reads:

```bash
cat ".claude/skills/humanizer-reference.md"
```

This goes alongside the existing brand constitution and carousel skill reads.

**New step — Step 4.1 (between Step 4 and Step 4.5):**

```
### Step 4.1 - Humanizer pass

Before producing Remotion props, apply the humanizer skill's full process to all written copy:

1. Scan every slide's text fields (title, subtitle, headline, quote, items, body) and the caption for the AI patterns listed in the humanizer skill
2. Rewrite any flagged copy
3. Ask: "What makes this obviously AI generated?" — list the remaining tells
4. Revise to fix them
5. Only then proceed to Step 4.5
```

**Medium-specific rules added inline (in the new Step 4.1):**

- Slide headlines: max 12 words, must land without context from other slides
- Caption: write like an operator sharing a lesson, not a brand posting content. No hashtag-stuffing tone.
- Avoid rule-of-three groupings in list slides unless the source material genuinely has three items
- Quote slides: must sound like something a real person would say, not a manufactured pull-quote
- Kickers are exempt from the humanizer pass (they are label tokens, not prose)

### short-form-writer.md

**Startup addition:**

Add a new "Before you start" section (this agent does not currently have one):

```
## Before you start

Read the humanizer skill in full:

```bash
cat ".claude/skills/humanizer-reference.md"
```

Do not skip this. You will apply these rules to every script you write.
```

**New step — Step 3.1 (between Step 3 and Step 4):**

```
### Step 3.1 - Humanizer pass

Before writing Remotion props, apply the humanizer skill's full process to both script variants:

1. Scan all HOOK, PROBLEM, TIP, and CTA lines for AI patterns listed in the humanizer skill
2. Rewrite any flagged lines
3. Ask: "What makes this obviously AI generated?" — list the remaining tells
4. Revise to fix them
5. Only then proceed to Step 4
```

**Medium-specific rules added inline (in the new Step 3.1):**

- Every line must be speakable in one breath at normal pace
- No textbook definitions. Rephrase as if explaining to someone standing next to you in a kitchen.
- Hook line: conversational surprise, not a headline
- Remotion prop text (hook, problem, cta) gets the same pass. These appear on screen.

### blog-writer.md

**Startup addition:**

Add the humanizer skill to required reads at the top of the process:

```bash
cat ".claude/skills/humanizer-reference.md"
```

**Replace the "Human writing standards (anti-AI pass)" section:**

Remove the entire inline section including:
- Banned words and phrases list
- Banned constructions list
- "What good writing looks like instead" subsection
- Self-audit process

Replace with:

```
## Human writing standards (anti-AI pass)

Read and apply the humanizer skill (loaded at startup) before finalising the post. Use its full two-pass audit process:

1. Scan the draft for all AI patterns in the skill
2. Ask: "What makes this sound AI-generated?" — identify the remaining tells
3. Revise to fix them
4. Only then proceed to publishing

In addition to the humanizer skill's rules, these blog-specific standards always apply:

- No em dashes. Rewrite with a comma, period, or parentheses.
- Sentence case in all headings
- No inline-header bullet lists (avoid **Bold label:** description format)
- Have an opinion. React to the numbers. "Food cost above 35% on a burger? You're working for free."
- Vary sentence length. Short punchy ones. Then a longer one that earns its length.
- Be specific about the reader's situation, not generic about "food businesses"
- Use "you" directly. Talk to the owner, not about them.
```

## What does not change

- The upstream humanizer plugin skill is not modified
- Pipeline flow and step ordering remain the same (new steps are inserted, not rearranged)
- Notion database interactions, property schemas, and handoff summaries are unchanged
- Remotion props schemas and rendering are unchanged
- Human review gates stay exactly where they are
- The topic-researcher, seo-specialist, community-monitor, and remotion-renderer agents are not touched

## File manifest

| File | Action |
|---|---|
| `.claude/skills/humanizer-reference.md` | New file. Local copy of humanizer rules for agent access. |
| `.claude/agents/carousel-writer.md` | Add humanizer read + new Step 4.1 |
| `.claude/agents/short-form-writer.md` | Add "Before you start" section + new Step 3.1 |
| `.claude/agents/blog-writer.md` | Replace inline anti-AI section with humanizer skill reference + blog-specific rules |

## Risks

**Agent execution time:** Each agent now reads one additional file and performs a revision pass. This adds ~10-20 seconds per run. Acceptable given the quality improvement.

**Local copy drift:** The local reference file could fall out of sync with the upstream humanizer plugin. Mitigated by the humanizer plugin being stable (pattern-based, not frequently updated). If the plugin updates, re-copy the relevant content.

**Over-correction risk:** The humanizer could strip personality from copy that was already good. Mitigated by the medium-specific rules that anchor the voice (operator-minded, number-first) and by the two-pass process which checks for remaining tells rather than blindly rewriting everything.
