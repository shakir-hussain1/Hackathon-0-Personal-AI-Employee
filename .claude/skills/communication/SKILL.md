# Communication Skill

**Purpose**: Compose, format, and deliver clear messages to humans and external parties
**Storage**: Markdown-based message drafts, templates, communication logs, tone profiles
**Scope**: Internal updates, email drafts, status messages, summaries, reports to humans, external outreach

---

## Core Functions

### 1. Compose Messages
Write clear, structured messages tailored to audience and purpose

### 2. Select Tone
Match communication style to context — formal, casual, urgent, informative

### 3. Format Output
Structure content for readability — headers, bullets, tables, summaries

### 4. Deliver
Route message to correct channel — Dashboard, notification, email draft, report

### 5. Track Communication
Log what was communicated, when, to whom, and outcome

### 6. Maintain Voice Consistency
Ensure all AI Employee communications feel coherent and professional

---

## Communication Channels

```
Channel               | Use Case                        | Tier
----------------------|---------------------------------|--------
Dashboard.md          | Status updates, alerts, summaries| Bronze
notifications.md      | Event log, action reminders      | Bronze
Logs/ files           | Technical audit trail            | Bronze
Task files (.md)      | Task instructions for AI/human   | Bronze
Email drafts (.md)    → Gmail send     | External messages       | Silver+
Social drafts (.md)   → LinkedIn/X     | Public posts            | Gold+
Reports (.md)         | Periodic summaries               | Bronze
Slack/Teams (future)  | Team messaging                   | Future
```

---

## Audience Profiles

### Audience 1: Self (AI Internal)
```
Purpose:  Logging, context passing, skill-to-skill instructions
Tone:     Technical, precise, structured
Format:   Consistent markdown, machine-readable fields
Length:   As short as possible while complete
Example:
  [CONTEXT] Entity matched: alice@company.com (confidence 92%)
  [ACTION]  Priority set to HIGH via RULE-001
  [OUTPUT]  task_file = Needs_Action/FILE_014.md
```

### Audience 2: Human Owner (Dashboard / Notifications)
```
Purpose:  Status updates, alerts, action requests, summaries
Tone:     Clear, direct, actionable — no jargon
Format:   Plain markdown, bullet points, tables for data
Length:   Short for alerts (1-3 lines), medium for summaries
Principle: Tell them WHAT happened, WHY it matters, WHAT to do
Example:
  3 files processed from Alice. 1 needs your review.
  → File: invoice_scan.jpg (unreadable — quarantined)
  → Action: Check Inbox/quarantine/ when convenient
```

### Audience 3: Professional Contact (Email)
```
Purpose:  Business communication on behalf of human
Tone:     Professional, respectful, concise
Format:   Standard email structure (greeting, body, closing)
Length:   Short to medium — get to the point quickly
Principle: Represent the human well — never embarrass them
Example:
  Subject: Re: Q1 Budget Review Meeting

  Hi Alice,

  Thank you for sending the budget report. I have reviewed
  the key figures and will share feedback by Thursday.

  Best regards,
  [Human's name]
```

### Audience 4: Public (Social Media)
```
Purpose:  LinkedIn posts, announcements, thought leadership
Tone:     Professional but approachable, engaging
Format:   Short paragraphs, no jargon, strong opening line
Length:   LinkedIn: 150-300 words optimal, max 3000 chars
Principle: Represent the human's brand — authentic, valuable
Example:
  Spent the week automating our document workflow.
  Result: 3 hours saved per week, zero missed deadlines.

  The key insight: AI works best when given clear structure
  to operate within — not unlimited freedom.

  What workflows have you automated recently?

  #Productivity #AI #Automation
```

### Audience 5: Vendor / External Party
```
Purpose:  Inquiries, follow-ups, acknowledgments
Tone:     Professional, specific, brief
Format:   Direct ask or response, no fluff
Length:   Short — respect their time
Principle: Clear ask + clear deadline + clear contact
Example:
  Hi John,

  Following up on invoice INV-045 sent on Feb 10.
  Could you confirm receipt and estimated payment date?

  Thank you,
  [Human's name]
```

