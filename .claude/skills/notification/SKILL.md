# Notification Skill

**Purpose**: Alert humans at the right time, through the right channel, with the right message
**Storage**: Markdown-based notification log and templates
**Scope**: Dashboard alerts, file-based notifications, Windows toast, email drafts, escalation chains

---

## Core Functions

### 1. Send Notifications
Deliver alerts via available channels (file, dashboard, Windows, email draft)

### 2. Route by Severity
Match notification urgency to the appropriate channel

### 3. Deduplicate Alerts
Prevent notification spam for the same recurring issue

### 4. Escalation
Auto-escalate unacknowledged critical alerts

### 5. Notification Log
Record every notification sent for audit trail

---

## Notification Channels

### Channel 1: Dashboard Alert (Always Available)
```
How it works:
  Write alert banner to top of Dashboard.md

Best for:
  - All severity levels (fallback channel)
  - Persistent visibility while VS Code is open
  - Non-urgent status updates

Format in Dashboard.md:
  ## ALERTS
  > [CRITICAL] 2026-02-16 14:30 - Disk usage at 96%, emergency cleanup running
  > [WARNING]  2026-02-16 13:00 - 5 files stuck in Needs_Action > 2 days
  > [INFO]     2026-02-16 12:00 - Weekly archive completed, 45 tasks moved
```

### Channel 2: Notification File (Always Available)
```
How it works:
  Append to Common/AI_Employee_Vault/Logs/notifications.md

Best for:
  - Persistent record
  - Human review at own pace
  - INFO and WARNING levels

File Format:
  | Timestamp           | Level    | Title                     | Message                        | Ack |
  |---------------------|----------|---------------------------|--------------------------------|-----|
  | 2026-02-16 14:30    | CRITICAL | Disk Almost Full          | 96% used, cleaning now         | NO  |
  | 2026-02-16 13:00    | WARNING  | Stale Tasks Detected      | 5 tasks >2 days old            | YES |
  | 2026-02-16 12:00    | INFO     | Archive Complete          | 45 tasks moved to Archive/     | YES |
```

### Channel 3: Windows Toast Notification
```
How it works:
  Write a trigger file → watcher detects it → sends Windows toast

Trigger file location:
  Common/AI_Employee_Vault/Inbox/.notify_trigger.txt

Trigger file format:
  TITLE: Disk Almost Full
  BODY: Vault is 96% full. Emergency cleanup started.
  LEVEL: CRITICAL
  TIMESTAMP: 2026-02-16 14:30

Best for:
  - CRITICAL and HIGH alerts
  - When human may not be watching VS Code
  - Immediate attention needed

Limitation:
  - Requires watcher to be running
  - Windows 10/11 only
  - User must have notifications enabled
```

### Channel 4: Email Draft (Silver Tier+)
```
How it works:
  Create draft file → Silver tier email skill sends it

Draft file location:
  Common/AI_Employee_Vault/Plans/email_drafts/NOTIFY_YYYY-MM-DD_HH-MM.md

Draft format:
  TO: [configured recipient]
  SUBJECT: [CRITICAL] AI Employee Alert - Disk Almost Full
  BODY:
    Your AI Employee detected a critical issue:
    Issue: Disk usage at 96%
    Time: 2026-02-16 14:30
    Action taken: Emergency cleanup started
    Review needed: Check vault storage

Best for:
  - CRITICAL issues when human is away
  - Daily summaries
  - Weekly reports
  - Requires Silver tier email capability
```

---

## Severity Levels

### CRITICAL
```
Definition: Immediate action required, system at risk

Triggers:
  - Disk usage > 95%
  - RAM usage > 90%
  - Watcher process crashed
  - Vault file corruption detected
  - 10+ consecutive task failures
  - Security anomaly detected

Channels (ALL of these):
  1. Dashboard.md  → top banner, red
  2. notifications.md → immediate append
  3. Windows toast → popup
  4. Email draft   → create for sending (Silver+)

Dedup window: 30 minutes (re-alert if still unresolved)
Escalation: If unacknowledged in 1 hour → repeat on all channels
```

