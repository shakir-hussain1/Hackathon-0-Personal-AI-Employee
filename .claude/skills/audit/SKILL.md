# 📊 Audit Skill

**Purpose**: Analyze system activity, track failures, measure performance
**Core Function**: Monitor → Analyze → Report → Improve
**Output**: Comprehensive audit reports with actionable insights

---

## 🎯 Core Capabilities

### 1. Analyze Logs
Parse and extract insights from activity logs

### 2. Track Failures
Identify, categorize, and trend error patterns

### 3. Measure Performance
Monitor speed, efficiency, resource usage

### 4. Generate Reports
Create comprehensive audit reports with recommendations

---

## 📋 What to Audit

### System Activity
- ✅ Tool invocations
- ✅ File operations
- ✅ API calls
- ✅ Task processing
- ✅ Error occurrences
- ✅ User actions

### Performance Metrics
- ⏱️ Response times
- 💾 Resource usage
- 📊 Throughput rates
- 🔄 Success/failure ratios
- ⏰ Queue times
- 📈 Trends over time

### Security Events
- 🔐 Authentication attempts
- 🚫 Permission denials
- ⚠️ Suspicious activity
- 📧 External communications
- 🗑️ Deletions
- 💰 Financial operations

---

## 🔍 Log Analysis

### Log Entry Structure

**Standard format**:
```
[TIMESTAMP] [LEVEL] [COMPONENT] [ACTION] - Details
```

**Example**:
```
[2026-02-16 14:30:00] [INFO] [FileWatcher] [DETECTED] - New file: report.pdf
[2026-02-16 14:30:05] [INFO] [TaskProcessor] [STARTED] - Processing task #123
[2026-02-16 14:30:12] [ERROR] [EmailSender] [FAILED] - SMTP timeout
[2026-02-16 14:30:15] [WARNING] [Dashboard] [UPDATED] - Stats refresh took 3.2s
```

---

### Log Parsing

**Extract from each entry**:
- **Timestamp**: When did it happen?
- **Level**: How severe? (DEBUG/INFO/WARNING/ERROR)
- **Component**: Which system?
- **Action**: What happened?
- **Details**: Additional context
- **Duration**: How long? (if applicable)
- **Result**: Success/failure

**Example parsed entry**:
```markdown
Entry: [2026-02-16 14:30:12] [ERROR] [EmailSender] [FAILED] - SMTP timeout

Parsed:
- timestamp: 2026-02-16 14:30:12
- level: ERROR
- component: EmailSender
- action: FAILED
- details: "SMTP timeout"
- severity: HIGH
- requires_action: YES
```

---

### Log Aggregation

**Group by category**:
```markdown
By Level:
- ERROR: 23 entries (2.3%)
- WARNING: 145 entries (14.5%)
- INFO: 789 entries (78.9%)
- DEBUG: 43 entries (4.3%)

By Component:
- FileWatcher: 234 entries (23.4%)
- TaskProcessor: 456 entries (45.6%)
- EmailSender: 156 entries (15.6%)
- Dashboard: 154 entries (15.4%)

By Time:
- 00:00-06:00: 12 entries (1.2%)
- 06:00-12:00: 234 entries (23.4%)
- 12:00-18:00: 567 entries (56.7%)
- 18:00-24:00: 187 entries (18.7%)
```

---

## 🚨 Failure Tracking

### Failure Categories

**1. Transient Failures**
```markdown
Type: Temporary, recoverable
Examples:
- Network timeouts
- API rate limits
- Resource temporarily unavailable

Characteristics:
- Usually resolve automatically
- Retry often succeeds
- No permanent impact

Tracking:
- Count occurrences
- Track retry success rate
- Monitor frequency
- Alert if pattern changes
```

**2. Persistent Failures**
```markdown
Type: Recurring, needs intervention
Examples:
- Invalid configuration
- Missing permissions
- Broken dependencies

Characteristics:
- Keeps failing
- Retry doesn't help
- Requires fix

Tracking:
- Identify root cause
- Count affected operations
- Estimate impact
- Prioritize fix
```