---

## Message Templates

### Template 1: Task Completion Update (Dashboard)
```
## Processed: {filename}
**Time**: {timestamp}
**From**: {sender}
**Category**: {category}
**Priority**: {priority}
**Summary**: {1-2 sentence summary}
**Action needed**: {YES/NO} — {action if yes}
**Location**: {Done/filename.md}
```

### Template 2: Alert Message (Dashboard)
```
> **[{LEVEL}]** {timestamp} — {title}
> {1-sentence description of what happened}
> {1-sentence description of what was done automatically}
> **Action needed**: {what human should do, if anything}
```

### Template 3: Status Summary (Dashboard — Daily)
```
## Today's Summary — {date}

**Processed**: {n} files | **Pending**: {n} tasks | **Errors**: {n}

### Highlights
- {most important thing that happened}
- {second most important}
- {third if relevant}

### Needs Your Attention
- {item requiring human action, or "Nothing — all clear"}
```

### Template 4: Business Email Draft
```
To: {recipient_email}
Subject: {subject_line}

{Greeting} {recipient_first_name},

{Opening line — why you are writing, 1 sentence}

{Body — key message, 2-4 sentences, one clear ask if any}

{Closing — next step or thank you}

{Sign-off},
{Human's name}
{Title if applicable}
```

### Template 5: Follow-Up Email
```
To: {recipient_email}
Subject: Following up: {original_subject}

Hi {recipient_first_name},

I wanted to follow up on {topic} from {original_date}.

{Specific ask or status check — 1-2 sentences}

Please let me know by {deadline} if possible.

Thank you,
{Human's name}
```

### Template 6: LinkedIn Post Draft
```
{Strong opening line — hook the reader, 1 sentence}

{Context or story — 2-3 sentences}

{Key insight or takeaway — 1-2 sentences}

{Question or call to action — 1 sentence}

{3-5 hashtags}
```

### Template 7: Escalation Message to Human
```
## Action Required — {task_title}

**Why this needs you**: {plain-language reason AI cannot proceed}
**Task**: {brief description}
**File**: {file path if relevant}

**Options**:
{table of options with recommendations}

**AI recommendation**: {option} — {1-sentence reason}
**No expiry** — AI will wait.
```

### Template 8: Weekly Briefing (Dashboard)
```
## Weekly Briefing — Week {n}, {year}

**Period**: {Mon date} → {Sun date}

### By the numbers
| Metric          | This Week | Last Week | Change |
|-----------------|-----------|-----------|--------|
| Files processed | {n}       | {n}       | {+/-}  |
| Tasks completed | {n}       | {n}       | {+/-}  |
| Errors          | {n}       | {n}       | {+/-}  |

### Highlights
{3 key things that happened this week}

### Watch out for next week
{1-2 upcoming events or potential issues}

**Full report**: Plans/reports/weekly/report_week_{date}.md
```

---

## Tone Guide

### Formal (External Email, Contracts, Legal)
```
DO:
  - Full sentences, proper grammar
  - Titles and last names (Dear Mr. Smith)
  - Clear subject lines
  - Professional closing (Best regards, Sincerely)
  - No contractions (do not → not don't)

DON'T:
  - Slang, casual phrases
  - Emojis (unless industry norm)
  - First name only for first contact
  - Vague language (soon, maybe, might)
```

### Professional (Most Business Communication)
```
DO:
  - First names (Hi Alice)
  - Contractions acceptable (I'll, we're)
  - Friendly but efficient
  - Clear asks and deadlines
  - Thank you when appropriate

DON'T:
  - Overly stiff or bureaucratic
  - Filler phrases (I hope this email finds you well)
  - Long-winded explanations
  - Passive voice when active works
```

### Conversational (Dashboard Updates, Internal Notes)
```
DO:
  - Direct and brief
  - Active voice
  - Bullets over paragraphs
  - Numbers over vague words (3 files not several files)
  - Time stamps

DON'T:
  - Over-explain obvious things
  - Apologize excessively
  - Write walls of text
  - Repeat information already visible on Dashboard
```

