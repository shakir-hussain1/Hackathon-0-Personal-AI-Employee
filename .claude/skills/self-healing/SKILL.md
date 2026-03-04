# Self-Healing Skill

**Purpose**: Automatically detect, diagnose, and recover from failures without human intervention
**Storage**: Markdown-based health checks, recovery logs, incident records
**Scope**: Process crashes, file corruption, stuck tasks, resource exhaustion, broken state

---

## Core Functions

### 1. Health Monitoring
Continuously check system components for signs of failure

### 2. Failure Detection
Identify failures early — before they cascade

### 3. Auto-Diagnosis
Determine root cause before attempting recovery

### 4. Auto-Recovery
Execute the correct fix for each failure type

### 5. Escalation
Know when to stop trying and alert a human

---

## Health Check System

### Components to Monitor

```
Component              | Check Method                  | Interval
-----------------------|-------------------------------|----------
Watcher Process        | .watcher.pid alive?           | 60s
Vault Folder Structure | Required folders exist?       | 5 min
Dashboard.md           | File exists, readable?        | 5 min
Log System             | Last log entry < 10 min old?  | 10 min
Scheduler              | Last run < interval+5min?     | 5 min
Inbox Processing       | No file stuck > 2 hours?      | 30 min
Queue Depth            | Needs_Action < 50 files?      | 15 min
Disk Space             | Vault < 90% full?             | 5 min
File Locks             | No .lock files older than 10m?| 5 min
Log File Size          | No single log > 10 MB?        | 30 min
```

### Health Status Levels

```
GREEN  → All checks passing, system nominal
YELLOW → 1-2 checks failing, degraded but functional
ORANGE → 3+ checks failing, needs attention soon
RED    → Critical failure, immediate action required
```

### Health Check File

```
Location: Common/AI_Employee_Vault/Logs/health.md

Format:
# System Health

**Last Check**: 2026-02-16 14:30:00
**Overall Status**: GREEN

| Component         | Status | Last OK             | Issue           |
|-------------------|--------|---------------------|-----------------|
| Watcher Process   | GREEN  | 2026-02-16 14:30    | -               |
| Vault Structure   | GREEN  | 2026-02-16 14:30    | -               |
| Dashboard.md      | GREEN  | 2026-02-16 14:30    | -               |
| Log System        | GREEN  | 2026-02-16 14:28    | -               |
| Scheduler         | GREEN  | 2026-02-16 14:00    | -               |
| Inbox Processing  | YELLOW | 2026-02-16 12:30    | 1 file stuck 2h |
| Queue Depth       | GREEN  | 2026-02-16 14:30    | -               |
| Disk Space        | GREEN  | 2026-02-16 14:30    | 66% used        |
| File Locks        | GREEN  | 2026-02-16 14:30    | -               |
| Log File Size     | GREEN  | 2026-02-16 14:30    | -               |
```

---

## Failure Detection Rules

### Rule 1: Watcher Crash
```
Detection:
  .watcher.pid file exists BUT process not running
  OR .watcher.pid missing AND watcher should be active
  OR last log entry older than check_interval * 3

Confidence: HIGH if PID dead + log stale
Severity:   HIGH
```

### Rule 2: Stuck File in Inbox/Needs_Action
```
Detection:
  File in Inbox/ with modified time > 2 hours ago
  AND no corresponding task in Needs_Action/
  OR file in Needs_Action/ with modified time > 24 hours
  AND status still PENDING

Confidence: MEDIUM (file may be intentionally left)
Severity:   MEDIUM
```

### Rule 3: Vault Folder Missing
```
Detection:
  Required folder does not exist:
  - Inbox/, Needs_Action/, Done/, Logs/, Plans/

Confidence: HIGH (folder missing is always a problem)
Severity:   CRITICAL
```

### Rule 4: Dashboard Corruption
```
Detection:
  Dashboard.md missing
  OR Dashboard.md is 0 bytes
  OR Dashboard.md last modified > 6 hours ago (no updates)
  OR Dashboard.md contains malformed markdown

Confidence: HIGH
Severity:   MEDIUM
```