### HIGH
```
Definition: Significant issue, needs attention today

Triggers:
  - Disk usage > 80%
  - RAM usage > 75%
  - 5+ tasks stuck in Needs_Action > 48 hours
  - 3 consecutive task failures
  - Watcher interval missed 3+ times

Channels:
  1. Dashboard.md  → alert section
  2. notifications.md → append
  3. Windows toast → popup

Dedup window: 2 hours
Escalation: If unacknowledged in 4 hours → escalate to CRITICAL channel
```

### WARNING
```
Definition: Something needs attention, but not urgent

Triggers:
  - Disk usage > 70%
  - Queue depth > 15
  - Task failed once
  - Log file > 4MB
  - Done/ folder > 400 files

Channels:
  1. Dashboard.md → alert section
  2. notifications.md → append

Dedup window: 6 hours
Escalation: No auto-escalation (human reviews at own pace)
```

### INFO
```
Definition: Normal operational status update

Triggers:
  - Task completed successfully
  - Archive run finished
  - Cleanup completed with space saved
  - Watcher started/stopped
  - Daily summary ready

Channels:
  1. notifications.md → append only
  2. Dashboard.md → activity log section (not alert)

Dedup window: 24 hours (don't repeat same info message)
Escalation: None
```

---

## Notification Templates

### Template 1: Disk Space Alert
```
TITLE: Vault Storage {level} - {percent}% Used
BODY:
  Current usage: {used_mb} MB of {total_mb} MB ({percent}%)
  Threshold: {threshold}%
  Location: {vault_path}
  Recommended action: {action}
  Auto-action taken: {auto_action}

CRITICAL version:
  TITLE: URGENT: Vault Almost Full - 96% Used
  BODY:
    Your AI Employee vault is critically full.
    Used: 238 MB / 250 MB (96%)
    Emergency cleanup has been started automatically.
    Files being archived: Done/ tasks older than 30 days
    Expected to free: ~40 MB
    Please review: Common/AI_Employee_Vault/Dashboard.md
```

### Template 2: Task Failure Alert
```
TITLE: Task Failed - {task_name}
BODY:
  Task: {task_id} - {task_name}
  Failed at: {timestamp}
  Attempt: {attempt} of {max_attempts}
  Error: {error_message}
  Status: {RETRYING / SUSPENDED / NEEDS_REVIEW}
  Log: {log_file_path}

SUSPENDED version:
  TITLE: Task Suspended After 3 Failures - {task_name}
  BODY:
    Task {task_id} has been suspended after 3 consecutive failures.
    Last error: {error_message}
    Action needed: Review logs and manually re-enable task
    Log file: Logs/scheduler_YYYY-MM-DD.log
    To re-enable: Set status = ACTIVE in Plans/schedule.md
```

### Template 3: Stale Tasks Alert
```
TITLE: {count} Tasks Stuck in Queue
BODY:
  {count} task(s) have been waiting in Needs_Action for over {hours} hours:

  {task_list}
    - FILE_report_20260214.md (waiting 48h, HIGH priority)
    - FILE_invoice_20260213.md (waiting 72h, MEDIUM priority)

  Possible causes:
    - Watcher is running but Claude Code not processing
    - Task files are malformed
    - Processing skill encountered an error

  To fix: Run /process_inbox manually
```

### Template 4: Daily Summary
```
TITLE: AI Employee Daily Summary - {date}
BODY:
  Good morning! Here's what happened yesterday:

  Tasks Processed: {processed_count}
  Files Organized: {files_count}
  Errors Encountered: {error_count}
  Storage Used: {storage_mb} MB ({storage_pct}%)

  Top Activities:
    {activity_1}
    {activity_2}
    {activity_3}

  {alerts_section if any}
  {pending_review_section if any}

  Full log: Common/AI_Employee_Vault/Logs/{date}.log
  Dashboard: Common/AI_Employee_Vault/Dashboard.md
```

