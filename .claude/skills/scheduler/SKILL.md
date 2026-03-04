# Scheduler Skill

**Purpose**: Schedule, queue, and execute tasks at the right time automatically
**Storage**: Markdown-based schedule files, human-readable
**Scope**: Time-based triggers, recurring jobs, task queuing, priority scheduling

---

## Core Functions

### 1. Schedule Tasks
Define when tasks should run (once, daily, weekly, monthly)

### 2. Queue Management
Hold pending tasks in order, prevent overload

### 3. Priority Execution
Run urgent tasks first, defer low-priority work

### 4. Recurring Jobs
Repeat tasks on a schedule (cron-style logic)

### 5. Missed Job Recovery
Detect and re-run jobs that were skipped (system was off)

---

## Schedule File Format

### Location
```
Common/AI_Employee_Vault/Plans/schedule.md
```

### Format
```markdown
# Task Schedule

**Last Updated**: 2026-02-16 14:00
**Next Run Check**: 2026-02-16 15:00
**Scheduler Status**: ACTIVE

---

## Scheduled Tasks

### TASK-001: Daily Vault Cleanup
- **ID**: TASK-001
- **Type**: RECURRING
- **Schedule**: DAILY at 00:00
- **Priority**: LOW
- **Status**: ACTIVE
- **Last Run**: 2026-02-15 00:01
- **Next Run**: 2026-02-16 00:00
- **Action**: Run cleanup → delete temp files, rotate logs
- **Owner**: optimization-skill

### TASK-002: Weekly Dashboard Refresh
- **ID**: TASK-002
- **Type**: RECURRING
- **Schedule**: WEEKLY on SUNDAY at 07:00
- **Priority**: MEDIUM
- **Status**: ACTIVE
- **Last Run**: 2026-02-09 07:02
- **Next Run**: 2026-02-16 07:00
- **Action**: Rebuild Dashboard stats from scratch
- **Owner**: update_dashboard skill

### TASK-003: Process Inbox
- **ID**: TASK-003
- **Type**: RECURRING
- **Schedule**: EVERY 60 minutes
- **Priority**: HIGH
- **Status**: ACTIVE
- **Last Run**: 2026-02-16 13:00
- **Next Run**: 2026-02-16 14:00
- **Action**: Check Inbox → create tasks → process files
- **Owner**: process_inbox skill

### TASK-004: Monthly Archive
- **ID**: TASK-004
- **Type**: RECURRING
- **Schedule**: MONTHLY on 1st at 01:00
- **Priority**: LOW
- **Status**: ACTIVE
- **Last Run**: 2026-02-01 01:03
- **Next Run**: 2026-03-01 01:00
- **Action**: Archive Done/ tasks older than 90 days
- **Owner**: memory-management skill
```

---

## Schedule Types

### One-Time Task
```
Run once at a specific datetime, then mark COMPLETED

Format:
  Schedule: ONCE at 2026-02-17 09:00

Use case:
  - Send a specific report on a deadline
  - Process a file at a scheduled time
  - Run a migration on a specific date
```

### Recurring - Interval
```
Run every N minutes/hours

Format:
  Schedule: EVERY 30 minutes
  Schedule: EVERY 2 hours
  Schedule: EVERY 90 minutes

Use case:
  - Check Inbox every hour
  - Refresh Dashboard every 30 min
  - Backup vault every 6 hours
```

### Recurring - Daily
```
Run once per day at a fixed time

Format:
  Schedule: DAILY at 00:00
  Schedule: DAILY at 08:00
  Schedule: DAILY at 23:30

Use case:
  - Midnight cleanup
  - Morning briefing at 8 AM
  - End-of-day log rotation
```

### Recurring - Weekly
```
Run once per week on a specific day

Format:
  Schedule: WEEKLY on MONDAY at 09:00
  Schedule: WEEKLY on FRIDAY at 17:00
  Schedule: WEEKLY on SUNDAY at 00:00

Days: MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY

Use case:
  - Weekly report every Friday
  - System audit every Sunday
  - Weekly archive every Saturday
```

