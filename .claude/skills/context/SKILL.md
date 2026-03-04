# Context Skill

**Purpose**: Build, maintain, and inject relevant context so the AI always knows what is happening, who is involved, and what has happened before
**Storage**: Markdown-based context files, session memory, entity profiles
**Scope**: Session context, user preferences, entity tracking, conversation history, situational awareness

---

## Core Functions

### 1. Build Context
Gather relevant information before starting any task

### 2. Maintain Context
Keep context fresh as the session progresses

### 3. Inject Context
Supply the right context at the right moment to the right skill

### 4. Track Entities
Remember people, projects, topics, and relationships

### 5. Summarize History
Compress past interactions into reusable context

### 6. Resolve Ambiguity
Use context to fill in missing information intelligently

---

## Context Layers

```
Layer 1: System Context       → What is the AI Employee? What are its rules?
Layer 2: Session Context      → What is happening right now in this session?
Layer 3: Task Context         → What is the current task about?
Layer 4: Entity Context       → Who/what is involved in this task?
Layer 5: Historical Context   → What happened before that is relevant?
Layer 6: Environmental Context→ What time is it? What mode? What resources?
```

---

## Layer Definitions

### Layer 1: System Context (Permanent)
```
Source: Company_Handbook.md
Loaded: Always, at every session start
Content:
  - AI Employee purpose and role
  - Behavior rules (DO / DON'T)
  - Approved actions and forbidden actions
  - Tier capabilities (Bronze / Silver / Gold / Platinum)
  - Owner identity and preferences

Never changes unless human edits Company_Handbook.md
```

### Layer 2: Session Context (Per Session)
```
Source: Built at session start, updated throughout
Location: Plans/context/session_{date}_{id}.md
Content:
  - Session start time
  - Current operating mode (Normal / Idle / Burst / Emergency)
  - Active workflows
  - Files processed this session
  - Decisions made this session
  - Errors encountered this session

Reset: Each new Claude Code session
Persist: Saved to file for continuity if session interrupted
```

### Layer 3: Task Context (Per Task)
```
Source: Built when a task is picked up from Needs_Action/
Content:
  - Task file contents
  - Source file metadata (type, size, age)
  - Related tasks (same sender, same topic)
  - Priority and deadline
  - Previous attempts if any

Scope: Lives only for duration of one task
```

### Layer 4: Entity Context (Persistent)
```
Source: Plans/context/entities.md
Content:
  - People: name, role, email, topics, last contact
  - Projects: name, status, related files, stakeholders
  - Companies: name, relationship, contact person
  - Topics: recurring subjects, how they are typically handled

Grows over time as AI Employee learns
Updated after every interaction with an entity
```

### Layer 5: Historical Context (Searchable)
```
Source: Logs/, Archive/, Done/
Content:
  - Summary of past tasks for this entity/topic
  - Previous decisions and outcomes
  - Patterns observed over time
  - Recurring issues or requests

Loaded: On demand when relevant to current task
Not loaded by default (too much data)
```

### Layer 6: Environmental Context (Real-time)
```
Source: Computed at time of use
Content:
  - Current date and time
  - Day of week (affects scheduling logic)
  - Current mode (Normal / Idle / Burst / Emergency)
  - Disk space available
  - Queue depth
  - Last X events (last 5 things that happened)

Refreshed: Every 60 seconds
```

---

## Context File Formats

### Session Context File

```markdown
# Session Context

**Session ID**: SES_20260216_003
**Started**: 2026-02-16 09:00
**Mode**: Normal
**Vault**: E:\Hackathon-0-Personal-AI-Employee\Common\AI_Employee_Vault

---

## This Session

### Files Processed
| Time  | File                 | Type     | Priority | Result   |
|-------|----------------------|----------|----------|----------|
| 09:15 | report_q1.pdf        | document | HIGH     | Done     |
| 09:18 | sales_data.csv       | data     | MEDIUM   | Done     |
| 10:30 | invoice_acme.pdf     | document | HIGH     | Pending  |

### Active Workflows
- RUN_20260216_004: WF-001 (invoice_acme.pdf) — paused at Step 3 (approval)

### Decisions Made
- 09:15 invoice_scan.jpg flagged as unreadable → moved to quarantine
- 09:20 Done/ has 187 files → noted, archive recommended

### Errors This Session
- 09:15 invoice_scan.jpg: unreadable binary content (quarantined)

### Key Facts Learned
- User typically processes PDFs with HIGH priority
- Sales CSV files follow a weekly pattern (every Monday)
```

---

### Entity Context File

