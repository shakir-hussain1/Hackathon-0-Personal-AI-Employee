# Analytics Skill

**Purpose**: Turn raw vault data into actionable insights — trends, patterns, forecasts, and recommendations
**Storage**: Markdown-based analytics reports, insight records, trend files, forecast models
**Scope**: Task analytics, productivity metrics, file trends, error analysis, resource forecasting, business intelligence

---

## Core Functions

### 1. Collect Data
Aggregate raw numbers from logs, task files, and metrics

### 2. Compute Metrics
Calculate rates, averages, percentages, and ratios

### 3. Identify Trends
Find patterns that are growing, shrinking, or repeating

### 4. Forecast
Project current trends forward to anticipate future needs

### 5. Generate Insights
Convert numbers into plain-language conclusions

### 6. Recommend Actions
Suggest specific next steps based on what the data shows

---

## Data Sources

```
Source File                          | Data Available
-------------------------------------|------------------------------------------
Logs/YYYY-MM-DD.log                  | Task events, errors, durations, file types
Logs/metrics.md                      | RAM, CPU, disk readings (time series)
Logs/scheduler_YYYY-MM-DD.log        | Task run times, success/fail counts
Logs/decisions.log                   | Decision types, confidence levels, overrides
Logs/delegation.log                  | Handler assignments, response times
Logs/security_audit.log              | Threat events, scan results
Logs/notifications.md                | Alert frequency, acknowledgment times
Logs/observations.log                | Learning signals, feedback patterns
Knowledge/feedback.md                | Human approval/rejection/correction signals
Plans/schedule.md                    | Scheduled task definitions and history
Plans/context/entities.md            | Entity interaction counts, patterns
Plans/reports/                       | Historical report data
Done/                                | File archive (count, types, dates)
Needs_Action/                        | Current queue depth and age
```

---

## Metric Taxonomy

### Category 1: Productivity Metrics
```
Files Processed Per Day (FPD)
  Formula:  count(files_moved_to_done) / working_days
  Target:   > 5 FPD (Bronze baseline)
  Trending: Compare 7-day avg vs 30-day avg

Task Completion Rate (TCR)
  Formula:  completed_tasks / total_tasks_created × 100
  Target:   > 90%
  Trending: Weekly trend

Tasks Requiring Human Intervention (THI)
  Formula:  human_touch_tasks / total_tasks × 100
  Target:   < 20% (more automation = lower THI)
  Trending: Should decrease as Learning Skill matures

Average Task Processing Time (ATPT)
  Formula:  sum(task_durations) / task_count (by type)
  Target:   Document < 3 min, CSV < 2 min, Image < 30s
  Trending: Compare weekly

Backlog Age Index (BAI)
  Formula:  avg(days_waiting) across all Needs_Action files
  Target:   < 0.5 days (half a day average wait)
  Trending: Alert if > 2 days and growing
```

### Category 2: Quality Metrics
```
AI Decision Accuracy (ADA)
  Formula:  decisions_not_overridden / total_decisions × 100
  Target:   > 90%
  Trending: Should increase as Learning Skill adds rules

Human Override Rate (HOR)
  Formula:  human_overrides / total_ai_decisions × 100
  Target:   < 10%
  Trending: Down trend = AI improving

Error Rate (ER)
  Formula:  errors / total_operations × 100
  Target:   < 5%
  Trending: Any spike above 10% = investigate

First-Time Resolution Rate (FTR)
  Formula:  tasks_completed_without_retry / total × 100
  Target:   > 85%
  Trending: Low FTR = recurring errors need fixing

Approval Rate (AR)
  Formula:  approved_actions / submitted_for_approval × 100
  Target:   > 75% (high reject rate = AI proposing wrong actions)
  Trending: Rising AR = AI learning preferences
```