### Template 5: System Started
```
TITLE: AI Employee Online
BODY:
  AI Employee started successfully.
  Time: {timestamp}
  Mode: {Normal / Idle / Burst}
  Vault: {vault_path}
  Scheduled tasks: {task_count} active
  Missed jobs recovered: {missed_count}
  Ready to process files in: Inbox/
```

### Template 6: Weekly Report Ready
```
TITLE: Weekly Report Ready - Week of {date}
BODY:
  Your weekly AI Employee report is ready.
  Location: Common/AI_Employee_Vault/Plans/weekly_report_{date}.md

  Quick Stats:
    Files processed this week: {count}
    Tasks completed: {count}
    Errors: {count}
    Storage change: {+/- MB}

  Open in VS Code: Plans/weekly_report_{date}.md
```

---

## Deduplication Logic

### How It Works
```
Before sending any notification:

1. Check notifications.md for recent same-type alerts
2. Extract: notification_type + severity + source
3. Compare with last sent time
4. IF within dedup_window → SKIP (log as "suppressed")
5. IF outside dedup_window → SEND

Dedup windows by severity:
  CRITICAL → 30 minutes
  HIGH     → 2 hours
  WARNING  → 6 hours
  INFO     → 24 hours

Exception: CRITICAL alerts with different error messages
  → Always send even within dedup window
  (New error = new notification)
```

### Suppression Log
```
When notification is suppressed, log to notifications.md:

| 2026-02-16 14:45 | SUPPRESSED | Disk Alert | Duplicate within 30min window |
```

---

## Escalation Chain

### Escalation Timeline
```
CRITICAL alert sent at T+0:
  T+0:00  → Dashboard + notifications.md + Windows toast
  T+1:00  → IF not acknowledged: Repeat all channels
  T+2:00  → IF not acknowledged: Create email draft
  T+4:00  → IF not acknowledged: Add [ESCALATED] prefix to all
  T+8:00  → IF not acknowledged: Final notice + mark as OVERDUE

Acknowledgment = Human edits Dashboard.md or notifications.md
  (Changes "NO" to "YES" in Ack column)
```

### Escalation Levels
```
Level 1: Normal notification (all severity levels)
Level 2: Repeat notification (CRITICAL only, after 1 hour)
Level 3: Email draft created (CRITICAL only, after 2 hours)
Level 4: [ESCALATED] tag added (CRITICAL only, after 4 hours)
Level 5: OVERDUE status (CRITICAL only, after 8 hours)
```

---

## Notification Log File

### Location
```
Common/AI_Employee_Vault/Logs/notifications.md
```

### Full Format
```markdown
# Notification Log

**Updated**: 2026-02-16 14:30
**Total Sent Today**: 12
**Unacknowledged**: 2 (1 CRITICAL, 1 HIGH)

---

## Unacknowledged (Action Needed)

| Timestamp        | Level    | Title                  | Message Summary              | Sent Via              | Ack |
|------------------|----------|------------------------|------------------------------|-----------------------|-----|
| 2026-02-16 14:30 | CRITICAL | Disk Almost Full       | 96% used, cleanup running    | Dashboard+Toast       | NO  |
| 2026-02-16 13:00 | HIGH     | 5 Stale Tasks          | Tasks waiting >48h           | Dashboard             | NO  |

---

## Today's Log

| Timestamp        | Level    | Title                  | Message Summary              | Channels              | Ack |
|------------------|----------|------------------------|------------------------------|-----------------------|-----|
| 2026-02-16 14:30 | CRITICAL | Disk Almost Full       | 96% used, cleanup running    | Dashboard+Toast       | NO  |
| 2026-02-16 13:00 | HIGH     | 5 Stale Tasks          | Tasks waiting >48h           | Dashboard             | NO  |
| 2026-02-16 12:00 | INFO     | Archive Complete       | 45 tasks archived, 13MB free | Log only              | YES |
| 2026-02-16 08:03 | INFO     | System Started         | Watcher online, 8 tasks      | Dashboard+Log         | YES |
| 2026-02-16 07:45 | SUPPRESSED | Disk Warning         | Duplicate within 6h window   | -                     | -   |

---

## Yesterday (2026-02-15)
[collapsed - 8 notifications, all acknowledged]
```

