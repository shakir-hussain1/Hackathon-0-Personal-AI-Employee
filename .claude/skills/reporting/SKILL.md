# Reporting Skill

**Purpose**: Generate clear, structured reports from vault data for human review
**Storage**: Markdown-based reports saved in Plans/ folder
**Scope**: Daily, weekly, monthly reports, performance summaries, task digests, exception reports

---

## Core Functions

### 1. Daily Report
Summarize what happened today — tasks, files, errors, stats

### 2. Weekly Report
Trends over 7 days — productivity, patterns, highlights

### 3. Monthly Report
Big picture — totals, averages, growth, recommendations

### 4. Exception Report
What went wrong — failures, errors, anomalies, stuck items

### 5. On-Demand Report
Generate any report instantly when human requests it

---

## Report File Locations

```
Common/AI_Employee_Vault/Plans/
├── reports/
│   ├── daily/
│   │   ├── report_2026-02-16.md
│   │   ├── report_2026-02-15.md
│   │   └── ...
│   ├── weekly/
│   │   ├── report_week_2026-W07.md
│   │   ├── report_week_2026-W06.md
│   │   └── ...
│   ├── monthly/
│   │   ├── report_2026-02.md
│   │   ├── report_2026-01.md
│   │   └── ...
│   └── exceptions/
│       ├── exception_2026-02-16.md
│       └── ...
```

---

## Daily Report

### Trigger
```
Schedule:  DAILY at 08:00 (generated for previous day)
On-demand: "Generate daily report"
Auto:      After processing 10+ files in a single session
```

### Template
```markdown
# Daily Report — 2026-02-16

**Generated**: 2026-02-16 08:00
**Period**: 2026-02-15 00:00 → 2026-02-15 23:59
**Status**: NORMAL | WARNING | CRITICAL

---

## Executive Summary

| Metric                | Value   | vs Yesterday | Status |
|-----------------------|---------|--------------|--------|
| Files Processed       | 12      | +3           | GOOD   |
| Tasks Completed       | 9       | +1           | GOOD   |
| Tasks Pending         | 3       | -2           | GOOD   |
| Errors Encountered    | 1       | -2           | GOOD   |
| Storage Used          | 165 MB  | +2 MB        | OK     |
| Watcher Uptime        | 23h 45m | -15m         | OK     |

**Overall Health**: GOOD

---

## Files Processed

### By Category
| Category   | Count | Files |
|------------|-------|-------|
| Documents  | 5     | report_q1.pdf, notes_feb.docx, ... |
| Data       | 3     | sales_data.csv, metrics.xlsx, ... |
| Images     | 2     | screenshot_001.png, diagram.jpg |
| Code       | 2     | update.py, config.json |

### By Priority
| Priority | Count | Processed | Pending |
|----------|-------|-----------|---------|
| HIGH     | 4     | 4         | 0       |
| MEDIUM   | 6     | 4         | 2       |
| LOW      | 2     | 1         | 1       |

---

## Activity Timeline

| Time  | Event                                      | Result  |
|-------|--------------------------------------------|---------|
| 00:01 | Daily cleanup ran                          | OK      |
| 08:03 | Watcher started                            | OK      |
| 09:15 | 3 files dropped in Inbox                   | Queued  |
| 09:17 | Processed: report_q1.pdf                   | Done    |
| 09:18 | Processed: notes_feb.docx                  | Done    |
| 09:18 | Processed: sales_data.csv                  | Done    |
| 11:30 | 5 more files arrived                       | Queued  |
| 11:35 | ERROR: invoice_scan.jpg — unreadable file  | Failed  |
| 11:36 | Processed: metrics.xlsx                    | Done    |
| 14:00 | Inbox check — 0 new files                  | Clear   |
| 23:55 | Log rotation ran                           | OK      |

---

## Errors & Issues

### Errors Today: 1

| Time  | Task ID  | Error                         | Action Taken        | Resolved |
|-------|----------|-------------------------------|---------------------|----------|
| 11:35 | FILE-034 | invoice_scan.jpg unreadable   | Moved to review/    | PENDING  |

### Pending Review
- `Inbox/invoice_scan.jpg` → Cannot process, needs human review

---

## Storage Report

| Location       | Size   | Change  | Status |
|----------------|--------|---------|--------|
| Inbox/         | 0 MB   | -8 MB   | Clear  |
| Needs_Action/  | 1 MB   | -3 MB   | OK     |
| Done/          | 145 MB | +11 MB  | OK     |
| Logs/          | 12 MB  | +1 MB   | OK     |
| Archive/       | 7 MB   | 0 MB    | OK     |
| **TOTAL**      | **165 MB** | **+2 MB** | **OK** |

---

## Scheduled Tasks Summary

| Task             | Scheduled  | Ran  | Duration | Result |
|------------------|------------|------|----------|--------|
| Daily Cleanup    | 00:00      | 00:01| 45s      | OK     |
| Process Inbox    | Every 60m  | 12x  | avg 2m   | OK     |
| Update Dashboard | Every 30m  | 24x  | avg 15s  | OK     |
| Log Rotation     | 23:55      | 23:55| 8s       | OK     |

---

## Recommendations

1. `invoice_scan.jpg` needs manual review — file appears corrupted
2. Done/ folder at 145 MB — consider archiving tasks >60 days old (saves ~40 MB)
3. All other systems nominal

---

**Next Report**: 2026-02-17 08:00
**Full Logs**: Logs/2026-02-15.log
```