### Category 3: Efficiency Metrics
```
Automation Coverage (AC)
  Formula:  fully_automated_tasks / total_tasks × 100
  Target:   > 80% (Bronze), > 90% (Silver), > 95% (Gold)
  Trending: Should grow as rules and patterns accumulate

Time Saved Per Week (TSW)
  Formula:  (manual_time_estimate × tasks_automated) / 60 (hours)
  Estimate: avg 15 min/task saved when AI handles it
  Target:   > 3 hours/week saved (Bronze)
  Trending: Increases with automation coverage

Queue Throughput (QT)
  Formula:  tasks_completed / tasks_created over same period
  Target:   > 1.0 (completing more than arriving)
  Alert:    < 0.8 = backlog growing faster than clearance

Skill Utilization Rate (SUR)
  Formula:  times_skill_called / total_operations × 100
  Report:   Top 5 most used skills vs bottom 5
  Use:      Identify underused or overloaded skills
```

### Category 4: Resource Metrics
```
Daily Disk Growth Rate (DDGR)
  Formula:  (disk_end_of_day - disk_start_of_day) MB
  Target:   < 5 MB/day
  Forecast: Days until Bronze limit (250 MB) reached

Memory Stability Index (MSI)
  Formula:  std_dev(ram_readings_per_day)
  Target:   < 10% std dev (stable memory usage)
  Alert:    > 20% = memory leak or burst activity

Storage Efficiency Score (SES)
  Formula:  useful_data_mb / total_vault_mb × 100
  Useful:   Active tasks + knowledge base
  Less useful: Old logs + stale Done/ files
  Target:   > 60% useful data

Uptime Percentage (UP)
  Formula:  (total_minutes - downtime_minutes) / total_minutes × 100
  Target:   > 98%
  Downtime: Watcher crashes, manual stops
```

### Category 5: Entity Analytics
```
Top Senders by Volume
  Formula:  count(files) grouped by sender, sorted descending
  Insight:  Who drives the most work?

Top Senders by Priority
  Formula:  avg(priority_score) by sender
  Insight:  Who sends the most urgent work?

Entity Response Time (ERT)
  Formula:  avg(time from file received to task complete) by sender
  Insight:  Which senders get fastest turnaround?

Topic Frequency Map
  Formula:  count(tasks) grouped by category/topic
  Insight:  What subjects dominate workload?

Interaction Cadence
  Formula:  avg(days between interactions) by entity
  Insight:  Who is most active? Who has gone quiet?
```

---

## Trend Analysis

### Trend Types

#### Upward Trend
```
Definition: Metric increasing consistently over time

Detection:
  Calculate linear regression slope over last 14 readings
  IF slope > +5% per period → UPWARD TREND

Examples:
  Files processed/day: 5 → 6 → 7 → 8 → 9 (growing)
  Disk usage: 140 MB → 150 MB → 163 MB → 173 MB (growing)

Interpretation depends on metric:
  Files processed UP → GOOD (more productive)
  Disk usage UP     → WATCH (approaching limit)
  Error rate UP     → BAD (investigate)
  Human overrides UP→ BAD (AI accuracy declining)
```

#### Downward Trend
```
Definition: Metric decreasing consistently over time

Detection:
  Slope < -5% per period → DOWNWARD TREND

Examples:
  Human override rate: 18% → 14% → 11% → 8% (improving)
  Error rate: 9% → 7% → 5% → 4% (improving)
  Files processed: 10 → 8 → 6 → 4 (concerning)

Interpretation:
  Override rate DOWN → GOOD (AI improving)
  Error rate DOWN    → GOOD (system stabilizing)
  Throughput DOWN    → INVESTIGATE (bottleneck?)
```

#### Cyclical Pattern
```
Definition: Metric rises and falls on a repeating schedule

Detection:
  Compare current value to same period last week/month
  Consistent deviation < ±15% = cyclical pattern

Examples:
  Files per hour peaks Mon 09:00, drops Sat-Sun
  RAM usage peaks during bulk processing (midday)
  Error rate slightly higher on Mondays (new files)

Use:
  Predict when to pre-allocate resources
  Schedule maintenance during low-activity cycles
  Set different baselines per time-of-week
```

#### Spike Pattern
```
Definition: Sudden single-period jump then return to baseline

Detection:
  Value > 3 standard deviations from recent mean
  Returns to normal within 2-3 periods

Examples:
  47 files arrived in 2 hours (unusual burst)
  RAM spiked to 84% during large PDF processing
  5 errors in 30 minutes (transient issue)

Use:
  Distinguish from sustained problems (spikes are less serious)
  Document spike context (what caused it?)
  Consider burst mode triggers based on spike patterns
```

