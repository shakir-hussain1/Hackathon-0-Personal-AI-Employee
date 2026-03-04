# Monitoring Skill

**Purpose**: Watch everything in real time — system health, file activity, resource usage, and external signals — and react before problems escalate
**Storage**: Markdown-based metrics files, watch lists, alert history
**Scope**: Process monitoring, file system events, resource thresholds, external API health, scheduled job tracking, anomaly detection

---

## Core Functions

### 1. Watch System Resources
Track RAM, CPU, disk — alert before limits are hit

### 2. Monitor File Activity
Detect new files, stuck files, unexpected changes

### 3. Track Process Health
Confirm watcher, scheduler, and workflows are alive

### 4. Monitor External Services
Check API health, token validity, sync status (Silver+)

### 5. Detect Anomalies
Flag anything that deviates from established baseline

### 6. Report Status
Maintain live metrics dashboard and historical trend data

---

## Monitoring Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MONITORING SKILL                      │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ Resource │  │  File    │  │ Process  │  │External│  │
│  │ Monitor  │  │ Monitor  │  │ Monitor  │  │Monitor │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘  │
│       │              │              │              │      │
│       └──────────────┴──────────────┴──────────────┘     │
│                            │                              │
│                     ┌──────▼──────┐                      │
│                     │  Aggregator │                      │
│                     └──────┬──────┘                      │
│                            │                              │
│          ┌─────────────────┼─────────────────┐           │
│          │                 │                 │           │
│    ┌─────▼────┐    ┌──────▼──────┐   ┌──────▼──────┐   │
│    │  Alert   │    │   Metrics   │   │  Dashboard  │   │
│    │ Dispatch │    │   Writer    │   │   Updater   │   │
│    └──────────┘    └─────────────┘   └─────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Monitor 1: Resource Monitor

### What to Watch
```
Metric          | Check Interval | Warning    | Critical   | Unit
----------------|----------------|------------|------------|------
RAM (total)     | 60s            | > 70%      | > 85%      | %
RAM (watcher)   | 60s            | > 40 MB    | > 50 MB    | MB
CPU (sustained) | 60s (avg 5min) | > 60%      | > 85%      | %
Disk (vault)    | 5 min          | > 75%      | > 90%      | %
Disk (logs)     | 30 min         | > 40 MB    | > 80 MB    | MB
Disk (free)     | 5 min          | < 20 MB    | < 10 MB    | MB
```

### Metric File Format
```
Location: Common/AI_Employee_Vault/Logs/metrics.md

# Live Metrics

**Updated**: 2026-02-16 14:30:00
**Check Interval**: 60s

## Resources
| Metric         | Current  | Warning  | Critical | Status  |
|----------------|----------|----------|----------|---------|
| RAM Total      | 62%      | 70%      | 85%      | GREEN   |
| RAM Watcher    | 38 MB    | 40 MB    | 50 MB    | GREEN   |
| CPU (5m avg)   | 12%      | 60%      | 85%      | GREEN   |
| Disk Vault     | 66%      | 75%      | 90%      | GREEN   |
| Disk Logs      | 12 MB    | 40 MB    | 80 MB    | GREEN   |
| Disk Free      | 85 MB    | <20 MB   | <10 MB   | GREEN   |

## Trend (last 6 readings)
RAM:   62% 61% 63% 62% 60% 59%  → STABLE
CPU:   12% 10% 15% 12% 11% 13%  → STABLE
Disk:  66% 66% 65% 66% 65% 64%  → STABLE
```

### Resource Alert Logic
```
On each check:
  1. Read current values
  2. Compare to thresholds
  3. IF value crosses WARNING for first time → send WARNING alert
  4. IF value stays in WARNING for 3+ checks → escalate to HIGH alert
  5. IF value crosses CRITICAL → send CRITICAL alert immediately
  6. IF value recovers → send RESOLVED notification (INFO)
  7. Write all readings to metrics.md
  8. Update Dashboard resource section

Hysteresis (prevent alert flapping):
  Do not re-alert on same threshold until:
  - CRITICAL: 30 minutes after last alert
  - WARNING:  2 hours after last alert
  - RESOLVED: Always send immediately
```

---

## Monitor 2: File Monitor