**3. Critical Failures**
```markdown
Type: Severe, immediate attention
Examples:
- Data corruption
- Security breach
- System crash

Characteristics:
- High impact
- Urgent
- May affect multiple systems

Tracking:
- Immediate alert
- Root cause analysis
- Incident report
- Post-mortem
```

---

### Failure Metrics

**Track for each failure type**:
```markdown
Metric: Error Rate
Formula: (Errors / Total Operations) × 100
Target: < 1% (excellent), < 5% (acceptable), > 5% (needs attention)

Metric: Mean Time Between Failures (MTBF)
Formula: Total Runtime / Number of Failures
Target: > 24 hours (excellent), > 8 hours (acceptable)

Metric: Mean Time To Recovery (MTTR)
Formula: Total Downtime / Number of Failures
Target: < 5 minutes (excellent), < 30 minutes (acceptable)

Metric: Failure Impact
Formula: Affected Operations / Total Operations
Target: < 1% (minimal), < 10% (moderate), > 10% (severe)
```

---

### Failure Analysis

**Root Cause Analysis**:
```markdown
For each failure:

1. WHAT happened?
   - Operation that failed
   - Error message
   - Timestamp

2. WHY did it happen?
   - Immediate cause
   - Contributing factors
   - Environmental conditions

3. WHEN does it happen?
   - Time of day pattern?
   - Day of week pattern?
   - Load-related?

4. WHERE in the system?
   - Which component?
   - Which function?
   - Which server/service?

5. WHO was affected?
   - User impact
   - System impact
   - Downstream effects

6. HOW to prevent?
   - Short-term fix
   - Long-term solution
   - Monitoring improvements
```

---

## 📊 Performance Measurement

### Key Performance Indicators (KPIs)

**1. Response Time**
```markdown
Definition: Time from request to response

Measurements:
- Average: 1.23 seconds
- Median (P50): 0.85 seconds
- 95th percentile (P95): 3.2 seconds
- 99th percentile (P99): 5.8 seconds
- Max: 12.3 seconds

Targets:
- P50 < 1 second (excellent)
- P95 < 3 seconds (good)
- P99 < 5 seconds (acceptable)

Analysis:
- If P50 increasing → general slowdown
- If P95-P99 increasing → outlier issues
- If Max spikes → investigate those requests
```

**2. Throughput**
```markdown
Definition: Operations completed per unit time

Measurements:
- Operations per second: 45
- Operations per minute: 2,700
- Operations per hour: 162,000
- Operations per day: 3,888,000

Targets:
- Bronze tier: 1000 ops/hour
- Silver tier: 5000 ops/hour
- Gold tier: 10000 ops/hour

Analysis:
- Declining → bottleneck or resource constraint
- Stable → healthy system
- Increasing → scaling well or increased demand
```

**3. Resource Usage**
```markdown
Definition: System resources consumed

CPU:
- Average: 35%
- Peak: 78%
- Idle: 22%

Memory:
- Used: 2.1 GB / 8 GB (26%)
- Peak: 3.5 GB (44%)
- Available: 5.9 GB (74%)

Disk I/O:
- Reads: 1.2 MB/s
- Writes: 0.8 MB/s
- IOPS: 150

Network:
- Inbound: 2.5 Mbps
- Outbound: 1.8 Mbps
- Latency: 12ms

Targets:
- CPU < 70% average
- Memory < 80% used
- Disk I/O < 80% capacity
```

**4. Success Rate**
```markdown
Definition: Percentage of successful operations

Formula: (Successful / Total) × 100

By Operation:
- File operations: 99.2% (excellent)
- Email sending: 94.5% (good)
- API calls: 97.8% (excellent)
- Task processing: 98.9% (excellent)

Overall: 97.6% (excellent)

Targets:
- > 99% (excellent)
- 95-99% (good)
- 90-95% (acceptable)
- < 90% (needs attention)
```

---

### Performance Trends