#### Plateau Pattern
```
Definition: Metric reached a stable level and stopped changing

Detection:
  Slope within ±2% for 10+ consecutive readings

Examples:
  AI accuracy stabilized at 94% (learning matured)
  File volume plateaued at ~10/day (workload stable)
  Disk growth stopped (archival keeping pace)

Use:
  Confirm system is in steady state
  Good time to introduce new features
  Baselines should be updated from plateau values
```

---

## Forecasting

### Forecast Models

#### Linear Projection
```
Use for: Steady growth trends (disk usage, task volume)

Formula:
  future_value = current_value + (slope × periods_ahead)

Example:
  Disk usage growing at +2 MB/day
  Current: 173 MB
  Bronze limit: 250 MB
  Headroom: 77 MB
  Days remaining: 77 / 2 = 38.5 days

Output:
  "At current growth (+2 MB/day), vault will reach 250 MB limit
   in approximately 38 days (around 2026-03-26).
   Recommendation: Run archival by 2026-03-12 (2-week buffer)."
```

#### Rate-Based Projection
```
Use for: Quota consumption, token expiry, credential rotation

Formula:
  days_remaining = remaining_quota / avg_daily_consumption

Example:
  Gmail API quota: 250 requests/day
  Current usage: 47 requests/day
  Remaining today: 203 requests
  Safe for: 203/47 ≈ 4.3 more hours

Output:
  "Gmail API quota sufficient for today.
   Monthly trend: 47 req/day avg (214 MB buffer).
   No quota risk at current usage."
```

#### Pattern-Based Forecast
```
Use for: Cyclical workloads, Monday morning file bursts

Formula:
  next_period_forecast = same_period_last_cycle × adjustment_factor

Example:
  Last 4 Mondays: 8, 9, 7, 10 files
  Avg: 8.5 files expected next Monday
  Adjustment for growth trend: ×1.05
  Forecast: 8.9 → round to 9 files

Output:
  "Expect ~9 files next Monday morning.
   Recommend: Ensure watcher running by 07:45."
```

---

## Insight Generation

### Insight Templates

#### Insight Type 1: Positive Trend
```
Format:
  📈 [METRIC] improved [X%] over [PERIOD]
  This means: [plain language explanation]
  Driven by: [cause if identifiable]
  Keep doing: [what is working]

Example:
  AI Decision Accuracy improved from 78% to 94% over 4 weeks.
  This means: 9 out of 10 AI decisions now match what human would choose.
  Driven by: 6 learned rules activated from observed corrections.
  Keep doing: Reviewing and approving rule proposals promptly.
```

#### Insight Type 2: Warning Trend
```
Format:
  ⚠️ [METRIC] trending [direction] — [X% change over PERIOD]
  Risk: [what happens if trend continues]
  Projected: [when will it become a problem]
  Recommend: [specific action]

Example:
  ⚠️ Vault disk usage trending UP — +32 MB over 4 weeks (+23%)
  Risk: Will exceed Bronze limit (250 MB) in ~38 days
  Projected: Limit reached around 2026-03-26
  Recommend: Archive Done/ tasks older than 45 days this week (saves ~50 MB)
```

#### Insight Type 3: Anomaly Found
```
Format:
  🔍 [ANOMALY TYPE] detected on [DATE]
  What happened: [description]
  Normal baseline: [what is typical]
  Actual value: [what was seen]
  Possible cause: [hypothesis]
  Recommended check: [what to look at]

Example:
  🔍 Error spike detected on 2026-02-14
  What happened: 7 errors in 30 minutes (normal: ~2/day)
  Normal baseline: 0.08 errors/hour
  Actual value: 14 errors/hour for 30 minutes
  Possible cause: Large batch of malformed Excel files from Finance team
  Recommended check: Logs/2026-02-14.log lines 340-420
```