```markdown
# Entity Context

**Last Updated**: 2026-02-16 14:00
**Total Entities**: 8

---

## People

### Alice Johnson
- **Role**: Project Manager
- **Email**: alice@company.com
- **First seen**: 2026-01-10
- **Last contact**: 2026-02-15
- **Interaction count**: 34
- **Common topics**: Sprint planning, budget, hiring
- **Typical priority**: HIGH
- **Files sent**: 28 (mostly .pdf reports, .docx briefs)
- **Pattern**: Sends files Monday morning before standup
- **Notes**: Prefers concise summaries, not full transcripts

### Bob Chen
- **Role**: Lead Developer
- **Email**: bob@company.com
- **First seen**: 2026-01-12
- **Last contact**: 2026-02-14
- **Interaction count**: 21
- **Common topics**: Code review, deployment, bugs
- **Typical priority**: MEDIUM
- **Files sent**: 18 (mostly .py scripts, .json configs)
- **Pattern**: Sends code files Friday afternoons
- **Notes**: Needs quick turnaround on code review tasks

---

## Projects

### Project Alpha
- **Status**: IN_PROGRESS
- **Owner**: Alice Johnson
- **Start date**: 2026-01-15
- **Files**: 23 files processed
- **Topics**: Planning, budget, design, implementation
- **Last activity**: 2026-02-15
- **Notes**: Q1 deadline, high visibility

### Project Beta
- **Status**: PLANNING
- **Owner**: Bob Chen
- **Start date**: 2026-02-10
- **Files**: 5 files processed
- **Topics**: Architecture, tech stack, team setup

---

## Companies

### Acme Corp
- **Relationship**: Client
- **Contact**: John Smith (john@acme.com)
- **First seen**: 2026-01-20
- **Files**: 8 invoices, 3 contracts
- **Notes**: Monthly invoices, usually mid-month

---

## Topics

### Budget & Finance
- **Frequency**: Monthly
- **Typical files**: .xlsx, .pdf reports
- **Owner**: Alice Johnson
- **Handling**: Flag HIGH, summarize key numbers, note action items

### Code Reviews
- **Frequency**: Weekly (Fridays)
- **Typical files**: .py, .js, .ts
- **Owner**: Bob Chen
- **Handling**: Summarize changes, flag breaking changes as HIGH
```

---

## Context Building Process

### On Session Start
```
Step 1: Load System Context
  → Read Company_Handbook.md (always)
  → Extract: rules, permissions, tier, owner info

Step 2: Load Environmental Context
  → Get current date, time, day of week
  → Check disk space, queue depth
  → Check current mode (Normal/Idle/Burst/Emergency)

Step 3: Load Entity Context
  → Read Plans/context/entities.md
  → Index: all known people, projects, companies, topics

Step 4: Check for Ongoing Work
  → Scan Needs_Action/ for pending tasks
  → Check Plans/workflows/runs/ for paused workflows
  → Load any active session context if session was interrupted

Step 5: Summarize Starting State
  → Write to session context file
  → Update Dashboard with session start
  → Log: "[CONTEXT] Session started, {n} entities loaded, {n} pending tasks"
```

### On New Task
```
Step 1: Parse Task File
  → Extract: source file, priority, type, any metadata

Step 2: Entity Resolution
  → Extract names, emails, companies from task content
  → Match against entities.md
  → IF known entity → load their profile
  → IF unknown → create new entity stub

Step 3: Find Related History
  → Search Done/ and Archive/ for:
    - Same sender / same entity
    - Same file type / topic
    - Same project
  → Load top 3 most relevant past interactions as summary

Step 4: Detect Patterns
  → Does this match a known recurring task?
  → Has this sender sent files before at this time?
  → Is this part of an ongoing project?

Step 5: Assemble Task Context
  → Combine: task data + entity profile + related history + patterns
  → Write assembled context to session context file
  → Pass assembled context to the skill handling this task
```

---

## Context Injection

### How Context is Passed to Skills

```
When calling any skill, prepend the relevant context:

Format:
  ## Context for this task

  **Who**: Alice Johnson (Project Manager, alice@company.com)
  **History**: Alice has sent 28 files. Last file: report_q4.pdf (2026-02-01)
  **Pattern**: She typically sends weekly status reports on Mondays
  **Project**: Project Alpha (IN_PROGRESS, Q1 deadline)
  **Previous action**: Last file was summarized and flagged HIGH

  **Current Task**:
  [task details here]

  **Suggested handling**: Treat as HIGH priority, summarize key metrics,
  check if this supersedes the Q4 report
```

### Context Size Management
```
Full context available but only inject what is relevant:

For simple file tasks:
  → Entity profile (2-3 lines) + last 1 interaction
  → Keep under 200 words

For complex tasks (email, report, decision):
  → Full entity profile + last 3 interactions + project context
  → Keep under 500 words

For new entity (first contact):
  → System context rules only
  → Flag as: NEW_ENTITY, no history available

Rule: Context should HELP, not overwhelm
Trim: Remove details older than 90 days unless directly relevant
```