**Track over time**:
```markdown
Daily Trend:
- Morning (6-12): Fast (0.8s avg)
- Afternoon (12-18): Moderate (1.2s avg)
- Evening (18-24): Fast (0.9s avg)
- Night (0-6): Very fast (0.5s avg)

Pattern: Slowdown during peak hours (12-18)
Action: Consider scaling during peak

Weekly Trend:
- Mon-Fri: Moderate load
- Sat-Sun: Light load

Pattern: Consistent weekday usage
Action: Maintain current capacity

Monthly Trend:
- Week 1: Light
- Week 2-3: Heavy
- Week 4: Moderate

Pattern: Mid-month spike
Action: Investigate cause, plan capacity
```

---

## 📑 Report Generation

### Daily Audit Report

```markdown
# Daily Audit Report
**Date**: 2026-02-16
**Period**: 00:00 - 23:59
**Generated**: 2026-02-17 00:15

---

## 📊 Executive Summary

**Overall Health**: 🟢 HEALTHY
**Total Operations**: 3,456
**Success Rate**: 97.8% (↑ 0.5% from yesterday)
**Average Response**: 1.2s (↓ 0.1s from yesterday)
**Errors**: 76 (2.2%) (↓ 12 from yesterday)

**Key Highlights**:
- ✅ Performance improved by 8%
- ✅ Error rate decreased
- ⚠️ 3 SMTP timeouts (recurring issue)
- 📈 Peak usage at 14:30 (highest this week)

---

## 📈 Activity Summary

### Total Operations by Type
| Type | Count | % | Success | Avg Time |
|------|-------|---|---------|----------|
| File Ops | 1,234 | 35.7% | 99.2% | 0.3s |
| Tasks | 987 | 28.6% | 98.9% | 2.1s |
| Emails | 654 | 18.9% | 94.5% | 1.8s |
| API Calls | 581 | 16.8% | 97.8% | 1.5s |

### Operations Timeline
```
00:00 ████░░░░░░░░░░░░░░░░ 45 ops
06:00 ██████████░░░░░░░░░░ 123 ops
12:00 ████████████████████ 456 ops ← Peak
18:00 ████████████░░░░░░░░ 234 ops
```

---

## 🚨 Error Analysis

### Error Breakdown
- **SMTP Timeout**: 23 (30%)
- **File Not Found**: 18 (24%)
- **Permission Denied**: 12 (16%)
- **Rate Limit**: 8 (11%)
- **Invalid Parameter**: 7 (9%)
- **Other**: 8 (11%)

### Top 3 Issues

**1. SMTP Timeouts (23 occurrences)**
- Component: EmailSender
- Impact: 3.5% of emails failed
- Pattern: Clustered around 14:00-15:00
- Action: Investigate SMTP server load
- Priority: HIGH

**2. File Not Found (18 occurrences)**
- Component: FileWatcher
- Impact: Task creation delayed
- Pattern: Random throughout day
- Action: Verify file cleanup timing
- Priority: MEDIUM

**3. Permission Denied (12 occurrences)**
- Component: TaskProcessor
- Impact: Tasks cancelled
- Pattern: Specific file types
- Action: Review file permissions
- Priority: MEDIUM

---

## ⚡ Performance Metrics

### Response Times
- **Average**: 1.2s (Target: <2s) ✅
- **Median (P50)**: 0.8s
- **P95**: 3.1s (Target: <3s) ✅
- **P99**: 4.8s (Target: <5s) ✅
- **Max**: 8.9s

**Status**: 🟢 All targets met

### Throughput
- **Operations/hour**: 144 avg (peak: 234)
- **Files processed**: 1,234
- **Emails sent**: 618
- **Tasks completed**: 987

### Resource Usage
- **CPU**: 42% avg (peak: 67%)
- **Memory**: 2.8 GB / 8 GB (35%)
- **Disk**: 45 GB / 128 GB (35%)
- **Network**: 15 MB transferred

**Status**: 🟢 All within limits

---

## 📊 Comparative Analysis

### vs Yesterday
- Operations: +8.5% (↑)
- Success Rate: +0.5% (↑)
- Response Time: -8.3% (↓ better)
- Errors: -13.6% (↓ better)

### vs Last Week (same day)
- Operations: +12.3% (↑)
- Success Rate: -0.2% (↓)
- Response Time: +5.1% (↑ slower)
- Errors: +8.7% (↑ worse)

### Month-to-Date
- Total Operations: 51,234
- Average Success: 97.4%
- Average Response: 1.3s
- Total Errors: 1,345 (2.6%)

---

## 🎯 Recommendations

### Immediate Actions (Today)
1. **Investigate SMTP timeouts**
   - Check SMTP server logs
   - Consider backup SMTP
   - Implement retry with backoff

2. **Review file permissions**
   - Audit Done/ folder permissions
   - Update file access rules
   - Test with affected file types

### Short-term (This Week)
3. **Optimize peak hour performance**
   - Analyze 12-18:00 load
   - Consider resource scaling
   - Implement caching

4. **Reduce File Not Found errors**
   - Review file lifecycle
   - Adjust cleanup timing
   - Add file existence checks

### Long-term (This Month)
5. **Performance monitoring**
   - Set up alerting for P99 > 5s
   - Track resource trends
   - Plan capacity upgrades

6. **Error prevention**
   - Implement pre-validation
   - Add fallback mechanisms
   - Improve error recovery

---

## 📋 Appendix

### Detailed Error Log
[View full log](logs/2026-02-16-errors.log)

### Performance Raw Data
[View CSV](reports/2026-02-16-performance.csv)

### System Configuration
- Bronze Tier
- Python 3.13
- Windows 10
- 8 GB RAM

---

**Next Report**: 2026-02-17 00:15
**Report Frequency**: Daily
**Retention**: 90 days

---

*Report generated automatically by Audit Skill*
```