---

## Dashboard Integration

### Alert Banner Format
```markdown
# AI Employee Dashboard

---

## ALERTS  ← This section at the very top

> **[CRITICAL]** `2026-02-16 14:30` Disk at 96% - Emergency cleanup running
> To acknowledge: Edit this file, change `NO` → `YES` in notifications.md

> **[HIGH]** `2026-02-16 13:00` 5 tasks stuck in queue over 48 hours
> Files: FILE_report_20260214.md, FILE_invoice_20260213.md (+3 more)

---

## System Status
...rest of dashboard...
```

### Clearing Alerts from Dashboard
```
Alert removed from Dashboard when:
  1. Human acknowledges (Ack = YES in notifications.md)
  2. Issue is resolved automatically (disk drops below threshold)
  3. Alert is older than 24 hours AND severity = INFO

CRITICAL alerts stay until manually acknowledged
HIGH alerts stay until resolved or acknowledged
```

---

## Configuration

### Notification Settings
```
Location: Common/AI_Employee_Vault/Company_Handbook.md

Settings section:
  notify_critical_channels: [dashboard, file, toast, email_draft]
  notify_high_channels:     [dashboard, file, toast]
  notify_warning_channels:  [dashboard, file]
  notify_info_channels:     [file]

  daily_summary_time:       08:00
  weekly_report_day:        FRIDAY
  weekly_report_time:       17:00

  dedup_critical_minutes:   30
  dedup_high_minutes:       120
  dedup_warning_minutes:    360
  dedup_info_minutes:       1440

  escalation_enabled:       true
  escalation_repeat_hours:  1
  escalation_email_hours:   2
```

---

## Integration with Other Skills

### With Audit Skill
```
notification → reads from → audit:
  Error counts for alert triggers
  Performance degradation for warnings
  Daily stats for summary notifications
```

### With Scheduler Skill
```
scheduler → triggers → notification for:
  Daily summary (DAILY at 08:00)
  Weekly report ready (WEEKLY FRIDAY 17:00)
  Missed jobs detected on startup
```

### With Optimization Skill
```
optimization → triggers → notification for:
  Resource threshold breaches (CRITICAL/HIGH)
  Cleanup completed (INFO)
  Mode changes (INFO)
```

### With Approval Handling Skill
```
notification → triggers → approval-handling for:
  Approval requests (sends notification to human)
  Approval expiring soon (WARNING 1h before expiry)
  Approval expired (HIGH alert)
```

---

## Best Practices

### DO
```
- Always log every notification (even suppressed ones)
- Use deduplication to prevent alert fatigue
- Keep notification messages clear and actionable
- Include "what happened + what was done + what human needs to do"
- Acknowledge resolved alerts promptly
- Use Dashboard as primary human interface
```

### DON'T
```
- Send INFO notifications to Windows toast (too noisy)
- Suppress CRITICAL alerts (always send)
- Write notifications without timestamps
- Use vague messages ("something went wrong")
- Send duplicate alerts within dedup window
- Leave unacknowledged CRITICAL alerts overnight
- Flood the notification log with redundant INFO messages
```

---

**Status**: Production Ready
**Priority**: HIGH (Human awareness layer)
**Channels**: Dashboard (always), File log (always), Toast (Windows), Email draft (Silver+)
**Dedup**: Enabled by default to prevent alert fatigue
**Escalation**: Automatic for unacknowledged CRITICAL alerts

*Good notifications = Human always informed, never overwhelmed*