---

## Entity Resolution

### Matching Rules
```
Exact match (high confidence):
  - Email address matches exactly → MATCH
  - Name matches exactly (case-insensitive) → MATCH

Fuzzy match (medium confidence):
  - Name similarity > 85% (e.g. "Jon Smith" vs "John Smith") → LIKELY_MATCH
  - Email domain matches + name partial match → LIKELY_MATCH
  - Flag as LIKELY, ask human to confirm if important

No match (new entity):
  - No similar name or email found → NEW_ENTITY
  - Create stub profile with available info
  - Mark as: unverified, needs more data
```

### New Entity Stub
```
When first contact is detected:

# New Entity: {name or "Unknown"}
- **First seen**: {date}
- **Source**: {email / file / task}
- **Known info**: {whatever was extractable}
- **Status**: UNVERIFIED — needs more data
- **Action**: Watch for more interactions to build profile
```

---

## Pattern Detection

### Recurring Task Patterns
```
Pattern: Same file type from same sender, weekly
  → Label: RECURRING_WEEKLY
  → Action: Process with standard template for this sender

Pattern: Monthly reports arriving on 1st
  → Label: MONTHLY_REPORT
  → Action: Compare with previous month, highlight changes

Pattern: Urgent requests after business hours
  → Label: AFTER_HOURS_URGENT
  → Action: Ensure HIGH priority, fast processing

Pattern: New project files (first from a project)
  → Label: PROJECT_KICKOFF
  → Action: Create project entity, link all future files

Pattern: Invoice from recurring vendor
  → Label: RECURRING_INVOICE
  → Action: Check against previous invoices, flag discrepancies
```

### Anomaly Detection via Context
```
Context anomaly = Something that breaks an established pattern

Examples:
  - Alice always sends PDFs, today she sent an .exe
    → FLAG: Unusual file type from known sender

  - Bob's files are always <1MB, this one is 45MB
    → FLAG: Unusually large file from known sender

  - Invoice from Acme Corp is 3x the usual amount
    → FLAG: Amount anomaly on recurring invoice

  - File arrived at 3am (Bob always sends at 4pm)
    → FLAG: Unusual timing for known sender

Action on context anomaly:
  → Add anomaly note to task context
  → Increase priority by one level (LOW→MEDIUM, MEDIUM→HIGH)
  → Notify human with specific anomaly description
```

---

## Memory Compression

### When Context Gets Too Large
```
Session context compression (end of day):
  Full session log → compressed summary

Before (full log, 200 lines):
  09:00 Session started
  09:01 Loaded 8 entities
  09:05 Processing report_q1.pdf
  09:08 Extracted: 12-page PDF, Q1 financial report
  09:09 Summary written: revenue +12%, expenses +8%
  09:10 Task moved to Done/
  ...

After (compressed, 5 lines):
  Session 2026-02-16: 12 files processed (HIGH:4, MED:6, LOW:2)
  Entities: Alice (3 files), Bob (2 files), Acme Corp (1 file)
  Top topic: Q1 financial review (3 related files)
  Anomaly: invoice_scan.jpg quarantined (unreadable)
  Outcome: All resolved except 1 pending approval (WF-002)

Compression ratio target: 90% size reduction
Preservation rule: Keep decisions, outcomes, anomalies — drop step-by-step details
```

### Entity Profile Pruning
```
Keep in active profile:
  - Last 5 interactions (summarized)
  - Established patterns
  - Current active projects
  - Any open items or anomalies

Move to archive:
  - Interactions older than 90 days
  - Resolved projects
  - Superseded patterns

Delete from profile:
  - Duplicate entries
  - Interactions with no notable outcome
  - Temporary notes that are no longer relevant
```

---

## Context for Ambiguity Resolution

### When AI Needs to Guess
```
Situation: File has no clear sender or topic
Context helps resolve:

  IF file is .xlsx AND arrives Monday morning
    → Likely: weekly metrics report (matches Alice's pattern)
    → Priority: HIGH (Alice's files are always HIGH)
    → Action: Treat as weekly report, compare with last week

  IF file is .py AND arrives Friday afternoon
    → Likely: code review from Bob (matches Bob's pattern)
    → Priority: MEDIUM
    → Action: Summarize code changes

  IF no matching pattern found:
    → Label: UNKNOWN_CONTEXT
    → Priority: MEDIUM (default)
    → Action: Process generically, flag for human review
    → Note: Will update entity profile after human clarifies
```