---

## Weekly Report

### Trigger
```
Schedule:  WEEKLY on FRIDAY at 17:00
On-demand: "Generate weekly report"
Coverage:  Monday 00:00 → Sunday 23:59 of current week
```

### Template
```markdown
# Weekly Report — Week 7, 2026 (Feb 10–16)

**Generated**: 2026-02-16 17:00
**Period**: 2026-02-10 → 2026-02-16
**Week Number**: W07

---

## Week at a Glance

| Metric              | This Week | Last Week | Change  |
|---------------------|-----------|-----------|---------|
| Files Processed     | 67        | 54        | +24%    |
| Tasks Completed     | 58        | 49        | +18%    |
| Errors              | 5         | 8         | -38%    |
| Avg Daily Files     | 9.6       | 7.7       | +25%    |
| Storage Growth      | +14 MB    | +9 MB     | +56%    |
| Watcher Uptime      | 98.2%     | 96.1%     | +2.1%   |

**Week Summary**: Productive week. Higher volume, fewer errors.

---

## Daily Breakdown

| Day       | Files | Tasks | Errors | Storage |
|-----------|-------|-------|--------|---------|
| Monday    | 8     | 7     | 1      | +2 MB   |
| Tuesday   | 12    | 10    | 0      | +3 MB   |
| Wednesday | 15    | 13    | 2      | +4 MB   |
| Thursday  | 9     | 8     | 1      | +2 MB   |
| Friday    | 14    | 12    | 1      | +2 MB   |
| Saturday  | 5     | 4     | 0      | +1 MB   |
| Sunday    | 4     | 4     | 0      | 0 MB    |
| **TOTAL** | **67**| **58**| **5**  | **+14 MB** |

---

## File Categories This Week

| Category   | Count | % of Total | Trend     |
|------------|-------|------------|-----------|
| Documents  | 28    | 42%        | Stable    |
| Data/CSV   | 18    | 27%        | Up +30%   |
| Images     | 11    | 16%        | Stable    |
| Code       | 7     | 10%        | Up +40%   |
| Other      | 3     | 4%         | Down -50% |

---

## Top Issues This Week

| Date     | Issue                         | Status   |
|----------|-------------------------------|----------|
| Feb 12   | invoice_scan.jpg unreadable   | PENDING  |
| Feb 14   | Disk hit 75% — warning issued | RESOLVED |
| Feb 15   | 2 tasks delayed >24h          | RESOLVED |

---

## Performance Trends

### Files Per Day (7-day chart — ASCII)
```
Mon  ████████ 8
Tue  ████████████ 12
Wed  ███████████████ 15
Thu  █████████ 9
Fri  ██████████████ 14
Sat  █████ 5
Sun  ████ 4
```

### Error Rate (lower is better)
```
Mon  █ 1
Tue    0
Wed  ██ 2
Thu  █ 1
Fri  █ 1
Sat    0
Sun    0
```

---

## Storage Trend

| Date   | Total   | Change |
|--------|---------|--------|
| Feb 10 | 151 MB  | base   |
| Feb 11 | 153 MB  | +2 MB  |
| Feb 12 | 156 MB  | +3 MB  |
| Feb 13 | 160 MB  | +4 MB  |
| Feb 14 | 162 MB  | +2 MB  |
| Feb 15 | 164 MB  | +2 MB  |
| Feb 16 | 165 MB  | +1 MB  |

**Projection**: At current rate (+2 MB/day), vault will reach 200 MB in ~17 days
**Recommendation**: Schedule archival to stay under 200 MB Bronze limit

---

## Recommendations for Next Week

1. **Review pending item**: invoice_scan.jpg still unread
2. **Plan archival**: Done/ has 187 files — archive tasks >60 days old
3. **Storage watch**: Growing at +2 MB/day — run monthly archive soon
4. **No watcher issues**: Uptime 98.2% — stable operation

---

**Next Report**: 2026-02-20 (Week 8)
**Daily Reports**: Plans/reports/daily/
```