### What to Watch
```
Location          | Event to Detect          | Check Interval | Action
------------------|--------------------------|----------------|--------
Inbox/            | New file arrived         | 60s            | Create task
Inbox/            | File stuck > 2 hours     | 30 min         | Alert + auto-task
Needs_Action/     | File stuck > 24 hours    | 30 min         | Alert human
Needs_Action/     | File count > 50          | 15 min         | Alert (queue overflow)
Done/             | File count > 500         | 1 hour         | Suggest archive
Inbox/quarantine/ | Any file present         | 15 min         | Alert human (review)
Logs/             | Single log > 10 MB       | 30 min         | Alert + rotate
Plans/            | Schedule.md modified     | 5 min          | Reload schedule
Dashboard.md      | Not updated > 6 hours    | 30 min         | Force refresh
.vault.lock       | Exists > 10 minutes      | 5 min          | Stale lock alert
```

### File Event Log
```
Location: Common/AI_Employee_Vault/Logs/file_events.log

Format:
[2026-02-16 09:00:15] [FILE] NEW     Inbox/report_q1.pdf         size=2.3MB
[2026-02-16 09:00:16] [FILE] TASK    Needs_Action/FILE_014.md    created
[2026-02-16 09:15:42] [FILE] MOVED   Inbox/report_q1.pdf         → Done/
[2026-02-16 11:30:00] [FILE] STUCK   Inbox/invoice_scan.jpg      2h 15m old, no task
[2026-02-16 11:30:01] [FILE] ALERT   Stuck file detected         notified human
[2026-02-16 14:00:00] [FILE] CHANGED Plans/schedule.md           reload triggered
[2026-02-16 14:30:00] [FILE] LOCK    .vault.lock exists 12 min   stale → removed
```

### File Baseline
```
Establish baseline on first run, update weekly:

Expected file counts (Bronze normal operation):
  Inbox/         : 0-5 files    (alert if > 10)
  Needs_Action/  : 0-20 tasks   (alert if > 50)
  Done/          : 0-500 files  (suggest archive if > 200)
  Logs/          : 1-30 files   (alert if > 60)
  Quarantine/    : 0 files      (alert immediately if any)

Expected file arrival patterns:
  Weekday mornings 08:00-10:00  → typically HIGH activity
  Weekday afternoons 13:00-15:00→ typically MEDIUM activity
  Evenings and weekends         → typically LOW activity
  Unexpected high activity outside patterns → flag anomaly
```

---

## Monitor 3: Process Monitor

### What to Watch
```
Process              | Check Method              | Interval | Alert If
---------------------|---------------------------|----------|----------
filesystem_watcher   | .watcher.pid exists?      | 60s      | PID dead
                     | Last log < 3x interval?   | 60s      | No recent log
Scheduler            | Last run vs schedule      | 5 min    | Missed 2+ runs
Active workflows     | Run file status           | 5 min    | RUNNING > timeout
Pending handoffs     | Handoff file age          | 30 min   | > 4h no response
Approval requests    | Approval file status      | 30 min   | > 24h no response
```

### Process Health File
```
Location: Common/AI_Employee_Vault/Logs/health.md

# Process Health

**Updated**: 2026-02-16 14:30

| Process            | Status  | Last Seen           | PID    | Note              |
|--------------------|---------|---------------------|--------|-------------------|
| Filesystem Watcher | GREEN   | 2026-02-16 14:29    | 5102   | Running normally  |
| Scheduler          | GREEN   | 2026-02-16 14:00    | -      | Next: 15:00       |
| Active Workflows   | GREEN   | 2026-02-16 14:28    | -      | 1 active (WF-001) |
| Pending Handoffs   | YELLOW  | -                   | -      | HT-003 waiting 5h |
| Pending Approvals  | GREEN   | -                   | -      | None pending      |
```

### Process Recovery Trigger
```
IF process status = RED:
  → Immediately notify Self-Healing Skill
  → Self-Healing executes recovery playbook
  → Monitoring tracks recovery progress
  → Alert resolved when process returns to GREEN

IF process status = YELLOW:
  → Log warning
  → Schedule follow-up check in 15 minutes
  → If still YELLOW after 3 checks → escalate to ORANGE

IF process status = ORANGE:
  → Alert human (HIGH notification)
  → Continue monitoring
  → Escalate to RED if no improvement in 1 hour
```

---

## Monitor 4: External Service Monitor (Silver+)