### Confidence Levels
```
HIGH confidence (act autonomously):
  - Exact entity match + known pattern + matching file type
  - Example: Alice's Monday PDF = weekly report

MEDIUM confidence (act with note):
  - Fuzzy entity match OR pattern partially matches
  - Example: Similar name, probably Alice, proceed but flag

LOW confidence (flag for human):
  - New entity + no recognizable pattern + unusual file type
  - Example: First email from unknown company with .zip file

NO confidence (stop, ask human):
  - Contradictory signals (known sender, completely wrong file type)
  - Example: Alice sends .exe file at 3am
```

---

## Context Log

### Location
```
Common/AI_Employee_Vault/Logs/context_{date}.log
```

### Log Format
```
[2026-02-16 09:00:01] [CONTEXT] Session started SES_20260216_003
[2026-02-16 09:00:02] [CONTEXT] Loaded system context (Company_Handbook.md)
[2026-02-16 09:00:03] [CONTEXT] Loaded 8 entities from entities.md
[2026-02-16 09:00:04] [CONTEXT] 3 pending tasks in Needs_Action/
[2026-02-16 09:15:01] [CONTEXT] Task: report_q1.pdf → entity match: Alice Johnson (HIGH confidence)
[2026-02-16 09:15:02] [CONTEXT] Pattern: RECURRING_WEEKLY (Alice, Monday PDF report)
[2026-02-16 09:15:02] [CONTEXT] History loaded: 3 related past reports for context
[2026-02-16 09:15:03] [CONTEXT] Context injected: 187 words for skill process_inbox
[2026-02-16 14:30:01] [CONTEXT] Anomaly: invoice_scan.jpg from unknown sender, binary content
[2026-02-16 14:30:01] [CONTEXT] Confidence: LOW → flagged for human review
```

---

## Integration with Other Skills

### With File Understanding Skill
```
context → enriches → file-understanding with:
  Entity profile for the sender
  Historical file patterns for this type
  Related past files for comparison
  Suggested priority based on sender's usual priority
```

### With Workflow Skill
```
workflow → requests → context at:
  Start of each workflow (load full task context)
  Human handoff step (summarize context for human)
  Rollback step (confirm context is consistent after undo)
```

### With Reporting Skill
```
reporting → uses → context for:
  Entity-specific sections in reports
  Pattern highlights ("Alice sent 3 reports this week vs 1 last week")
  Anomaly summaries in weekly/monthly reports
```

### With Security Skill
```
security → consults → context for:
  Known vs unknown sender detection
  Anomaly flagging (unusual file from known sender)
  Confidence level in entity resolution
```

### With Planning Skill
```
planning → uses → context for:
  Understanding dependencies (task relates to project X)
  Identifying the right stakeholders from entity profiles
  Estimating effort based on similar past tasks
```

### With Memory Management Skill
```
memory-management → manages → context storage:
  Compress session logs daily
  Archive entity profiles older than 90 days
  Prune entity profiles that are too large
  Maintain entities.md index
```

---

## Best Practices

### DO
```
- Load entity context before every task (even if short)
- Flag anomalies immediately when patterns break
- Compress session context at end of each day
- Update entity profiles after every interaction
- Use context to set priority (known HIGH sender → HIGH priority)
- Record decisions in session context (why X was chosen)
- Keep context focused — inject only what is relevant
- Mark confidence level on every context-based decision
```

### DON'T
```
- Inject entire vault history for every task (overwhelming)
- Store raw PII in entity profiles (summarize instead)
- Treat context as certainty (it informs, not decides)
- Let entity profiles grow without pruning
- Skip context loading to save time (defeats the purpose)
- Confuse two entities because of similar names (verify first)
- Discard session context without compressing it
- Make irreversible decisions based on LOW confidence context
```

---

## Quick Reference: Context by Situation

```
Situation                   | Context Loaded             | Confidence
----------------------------|----------------------------|------------
Known sender, known pattern | Full entity + history      | HIGH
Known sender, new file type | Full entity + anomaly flag | MEDIUM
Unknown sender, normal file | System rules only          | LOW
Unknown sender, unusual file| System rules + security    | NO CONFIDENCE
Recurring task              | Pattern + last 3 similar   | HIGH
First-ever task type        | System rules only          | LOW
After session interruption  | Previous session context   | HIGH
Emergency mode              | Minimal (speed over depth) | MEDIUM
```

---

**Status**: Production Ready
**Priority**: HIGH (Enables intelligent, context-aware AI behavior)
**Layers**: 6 (System → Session → Task → Entity → Historical → Environmental)
**Entity Storage**: Plans/context/entities.md
**Session Storage**: Plans/context/session_{date}_{id}.md
**Compression**: Daily session compression, 90% size reduction target

*Good context = AI Employee that remembers, learns, and acts like it knows you*