### Recurring - Monthly
```
Run once per month on a specific day

Format:
  Schedule: MONTHLY on 1st at 01:00
  Schedule: MONTHLY on 15th at 12:00
  Schedule: MONTHLY on LAST at 23:00

Use case:
  - Monthly archive on 1st
  - Mid-month report on 15th
  - End-of-month summary on last day
```

### Conditional Trigger
```
Run when a condition becomes true

Format:
  Schedule: WHEN inbox_count > 10
  Schedule: WHEN disk_usage > 80%
  Schedule: WHEN error_count > 5 in last hour
  Schedule: WHEN Needs_Action has files older than 2 days

Use case:
  - Emergency cleanup when disk fills up
  - Alert when too many errors occur
  - Process backlog when queue builds up
```

---

## Task Queue

### Queue File Location
```
Common/AI_Employee_Vault/Plans/queue.md
```

### Queue Format
```markdown
# Task Queue

**Updated**: 2026-02-16 14:05
**Queue Depth**: 4 tasks
**Processing**: TASK-A003

---

## Running Now
| ID       | Task               | Started     | ETA     |
|----------|--------------------|-------------|---------|
| TASK-A003| Process Inbox      | 14:03       | 14:05   |

## Waiting (Priority Order)
| Position | ID       | Task               | Priority | Queued At   |
|----------|----------|--------------------|----------|-------------|
| 1        | TASK-A007| Update Dashboard   | HIGH     | 14:00       |
| 2        | TASK-A009| Compress Logs      | MEDIUM   | 13:45       |
| 3        | TASK-A011| Archive Done Tasks | LOW      | 12:00       |

## Completed Today
| ID       | Task               | Completed   | Result  |
|----------|--------------------|-------------|---------|
| TASK-A001| Daily Cleanup      | 00:01       | OK      |
| TASK-A002| Inbox Check 08:00  | 08:03       | OK      |
```

### Queue Rules
```
FIFO within same priority level
Priority order: CRITICAL > HIGH > MEDIUM > LOW

Max queue depth: 20 tasks
  IF queue > 20 → reject LOW priority tasks
  IF queue > 15 → warn in Dashboard
  IF queue > 10 → log warning

Max concurrent tasks: 1 (sequential, not parallel)
  Reason: Avoid race conditions on shared vault files
  Exception: Read-only tasks can run in parallel
```

---

## Priority Levels

### CRITICAL
```
Triggers: Resource emergency, system failure, security alert
Wait time: 0s (jump to front of queue)
Timeout:   10 minutes max
Examples:
  - Emergency cleanup when disk >95%
  - Watcher crashed → restart
  - Vault corruption detected → backup now
```

### HIGH
```
Triggers: Time-sensitive user-facing tasks
Wait time: Next available slot
Timeout:   30 minutes max
Examples:
  - Process Inbox files
  - Respond to urgent file drop
  - Update Dashboard after new files
```

### MEDIUM
```
Triggers: Regular operational tasks
Wait time: Up to 15 minutes acceptable
Timeout:   60 minutes max
Examples:
  - Dashboard refresh
  - Weekly report generation
  - Log compression
```

### LOW
```
Triggers: Maintenance, archival, optimization
Wait time: Up to 2 hours acceptable
Timeout:   120 minutes max
Examples:
  - Archive old tasks
  - Monthly summary
  - Storage optimization
  - Index rebuild
```

---

## Scheduling Logic

### How to Determine Next Run