### Urgent (Alerts, Critical Notifications)
```
DO:
  - Lead with the problem immediately
  - State impact in first sentence
  - Say what was done or what is needed
  - Use [CRITICAL] / [HIGH] prefix clearly

DON'T:
  - Bury the lead
  - Soften critical issues
  - Use vague language
  - Include non-essential detail in the alert
```

---

## Message Quality Rules

### Clarity Rules
```
Rule 1: One message = one main point
  Bad:  "The file was processed, and also the disk is getting full,
         and by the way Alice sent another report."
  Good: Three separate updates, each clear and focused

Rule 2: Lead with the most important information
  Bad:  "After reviewing all the context and considering various factors,
         it appears that the file may need your attention."
  Good: "Action needed: invoice_acme.pdf needs your approval."

Rule 3: Be specific with numbers
  Bad:  "Several files were processed."
  Good: "12 files processed (8 documents, 3 CSVs, 1 image)."

Rule 4: Name the action, not just the situation
  Bad:  "The disk is getting full."
  Good: "Disk at 82%. To free space: Archive Done/ tasks >60 days old."
```

### Length Rules
```
Alert / Dashboard update:     1-3 lines (under 50 words)
Task summary:                 3-5 lines (under 100 words)
Email (simple):               50-150 words
Email (complex):              150-300 words (max)
LinkedIn post:                150-300 words
Weekly briefing:              200-400 words
Daily report (executive):     Under 250 words for summary section
Full report:                  No limit (but structure with headers)
```

### Completeness Rules
```
Every outbound message must answer:
  WHO:   Who is this from / about?
  WHAT:  What happened or what is needed?
  WHY:   Why does this matter?
  WHEN:  When did it happen / when is action needed?
  HOW:   How should the human respond (if action needed)?

Internal messages (logs, context) need:
  WHAT:  What happened?
  WHEN:  Timestamp
  RESULT: What was the outcome?
```

---

## Communication Log

### Location
```
Common/AI_Employee_Vault/Logs/communication.log
```

### Log Format
```
[2026-02-16 09:15] [COMM] channel=dashboard type=task_complete
  message="Processed report_q1.pdf (HIGH) from Alice. Summary written."
  audience=human_owner length=42_words

[2026-02-16 09:20] [COMM] channel=notification type=alert level=WARNING
  message="Disk at 75%. Consider archiving Done/ tasks >60 days."
  audience=human_owner length=11_words

[2026-02-16 11:30] [COMM] channel=email_draft type=follow_up
  to=john@acme.com subject="Following up: Invoice INV-045"
  status=PENDING_APPROVAL audience=external_vendor length=67_words

[2026-02-16 14:00] [COMM] channel=email_draft type=follow_up
  status=APPROVED sent=true message_id=gmail_msg_abc123
```

---

## Draft Review Checklist

### Before Any Outbound Communication

```
Content:
  [ ] Message has one clear main point
  [ ] Lead sentence states the purpose immediately
  [ ] All claims are factually accurate
  [ ] No vault data included that was not intended
  [ ] No PII included without authorization
  [ ] No credentials, keys, or secrets in message

Tone:
  [ ] Tone matches audience profile
  [ ] No language that could embarrass the human
  [ ] No aggressive or inappropriate content
  [ ] Consistent with previous communications to same recipient

Format:
  [ ] Subject line is clear and specific (for email)
  [ ] Length is appropriate for channel
  [ ] Greeting and closing are appropriate
  [ ] No broken markdown or formatting errors

Compliance:
  [ ] Approved by Approval Handling Skill (outbound)
  [ ] Logged in communication.log
  [ ] Risk level assessed (risk-detection checked)
  [ ] Recipient is on approved contacts list (Silver+)
```

---

## Common Phrases to Use / Avoid

### USE (Clear, Professional)
```
"3 files processed" (not "several files were processed")
"Action needed by Friday" (not "please respond when convenient")
"I've reviewed the document" (not "upon reviewing said document")
"Could you confirm by Thursday?" (not "I was wondering if you might")
"The task is complete" (not "it appears the task may be complete")
"Disk at 82% — archive recommended" (not "storage situation is concerning")
```