### What to Watch
```
Service            | Check Method              | Interval | Alert If
-------------------|---------------------------|----------|----------
Gmail API          | Token valid?              | 15 min   | Token expired
Gmail API          | Quota remaining?          | 30 min   | < 10% quota
Google Calendar    | Token valid?              | 15 min   | Token expired
LinkedIn API       | Token valid?              | 1 hour   | Token expired
Odoo (local)       | HTTP 200 on health check  | 5 min    | No response
Cloud Storage      | Credentials valid?        | 1 hour   | Auth failure
Internet           | DNS resolution works      | 5 min    | No connectivity
```

### External Health File (Silver+)
```
Location: Common/AI_Employee_Vault/Logs/external_health.md

# External Services Health

**Updated**: 2026-02-16 14:30

| Service         | Status  | Last Check          | Token Expires    | Quota |
|-----------------|---------|---------------------|------------------|-------|
| Gmail API       | GREEN   | 2026-02-16 14:15    | 2026-03-01       | 87%   |
| Google Calendar | GREEN   | 2026-02-16 14:15    | 2026-03-01       | 95%   |
| LinkedIn        | GREY    | Never               | Not configured   | -     |
| Odoo            | GREY    | Never               | Not configured   | -     |
| Cloud Storage   | GREY    | Never               | Not configured   | -     |
| Internet        | GREEN   | 2026-02-16 14:30    | -                | -     |
```

---

## Anomaly Detection

### Baseline Metrics (Auto-Calculated)
```
Monitoring builds baseline from 7 days of data:

Baseline for file arrivals:
  Mon-Fri 08-10: avg 3.2 files/hour ± 2.1
  Mon-Fri 10-18: avg 1.8 files/hour ± 1.4
  Evenings/Weekend: avg 0.2 files/hour ± 0.3

Baseline for processing time:
  Document (PDF):     avg 95s ± 30s
  Data (CSV/XLSX):    avg 45s ± 15s
  Image:              avg 10s ± 5s
  Code:               avg 20s ± 10s

Baseline for error rate:
  Avg errors/day:     2.1 ± 1.8
  Error spike:        > 5 errors in 1 hour

Baseline for resource usage:
  RAM: avg 62% ± 8%
  CPU: avg 15% ± 12%
  Disk growth: avg +2 MB/day
```

### Anomaly Alert Conditions
```
Anomaly: File volume spike
  IF files_per_hour > baseline_mean + (3 × std_dev)
  → FLAG: Unusual file volume detected
  → Action: Switch to Burst mode, notify human

Anomaly: Processing time spike
  IF task_duration > baseline_mean + (2 × std_dev) for type
  → FLAG: Task taking longer than usual
  → Action: Log, check if system under load

Anomaly: Error rate spike
  IF errors_in_last_hour > 5 AND baseline_errors_per_hour < 2
  → FLAG: Error spike detected
  → Action: HIGH alert, check error types, notify human

Anomaly: Resource usage spike
  IF RAM > baseline_mean + (2 × std_dev) AND baseline_mean < 70%
  → FLAG: Unexpected memory growth
  → Action: Check for memory leak, switch optimization mode

Anomaly: Unusual file from known sender
  IF sender = known_entity AND file_type != their_usual_type
  → FLAG: Unexpected file type from known sender
  → Action: Log, increase priority, check with security skill

Anomaly: Activity at unusual time
  IF high_volume AND current_time = low_activity_period
  → FLAG: Unusual off-hours activity
  → Action: Log, review file sources, notify human
```

---

## Live Monitoring Dashboard Section

### Dashboard Format
```markdown
## System Monitor

**Updated**: 2026-02-16 14:30:00
**Overall Status**: 🟢 GREEN

### Resources
| Metric       | Now   | Trend  | Status |
|--------------|-------|--------|--------|
| RAM          | 62%   | STABLE | GREEN  |
| CPU          | 12%   | STABLE | GREEN  |
| Disk         | 66%   | STABLE | GREEN  |

### Processes
| Process         | Status | Uptime   |
|-----------------|--------|----------|
| Watcher         | ALIVE  | 6h 14m   |
| Scheduler       | ACTIVE | On time  |
| Workflows       | 1 RUNNING | WF-001 |

### File Activity (Last Hour)
| Location        | Count | Status  |
|-----------------|-------|---------|
| Inbox           | 0     | CLEAR   |
| Needs_Action    | 3     | OK      |
| Done (today)    | 12    | OK      |
| Quarantine      | 0     | CLEAR   |

### Anomalies
  None detected

### External Services
  File System: ACTIVE
  Gmail: ACTIVE (Silver)
  Others: Not configured
```