### Rule 5: Log System Failure
```
Detection:
  Logs/ folder missing
  OR today's log file not created
  OR last log entry timestamp > 30 minutes old
    (when watcher supposedly running)

Confidence: HIGH
Severity:   HIGH
```

### Rule 6: Stale File Lock
```
Detection:
  .vault.lock exists AND modified time > 10 minutes ago
  OR .watcher.pid exists AND process not alive
  OR any .lock file in vault older than 15 minutes

Confidence: HIGH (fresh locks should resolve in seconds)
Severity:   HIGH
```

### Rule 7: Queue Overflow
```
Detection:
  Needs_Action/ has > 50 files
  OR Done/ has > 1000 files
  OR Inbox/ has > 100 files unprocessed

Confidence: HIGH
Severity:   MEDIUM
```

### Rule 8: Disk Exhaustion
```
Detection:
  Vault disk usage > 90%
  OR less than 10 MB free
  OR single file > 50 MB in vault

Confidence: HIGH
Severity:   CRITICAL if > 95%, HIGH if 90-95%
```

### Rule 9: Corrupted Task File
```
Detection:
  Task file in Needs_Action/ is 0 bytes
  OR task file missing required header fields
  OR task file has invalid date format
  OR task file binary content (not text)

Confidence: MEDIUM
Severity:   LOW (skip and continue)
```

### Rule 10: Scheduler Missed Runs
```
Detection:
  Scheduled task next_run is in the past by > (interval * 2)
  AND no log entry showing it ran
  AND watcher was supposed to be running

Confidence: MEDIUM
Severity:   MEDIUM
```

---

## Recovery Playbooks

### Playbook 1: Watcher Crash Recovery
```
Trigger: Watcher process dead

Step 1 - Verify failure
  → Check .watcher.pid (dead process?)
  → Check last log entry timestamp
  → Confirm: watcher should be running

Step 2 - Clean up stale state
  → Delete .watcher.pid (stale)
  → Delete .vault.lock if exists (stale)
  → Log: "[RECOVERY] Watcher crash detected, cleaning state"

Step 3 - Identify cause
  → Read last 20 lines of today's log
  → IF MemoryError → switch to LOW_MEMORY mode before restart
  → IF PermissionError → check folder permissions
  → IF FileNotFoundError → verify vault paths exist

Step 4 - Restart
  → Write new .watcher.pid
  → Start watcher process
  → Wait 10 seconds
  → Verify: new log entry appeared

Step 5 - Verify recovery
  → Health check: watcher status = GREEN?
  → IF YES → log success, notify INFO
  → IF NO → attempt 2 more times, then escalate

Max attempts: 3
Escalate after: 3 failures
```

### Playbook 2: Stuck File Recovery
```
Trigger: File stuck in Inbox > 2 hours

Step 1 - Diagnose
  → Check if corresponding task exists in Needs_Action/
  → Check watcher logs for detection attempts
  → Check if file is locked by another process

Step 2 - Attempt resolution
  IF no task exists AND watcher running:
    → Manually create task file for stuck file
    → Log: "[RECOVERY] Created missing task for {filename}"

  IF file is locked:
    → Wait 15 minutes, retry
    → If still locked → alert human

  IF watcher not running:
    → Execute Watcher Crash Recovery (Playbook 1)

Step 3 - Verify
  → Task file now exists in Needs_Action/
  → Original file is processable
  → Log recovery action

Max wait time: 4 hours before escalating to human
```

### Playbook 3: Missing Vault Folder Recovery
```
Trigger: Required folder does not exist

Step 1 - Identify missing folders
  Required: Inbox/, Needs_Action/, Done/, Logs/, Plans/

Step 2 - Recreate immediately
  → Create missing folder
  → Create .gitkeep placeholder inside
  → Log: "[RECOVERY] Recreated missing folder: {folder}"

Step 3 - Investigate why it disappeared
  → Check git history if applicable
  → Check if user accidentally deleted it
  → Check disk errors

Step 4 - Notify
  → Send HIGH notification: "Vault folder was missing, recreated"
  → Human should verify no data was lost

Recovery time: < 30 seconds
Human action: Verify data integrity
```

