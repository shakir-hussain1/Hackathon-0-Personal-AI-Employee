---
name: linkedin-post
description: |
  Generate a professional LinkedIn post from business content in the vault.
  Reads LINKEDIN_POST_*.md task files from Needs_Action/, drafts a post using
  the linkedin-poster MCP tool, and queues it for human approval.
  Use when LINKEDIN_POST_*.md tasks appear or user asks to promote a milestone/service.
---

# LinkedIn Post Skill

**Purpose**: Turn business milestones and insights into engaging LinkedIn posts
**Tier**: Silver
**Input**: `LINKEDIN_POST_*.md` task in `Needs_Action/` or direct user request
**Output**: Draft post saved via `linkedin-poster` MCP, queued in `LinkedIn_Queue/`

---

## When to Use

- A `LINKEDIN_POST_*.md` task appears in `Needs_Action/`
- User asks: "post about [project/service/milestone]"
- New content in `Done/` has business value worth sharing
- LinkedIn Watcher queued a new post suggestion

---

## Workflow

### Step 1 — Read the Task
Open the `LINKEDIN_POST_*.md` file from `Needs_Action/`. It contains:
- Source document path
- Content preview
- Suggested post types
- Posting guidelines

### Step 2 — Read the Source Document
Open the referenced source file. Identify:
- What was accomplished or delivered?
- Client/industry impact (avoid naming clients without permission)
- Specific numbers or outcomes (e.g., "3x faster", "40% conversion lift")
- What insight can the audience take away?

### Step 3 — Choose Post Type

| Post Type | Use When |
|-----------|----------|
| `milestone` | Project completed, contract signed, major delivery |
| `insight` | Learned something valuable from the work |
| `announcement` | New service, new hire, new partnership |
| `thought_leadership` | Opinion on industry trend |
| `promotion` | Direct offer for a service or product |

### Step 4 — Draft the Post

**Structure:**
```
[Hook — one sentence that stops the scroll]

[Body — 2-4 short paragraphs, max 3 lines each]
• What happened / the situation
• What you did / the approach
• What the result was / value delivered

[Call to action — one sentence]

[3-5 relevant hashtags]
```

**Rules:**
- Total: 150–1200 characters (LinkedIn sweet spot)
- First 2 lines visible before "see more" — make them count
- Use line breaks — no walls of text
- Write in first person ("We delivered..." or "I learned...")
- Never name clients or share financial figures without permission
- Avoid: synergy, leverage, utilize, robust, scalable

### Step 5 — Call the MCP Tool

```
Tool: create_linkedin_draft
Arguments:
  content: <your drafted post>
  post_type: <milestone/insight/announcement/thought_leadership/promotion>
  visibility: PUBLIC
```

### Step 6 — Update the Task File

Update `LINKEDIN_POST_*.md`:
```markdown
Status: COMPLETED
Draft: LinkedIn_Queue/{draft_filename}
```

Move the task file to `Done/`.

---

## Post Templates

### Milestone Post
```
We just delivered [OUTCOME] for [INDUSTRY type].

Here's what made it work:
→ [Key action 1]
→ [Key action 2]
→ [Key insight]

The result: [specific outcome or metric if shareable].

If you're working on [CHALLENGE], happy to share more.

#[Industry] #[Relevant skill] #BusinessGrowth
```

### Insight Post
```
[Counterintuitive statement or surprising finding]

After [CONTEXT], here's what we discovered:

[Insight 1]
[Insight 2]
[Insight 3]

The takeaway: [one clear sentence].

What's your experience with this?

#[Topic] #[Industry] #Insight
```

### Promotion Post
```
[Problem your ideal client faces]

That's why we built [SERVICE/OFFER].

[Benefit 1]
[Benefit 2]
[Benefit 3]

[Clear CTA — DM, link, comment]

#[Service] #[Industry] #[Location if relevant]
```

---

## Approval Workflow

```
Draft saved to LinkedIn_Queue/
    ↓
Human reviews (Claude shows draft, human approves)
    ↓
Human approves → move file to LinkedIn_Approved/
    ↓
post_approved_linkedin_drafts MCP tool → posts to LinkedIn
    ↓
Posted draft archived to Done/Communications/
```

**MCP Tools available:**
- `create_linkedin_draft` — save post to queue
- `list_linkedin_queue` — view pending posts
- `post_approved_linkedin_drafts` — publish approved posts

---

## Content Quality Checklist

```
[ ] Hook line is specific and creates curiosity or value
[ ] Under 1200 characters
[ ] No confidential client names or financial data
[ ] Written in first person (I/We)
[ ] 3-5 relevant hashtags included
[ ] No vague buzzwords
[ ] Clear call to action or question at end
[ ] Line breaks used (not a wall of text)
```

---

**Status**: Production Ready
**Tier**: Silver
**Depends on**: linkedin-poster MCP server, LinkedIn API credentials in `.env`
**Related**: LinkedIn Watcher (`Silver-Tier/watchers/linkedin_watcher.py`)