---

## Alert Routing

### Severity → Action Map
```
CRITICAL (RED):
  → Immediately notify Self-Healing Skill
  → CRITICAL notification (all channels)
  → Update Dashboard with red banner
  → Log to health.md and metrics.md
  → Start escalation timer (1 hour)

HIGH (ORANGE):
  → HIGH notification (Dashboard + Toast)
  → Update health.md
  → Schedule follow-up in 15 minutes
  → Log to file_events.log or health.md

WARNING (YELLOW):
  → WARNING notification (Dashboard + notifications.md)
  → Log metric reading
  → Monitor more frequently (2x interval)
  → Auto-resolve check after 3 readings

INFO (GREEN restored):
  → RESOLVED notification (INFO)
  → Update Dashboard status to GREEN
  → Log resolution time
  → Calculate: how long was issue active?
```

---

## Monitoring Metrics File

### Location
```
Common/AI_Employee_Vault/Logs/monitoring_summary.md
```

### Weekly Monitoring Summary Format
```markdown
# Monitoring Summary — Week 7, 2026

**Period**: 2026-02-10 → 2026-02-16
**Total Checks**: 10,080 (every 60s)
**Alerts Generated**: 18
**False Positives**: 2
**Incidents Escalated**: 1

---

## Alert Breakdown

| Level    | Count | Auto-resolved | Needed Human |
|----------|-------|---------------|--------------|
| CRITICAL | 1     | 1             | 0            |
| HIGH     | 4     | 3             | 1            |
| WARNING  | 11    | 11            | 0            |
| INFO     | 2     | 2             | 0            |

---

## Resource Trends This Week

| Day   | Avg RAM | Peak RAM | Avg CPU | Disk End |
|-------|---------|----------|---------|----------|
| Mon   | 61%     | 74%      | 13%     | 163 MB   |
| Tue   | 62%     | 78%      | 15%     | 166 MB   |
| Wed   | 63%     | 82%      | 14%     | 169 MB   |
| Thu   | 62%     | 71%      | 12%     | 171 MB   |
| Fri   | 64%     | 79%      | 16%     | 173 MB   |
| Sat   | 58%     | 63%      | 8%      | 173 MB   |
| Sun   | 57%     | 61%      | 7%      | 173 MB   |

---

## Top Anomalies Detected

1. Wed 14:30 — Disk hit 82% (WARNING → resolved after cleanup)
2. Thu 09:15 — Watcher PID died (CRITICAL → self-healed in 11s)
3. Fri 16:00 — Error spike: 7 errors in 30 min (HIGH → investigated)

---

## Monitoring Health (Self-Check)

- All checks ran on schedule: YES (100%)
- No monitoring gaps detected
- Baseline updated: YES (weekly)
- False positive rate: 11.1% (target < 10% — review thresholds)
```

---

## Monitoring Self-Check

### Monitor the Monitor
```
Every 6 hours, verify monitoring itself is healthy:

Check 1: Last metrics.md update < 2 minutes ago?
  IF stale → monitoring loop may have stopped → alert

Check 2: health.md last update < 10 minutes ago?
  IF stale → health monitor may have stopped → alert

Check 3: file_events.log has entries for today?
  IF empty → file monitor may have stopped → alert

Check 4: Did all scheduled checks run on time?
  Compare actual check times vs expected intervals
  IF gap > 2x interval → monitoring interrupted → alert

On failure: Alert via Dashboard directly (bypass normal notification flow)
This is the last-resort safety net.
```

---

## Integration with Other Skills

### With Self-Healing Skill
```
monitoring → triggers → self-healing when:
  Any process goes RED (immediate)
  Resource reaches CRITICAL threshold
  Stale lock file detected
  Monitoring detects vault tampering
```

### With Optimization Skill
```
monitoring → triggers → optimization when:
  Resource crosses WARNING threshold
  Disk approaching CRITICAL
  RAM trending upward over 3+ readings
  CPU sustained above WARNING for 5+ minutes
```

### With Notification Skill
```
monitoring → triggers → notification for:
  Every threshold crossing (WARNING/HIGH/CRITICAL)
  Anomaly detection events
  Resolved alerts (INFO)
  Monitoring self-check failures
```

