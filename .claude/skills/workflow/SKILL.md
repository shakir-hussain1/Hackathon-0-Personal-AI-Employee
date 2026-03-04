# Workflow Skill

**Purpose**: Orchestrate multi-step processes end-to-end, from trigger to completion
**Storage**: Markdown-based workflow definitions, run history, state tracking
**Scope**: Task pipelines, conditional branching, parallel steps, human handoffs, rollback

---

## Core Functions

### 1. Define Workflows
Describe a process as a sequence of named steps with conditions

### 2. Execute Workflows
Run steps in order, track state, pass data between steps

### 3. Branch on Conditions
Take different paths based on results, priority, or file type

### 4. Handle Human Handoffs
Pause workflow, wait for human input, resume cleanly

### 5. Rollback
Undo completed steps if a later step fails

### 6. Track History
Record every workflow run — start, steps, outcome, duration

---

## Workflow File Structure

```
Common/AI_Employee_Vault/Plans/
├── workflows/
│   ├── definitions/           # Workflow blueprints
│   │   ├── process_inbox.md
│   │   ├── onboard_file.md
│   │   ├── send_email.md
│   │   ├── weekly_review.md
│   │   └── emergency_cleanup.md
│   ├── runs/                  # Active + recent runs
│   │   ├── RUN_20260216_001.md
│   │   ├── RUN_20260216_002.md
│   │   └── ...
│   └── history/               # Completed runs (archived)
│       ├── 2026-02/
│       └── summary.md
```

---

## Workflow Definition Format

```markdown
# Workflow: {name}

**ID**: WF-{id}
**Version**: 1.0
**Trigger**: {manual | scheduled | event | conditional}
**Timeout**: {max duration, e.g. 30 minutes}
**On Failure**: {stop | continue | rollback | escalate}
**Owner**: {skill that owns this workflow}

---

## Description
{What this workflow does in 1-2 sentences}

---

## Input
| Field       | Type   | Required | Description              |
|-------------|--------|----------|--------------------------|
| file_path   | string | YES      | Path to file to process  |
| priority    | enum   | NO       | HIGH/MEDIUM/LOW (default MEDIUM) |

---

## Steps

### Step 1: {step name}
- **Action**: {what to do}
- **Skill**: {which skill handles this}
- **Input**: {data passed in}
- **Output**: {data produced}
- **On Success**: → Step 2
- **On Failure**: → Rollback Step 1 → Stop
- **Timeout**: 60 seconds

### Step 2: {step name}
...

---

## Rollback Steps

### Rollback Step 1
- **Trigger**: Step 2 or later fails
- **Action**: {how to undo step 1}
- **Verifies**: {how to confirm undo worked}
```

---

## Built-in Workflow Definitions

---

### Workflow 1: Process Inbox File