### AVOID (Vague, Weak, Filler)
```
"I hope this message finds you well" → just start with the point
"As per my previous email" → quote the relevant part instead
"Please don't hesitate to reach out" → "Reply to this email" is clearer
"It appears that" / "It seems like" → state it directly if you know
"ASAP" → give a specific date/time
"Various issues" → list the issues
"Moving forward" → just state what will happen next
"Touch base" → "meet" or "discuss" is clearer
```

---

## Sensitive Communication Rules

### Never Include in Any Message
```
- API keys, tokens, passwords (even partial)
- Personal financial details without authorization
- Health or medical information
- Confidential business data to external parties
- Other people's private information without consent
- Speculative or unverified facts stated as certain
- Content that could be defamatory
- Political or religious opinions attributed to the human
```

### Always Verify Before External Send
```
- Is the recipient address correct? (double-check)
- Is this the right reply-to or a new thread?
- Does the human know this email is going out?
- Would the human be comfortable if anyone read this?
- Is the subject line appropriate and accurate?
```

---

## Integration with Other Skills

### With Notification Skill
```
communication → formats messages for → notification:
  Alert text for Dashboard banners
  Notification log entries
  Toast notification content (short, clear)
```

### With Reporting Skill
```
communication → writes → reporting output:
  Executive summaries in reports
  Weekly briefing narrative
  Exception report descriptions
```

### With Delegation Skill
```
delegation → uses → communication for:
  Human task assignment messages (Level 3/4)
  Follow-up reminder messages
  Stalled delegation alerts
```

### With Approval Handling Skill
```
communication → submits drafts to → approval-handling:
  All external emails before send
  All social posts before publish
  Any message that speaks on behalf of human
```

### With Security Skill
```
security → reviews → communication output:
  Scan outbound messages for credential leaks
  Check for PII in external messages
  Verify recipient against approved list
```

### With Context Skill
```
context → enriches → communication with:
  Recipient's communication history
  Preferred tone and length for this contact
  Previous message thread for continuity
  Entity profile for accurate personalization
```

### With Learning Skill
```
learning → improves → communication over time:
  Track which message formats get approved quickly
  Learn human's preferred tone adjustments
  Detect patterns in human edits to drafts
  Improve template defaults based on feedback
```

---

## Best Practices

### DO
```
- Lead with the most important information always
- Match tone to audience every time
- Keep messages short — respect attention
- Use specific numbers, dates, and names
- Run every external message through approval-handling
- Log every communication in communication.log
- Use templates as starting points, customize as needed
- Proofread for accuracy before flagging for approval
```

### DON'T
```
- Send any external message without human approval
- Include sensitive data in communication logs
- Use vague language when specific words exist
- Write walls of text when bullets work better
- Copy-paste vault contents verbatim into emails
- Use the same tone for all audiences
- Ignore past communication with the same recipient
- Communicate speculatively (only state what is known)
```

---

## Quick Reference: Message Type → Template

```
Message Type             | Template  | Channel          | Approval?
-------------------------|-----------|------------------|----------
Task completed           | T1        | Dashboard        | No
Alert (any level)        | T2        | Notification     | No
Daily status             | T3        | Dashboard        | No
Business email           | T4        | Email draft      | YES
Follow-up email          | T5        | Email draft      | YES
LinkedIn post            | T6        | Social draft     | YES
Escalation to human      | T7        | Dashboard + notif| No
Weekly briefing          | T8        | Dashboard        | No
Internal log entry       | (raw log) | Logs/            | No
Skill-to-skill message   | (context) | Internal only    | No
```

---

**Status**: Production Ready
**Priority**: HIGH (Every human-facing output passes through here)
**Audiences**: 5 (Self, Human Owner, Professional Contact, Public, Vendor)
**Templates**: 8 ready-to-use message templates
**Approval**: Required for all external communication (Silver+ channels)
**Tone Profiles**: 4 (Formal, Professional, Conversational, Urgent)

*Good communication = AI Employee that speaks clearly, appropriately, and always on behalf of — never instead of — the human*
