---
name: process-email
description: |
  Process email tasks created by the Gmail Watcher in Needs_Action/.
  Analyzes EMAIL_*.md task files, categorizes emails, determines required action,
  calls draft-reply if a reply is needed, and moves processed tasks to Done/.
  Use when EMAIL_*.md files appear in Needs_Action/.
---

# Process Email Skill

**Purpose**: Analyze and action email tasks created by the Gmail Watcher
**Tier**: Silver
**Input**: `EMAIL_*.md` files in `Needs_Action/`
**Output**: Analysis added to task, draft reply created if needed, task moved to `Done/`

---

## When to Use

- `EMAIL_*.md` files appear in `Needs_Action/`
- User says "check emails" or "process my inbox"
- Orchestrator triggers this on schedule

---

## Workflow

### Step 1 — Scan for Email Tasks
List all `EMAIL_*.md` files in `Needs_Action/`. If none, report "No pending email tasks."

### Step 2 — Read Each Task
For each file, read the full content. The file contains:
- Sender name and email
- Subject line
- Email preview/body
- Current priority (may need revision)
- Timestamp

### Step 3 — Analyze the Email

Answer these questions:
1. What is the sender asking for?
2. Is there a deadline or urgency signal?
3. Does it require a reply? (most do)
4. Category: `invoice` / `meeting` / `request` / `information` / `complaint` / `other`
5. Should priority be revised? (bump to HIGH if urgent keywords found)

### Step 4 — Update Task File

Append an `## Analysis` section to the task file:

```markdown
## Analysis
**Analyzed**: {timestamp}
**Category**: {invoice/meeting/request/information/complaint/other}
**Revised Priority**: {HIGH/MEDIUM/LOW — reason if changed}
**Action Required**: {YES/NO}
**Action Type**: {reply/archive/escalate/forward}
**Summary**: {1-2 sentence plain-language description of what this email is about and what it needs}
**Key Details**: {any dates, amounts, names, or deadlines extracted from the email}
```

### Step 5 — Determine Next Action

| Condition | Action |
|-----------|--------|
| Reply needed | Call `draft-reply` skill |
| Just archive | Move to `Done/Communications/` |
| Escalate | Add `[ESCALATE]` tag, update Dashboard |
| Has attachment | Note in task, process attachment separately |

### Step 6 — Log Activity

Append to `Logs/YYYY-MM-DD.log`:
```
[{timestamp}] [PROCESS_EMAIL] Processed: {subject} from {sender} | Category: {cat} | Action: {action}
```

### Step 7 — Update Dashboard

Increment processed count and log last activity timestamp in `Dashboard.md`.

---

## Output Files

- Updated task file with `## Analysis` section
- (If reply needed) Draft file in `Plans/email_drafts/DRAFT_{timestamp}.md`
- Log entry in `Logs/YYYY-MM-DD.log`
- Updated `Dashboard.md`

---

## Email Categories

| Category | Signals | Default Action |
|----------|---------|----------------|
| `invoice` | invoice, payment, bill, amount due | Reply + escalate |
| `meeting` | meeting, call, schedule, calendar | Reply with availability |
| `request` | please, could you, need, help | Draft reply |
| `information` | FYI, update, newsletter, no CTA | Archive |
| `complaint` | unhappy, problem, disappointed | Reply + HIGH priority |
| `other` | Does not fit above | Archive or reply |

---

## Integration with MCP Email Sender

When a draft is approved by the human (moved to `Approved/`), the `email-sender` MCP server automatically sends it within 5 minutes. No further action required.

---

**Status**: Production Ready
**Depends on**: Gmail Watcher (Silver), draft-reply skill (optional), email-sender MCP
