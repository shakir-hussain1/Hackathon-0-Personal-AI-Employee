# Agent Skill: LinkedIn Post Generator

## Purpose
Generate professional LinkedIn posts from business content in the vault to build brand presence and generate sales leads.

## When to Use
- A `LINKEDIN_POST_*.md` task appears in `Needs_Action/`
- User asks to promote a project, milestone, or service
- New content in `Done/` has business value worth sharing

## Workflow

### Step 1 — Read the Task
Read the `LINKEDIN_POST_*.md` file from `Needs_Action/` to understand the source content.

### Step 2 — Review Source Content
Read the referenced source document. Identify:
- What was accomplished or delivered?
- What is the business/client impact?
- Any numbers, outcomes, or milestones?
- What insight can be drawn for the target audience?

### Step 3 — Choose Post Type
| Type | Use When |
|------|----------|
| `milestone` | Project completed, contract signed, major delivery |
| `insight` | Learned something valuable that others in the industry would care about |
| `announcement` | New service, new hire, new partnership |
| `thought_leadership` | Opinion or perspective on an industry trend |
| `promotion` | Direct offer for a service or product |

### Step 4 — Draft the Post
Use this structure:
```
[Hook — one sentence that stops the scroll]

[Body — 2-4 short paragraphs, max 3 lines each]
- What happened / the situation
- What you did / the approach
- What the result was / the value delivered

[Call to action — one sentence]

[Hashtags — 3-5 relevant tags]
```

**Content rules:**
- Total length: 150–1200 characters (sweet spot for LinkedIn algorithm)
- First 2 lines visible before "see more" — make them count
- Use line breaks generously (no walls of text)
- Write in first person ("We delivered..." or "I learned...")
- Never mention confidential client names or financial figures without permission
- Avoid buzzwords: synergy, leverage, utilize, robust, scalable

### Step 5 — Call the MCP Tool
Use the `linkedin-poster` MCP server to save the draft:
```
Tool: create_linkedin_draft
Arguments:
  content: <your drafted post>
  post_type: <chosen type from Step 3>
  visibility: PUBLIC
```

### Step 6 — Update the Task
Mark the `LINKEDIN_POST_*.md` task as complete:
- Update Status from PENDING → COMPLETED
- Note the draft file created
- Move the task file to `Done/`

## Post Templates

### Milestone Post
```
We just delivered [OUTCOME] for [INDUSTRY/client type].

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

After [CONTEXT], we discovered:

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