```markdown
# Workflow: Process Inbox File

**ID**: WF-001
**Trigger**: Event (new file in Inbox/) OR Manual
**Timeout**: 10 minutes
**On Failure**: Rollback → move file back to Inbox/

---

## Steps

### Step 1: Security Scan
- Action: Scan file for threats (path traversal, malicious type, injection)
- Skill: security
- Input: file_path
- Output: scan_result (CLEAN / QUARANTINED)
- On Success (CLEAN): → Step 2
- On Failure (QUARANTINED): → Stop (file quarantined, human alerted)
- Timeout: 30 seconds

### Step 2: Detect File Type
- Action: Identify file category (document, data, image, code, other)
- Skill: file-understanding
- Input: file_path
- Output: file_type, priority
- On Success: → Step 3
- On Failure: → flag as UNKNOWN → Step 3 (process as unknown)
- Timeout: 10 seconds

### Step 3: Create Task File
- Action: Write task .md file to Needs_Action/
- Skill: file-understanding
- Input: file_path, file_type, priority
- Output: task_file_path
- On Success: → Step 4
- On Failure: → Rollback Step 3 → Stop
- Timeout: 15 seconds

### Step 4: Analyze Content
- Action: Read file, extract key information, write summary to task
- Skill: process_inbox
- Input: file_path, task_file_path, file_type
- Output: summary, action_required, tags
- On Success: → Step 5
- On Failure: → mark task as NEEDS_REVIEW → Step 5
- Timeout: 3 minutes

### Step 5: Move File to Done
- Action: Move original file from Inbox/ to Done/
- Skill: file-understanding
- Input: file_path, task_file_path
- Output: done_file_path
- On Success: → Step 6
- On Failure: → Rollback Steps 3–5 → Stop
- Timeout: 15 seconds

### Step 6: Update Dashboard
- Action: Increment processed count, add to activity log
- Skill: update_dashboard
- Input: task summary, file type, priority
- Output: dashboard_updated
- On Success: → Step 7
- On Failure: → Log warning (non-fatal, continue)
- Timeout: 30 seconds

### Step 7: Log Completion
- Action: Write completion entry to daily log
- Skill: audit
- Input: full workflow run context
- Output: log_entry
- On Success: → COMPLETE
- On Failure: → Log to stderr (non-fatal)
- Timeout: 10 seconds

---

## Rollback Steps

### Rollback Step 3 (task file created)
- Action: Delete task file from Needs_Action/
- Verify: File no longer exists

### Rollback Step 5 (file moved to Done)
- Action: Move file back from Done/ to Inbox/
- Verify: File back in Inbox/, gone from Done/

---

## Output
- Task file in Needs_Action/ (or Done/ if fully processed)
- Dashboard updated
- Log entry written
- Workflow run record in Plans/workflows/runs/
```

---

### Workflow 2: Send Email (Silver+)

```markdown
# Workflow: Send Email

**ID**: WF-002
**Trigger**: Manual OR scheduled
**Timeout**: 24 hours (includes approval wait)
**On Failure**: Stop, notify human, do NOT retry send

---

## Steps

### Step 1: Validate Draft
- Action: Check email draft has required fields (TO, SUBJECT, BODY)
- Skill: file-understanding
- Input: draft_file_path
- Output: validation_result
- On Success: → Step 2
- On Failure: → Stop, notify human of missing fields
- Timeout: 10 seconds

### Step 2: Security Check
- Action: Scan draft for PII, credentials, sensitive data
- Skill: security
- Input: draft content
- Output: security_result, redaction_list
- On Success (CLEAN): → Step 3
- On Failure (FLAGGED): → Stop, alert human — NEVER send flagged content
- Timeout: 30 seconds

### Step 3: Request Approval
- Action: Submit to approval workflow, wait for human
- Skill: approval-handling
- Input: draft_file_path, requester, reason
- Output: approval_status (APPROVED / REJECTED / EXPIRED)
- On APPROVED: → Step 4
- On REJECTED: → Archive draft as REJECTED, Stop
- On EXPIRED: → Notify human, Stop (never auto-approve on expiry)
- Timeout: 24 hours

### Step 4: Send via Gmail
- Action: Call Gmail API to send email
- Skill: integration (Gmail)
- Input: draft content, recipient, subject
- Output: message_id, sent_timestamp
- On Success: → Step 5
- On Failure: → Do NOT retry automatically → notify human
- Timeout: 60 seconds

### Step 5: Log and Notify
- Action: Write send confirmation, update draft as SENT
- Skill: audit + notification
- Input: message_id, recipient, subject, sent_timestamp
- Output: log entry, INFO notification
- On Success: → COMPLETE
- On Failure: → Log error (non-fatal, email already sent)
- Timeout: 10 seconds

---

## Rollback Steps
Email sending has NO rollback (cannot unsend)
Prevention: Approval step (Step 3) is the safety gate
```

---

### Workflow 3: Weekly Review

