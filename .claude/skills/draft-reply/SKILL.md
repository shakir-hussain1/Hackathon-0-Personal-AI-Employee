---
name: draft-reply
description: |
  Generate a professional email reply draft for human review and approval.
  Reads the original email task, drafts a contextually appropriate reply,
  saves it to Plans/email_drafts/, and notifies the human via Dashboard.
  Use after process-email determines a reply is required.
---

# Draft Reply Skill

**Purpose**: Generate a professional email reply draft for human approval before sending
**Tier**: Silver
**Input**: `EMAIL_*.md` task file in `Needs_Action/`
**Output**: Draft reply saved to `Plans/email_drafts/`, Dashboard notification

---

## When to Use

- `process-email` skill determined a reply is needed
- User asks "draft a reply to X"
- Email is categorized as `request`, `meeting`, `invoice`, or `complaint`

---

## Workflow

### Step 1 — Read Original Email
Read the full `EMAIL_*.md` task file. Extract:
- Sender name and email address
- Subject line
- Full email body/preview
- Category (from `## Analysis` section if already processed)
- Any deadlines, amounts, or specific asks

### Step 2 — Determine Tone and Template

| Category | Tone | Template |
|----------|------|----------|
| `invoice` | Professional, precise | Acknowledge receipt, state action/timeline |
| `meeting` | Friendly, professional | Accept/decline/propose alternative |
| `request` | Helpful, professional | Address the ask directly |
| `complaint` | Empathetic, professional | Acknowledge issue, state resolution |
| `information` | Brief, professional | Acknowledge/thank if required |

### Step 3 — Draft the Reply

Use this structure:
```
Subject: Re: {original subject}

Hi {sender first name},

{Opening — acknowledge or thank, 1 sentence}

{Body — address their ask directly, 2-4 sentences}
{Include: specific answers, next steps, any relevant data}

{Closing — next step or thank you, 1 sentence}

Best regards,
[Your Name]
```

**Rules:**
- Keep it under 200 words unless the topic requires more
- Answer every question asked in the original email
- Never include information not authorized to share
- Do not make commitments the human has not agreed to

### Step 4 — Save Draft

Create file at `Plans/email_drafts/DRAFT_{timestamp}.md`:

```markdown
# Email Draft
Created: {timestamp}
Status: PENDING_APPROVAL
Source Task: {task_filename}

---

To: {recipient_email}
Subject: Re: {subject}

---

{full draft body}

---

## Approval Instructions
- **To APPROVE**: Use the `email-sender` MCP tool or move this file to `Approved/`
- **To EDIT**: Modify the body above, then move to `Approved/`
- **To REJECT**: Delete this file
```

### Step 5 — Update Source Task

Append to the `EMAIL_*.md` task file:
```markdown
## Reply Drafted
Draft file: `Plans/email_drafts/DRAFT_{timestamp}.md`
Status: AWAITING_HUMAN_APPROVAL
```

### Step 6 — Notify via Dashboard

Add a notification line to `Dashboard.md`:
```
> **APPROVAL NEEDED** — Email reply ready: `Plans/email_drafts/DRAFT_{timestamp}.md` | To: {recipient} | Re: {subject}
```

### Step 7 — Log Activity
```
[{timestamp}] [DRAFT_REPLY] Draft created for {sender} re: {subject} | File: DRAFT_{timestamp}.md | Status: PENDING_APPROVAL
```

---

## Approval Workflow

```
Draft saved to Plans/email_drafts/
    ↓
Human reviews in VS Code / Obsidian
    ↓
Human approves → [use email-sender MCP tool OR move to Approved/]
    ↓
Email Sender polls Approved/ every 5 minutes → sends via Gmail
    ↓
Sent email archived to Done/Communications/
```

---

## Common Draft Mistakes to Avoid

- Do NOT write "I hope this email finds you well"
- Do NOT include uncertain facts as if they are certain
- Do NOT commit to deadlines the human hasn't confirmed
- Do NOT expose other clients' details
- Do NOT use ALL CAPS or excessive exclamation marks

---

**Status**: Production Ready
**Depends on**: process-email skill, email-sender MCP (Silver)
**Used by**: process-email skill (auto-triggered when reply needed)