```
For INTERVAL tasks:
  next_run = last_run + interval_minutes

For DAILY tasks:
  next_run = today's date + scheduled_time
  IF scheduled_time already passed today:
    next_run = tomorrow's date + scheduled_time

For WEEKLY tasks:
  next_run = next occurrence of target_day + scheduled_time
  IF today is target_day AND time not yet passed:
    next_run = today + scheduled_time

For MONTHLY tasks:
  next_run = this month's target_date + scheduled_time
  IF target_date already passed this month:
    next_run = next month's target_date + scheduled_time
  SPECIAL: "LAST" = last day of month

For ONCE tasks:
  next_run = specified datetime
  After completion: status → COMPLETED (never runs again)

For CONDITIONAL tasks:
  next_run = whenever condition becomes true
  Re-check condition: every check_interval seconds
```

### Missed Job Handling
```
On startup, check all scheduled tasks:

For each task:
  IF next_run < now AND status = ACTIVE:
    → Task was MISSED (system was off or crashed)

    IF task.type = ONCE:
      IF missed by < 24 hours → run now (still relevant)
      IF missed by > 24 hours → mark EXPIRED, log warning

    IF task.type = RECURRING:
      IF last_run > 24 hours ago → run now (catch up)
      IF last_run < 24 hours ago → skip (already ran today)
      Update next_run = calculate from NOW

Log all missed jobs:
  [SCHEDULER] MISSED: TASK-001 was due 2026-02-15 00:00
  [SCHEDULER] ACTION: Running now (missed by 14 hours)
```

---

## Execution Flow

### Step 1: Check Schedule
```
Every check_interval (default: 60s):
  1. Read schedule.md
  2. Find tasks where next_run <= now
  3. Filter by status = ACTIVE
  4. Sort by priority (CRITICAL first)
  5. Add to queue
```

### Step 2: Queue Processing
```
While queue not empty:
  1. Pop highest-priority task from queue
  2. Mark task as RUNNING in queue.md
  3. Execute task action
  4. On success: update last_run, calculate next_run
  5. On failure: log error, increment fail_count
  6. Remove from queue
  7. Update schedule.md
```

### Step 3: Post-Execution
```
After each task completes:
  1. Write result to Logs/scheduler_YYYY-MM-DD.log
  2. Update schedule.md (last_run, next_run, status)
  3. Update queue.md (remove completed, show next)
  4. IF fail_count >= 3 → mark task SUSPENDED, alert human
  5. IF task.type = ONCE → mark COMPLETED
```

---

## Scheduler Log Format

### Location
```
Common/AI_Employee_Vault/Logs/scheduler_YYYY-MM-DD.log
```

### Entry Format
```
[2026-02-16 14:00:01] [SCHEDULER] [INFO]  Checking schedule (6 active tasks)
[2026-02-16 14:00:01] [SCHEDULER] [INFO]  Due: TASK-003 (Process Inbox - HIGH)
[2026-02-16 14:00:02] [SCHEDULER] [START] TASK-003 → Process Inbox
[2026-02-16 14:02:15] [SCHEDULER] [DONE]  TASK-003 → Success (2m 13s) → 3 files processed
[2026-02-16 14:02:15] [SCHEDULER] [NEXT]  TASK-003 next run: 2026-02-16 15:00:00
```

### Error Entry
```
[2026-02-16 14:00:02] [SCHEDULER] [START] TASK-005 → Compress Logs
[2026-02-16 14:01:30] [SCHEDULER] [ERROR] TASK-005 → Failed: PermissionError on Logs/2026-01-15.log
[2026-02-16 14:01:30] [SCHEDULER] [RETRY] TASK-005 → Attempt 2/3 in 5 minutes
[2026-02-16 14:06:30] [SCHEDULER] [DONE]  TASK-005 → Success on retry 2
```

---

## Built-in Scheduled Tasks (Bronze Tier)

### Default Schedule on First Run