---

### Weekly Audit Report

```markdown
# Weekly Audit Report
**Week**: 2026-02-10 to 2026-02-16 (Week 7)
**Generated**: 2026-02-17 00:30

---

## 📊 Week Summary

**Total Operations**: 24,192
**Daily Average**: 3,456
**Success Rate**: 97.3% (↑ 0.3% from last week)
**Weekly Uptime**: 99.8%

---

## 📈 Trends

### Operations Trend
```
Mon █████████░░░░░░░ 3,234 ops
Tue ██████████░░░░░░ 3,567 ops
Wed ███████████░░░░░ 3,890 ops
Thu ████████████░░░░ 4,123 ops ← Peak
Fri ███████████░░░░░ 3,678 ops
Sat ████░░░░░░░░░░░░ 2,345 ops
Sun ████░░░░░░░░░░░░ 2,355 ops
```

**Pattern**: Weekday peaks Thu-Fri, weekend dips
**Action**: Normal pattern, maintain capacity

### Error Rate Trend
```
Mon 2.5% ████████████████████████░░░░░░
Tue 2.1% ████████████████████░░░░░░░░░░
Wed 1.8% ██████████████████░░░░░░░░░░░░
Thu 2.3% ███████████████████████░░░░░░░
Fri 2.0% ████████████████████░░░░░░░░░░
Sat 1.5% ███████████████░░░░░░░░░░░░░░░
Sun 1.4% ██████████████░░░░░░░░░░░░░░░░
```

**Pattern**: Decreasing through week, lowest on weekend
**Action**: Good trend, continue monitoring

---

## 🏆 Week Highlights

**Best Day**: Wednesday
- Highest success rate: 98.2%
- Fastest avg response: 1.1s
- Lowest errors: 1.8%

**Worst Day**: Monday
- Lowest success rate: 97.5%
- Slowest avg response: 1.4s
- Highest errors: 2.5%

**Most Active**: Thursday
- 4,123 operations
- Peak hour: 14:00 (234 ops)

---

## 🎯 Week Goals Progress

| Goal | Target | Actual | Status |
|------|--------|--------|--------|
| Success Rate | > 97% | 97.3% | ✅ MET |
| Avg Response | < 2s | 1.2s | ✅ MET |
| Error Rate | < 3% | 2.7% | ✅ MET |
| Uptime | > 99% | 99.8% | ✅ MET |

**Achievement**: 4/4 goals met ✅

---

## 🔍 Deep Dive: Top Issues

### Issue #1: SMTP Timeouts
- **This week**: 156 occurrences
- **Last week**: 89 occurrences
- **Change**: +75% ⚠️
- **Root cause**: SMTP server overload during peak hours
- **Impact**: 6.3% of emails delayed
- **Resolution**:
  - Implemented connection pooling
  - Added retry logic
  - Monitoring server capacity
- **Status**: 🟡 IN PROGRESS

### Issue #2: File Access Delays
- **This week**: 45 occurrences
- **Last week**: 67 occurrences
- **Change**: -33% ✅
- **Root cause**: Disk I/O bottleneck
- **Impact**: 3.6% of file ops slower
- **Resolution**:
  - Optimized file reading
  - Implemented caching
  - Reduced concurrent access
- **Status**: 🟢 RESOLVED

---

## 📊 Month-to-Date (Feb 1-16)

- **Total Operations**: 51,234
- **Success Rate**: 97.4%
- **Average Response**: 1.3s
- **Total Errors**: 1,345
- **On track for**: 78,000 operations (projected month-end)

---

**Next Weekly Report**: 2026-02-24 00:30
**Report Frequency**: Weekly (Sunday nights)

---

*Week 7 Report - System performing well*
```

