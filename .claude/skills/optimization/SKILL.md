# Optimization AI Skill

**Purpose**: Reduce resource consumption, limit background tasks, auto-clean files, and improve overall system performance
**Storage**: Lightweight markdown-based optimization rules
**Scope**: RAM, CPU, disk, background processes, vault cleanliness

---

## Core Functions

### 1. RAM Usage Reduction
Monitor and minimize memory footprint across all components

### 2. Background Task Limiting
Detect, throttle, and terminate unnecessary background processes

### 3. Auto-Clean Files
Remove temporary files, stale tasks, duplicate data, old logs

### 4. Performance Improvement
Tune intervals, batch operations, defer non-urgent work

---

## Resource Budget

### Bronze Tier Targets

```
Component          | Max RAM  | Max CPU | Check Interval
-------------------|----------|---------|---------------
File Watcher       | 50 MB    | 2%      | 60s (not 10s)
Claude Code        | 300 MB   | 30%     | On-demand
VS Code            | 150 MB   | 5%      | -
Python Scripts     | 30 MB    | 1%      | -
OS Reserved        | 2500 MB  | -       | -
TOTAL              | 3030 MB  | 38%     | -
Available Buffer   | 5000 MB  | 62%     | -
```

### Warning Thresholds

```
RAM:   >70% total = WARNING   |  >85% = CRITICAL → trigger cleanup
CPU:   >60% sustained = HIGH  |  >90% sustained = CRITICAL
Disk:  >80% vault = WARN      |  >95% = CRITICAL → aggressive clean
```

---

## RAM Optimization Rules

### Rule 1: Lazy Loading
```
NEVER load entire vault into memory
DO:   Read only the file currently needed
DO:   Close file handles after reading
DO:   Use streaming for large files (>1MB)
DONT: Load all Needs_Action tasks at startup
```

### Rule 2: Watcher Interval Tuning
```
Default interval:  30 seconds  (too aggressive)
Optimized:         60 seconds  (saves ~40% CPU cycles)
Low-activity mode: 120 seconds (when Inbox empty for >1 hour)
Burst mode:        10 seconds  (when files actively arriving)

Auto-switch logic:
  IF inbox_empty_for > 3600s → set interval = 120s
  IF new_files_in_last_hour  → set interval = 10s
  ELSE                       → set interval = 60s
```

### Rule 3: Log Buffer Management
```
Write logs:        Batched every 5 minutes (not per-event)
Log file size:     Max 5MB per file → rotate
Log retention:     Keep 7 days → delete older
Log level:         INFO in production (not DEBUG)

Exception: CRITICAL and ERROR → write immediately (no buffer)
```

### Rule 4: Processed Files Cache
```
Cache size:        Max 1000 entries (not unlimited)
Cache type:        Set of filenames only (not full paths)
Eviction policy:   LRU (Least Recently Used)
Persist cache:     Write to .processed_cache.txt on shutdown
Reload on start:   Read cache file if exists
```

---

## Background Task Limiting

### Allowed Background Tasks (Bronze)

```
ALLOWED:
  - filesystem_watcher.py    (1 instance max)
  - VS Code                  (1 instance)
  - Claude Code session       (1 instance max)

BLOCKED / NOT NEEDED:
  - Multiple watcher instances
  - Auto-update checks during work
  - Telemetry or analytics processes
  - Scheduled tasks during active session
```

### Duplicate Process Detection

```
On startup, check:
  1. Is another watcher already running?
     → Read .watcher.pid file
     → If PID alive → log "Already running" → EXIT
     → If PID dead → overwrite .watcher.pid → CONTINUE

  2. Is vault locked?
     → Check for .vault.lock file
     → If exists and fresh (<5 min) → wait 30s → retry
     → If exists and stale (>5 min) → remove lock → CONTINUE

PID file location: Bronze-Tier/.watcher.pid
Lock file location: Common/AI_Employee_Vault/.vault.lock
```

### Graceful Shutdown

```
On CTRL+C or SIGTERM:
  1. Stop accepting new files
  2. Finish current file processing
  3. Write log buffer to disk
  4. Save processed files cache
  5. Remove .watcher.pid
  6. Remove .vault.lock
  7. Exit cleanly

Timeout: If step 2 takes >30s → force exit anyway
```

---

## Auto-Clean Rules

### Clean Trigger Conditions

```
Trigger auto-clean when ANY of:
  - Vault disk usage > 80%
  - Log folder > 50MB
  - Done/ folder > 500 files
  - Temp files detected
  - Watcher running > 24 hours (daily maintenance)
```

### Clean Priority Order