```markdown
# Workflow: Weekly Review

**ID**: WF-003
**Trigger**: Scheduled (WEEKLY on FRIDAY at 17:00)
**Timeout**: 15 minutes
**On Failure**: Continue to next step (best-effort report)

---

## Steps

### Step 1: Collect Data
- Action: Aggregate week's logs, task counts, error counts
- Skill: audit + reporting
- Input: week_start_date, week_end_date
- Output: raw_metrics

### Step 2: Detect Anomalies
- Action: Compare this week vs last week, flag outliers
- Skill: audit
- Input: raw_metrics, previous_week_metrics
- Output: anomaly_list, trend_summary

### Step 3: Generate Weekly Report
- Action: Write full report to Plans/reports/weekly/
- Skill: reporting
- Input: raw_metrics, anomaly_list, trend_summary
- Output: report_file_path

### Step 4: Archive Completed Tasks
- Action: Move Done/ tasks older than 7 days to Archive/
- Skill: memory-management
- Input: cutoff_date (today - 7 days)
- Output: archived_count, space_freed

### Step 5: Run Optimization Check
- Action: Check resource usage, suggest cleanups
- Skill: optimization
- Input: current disk/RAM metrics
- Output: recommendations_list

### Step 6: Update Dashboard
- Action: Refresh dashboard with weekly summary
- Skill: update_dashboard
- Input: report_file_path, recommendations_list
- Output: dashboard_updated

### Step 7: Send Notification
- Action: Notify human — weekly report ready
- Skill: notification
- Input: report_file_path, key_metrics
- Output: notification_sent

→ COMPLETE
```

---

### Workflow 4: Emergency Cleanup

```markdown
# Workflow: Emergency Cleanup

**ID**: WF-004
**Trigger**: Conditional (disk > 90% OR RAM > 85%)
**Timeout**: 5 minutes
**On Failure**: Escalate immediately — do not retry

---

## Steps

### Step 1: Snapshot State
- Action: Record current disk/RAM/file counts before changes
- Skill: audit
- Output: pre_cleanup_snapshot

### Step 2: Delete Temp Files
- Action: Remove all *.tmp, *.bak files
- Skill: optimization
- Output: deleted_count, freed_mb (round 1)

### Step 3: Compress Old Logs
- Action: Compress log files older than 7 days
- Skill: optimization
- Output: compressed_count, freed_mb (round 2)

### Step 4: Archive Old Done Tasks
- Action: Archive Done/ tasks older than 30 days
- Skill: memory-management
- Output: archived_count, freed_mb (round 3)

### Step 5: Check if Resolved
- Action: Measure disk/RAM again
- Condition:
    IF disk < 85% → Step 6 (SUCCESS path)
    IF disk >= 85% → Step 5b (aggressive cleanup)

### Step 5b: Aggressive Cleanup (if needed)
- Action: Archive Done/ tasks older than 14 days, delete logs > 7 days
- Skill: optimization + memory-management
- Output: additional freed_mb

### Step 6: Report and Notify
- Action: Log total space freed, update Dashboard, notify human
- Skill: audit + notification
- Output: cleanup_report, CRITICAL resolved notification

→ COMPLETE
```

---

## Workflow Run Record Format

```markdown
# Workflow Run: RUN_20260216_007

**Workflow**: WF-001 Process Inbox File
**Run ID**: RUN_20260216_007
**Started**: 2026-02-16 14:30:01
**Finished**: 2026-02-16 14:31:45
**Duration**: 1 minute 44 seconds
**Status**: COMPLETED
**Input**: file_path = Inbox/report_q1.pdf
**Result**: Task created, file moved to Done/

---

## Step Execution Log

| Step | Name             | Started  | Duration | Status  | Output                   |
|------|------------------|----------|----------|---------|--------------------------|
| 1    | Security Scan    | 14:30:01 | 3s       | PASS    | CLEAN                    |
| 2    | Detect File Type | 14:30:04 | 1s       | PASS    | document, HIGH           |
| 3    | Create Task File | 14:30:05 | 2s       | PASS    | Needs_Action/FILE_014.md |
| 4    | Analyze Content  | 14:30:07 | 95s      | PASS    | Summary written          |
| 5    | Move to Done     | 14:31:42 | 1s       | PASS    | Done/report_q1.pdf       |
| 6    | Update Dashboard | 14:31:43 | 1s       | PASS    | Dashboard refreshed      |
| 7    | Log Completion   | 14:31:44 | 1s       | PASS    | Log entry written        |

---

## Data Passed Between Steps
- Step 1 → Step 2: scan_result = CLEAN
- Step 2 → Step 3: file_type = document, priority = HIGH
- Step 3 → Step 4: task_file = Needs_Action/FILE_014.md
- Step 4 → Step 5: summary = "Q1 financial report, 12 pages, action: review budget"
- Step 5 → Step 6: done_path = Done/report_q1.pdf
```