#### Insight Type 4: Pattern Discovery
```
Format:
  💡 Pattern discovered: [description]
  Observed: [how many times, over what period]
  Confidence: [%]
  Opportunity: [how to act on this]
  Potential saving: [time or resource estimate]

Example:
  💡 Pattern discovered: Finance team sends Excel files every Tuesday
  Observed: 4 consecutive Tuesdays, 3-5 files each
  Confidence: 82%
  Opportunity: Pre-schedule Tuesday batch processing at 10:00
  Potential saving: 15-minute faster turnaround on Finance files
```

#### Insight Type 5: Forecast Alert
```
Format:
  🔮 [RESOURCE/METRIC] forecast: [projected value] by [date]
  Current rate: [rate]
  Action window: [days before action needed]
  Recommended action: [specific action + deadline]

Example:
  🔮 Vault storage forecast: 250 MB (limit) by 2026-03-26
  Current rate: +2 MB/day growth
  Action window: 38 days (but act in 24 days for 2-week buffer)
  Recommended action: Run archive on 2026-03-12 → free ~50 MB
```

---

## Analytics Reports

### Weekly Analytics Report
```
Location: Plans/reports/analytics/analytics_week_{YYYY-Www}.md

Sections:
  1. Executive Dashboard (top 5 KPIs vs last week)
  2. Productivity Summary (FPD, TCR, THI, ATPT)
  3. Quality Summary (ADA, HOR, ER, FTR, AR)
  4. Efficiency Summary (AC, TSW, QT)
  5. Resource Summary (DDGR, MSI, SES, UP)
  6. Top Insights (3-5 key findings)
  7. Trend Chart (ASCII, last 7 days per key metric)
  8. Forecasts (next 7 days projection)
  9. Recommendations (top 3 prioritized actions)
```

### Monthly Analytics Report
```
Location: Plans/reports/analytics/analytics_{YYYY-MM}.md

Sections:
  1. Month-in-review (all major KPIs vs previous month)
  2. Entity Analytics (top senders, top topics, response times)
  3. Learning Progress (rules added, accuracy improvement)
  4. 30-day Trend Charts (ASCII)
  5. Forecast for next 30 days
  6. ROI Estimate (time saved, errors avoided)
  7. Tier Upgrade Readiness (Bronze → Silver signal strength)
  8. Strategic Recommendations
```

---

## ROI Calculation

### Time Saved Estimate
```
Per task type, estimate manual time saved:

Document processing:   15 min/file → AI does in avg 2 min → saves 13 min
CSV analysis:          20 min/file → AI does in avg 1 min → saves 19 min
Email triage (Silver): 5 min/email → AI does in avg 30s → saves 4.5 min
Filing and organizing: 3 min/file  → AI does in avg 10s → saves 2.8 min

Weekly ROI calculation:
  Documents processed: 28 files × 13 min = 364 min = 6.1 hours saved
  CSVs processed:      12 files × 19 min = 228 min = 3.8 hours saved
  Filing:              40 files × 2.8 min = 112 min = 1.9 hours saved
  Total saved this week: 11.8 hours

Annual projection: 11.8 × 52 = 614 hours/year saved
```

### Error Cost Avoided
```
Per error type, estimate cost if not caught:

Missed invoice:        High cost (payment delay, relationship damage)
Duplicate task:        Low cost (5 min wasted)
Missed urgent file:    Medium cost (delay + human attention)
Security incident:     Very high cost (varies)

Weekly error cost avoided:
  Errors caught by AI before reaching human: {n}
  Estimated cost per error: $10-50 (admin time)
  Weekly saving: {n} × $15 avg = ${estimate}
```

---

## Analytics Storage

### Data Retention
```
Raw metric readings:    Compress after 30 days, delete after 90 days
Weekly analytics:       Keep 12 weeks (3 months)
Monthly analytics:      Keep 24 months (2 years)
Insight records:        Keep indefinitely (searchable knowledge)
Forecast records:       Keep 6 months (compare forecast vs actual)
ROI estimates:          Keep 24 months (show value over time)
```