### Playbook 4: Dashboard Recovery
```
Trigger: Dashboard.md missing, empty, or stale

Step 1 - Determine type of failure
  → Missing: Recreate from template
  → Empty (0 bytes): Recreate from template
  → Stale (>6h no update): Force dashboard refresh
  → Corrupted: Restore from last backup in Logs/

Step 2a - If missing or empty
  → Write Dashboard.md from template
  → Populate with current live data
  → Log: "[RECOVERY] Dashboard recreated from template"

Step 2b - If stale
  → Run update_dashboard skill
  → Force write new timestamp
  → Log: "[RECOVERY] Dashboard force-refreshed"

Step 2c - If corrupted
  → Check Logs/dashboard_backup_{date}.md
  → Restore last good backup
  → Run update_dashboard to refresh data
  → Log: "[RECOVERY] Dashboard restored from backup"

Step 3 - Prevention
  → Create daily backup: Logs/dashboard_backup_{date}.md
  → Backup trigger: Before every dashboard write

Recovery time: < 60 seconds
```

### Playbook 5: Stale Lock File Recovery
```
Trigger: .vault.lock or .watcher.pid older than 10 minutes

Step 1 - Verify lock is truly stale
  → IF process in PID file is alive → do NOT remove (not stale)
  → IF process dead AND lock > 10 min → stale confirmed

Step 2 - Safe removal
  → Log: "[RECOVERY] Removing stale lock: {lock_file}"
  → Delete stale .vault.lock
  → Delete stale .watcher.pid
  → Log: "[RECOVERY] Stale locks cleared"

Step 3 - Verify system can proceed
  → Attempt vault access (read Dashboard.md)
  → IF successful → recovery complete
  → IF still locked → escalate to human

Recovery time: < 10 seconds
Risk: LOW (stale locks are safe to remove)
```

### Playbook 6: Disk Exhaustion Recovery
```
Trigger: Disk usage > 90%

Step 1 - Immediate triage
  → Calculate: how much space needed vs available
  → Identify: top 5 largest folders/files

Step 2 - Emergency cleanup (safe operations only)
  → Delete: all *.tmp files
  → Delete: all *.bak files older than 24h
  → Compress: log files older than 7 days
  → Archive: Done/ tasks older than 30 days
  → Estimate: how much space freed

Step 3 - Check if resolved
  → IF usage dropped below 85% → log success, notify WARNING
  → IF usage still > 85% → continue to step 4

Step 4 - Aggressive cleanup
  → Archive: Done/ tasks older than 14 days
  → Delete: log files older than 14 days (keep summary)
  → Compress: Archive/ content

Step 5 - Final check
  → IF usage < 80% → notify: "Disk emergency resolved"
  → IF usage still > 90% → ESCALATE immediately

Max auto-cleanup: 2 rounds
Escalate if: Cannot get below 85% after cleanup
Human action: Review and delete large files manually
```

### Playbook 7: Corrupted Task File Recovery
```
Trigger: Task file in Needs_Action/ is invalid

Step 1 - Assess corruption type
  → 0 bytes: File is empty
  → Binary content: Not a text file
  → Missing headers: Incomplete task
  → Invalid dates: Formatting error

Step 2 - Attempt repair
  IF 0 bytes:
    → Check if original source file still in Inbox/
    → If yes → recreate task file from source
    → If no → log as unrecoverable, move to review/

  IF missing headers:
    → Extract what data is available
    → Fill in defaults for missing fields
    → Mark as: NEEDS_REVIEW

  IF binary/unreadable:
    → Move to Inbox/unreadable/ folder
    → Log: "[RECOVERY] Unreadable task moved to unreadable/"
    → Notify human

Step 3 - Continue with other tasks
  → Never let one bad file stop all processing
  → Skip and log, then move on

Recovery time: < 30 seconds per file
```

---

## Recovery Log Format

### Location
```
Common/AI_Employee_Vault/Logs/recovery_YYYY-MM-DD.log
```