```
Priority 1 (Always safe, do immediately):
  - *.tmp files anywhere in vault
  - *.bak files older than 7 days
  - Empty files (0 bytes)
  - Duplicate files (same content, different name)

Priority 2 (Safe after confirmation):
  - Log files older than 30 days
  - Done/ tasks older than 90 days → move to Archive/

Priority 3 (Requires human approval):
  - Done/ tasks older than 30 days → flag for review
  - Large files (>10MB) in vault
  - Anything in Needs_Action/ older than 7 days (stale)
```

### Log Rotation

```
Daily (midnight):
  - Rename: YYYY-MM-DD.log → YYYY-MM-DD.log.1
  - Create fresh: YYYY-MM-DD.log
  - Compress: .log.1 → .log.1.gz (if >1MB)
  - Delete: Files older than 30 days

Weekly (Sunday):
  - Scan all log files
  - Report: Total size, oldest file, line count
  - Auto-delete: Files older than 30 days
```

### Vault Clean Report

```
After each cleanup, write to Logs/cleanup_YYYY-MM-DD.log:

== Vault Cleanup Report ==
Date: 2026-02-16 03:00
Triggered By: Scheduled daily

Files Removed:
  - 12 temp files           → 45 KB freed
  - 8 log files (>30 days)  → 12 MB freed
  - 3 empty files           → 0 KB freed

Files Archived:
  - 45 tasks from Done/     → Archive/2026-01/

Space Summary:
  Before: 180 MB
  After:  167 MB
  Saved:  13 MB (7.2%)

Next cleanup: 2026-02-17 03:00
```

---

## Performance Improvement Patterns

### Pattern 1: Batch Processing

```
INSTEAD OF:
  For each file in Inbox:
    → Read file
    → Write task
    → Update dashboard
    → Write log
    (4 I/O ops per file)

DO:
  Collect all files in Inbox → list
  Process all files → results list
  Write all tasks at once
  Update dashboard once
  Write all logs at once
  (4 I/O ops total regardless of file count)

Benefit: 75% fewer disk writes for 4+ files
```

### Pattern 2: Dashboard Update Throttling

```
INSTEAD OF:
  Update dashboard after every single file

DO:
  Queue dashboard updates
  Flush queue every 60 seconds OR when queue > 10 items

Exception: Always update immediately for CRITICAL events
```

### Pattern 3: Index-First Search

```
INSTEAD OF:
  Scan all files when looking for a task

DO:
  1. Check Archive/index.md first (fast lookup)
  2. If not in index → scan Needs_Action/ (small folder)
  3. If not there → scan Done/ (medium folder)
  4. Only scan Archive/ as last resort

Build index after each processing run
```

### Pattern 4: Conditional File Reads

```
INSTEAD OF:
  Read every file to check if it needs processing

DO:
  Check filename + modified timestamp first
  IF already in processed_cache → SKIP (no disk read)
  IF timestamp < last_check_time → SKIP
  ELSE → READ file

Saves: ~90% of disk reads on repeat scans
```

---

## Optimization Modes

### Mode 1: Normal Operation
```
Use when: Active session, files arriving regularly

Settings:
  check_interval = 60s
  log_level      = INFO
  batch_size     = 10 files
  dashboard_freq = 60s
  cleanup_freq   = daily
```

### Mode 2: Low Activity (Idle)
```
Use when: Inbox empty for >1 hour

Auto-trigger: inbox_empty_duration > 3600s

Settings:
  check_interval = 120s    (2x slower)
  log_level      = WARNING (less verbose)
  batch_size     = 5
  dashboard_freq = 300s    (5 min)
  cleanup_freq   = daily

Revert to Normal: When new file detected in Inbox
```

### Mode 3: High Load (Burst)
```
Use when: Many files arriving quickly (>5 in last minute)

Auto-trigger: files_per_minute > 5

Settings:
  check_interval = 10s     (fast detection)
  log_level      = INFO
  batch_size     = 50      (larger batches)
  dashboard_freq = 30s
  cleanup_freq   = disabled (don't clean during burst)

Revert to Normal: When rate drops below 1 file/minute for 5min
```

### Mode 4: Emergency (Resource Critical)
```
Use when: RAM > 85% OR Disk > 95%

Auto-trigger: resource_check() detects threshold breach

Settings:
  check_interval = 300s    (5 min, minimal impact)
  log_level      = ERROR   (critical only)
  batch_size     = 1       (minimal memory)
  dashboard_freq = 600s
  cleanup_freq   = immediate (run now)

Actions taken:
  1. Run Priority 1 cleanup immediately
  2. Compress old log files
  3. Clear processed_cache if >1000 entries
  4. Alert human via Dashboard.md

Revert: When resources drop below 70%
```