### Analytics Index
```
Location: Plans/reports/analytics/index.md

Format:
| Period       | Report File                        | Top Insight                    |
|--------------|------------------------------------|--------------------------------|
| 2026-W07     | analytics_week_2026-W07.md        | AI accuracy hit 94%            |
| 2026-W06     | analytics_week_2026-W06.md        | Disk growth accelerated        |
| 2026-02      | analytics_2026-02.md              | 23% more files vs Jan          |
| 2026-01      | analytics_2026-01.md              | System established baseline    |
```

---

## Integration with Other Skills

### With Monitoring Skill
```
analytics → consumes → monitoring data:
  All metric readings (time series)
  Alert history (frequency, duration, type)
  Anomaly events (for deeper analysis)
  Resource trends for forecasting
```

### With Audit Skill
```
analytics → consumes → audit data:
  Task event logs (for productivity metrics)
  Error logs (for quality metrics)
  Decision logs (for accuracy metrics)
  Performance KPIs (already computed)
```

### With Reporting Skill
```
analytics → feeds → reporting with:
  Computed metrics (ready to embed in reports)
  Trend charts (ASCII format)
  Key insights (top 3-5 per period)
  Forecasts (projected values for next period)
```

### With Learning Skill
```
analytics → informs → learning:
  Which metrics are improving (reinforce those behaviors)
  Which metrics are declining (flag for rule review)
  Accuracy trends (signal when learning is working)
  Pattern discoveries (potential new rules to propose)
```

### With Context Skill
```
analytics → enriches → context with:
  Entity-level analytics (Alice sends 3x more than Bob)
  Topic frequency data (finance is dominant topic)
  Historical volume data (for better context injection)
```

### With Optimization Skill
```
analytics → triggers → optimization when:
  Disk growth forecast shows limit approaching
  Resource efficiency score dropping
  Storage efficiency < 50% (too much dead weight)
```

### With Decision Skill
```
analytics → informs → decision making:
  Confidence calibration (is AI accuracy on track?)
  Handler performance data (which skills are most reliable?)
  Historical decision outcomes (what worked before?)
```

---

## Best Practices

### DO
```
- Compute metrics consistently (same formula every period)
- Compare to previous period (context makes numbers meaningful)
- Lead with insights, follow with data (humans read insights first)
- Flag both positive and negative trends
- Make every recommendation specific and actionable
- Archive old analytics before deleting (insights age well)
- Update baselines when system changes significantly
- Separate correlation from causation in insights
```

### DON'T
```
- Report numbers without context (94% means nothing alone)
- Generate analytics on too little data (<7 days for trends)
- Forecast beyond 90 days (accuracy drops sharply)
- Overload reports with every metric (top 5-10 only)
- Confuse a spike with a trend (verify with multiple readings)
- State opinions as data (label insights as interpretations)
- Skip the "so what" — every metric needs a takeaway
- Store raw logs indefinitely (compress and summarize instead)
```

---

## Quick Reference: Metric Health Signals

```
Metric                  | Healthy         | Warning          | Critical
------------------------|-----------------|------------------|-------------------
Files Processed/Day     | > 5             | 2-5              | < 2
Task Completion Rate    | > 90%           | 75-90%           | < 75%
AI Decision Accuracy    | > 90%           | 75-90%           | < 75%
Human Override Rate     | < 10%           | 10-25%           | > 25%
Error Rate              | < 5%            | 5-15%            | > 15%
Automation Coverage     | > 80%           | 60-80%           | < 60%
Queue Throughput        | > 1.0           | 0.8-1.0          | < 0.8
Disk Growth/Day         | < 3 MB          | 3-7 MB           | > 7 MB
Uptime                  | > 98%           | 95-98%           | < 95%
Approval Rate           | > 75%           | 50-75%           | < 50%
```

---

**Status**: Production Ready
**Priority**: MEDIUM-HIGH (Drives continuous improvement and planning)
**Metrics Tracked**: 20 KPIs across 5 categories
**Trend Detection**: Linear regression + cyclical + spike + plateau
**Forecast Horizon**: 7 days (accurate), 30 days (indicative), 90 days (directional)
**Reports**: Weekly + Monthly + On-demand

*Good analytics = Numbers that tell a story and actions that follow*