---

## Monthly Report

### Trigger
```
Schedule:  MONTHLY on 1st at 06:00 (for previous month)
On-demand: "Generate monthly report for February"
Coverage:  1st → last day of specified month
```

### Template
```markdown
# Monthly Report — February 2026

**Generated**: 2026-03-01 06:00
**Period**: 2026-02-01 → 2026-02-28
**Month**: February 2026

---

## Month Summary

| Metric              | February | January | Change  |
|---------------------|----------|---------|---------|
| Files Processed     | 284      | 231     | +23%    |
| Tasks Completed     | 261      | 215     | +21%    |
| Total Errors        | 18       | 25      | -28%    |
| Error Rate          | 6.3%     | 10.8%   | Improved|
| Storage Start       | 140 MB   | 112 MB  | -       |
| Storage End         | 185 MB   | 140 MB  | +45 MB  |
| Avg Files/Day       | 10.1     | 7.5     | +35%    |
| Watcher Uptime      | 97.8%    | 95.2%   | +2.6%   |

---

## Weekly Breakdown

| Week | Files | Tasks | Errors | Storage Added |
|------|-------|-------|--------|---------------|
| W05  | 62    | 57    | 6      | +9 MB         |
| W06  | 71    | 65    | 5      | +11 MB        |
| W07  | 67    | 58    | 5      | +14 MB        |
| W08  | 84    | 81    | 2      | +11 MB        |

---

## Top File Types

| Extension | Count | % | Notes              |
|-----------|-------|---|--------------------|
| .pdf      | 89    | 31% | Increased sharply |
| .csv      | 76    | 27% | Data uploads      |
| .docx     | 55    | 19% | Meeting notes     |
| .png/.jpg | 38    | 13% | Screenshots       |
| .py/.json | 26    | 9%  | Code reviews      |

---

## Resolved vs Pending

| Status         | Count | Notes                    |
|----------------|-------|--------------------------|
| Completed      | 261   | 91.9% completion rate    |
| Archived       | 45    | Moved to Archive/2026/02 |
| Still Pending  | 3     | Needs human review       |
| Errors/Failed  | 18    | 16 resolved, 2 open      |

---

## Storage Analysis

**Start of month**: 140 MB
**End of month**: 185 MB
**Growth**: +45 MB (+32%)
**Bronze limit**: 250 MB
**Headroom remaining**: 65 MB (~1.5 months at current rate)

**Action Required**: Plan storage strategy before April

---

## System Health

| Component      | Uptime  | Incidents | Status  |
|----------------|---------|-----------|---------|
| File Watcher   | 97.8%   | 2 crashes | Good    |
| Scheduler      | 100%    | 0         | Excellent|
| Vault Integrity| 100%    | 0         | Excellent|
| Log System     | 100%    | 0         | Excellent|

---

## Monthly Recommendations

1. **Storage**: At +45 MB/month growth, will hit Bronze limit in ~1.5 months
   - Action: Run archive now, move Done/ tasks >60 days to Archive/
   - Expected savings: ~50 MB

2. **Watcher crashes**: 2 unplanned restarts in February
   - Action: Review base_watcher.py error handling
   - Consider: Add auto-restart on crash

3. **Error rate improvement**: 10.8% → 6.3% — good trend, continue monitoring

4. **Productivity**: +23% file volume with -28% errors — system improving

---

**Archive Created**: Archive/2026/02/
**Next Report**: 2026-04-01 (March report)
```