---

## Failed Run Record

```markdown
# Workflow Run: RUN_20260216_009

**Workflow**: WF-001 Process Inbox File
**Run ID**: RUN_20260216_009
**Started**: 2026-02-16 15:10:00
**Finished**: 2026-02-16 15:10:35
**Duration**: 35 seconds
**Status**: FAILED (rolled back)
**Input**: file_path = Inbox/suspicious_file.exe
**Result**: Quarantined at Step 1

---

## Step Execution Log

| Step | Name          | Started  | Duration | Status      | Output                    |
|------|---------------|----------|----------|-------------|---------------------------|
| 1    | Security Scan | 15:10:00 | 2s       | BLOCKED     | QUARANTINED (.exe type)   |

## Rollback
- No rollback needed (failed at Step 1, nothing was created)

## Actions Taken
- File moved to: Inbox/quarantine/suspicious_file.exe
- Security event logged: security_audit.log
- Notification sent: HIGH — malicious file type detected
```

---

## Workflow State Machine

```
States:
  PENDING    → In queue, not started yet
  RUNNING    → Currently executing a step
  PAUSED     → Waiting for human input (approval/review)
  COMPLETED  → All steps finished successfully
  FAILED     → A step failed, rollback executed
  ROLLED_BACK → Rollback completed after failure
  ESCALATED  → Cannot resolve, human must intervene
  CANCELLED  → Stopped by human before completion

Transitions:
  PENDING    → RUNNING    : Scheduler picks up workflow
  RUNNING    → PAUSED     : Human handoff step reached
  PAUSED     → RUNNING    : Human provides input/approval
  PAUSED     → CANCELLED  : Human cancels
  RUNNING    → COMPLETED  : All steps succeed
  RUNNING    → FAILED     : A step fails
  FAILED     → ROLLED_BACK: Rollback executes successfully
  FAILED     → ESCALATED  : Rollback also fails
  ROLLED_BACK → PENDING   : Retry if allowed
```

---

## Conditional Branching

### Branch on File Type
```
IF file_type = document   → WF-001 path A (full text analysis)
IF file_type = data/csv   → WF-001 path B (table analysis)
IF file_type = image      → WF-001 path C (basic metadata only)
IF file_type = code       → WF-001 path D (code review summary)
IF file_type = UNKNOWN    → WF-001 path E (flag for human review)
```

### Branch on Priority
```
IF priority = CRITICAL → skip queue, run immediately
IF priority = HIGH     → add to front of queue
IF priority = MEDIUM   → add to queue in order
IF priority = LOW      → add to back of queue, defer if busy
```

### Branch on Security Result
```
IF scan = CLEAN        → continue to next step
IF scan = WARNING      → continue but flag task
IF scan = QUARANTINED  → stop, do not continue
```

---

## Human Handoff Points

### When Workflow Pauses for Human
```
Pause triggers:
  - Approval required (email send, post, payment)
  - Ambiguous file content (AI unsure of category)
  - Security flag requiring review
  - Error that needs human decision
  - File contains sensitive/personal data

Pause behavior:
  1. Save full workflow state to run file
  2. Write clear instructions for human to Dashboard.md
  3. Send notification with specific action needed
  4. Wait indefinitely (respect human schedule)
  5. On human response → resume from exact pause point

Handoff format in Dashboard.md:
  ## Action Required
  **Workflow**: WF-002 Send Email (paused at Step 3)
  **Waiting for**: Approval of email draft
  **Draft**: Plans/email_drafts/DRAFT_007.md
  **Action**: Open draft, review, then:
    - To APPROVE: Change status to APPROVED in draft file
    - To REJECT: Change status to REJECTED in draft file
  **Expires**: 2026-02-17 14:30 (24 hours)
```