```
ID        | Task                  | Schedule          | Priority
----------|----------------------|-------------------|----------
SCH-001   | Process Inbox        | EVERY 60 min      | HIGH
SCH-002   | Update Dashboard     | EVERY 30 min      | MEDIUM
SCH-003   | Daily Cleanup        | DAILY at 00:00    | LOW
SCH-004   | Log Rotation         | DAILY at 23:55    | LOW
SCH-005   | Weekly Archive       | WEEKLY SUN 01:00  | LOW
SCH-006   | Monthly Summary      | MONTHLY 1st 02:00 | LOW
SCH-007   | Resource Check       | EVERY 5 min       | MEDIUM
SCH-008   | Missed Job Recovery  | ON STARTUP        | HIGH
```

---

## Task Status Reference

```
Status      | Meaning
------------|----------------------------------------------
ACTIVE      | Enabled, will run on schedule
RUNNING     | Currently executing
PAUSED      | Temporarily disabled (manual)
SUSPENDED   | Auto-disabled after 3 failures (needs review)
COMPLETED   | One-time task finished successfully
EXPIRED     | One-time task missed by >24 hours
CANCELLED   | Permanently disabled
```

### Status Transitions
```
ACTIVE → RUNNING       (when triggered by scheduler)
RUNNING → ACTIVE       (after successful completion)
RUNNING → SUSPENDED    (after 3 consecutive failures)
ACTIVE → PAUSED        (manual pause by human)
PAUSED → ACTIVE        (manual resume by human)
ACTIVE → COMPLETED     (one-time task done)
ACTIVE → EXPIRED       (one-time task missed >24h)
SUSPENDED → ACTIVE     (after human review + reset)
ANY → CANCELLED        (manual permanent disable)
```

---

## Human Control Commands

### In Company_Handbook.md or via Claude

```
Pause a task:
  "Pause TASK-003 until tomorrow"
  → Sets status = PAUSED, resumes at specified time

Resume a task:
  "Resume TASK-003"
  → Sets status = ACTIVE, calculates next_run from now

Run immediately:
  "Run TASK-005 now"
  → Adds to queue with HIGH priority, skips wait

Change schedule:
  "Change TASK-001 to run every 2 hours"
  → Updates interval, recalculates next_run

Disable permanently:
  "Cancel TASK-007"
  → Sets status = CANCELLED (never runs again)

Add new task:
  "Schedule: Run weekly report every Friday at 17:00"
  → Creates new entry in schedule.md
```

---

## Integration with Other Skills

### With Optimization Skill
```
scheduler → calls → optimization when:
  SCH-003 fires (daily cleanup)
  SCH-007 fires (resource check)
  Disk > 80% condition triggers
```

### With Memory Management Skill
```
scheduler → calls → memory-management when:
  SCH-005 fires (weekly archive)
  SCH-006 fires (monthly summary)
  Done/ folder > 500 files
```

### With Audit Skill
```
scheduler → reports to → audit:
  Every task start/stop/fail
  Missed jobs detected on startup
  Queue depth warnings
  Suspension events
```

### With Approval Handling Skill
```
scheduler → requests approval from → approval-handling when:
  Task touches sensitive data
  Task would delete files
  Task is HIGH cost operation
  Human override needed
```

---

## Best Practices

### DO
```
- Always log every scheduled task execution
- Calculate next_run immediately after each run
- Handle missed jobs on every startup
- Keep queue depth below 10 for responsiveness
- Use CONDITIONAL triggers for resource-based events
- Set realistic timeouts for each task
- Suspend tasks after 3 failures (don't loop forever)
```

### DON'T
```
- Run tasks in parallel on shared vault files
- Set interval below 5 minutes (too aggressive)
- Ignore SUSPENDED tasks (review and fix them)
- Schedule CRITICAL tasks too frequently
- Let queue depth exceed 20
- Skip logging for "quick" tasks (log everything)
- Hard-code task times without considering timezones
```

---

**Status**: Production Ready
**Priority**: HIGH (Backbone of autonomous operation)
**Default Check Interval**: 60 seconds
**Max Queue Depth**: 20 tasks
**Concurrent Tasks**: 1 (sequential execution)

*Good scheduling = Autonomous AI that works while you sleep*