---

## Exception Report

### Trigger
```
Auto:      When errors > 5 in one day
Auto:      When a CRITICAL alert is raised
Auto:      When task is SUSPENDED after 3 failures
On-demand: "Generate exception report"
```

### Template
```markdown
# Exception Report — 2026-02-16

**Generated**: 2026-02-16 14:35
**Trigger**: CRITICAL alert — disk usage 96%
**Severity**: CRITICAL

---

## Issue Summary

**Primary Issue**: Vault disk usage reached 96% (240 MB / 250 MB)
**Detected at**: 2026-02-16 14:30
**Auto-action**: Emergency cleanup started
**Status**: IN PROGRESS

---

## Root Cause Analysis

| Factor               | Finding                              |
|----------------------|--------------------------------------|
| Trigger              | 47 large PDF files added in 2 hours  |
| Contributing factor  | Monthly archive not run since Jan    |
| Done/ folder size    | 178 MB (97 files, oldest: 95 days)   |
| Log folder size      | 32 MB (rotation skipped Feb 10-14)   |

---

## Actions Taken Automatically

| Time  | Action                                  | Result         |
|-------|-----------------------------------------|----------------|
| 14:30 | Emergency cleanup triggered             | Started        |
| 14:31 | Deleted 12 temp files                   | Freed 3 MB     |
| 14:32 | Compressed logs older than 14 days      | Freed 18 MB    |
| 14:33 | Archived Done/ tasks older than 60 days | Freed 55 MB    |
| 14:34 | Vault now at 164 MB (66%)               | RESOLVED       |

---

## Actions Required from Human

- [ ] Review why log rotation skipped Feb 10-14
- [ ] Confirm archived tasks in Archive/2026/02/ look correct
- [ ] Consider upgrading to Silver tier storage if volume continues growing

---

## Prevention Recommendations

1. Lower archive trigger: 60 days → 45 days
2. Enforce log rotation daily without exception
3. Set WARNING threshold at 70% (currently 80%)
4. Review Done/ folder weekly not monthly

---

**Issue Resolved**: YES (auto-cleanup successful)
**Follow-up needed**: YES (see actions above)
**Related logs**: Logs/2026-02-16.log, Logs/cleanup_2026-02-16.log
```

---

## Report Data Sources

### Where Each Report Gets Its Data

```
Metric               | Source File
---------------------|------------------------------------------
Files processed      | Logs/YYYY-MM-DD.log (parse [PROCESSED])
Task counts          | Needs_Action/ + Done/ file count
Error count          | Logs/YYYY-MM-DD.log (parse [ERROR])
Storage sizes        | Vault folder sizes (check each folder)
Watcher uptime       | Logs/scheduler_YYYY-MM-DD.log
Scheduled tasks      | Plans/schedule.md
Notifications        | Logs/notifications.md
Activity timeline    | Logs/YYYY-MM-DD.log (chronological)
Weekly trends        | Aggregate 7x daily logs
Monthly totals       | Aggregate 4x weekly or 28-31x daily
```