---

## Resource Monitoring

### Metrics to Track

```
Every 5 minutes, record to Logs/metrics.log:

timestamp        | 2026-02-16 14:30:00
watcher_ram_mb   | 48
vault_disk_mb    | 165
log_folder_mb    | 12
inbox_count      | 0
needs_action_cnt | 3
done_count       | 47
current_mode     | idle
uptime_hours     | 6.5
files_processed  | 12
errors_today     | 0
```

### Auto-Alert Conditions

```
CRITICAL (write to Dashboard immediately):
  - RAM > 85%  → "ALERT: High memory usage, running emergency cleanup"
  - Disk > 95% → "ALERT: Disk nearly full, archiving old files"
  - Watcher crashed → "ALERT: Watcher stopped, restart needed"

WARNING (write to Dashboard, no panic):
  - RAM > 70%  → "WARN: Memory rising, consider closing other apps"
  - Disk > 80% → "WARN: Vault storage filling, auto-clean scheduled"
  - Errors > 10/day → "WARN: Multiple errors today, check logs"
```

---

## Optimization Checklist

### Before Starting Watcher
- [ ] Close unnecessary browser tabs (free ~500MB RAM)
- [ ] Verify only 1 watcher instance will run
- [ ] Check available disk space > 20% free
- [ ] Set check_interval to 60s (not default 30s)

### During Operation
- [ ] Monitor Dashboard for WARN/ALERT messages
- [ ] Verify log files not growing unbounded
- [ ] Check Done/ folder count (archive if >200 files)
- [ ] Confirm no duplicate watcher processes

### Weekly Maintenance
- [ ] Run cleanup: Delete logs older than 30 days
- [ ] Archive Done/ tasks older than 90 days
- [ ] Verify metrics.log showing healthy numbers
- [ ] Confirm all modes still switching correctly

### Monthly Optimization Review
- [ ] Compare RAM usage: this month vs last month
- [ ] Review error rate trends
- [ ] Adjust check_interval if activity patterns changed
- [ ] Compress old archives if disk > 60% used

---

## Integration with Other Skills

### With Memory Management Skill
```
optimization → triggers → memory-management when:
  Disk > 80%: Call archive_old_tasks(days=60)
  Disk > 90%: Call compress_archive(year=current-1)
  Duplicates found: Call find_duplicates() + merge
```

### With Audit Skill
```
optimization → reports to → audit when:
  Mode change: Log new mode + reason
  Cleanup run: Log files removed + space freed
  Resource alert: Log threshold breach + action taken
  Performance dip: Log metrics + diagnosis
```

### With Error Recovery Skill
```
optimization → notifies → error-recovery when:
  Watcher crash detected: Trigger restart sequence
  Disk full error: Trigger emergency cleanup first
  Memory error: Switch to emergency mode + cleanup
```

---

## Anti-Patterns to Avoid

```
NEVER:
  - Run multiple watcher instances simultaneously
  - Set check_interval below 10s (CPU killer)
  - Keep unlimited processed_files in memory
  - Write logs synchronously per-event (use buffer)
  - Load entire vault into memory at once
  - Skip cleanup when approaching disk limits
  - Ignore resource warnings (they escalate)
  - Delete files without logging the deletion

ALWAYS:
  - Use .watcher.pid to prevent duplicate instances
  - Batch I/O operations wherever possible
  - Log what was cleaned and how much space freed
  - Switch modes automatically based on conditions
  - Keep cleanup non-destructive (archive > delete)
  - Test in DRY_RUN before actual cleanup
```

---

## Quick Reference

```
Resource Issue        | Action
----------------------|----------------------------------------
RAM high (>70%)       | Switch to Idle mode, clear cache
RAM critical (>85%)   | Emergency mode + immediate cleanup
Disk high (>80%)      | Archive Done/ tasks, rotate logs
Disk critical (>95%)  | Aggressive cleanup + archive
CPU high (>60%)       | Increase check_interval to 120s+
Multiple watchers     | Kill extras, keep only 1
Watcher crashed       | Remove .pid, restart watcher
Log folder too big    | Delete logs older than 30 days
Done/ folder full     | Archive tasks older than 90 days
Temp files found      | Delete immediately (always safe)
```

---

**Status**: Production Ready
**Priority**: HIGH (Ensures long-term stability)
**RAM Target**: <50MB for watcher process
**Disk Target**: <250MB total vault (Bronze Tier)
**CPU Target**: <2% average (30% peaks during processing)

*Optimized AI = Fast response + Low cost + Long runtime*
