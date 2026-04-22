# Carousel Writer Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a `carousel-writer` agent that picks a published blog post from Notion, reads the carousel skill, produces a fully-specified slide-by-slide carousel brief, and saves it to a new Notion database (Carousels).

**Architecture:** Single agent file at `.claude/agents/carousel-writer.md`. The agent queries the Blog DB for posts where `Social Content Created = false`, picks the best candidate (highest GSC Impressions), reads the brand constitution and carousel skill for formatting rules, writes the carousel brief to a local markdown file, creates a page in the Carousels Notion DB, and marks the blog post `Social Content Created = true`. No new Python scripts needed — all Notion operations use the existing scripts in `scripts/notion/`.

**Tech Stack:** Claude agent (markdown), existing Notion Python scripts (`query_database.py`, `fetch_page.py`, `create_page.py`, `update_page.py`), Notion API.

---

## File Structure

| Action | Path | Responsibility |
|---|---|---|
| Create | `.claude/agents/carousel-writer.md` | The agent definition — instructions, process, and formatting rules |
| Create (Notion) | Carousels DB | New Notion database to store carousel briefs — created manually by Ahmed before first run |

No new Python scripts. No new skills. Relies entirely on:
- `scripts/notion/query_database.py`
- `scripts/notion/fetch_page.py`
- `scripts/notion/create_page.py`
- `scripts/notion/update_page.py`
- `.claude/skills/foodcosting-carousel-skill/SKILL.md` (referenced in agent instructions)
- `.claude/skills/foodcosting-carousel-skill/references/brand-constitution.md`

---

## Task 1: Create the Carousels Notion database

This database stores finished carousel briefs. Ahmed creates it manually in Notion — the agent writes to it.

**Files:**
- No files — this is a Notion setup step
- Modify: `C:\Users\admin\.claude\projects\c--Users-admin-Documents-Foodcosting-app\memory\reference_notion_databases.md` (add Carousels DB ID once created)

- [ ] **Step 1: Create the Carousels database in Notion**

In Notion, under the same Foodcosting parent page (`27b80496c886803cb3face103ea63b4e`), create a new database called **Carousels** with these properties:

| Property | Type | Notes |
|---|---|---|
| Title | Title | Carousel title (mirrors blog post title) |
| Status | Select | Options: `Draft`, `Reviewed`, `Published` |
| Slide Count | Number | How many slides in this carousel |
| Blog Post ID | Text | Notion page ID of the source blog post |
| Blog Slug | Text | e.g. `/ideal-food-cost-percentage` |
| Created Date | Date | Date agent ran |
| Format | Select | Options: `Educational`, `Data story`, `Quick tip`, `Deep dive` |

- [ ] **Step 2: Copy the Carousels database ID**

After creating the database, open it in Notion, copy the URL, and extract the database ID (the 32-char hex string after the last `/` and before `?`).

Format it with hyphens: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

- [ ] **Step 3: Update memory with the new DB ID**

Open `C:\Users\admin\.claude\projects\c--Users-admin-Documents-Foodcosting-app\memory\reference_notion_databases.md` and add a row to the table:

```markdown
| Carousels | `<DB-ID-HERE>` | — | Carousel briefs produced by carousel-writer agent. Status: Draft → Reviewed → Published |
```

---

## Task 2: Write the carousel-writer agent

**Files:**
- Create: `.claude/agents/carousel-writer.md`

- [ ] **Step 1: Create the agent file**

Create `.claude/agents/carousel-writer.md` with the following exact content:

```markdown
---
name: carousel-writer
description: Reads a published blog post from Notion, produces a fully-specified Instagram carousel brief following the foodcosting.app brand and carousel skill standards, and saves it to the Carousels Notion database.
tools: Bash, Read, Write
---

You are the Carousel Writer for foodcosting.app.

Your job is to take a published blog post and turn it into a complete, designer-ready Instagram carousel brief. You follow the foodcosting.app brand constitution and carousel skill exactly. Every slide you specify must have precise pixel measurements, font sizes, colors, and copy — no vague instructions.

You do not design. You do not render. You produce the brief that a designer or renderer uses.

## Before you start

Read the brand constitution and carousel skill in full:

```bash
cat "c:/Users/admin/Documents/Foodcosting.app/.claude/skills/foodcosting-carousel-skill/references/brand-constitution.md"
cat "c:/Users/admin/Documents/Foodcosting.app/.claude/skills/foodcosting-carousel-skill/SKILL.md"
```

Do not skip this. The skill contains the canvas specs, typography table, layout zones, chart specs, and output format you must follow exactly.

## Your process

### Step 1 — Pick the best blog post

Query the Blog database for published posts where `Social Content Created` is false:

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/query_database.py \
  --database-id 2e880496-c886-80c7-9396-db6073f91041 \
  --filter '{"and": [{"property": "Status", "select": {"equals": "Published"}}, {"property": "Social Content Created", "checkbox": {"equals": false}}]}' \
  --output pipeline/context/carousel-candidates.json
```

Read `pipeline/context/carousel-candidates.json`. Pick the post with the highest `GSC Impressions` value. If impressions are null for all candidates, pick the most recently dated post.

Record its `id`, `Title`, `Slug`, `Target Keyword`, and `Excerpt`.

### Step 2 — Fetch the full post

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/fetch_page.py \
  --page-id <blog-page-id> \
  --output pipeline/context/carousel-source-post.json
```

Read `pipeline/context/carousel-source-post.json`. The `body` field is the full post text.

### Step 3 — Choose the carousel format

Based on the post content, choose the best format from the carousel skill:

| Format | When to use |
|---|---|
| Quick tip | Post has one clear, actionable insight (4 slides) |
| Educational explainer | Post explains a concept with multiple steps or causes (6 slides) |
| Data story | Post is built around a key number or benchmark (7 slides) |
| Deep dive | Post covers a complex topic with multiple sub-points (9–10 slides) |

State your format choice and why before writing the brief.

### Step 4 — Write the carousel brief

Follow the carousel skill's output format exactly. Every slide must include:

- Precise pixel positions (x, y coordinates)
- Exact font sizes from the typography table — no other sizes permitted
- Exact hex colors from the brand constitution
- Copy that is specific (includes numbers, named scenarios, or concrete consequences)

Apply the bottom-third rule: all text anchors to y=620 or below on content slides. The top half of content slides must be empty.

Apply the slide sequence from the skill:
1. Hook slide
2. Content slides (one point per slide)
3. Data slide(s) where the number is the hero (if applicable)
4. Tension slide (cost of inaction)
5. CTA slide (black background, centered, foodcosting.app →)

Write the complete carousel brief in the skill's output format — no abbreviations, no "similar to slide N".

### Step 5 — Write the brief to a local file

Write the complete brief to `pipeline/context/carousel-body.md` using the Write tool.

### Step 6 — Save to the Carousels Notion database

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/create_page.py \
  --database-id <CAROUSELS_DB_ID> \
  --properties '{
    "Title": "<post title> — Carousel",
    "Status": "Draft",
    "Slide Count": <number of slides>,
    "Blog Post ID": "<blog-page-id>",
    "Blog Slug": "<slug>",
    "Created Date": "<YYYY-MM-DD>",
    "Format": "<Educational|Data story|Quick tip|Deep dive>"
  }' \
  --body-file pipeline/context/carousel-body.md \
  --output pipeline/context/carousel-created.json
```

Read `pipeline/context/carousel-created.json` for the new page `url`.

### Step 7 — Mark the blog post as social content created

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <blog-page-id> \
  --properties '{"Social Content Created": true}'
```

### Step 8 — Handoff summary

Output a clean summary:

```
## Carousel brief complete

Source post: <Title> (<Slug>)
Format: <format>
Slides: <n>
Notion page: <carousel-created url>
Status: Draft — ready for Ahmed's review
```

Do not post, schedule, or publish anything. Ahmed reviews and approves all social content before it goes live.
```