### Entry Format
```
[2026-02-16 14:30:05] [RECOVERY] [DETECT]  Watcher crash detected (PID 4521 dead)
[2026-02-16 14:30:05] [RECOVERY] [DIAGNOSE] Last log: 14:18 (12 min ago), cause: unknown
[2026-02-16 14:30:06] [RECOVERY] [ACTION]  Cleaning stale .watcher.pid
[2026-02-16 14:30:06] [RECOVERY] [ACTION]  Starting watcher process
[2026-02-16 14:30:16] [RECOVERY] [VERIFY]  Watcher confirmed alive (PID 5102)
[2026-02-16 14:30:16] [RECOVERY] [SUCCESS] Watcher crash recovered in 11 seconds
[2026-02-16 14:30:16] [RECOVERY] [NOTIFY]  INFO notification sent to Dashboard
```

### Failed Recovery Entry
```
[2026-02-16 15:45:00] [RECOVERY] [DETECT]  Disk usage 97% (CRITICAL)
[2026-02-16 15:45:01] [RECOVERY] [ACTION]  Emergency cleanup round 1 — freed 8 MB
[2026-02-16 15:45:30] [RECOVERY] [ACTION]  Aggressive cleanup round 2 — freed 12 MB
[2026-02-16 15:45:35] [RECOVERY] [VERIFY]  Disk still at 91% — below target
[2026-02-16 15:45:35] [RECOVERY] [ESCALATE] Cannot resolve — alerting human
[2026-02-16 15:45:35] [RECOVERY] [NOTIFY]  CRITICAL notification sent — human action required
```

---

## Incident Record

### Location
```
Common/AI_Employee_Vault/Logs/incidents.md
```

### Format
```markdown
# Incident Log

## INC-2026-002 — Watcher Crash
**Date**: 2026-02-16 14:30
**Severity**: HIGH
**Duration**: 11 seconds
**Auto-resolved**: YES

**What happened**: Watcher process died (PID 4521)
**Root cause**: Unknown (no error in logs before crash)
**Recovery**: Cleaned PID file, restarted watcher
**Prevention**: Added crash detection to health monitor
**Status**: RESOLVED

---

## INC-2026-001 — Disk Exhaustion
**Date**: 2026-02-14 09:15
**Severity**: CRITICAL
**Duration**: 4 minutes
**Auto-resolved**: YES (partial — human verified)

**What happened**: Vault disk reached 96%
**Root cause**: 47 large PDFs dropped in 2 hours
**Recovery**: Emergency cleanup freed 76 MB
**Prevention**: Lowered archive trigger from 90 to 60 days
**Status**: RESOLVED
```

---

## Escalation Decision Tree

```
Failure detected
      │
      ▼
Is this a known failure type? ──NO──→ Log as UNKNOWN, alert human
      │
     YES
      ▼
Have we tried recovering already?
  NO  → Execute recovery playbook
  YES → How many attempts?
          < 3  → Retry playbook
          >= 3 → ESCALATE
      │
      ▼
Did recovery succeed?
  YES → Log success, send INFO notification, done
  NO  → Increment attempt counter
         IF attempts >= 3 → ESCALATE

ESCALATE:
  1. Write to incidents.md (OPEN)
  2. Send CRITICAL notification (all channels)
  3. Suspend automated recovery for this component
  4. Wait for human acknowledgment
  5. After human ACK → resume monitoring
```

---

## Self-Healing Limits

### What Self-Healing CAN Fix Automatically
```
Watcher crashed                    → Restart it
Stale lock files                   → Delete them
Missing vault folders              → Recreate them
Dashboard missing/stale            → Recreate/refresh it
Stuck files in Inbox               → Create task manually
Corrupted task files (recoverable) → Repair or skip
Disk too full                      → Run cleanup
Missed scheduled tasks             → Re-run them
Log rotation missed                → Run it now
```

### What Self-Healing CANNOT Fix (Escalate to Human)
```
Disk full even after cleanup       → Need human to delete data
Watcher keeps crashing (3+ times)  → Code bug, needs developer
Vault folder permissions changed   → System admin needed
File corruption (binary in vault)  → Human must investigate
Approval workflow stuck            → Human decision required
Unknown error type                 → Human diagnosis needed
Data loss suspected                → Human must verify
Security anomaly detected          → Human must review
```