### With Audit Skill
```
monitoring → feeds → audit:
  All metric readings (time-series data)
  Alert history (what was flagged, when, duration)
  Anomaly events for pattern analysis
  Weekly monitoring summary
```

### With Reporting Skill
```
reporting → pulls from → monitoring:
  Resource usage data for daily/weekly/monthly reports
  Alert counts and types
  Uptime statistics
  Anomaly list for exception reports
```

### With Security Skill
```
monitoring → notifies → security when:
  Vault file hash changes unexpectedly (tampering)
  Unusual file arrives from unknown source at odd hours
  External service auth failures (credential issue)
  Anomalous off-hours activity detected
```

### With Scheduler Skill
```
monitoring → watches → scheduler for:
  Missed scheduled runs
  Scheduler process alive
  Tasks stuck in RUNNING state
  Queue depth growing unexpectedly
```

### With Learning Skill
```
learning → uses → monitoring data:
  Baseline metrics (what is normal?)
  Anomaly frequency per type (what to watch more closely?)
  Alert false positive rate (improve thresholds)
  Resource trends for capacity planning
```

---

## Configuration

### Monitoring Settings
```
Location: Common/AI_Employee_Vault/Company_Handbook.md

monitor_resource_interval:      60        # seconds
monitor_file_interval:          60        # seconds
monitor_process_interval:       60        # seconds
monitor_external_interval:      900       # seconds (15 min)
monitor_anomaly_window:         3600      # seconds (1 hour)
monitor_baseline_days:          7         # days to build baseline

alert_dedup_critical_seconds:   1800      # 30 min
alert_dedup_high_seconds:       7200      # 2 hours
alert_dedup_warning_seconds:    21600     # 6 hours

resource_warn_ram_pct:          70
resource_crit_ram_pct:          85
resource_warn_disk_pct:         75
resource_crit_disk_pct:         90
resource_warn_cpu_pct:          60
resource_crit_cpu_pct:          85
```

---

## Best Practices

### DO
```
- Check everything on a regular interval (nothing unmonitored)
- Build a 7-day baseline before trusting anomaly alerts
- Use hysteresis (don't alert on single spike — confirm trend)
- Monitor the monitoring system itself
- Log every metric reading (enables trend analysis)
- Auto-resolve alerts when condition clears
- Tune thresholds based on false positive rate
- Keep metrics.md and health.md always up to date
```

### DON'T
```
- Alert on single-point spikes without confirmation
- Let monitoring intervals get too short (CPU killer)
- Ignore YELLOW status (it becomes RED if unattended)
- Skip the monitoring self-check (blind spot risk)
- Alert on the same condition more than once per dedup window
- Monitor external services more frequently than needed (quota risk)
- Store raw time-series data indefinitely (compress after 30 days)
- Trust a GREEN status if monitoring itself is stale
```

---

## Quick Reference: Metric → Response

```
Metric           | Warning Action          | Critical Action
-----------------|-------------------------|---------------------------
RAM > 70%        | Log + notify WARNING    | Trigger optimization
RAM > 85%        | -                       | Emergency mode + cleanup
CPU > 60% (5min) | Log + notify WARNING    | Investigate + slow checks
Disk > 75%       | Log + notify WARNING    | Schedule archive
Disk > 90%       | -                       | Emergency cleanup NOW
New Inbox file   | Create task             | -
File stuck 2h    | Auto-create task        | Notify human
Queue > 50       | Notify WARNING          | Pause new intake
Watcher dead     | Self-heal trigger       | CRITICAL alert
Stale lock > 10m | Remove lock + log       | If recurring → alert
Quarantine > 0   | Alert human to review   | -
Schedule missed  | Re-run job              | Alert if 3+ missed
External API down| Pause integration       | HIGH alert + human
Anomaly detected | Flag + increase priority| CRITICAL if repeated
```

---

**Status**: Production Ready
**Priority**: CRITICAL (Eyes and ears of the entire system)
**Check Intervals**: 60s (resources/files/processes), 15min (external)
**Anomaly Detection**: 7-day rolling baseline with standard deviation
**Self-Monitoring**: Every 6 hours (monitor the monitor)
**Alert Dedup**: 30min (CRITICAL), 2h (HIGH), 6h (WARNING)

*Good monitoring = Problems found in seconds, not hours — before users notice*