- [ ] **Step 2: Verify the file was written correctly**

```bash
head -5 "c:/Users/admin/Documents/Foodcosting.app/.claude/agents/carousel-writer.md"
```

Expected output:
```
---
name: carousel-writer
description: Reads a published blog post from Notion, produces a fully-specified Instagram carousel brief following the foodcosting.app brand and carousel skill standards, and saves it to the Carousels Notion database.
tools: Bash, Read, Write
---
```

- [ ] **Step 3: Commit the agent file**

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  git add .claude/agents/carousel-writer.md && \
  git commit -m "feat: add carousel-writer agent for Instagram carousel brief production"
```

---

## Task 3: Insert the Carousels DB ID into the agent

Once Task 1 is complete and you have the Carousels DB ID, replace the placeholder in the agent file.

**Files:**
- Modify: `.claude/agents/carousel-writer.md`

- [ ] **Step 1: Replace the DB ID placeholder**

In `.claude/agents/carousel-writer.md`, find this line:

```
  --database-id <CAROUSELS_DB_ID> \
```

Replace `<CAROUSELS_DB_ID>` with the actual database ID from Task 1 (formatted with hyphens).

- [ ] **Step 2: Commit the update**

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  git add .claude/agents/carousel-writer.md && \
  git commit -m "feat: wire carousel-writer to Carousels Notion database"
```

---

## Task 4: Run the carousel-writer agent end-to-end test

**Files:**
- Read: `pipeline/context/carousel-candidates.json` (produced by agent)
- Read: `pipeline/context/carousel-created.json` (produced by agent)

- [ ] **Step 1: Run the agent**

```bash
claude --agent carousel-writer
```

Or invoke it from within Claude Code using the Agent tool with `subagent_type: carousel-writer`.

- [ ] **Step 2: Verify the carousel brief was written to Notion**

Check `pipeline/context/carousel-created.json` exists and contains a valid `url` field:

```bash
python -c "import json; d=json.load(open('pipeline/context/carousel-created.json')); print(d.get('url', 'MISSING'))"
```

Expected: a valid Notion URL.

- [ ] **Step 3: Verify the source blog post was marked**

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/query_database.py \
  --database-id 2e880496-c886-80c7-9396-db6073f91041 \
  --filter '{"and": [{"property": "Status", "select": {"equals": "Published"}}, {"property": "Social Content Created", "checkbox": {"equals": true}}]}' \
  --output pipeline/context/marked-posts.json && \
  python -c "import json; posts=json.load(open('pipeline/context/marked-posts.json')); print(len(posts), 'post(s) marked as social content created')"
```

Expected: at least 1 post marked.

- [ ] **Step 4: Open the Notion carousel page and review**

Open the URL from `pipeline/context/carousel-created.json` in a browser. Confirm:
- All slides are present and numbered
- Every slide has pixel-level specs (positions, font sizes, hex colors)
- No slide has vague instructions like "add chart here"
- The CTA slide has a black background spec
- The caption and hashtags are present at the end

---

## Self-Review

**Spec coverage:**
- ✅ Agent picks best blog post (highest GSC impressions, no social content yet)
- ✅ Agent reads carousel skill and brand constitution before writing
- ✅ Agent follows carousel skill output format exactly
- ✅ Agent saves brief to Carousels Notion DB
- ✅ Agent marks blog post `Social Content Created = true`
- ✅ Agent outputs handoff summary
- ✅ Human review preserved — agent never publishes

**Placeholder scan:** No TBDs, no "implement later", no vague steps. The Carousels DB ID is the only placeholder — it cannot be resolved until Task 1 creates the database. Task 3 wires it in immediately after.

**Type consistency:** All script invocations use the same CLI interface (`--database-id`, `--filter`, `--output`, `--properties`, `--body-file`) as the existing agents. Property names match the Blog DB schema (`Social Content Created`, `Status`, `Slug`).