---

## Recovery State Machine

```
States:
  MONITORING   → Normal, health checks running
  DETECTING    → Anomaly found, verifying
  DIAGNOSING   → Root cause analysis running
  RECOVERING   → Executing playbook
  VERIFYING    → Checking if fix worked
  RECOVERED    → Back to normal
  ESCALATED    → Human needed, auto-recovery suspended

Transitions:
  MONITORING  → DETECTING   : health check fails
  DETECTING   → DIAGNOSING  : failure confirmed
  DETECTING   → MONITORING  : false alarm
  DIAGNOSING  → RECOVERING  : cause identified
  DIAGNOSING  → ESCALATED   : cause unknown after 60s
  RECOVERING  → VERIFYING   : playbook executed
  VERIFYING   → RECOVERED   : all checks green
  VERIFYING   → RECOVERING  : still failing (retry)
  RECOVERING  → ESCALATED   : 3 attempts failed
  ESCALATED   → MONITORING  : human ACK + issue resolved
  RECOVERED   → MONITORING  : resume normal monitoring
```

---

## Integration with Other Skills

### With Optimization Skill
```
self-healing → calls → optimization when:
  Disk > 90% → trigger emergency cleanup
  RAM > 85% → switch to emergency mode
  Recovery freed space → report to optimization metrics
```

### With Notification Skill
```
self-healing → triggers → notification for:
  Every recovery attempt (INFO or higher)
  Successful auto-recovery (INFO)
  Failed recovery requiring escalation (CRITICAL)
  New incident opened (HIGH)
```

### With Audit Skill
```
self-healing → reports to → audit:
  All recovery events (timestamped)
  MTTR (mean time to recover) per failure type
  Failure frequency trends
  Unresolved incidents
```

### With Error Recovery Skill
```
self-healing → uses → error-recovery for:
  Retry logic with backoff during recovery
  Circuit breaker if component keeps failing
  Checkpoint/resume for long recovery operations
```

### With Scheduler Skill
```
self-healing → tells → scheduler:
  Suspend tasks for crashed components
  Re-enable tasks after successful recovery
  Reschedule missed jobs post-recovery
```

---

## Best Practices

### DO
```
- Always diagnose before acting (don't guess)
- Log every recovery step in detail
- Verify recovery worked before marking resolved
- Respect the 3-attempt limit before escalating
- Keep recovery playbooks simple and safe
- Back up before any destructive recovery action
- Record every incident for pattern analysis
- Resume monitoring immediately after recovery
```

### DON'T
```
- Delete files without backing them up first
- Retry the same failed action indefinitely
- Auto-recover from security anomalies (always escalate)
- Ignore unknown failure types (always log + escalate)
- Run recovery during active burst mode (wait for idle)
- Suppress notifications during recovery attempts
- Assume recovery worked without verification
- Let one failure block recovery of other components
```

---

## Quick Reference: Failure → Playbook

```
Failure Type              | Playbook   | Auto-fix? | Escalate After
--------------------------|------------|-----------|----------------
Watcher crash             | PB-1       | YES       | 3 attempts
Stuck file in Inbox       | PB-2       | YES       | 4 hours
Missing vault folder      | PB-3       | YES       | Never (safe)
Dashboard missing/stale   | PB-4       | YES       | 3 attempts
Stale lock file           | PB-5       | YES       | 1 attempt
Disk exhaustion           | PB-6       | YES       | 2 rounds
Corrupted task file       | PB-7       | PARTIAL   | If unreadable
Unknown failure           | NONE       | NO        | Immediately
Security anomaly          | NONE       | NO        | Immediately
Data loss suspected       | NONE       | NO        | Immediately
```

---

**Status**: Production Ready
**Priority**: CRITICAL (Ensures system stays alive autonomously)
**Health Check Interval**: 60 seconds
**Max Auto-Recovery Attempts**: 3 per failure
**Escalation**: After 3 failed attempts or unknown failure type
**Goal**: Zero unplanned downtime, zero human intervention for known failures

*Good self-healing = AI Employee that fixes itself before anyone notices*