---

### Monthly Audit Report

```markdown
# Monthly Audit Report
**Month**: February 2026
**Period**: 2026-02-01 to 2026-02-28
**Generated**: 2026-03-01 01:00

---

## 📊 Monthly Summary

**Total Operations**: 96,789
**Daily Average**: 3,457
**Success Rate**: 97.1%
**Monthly Uptime**: 99.7%
**Total Errors**: 2,806 (2.9%)

**Month Grade**: A- (Excellent performance)

---

## 📈 Month Trends

[Monthly charts and detailed analysis...]

---

## 🎯 February Goals

✅ All 5 goals achieved
📈 3 new performance records set
🏆 Best month of Q1

---

## 🔮 March Recommendations

1. Scale SMTP capacity
2. Implement advanced caching
3. Add predictive alerting
4. Expand to Silver tier features

---

*Monthly Report - February 2026*
```

---

## 🔔 Alert Thresholds

### When to Alert

**CRITICAL** (Immediate):
- Error rate > 10%
- System down
- Security breach
- Data corruption

**HIGH** (Within 1 hour):
- Error rate > 5%
- Response time > 10s
- Success rate < 90%
- Resource > 90%

**MEDIUM** (Within 4 hours):
- Error rate > 3%
- Response time > 5s
- Success rate < 95%
- Trend deteriorating

**LOW** (Daily review):
- Error rate > 1%
- Response time > 3s
- Success rate < 98%
- Minor issues

---

## 🎯 Best Practices

### DO ✅

**1. Audit regularly**
- Daily reports
- Weekly reviews
- Monthly analysis
- Quarterly planning

**2. Track trends**
- Not just snapshots
- Week-over-week
- Month-over-month
- Year-over-year

**3. Act on insights**
- Don't just report
- Create action items
- Assign owners
- Follow up

**4. Automate everything**
- Report generation
- Log analysis
- Metric calculation
- Alert triggering

**5. Share reports**
- Stakeholders
- Team members
- Management
- Historical archive

---

### DON'T ❌

**1. Don't ignore warnings**
- Small issues become big
- Trends matter
- Early intervention cheaper

**2. Don't over-alert**
- Alert fatigue
- Desensitization
- Missed critical alerts

**3. Don't audit in isolation**
- Cross-reference data
- Context matters
- Look at full picture

**4. Don't keep stale data**
- Archive old reports
- Compress logs
- Retain only useful data

---

## 📚 Quick Reference

### Report Schedule
- **Daily**: 00:15 (overnight)
- **Weekly**: Sunday 00:30
- **Monthly**: 1st of month 01:00
- **Quarterly**: 1st of quarter 02:00

### Retention Policy
- **Detailed logs**: 30 days
- **Daily reports**: 90 days
- **Weekly reports**: 1 year
- **Monthly reports**: Forever

### Report Locations
- `Common/AI_Employee_Vault/Reports/`
  - `daily/`
  - `weekly/`
  - `monthly/`
  - `audit_dashboard.md`

---

**Status**: Production Ready
**Core Function**: Monitor system health and performance
**Output**: Actionable insights and recommendations

*Good auditing enables continuous improvement*