---

## Report Generation Steps

### For Any Report Type

```
Step 1: Collect raw data
  - Read relevant log files
  - Count files in each vault folder
  - Parse task statuses from Needs_Action/ and Done/
  - Check notifications.md for alerts

Step 2: Calculate metrics
  - Totals, averages, percentages
  - Compare with previous period
  - Calculate trends (up/down/stable)
  - Identify anomalies

Step 3: Assess health
  - Green: All metrics within normal range
  - Yellow: 1-2 metrics outside normal
  - Red: Critical metrics breached

Step 4: Write recommendations
  - Based on trends and anomalies
  - Specific and actionable
  - Prioritized (most important first)

Step 5: Save report
  - Write to Plans/reports/{type}/report_{date}.md
  - Update Dashboard with report link
  - Send notification (INFO level)
```

---

## On-Demand Report Commands

### Human Requests

```
"Generate daily report"
  → Creates report for today (or yesterday if <08:00)
  → Saves to Plans/reports/daily/report_{date}.md

"Generate weekly report"
  → Creates report for current week (Mon-today)
  → Saves to Plans/reports/weekly/report_week_{YYYY-Www}.md

"Generate monthly report for January"
  → Creates full January 2026 report
  → Saves to Plans/reports/monthly/report_2026-01.md

"Generate exception report"
  → Creates report of all errors in last 24 hours
  → Saves to Plans/reports/exceptions/exception_{date}.md

"How many files did I process this week?"
  → Quick inline answer (no full report generated)

"Show storage trend for last 30 days"
  → Quick table output (no full report)
```

---

## Report Retention Policy

```
Daily reports:    Keep 30 days → delete older
Weekly reports:   Keep 12 weeks (3 months) → delete older
Monthly reports:  Keep 24 months (2 years) → delete older
Exception reports: Keep 6 months → delete older

Archive before delete:
  Monthly reports → Archive/reports/ before deletion
  Exception reports → Archive/exceptions/ before deletion
```

---

## Integration with Other Skills

### With Audit Skill
```
reporting → reads from → audit:
  Error rates and failure analysis
  Performance KPIs (P50/P95/P99 response times)
  System health metrics
```

### With Scheduler Skill
```
scheduler → triggers → reporting:
  SCH-DAILY: daily report at 08:00
  SCH-WEEKLY: weekly report Friday 17:00
  SCH-MONTHLY: monthly report 1st at 06:00
```

### With Notification Skill
```
reporting → triggers → notification after each report:
  INFO: "Daily report ready: Plans/reports/daily/report_2026-02-16.md"
  INFO: "Weekly report ready: Plans/reports/weekly/report_week_2026-W07.md"
```

### With Memory Management Skill
```
reporting → triggers → memory-management:
  Monthly report flags if storage growth too fast
  Recommends archive cadence based on growth rate
```

---

## Best Practices

### DO
```
- Always include comparison vs previous period
- Add actionable recommendations (not just data)
- Keep executive summary at top (humans skim first)
- Use ASCII charts for trends (no external tools needed)
- Save all reports as files (never just display and discard)
- Generate exception reports immediately when triggered
- Link reports from Dashboard for easy access
```

### DON'T
```
- Generate reports without saving them
- Include raw log dumps (summarize instead)
- Write recommendations without priority order
- Skip the health status indicator
- Generate duplicate reports for same period
- Omit the data source references
- Make reports longer than needed (be concise)
```

---

**Status**: Production Ready
**Priority**: MEDIUM (Visibility and accountability layer)
**Report Types**: Daily, Weekly, Monthly, Exception, On-demand
**Storage**: Plans/reports/ (with 30/90/730 day retention)
**Default Schedule**: Daily 08:00, Weekly Fri 17:00, Monthly 1st 06:00

*Good reporting = Human always knows what the AI did and why*