---

## Workflow Registry

```markdown
# Workflow Registry

| ID     | Name                  | Trigger              | Status  | Last Run         |
|--------|-----------------------|----------------------|---------|------------------|
| WF-001 | Process Inbox File    | Event / Manual       | ACTIVE  | 2026-02-16 14:31 |
| WF-002 | Send Email            | Manual               | ACTIVE  | 2026-02-15 11:20 |
| WF-003 | Weekly Review         | Scheduled Fri 17:00  | ACTIVE  | 2026-02-13 17:02 |
| WF-004 | Emergency Cleanup     | Conditional disk>90% | ACTIVE  | Never            |
| WF-005 | Onboard New File Type | Manual               | DRAFT   | Never            |
```

---

## Integration with Other Skills

### With Scheduler Skill
```
scheduler → triggers → workflow for:
  Timed workflows (WF-003 Weekly Review)
  Conditional workflows (WF-004 Emergency Cleanup)
  Retry of failed workflows (if retry allowed)
```

### With Approval Handling Skill
```
workflow → pauses for → approval-handling at:
  Any step requiring human approval
  Resumes when approval-handling returns APPROVED/REJECTED
```

### With Security Skill
```
workflow → calls → security at:
  Step 1 of every workflow (always scan first)
  Before any outbound action step
  Blocks entire workflow if security check fails
```

### With Audit Skill
```
workflow → logs to → audit:
  Every workflow start / step / end
  Duration of each step
  Data passed between steps (metadata only)
  All failures and rollbacks
```

### With Notification Skill
```
workflow → triggers → notification for:
  Workflow started (INFO, suppressed if frequent)
  Workflow completed (INFO)
  Workflow paused for human (HIGH)
  Workflow failed (HIGH or CRITICAL)
  Workflow escalated (CRITICAL)
```

### With Self-Healing Skill
```
self-healing → monitors → workflow for:
  Workflows stuck in RUNNING > timeout
  Workflows stuck in PAUSED > 48 hours
  Repeated workflow failures (same workflow, 3x)
  Auto-cancel stuck workflows after timeout
```

---

## Best Practices

### DO
```
- Define rollback for every step that creates or moves files
- Always scan files at Step 1 before any other processing
- Save full workflow state on every pause
- Log data passed between steps (metadata, not raw content)
- Set realistic timeouts per step (not one global timeout)
- Keep workflow definitions version-controlled
- Write human handoff instructions in plain language
- Archive completed run records (keep 30 days)
```

### DON'T
```
- Skip Step 1 security scan for "trusted" files
- Let workflows run indefinitely without a timeout
- Auto-approve human handoff steps after expiry
- Retry failed send/post/payment steps automatically
- Build workflows with more than 10 steps (split instead)
- Share mutable state between concurrent workflows
- Delete run records before archiving (30 day minimum)
- Continue a workflow after a security QUARANTINE result
```

---

## Quick Reference: Workflow → Steps

```
Workflow              | Steps | Human Pause? | Rollback?
----------------------|-------|--------------|----------
Process Inbox File    | 7     | NO           | YES (file moves)
Send Email            | 5     | YES (Step 3) | NO (cannot unsend)
Weekly Review         | 7     | NO           | NO (reports only)
Emergency Cleanup     | 6     | NO           | NO (time-critical)
```

---

**Status**: Production Ready
**Priority**: HIGH (Backbone of all multi-step operations)
**Max Steps per Workflow**: 10 (split larger ones)
**Concurrent Workflows**: Sequential preferred (1 at a time per resource)
**Run History**: 30 days active, then archived to history/

*Good workflows = Complex tasks that run reliably, every time, without supervision*
