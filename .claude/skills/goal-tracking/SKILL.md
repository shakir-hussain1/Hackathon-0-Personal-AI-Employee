# Goal Tracking Skill

**Purpose**: Define, monitor, measure, and achieve goals — from daily targets to long-term strategic objectives
**Storage**: Markdown-based goal files, milestone records, progress journals, OKR documents
**Scope**: Personal goals, business goals, system goals, team goals, KPI tracking, milestone management

---

## Core Functions

### 1. Define Goals
Capture clear, measurable, time-bound objectives

### 2. Break Down
Decompose goals into milestones, tasks, and weekly targets

### 3. Track Progress
Measure advancement against defined success criteria

### 4. Detect Drift
Identify when progress is falling behind plan

### 5. Forecast Completion
Project whether the goal will be met on time

### 6. Celebrate and Learn
Record achievements and extract lessons from both success and failure

---

## Goal Hierarchy

```
VISION (3-5 years)
  └── STRATEGIC GOAL (1 year)
        └── QUARTERLY GOAL / OKR (90 days)
              └── MONTHLY MILESTONE (30 days)
                    └── WEEKLY TARGET (7 days)
                          └── DAILY TASK (1 day)
                                └── TASK file in Needs_Action/
```

---

## Goal Types

### Type 1: Outcome Goal
```
Definition: What you want to achieve (result-focused)

Examples:
  - "Process 100% of inbox files within 24 hours"
  - "Reduce error rate to below 3%"
  - "Save 10 hours per week through automation"
  - "Complete Project Alpha by March 31"

Measurement: Binary (achieved / not achieved) or percentage
Best for: Clear end states with definite completion criteria
```

### Type 2: Process Goal
```
Definition: What you commit to doing consistently (behavior-focused)

Examples:
  - "Review Dashboard every morning at 08:00"
  - "Archive completed tasks every Friday"
  - "Run weekly analytics report without fail"
  - "Respond to all HIGH priority tasks within 4 hours"

Measurement: Streak (days consistent), compliance rate (%)
Best for: Building habits and sustainable operations
```

### Type 3: Learning Goal
```
Definition: What capability you want to develop over time

Examples:
  - "AI accuracy reaches 95% on priority assignment"
  - "Zero human corrections needed for known senders"
  - "Classifier correctly handles 10 new file types"
  - "All 50 learned rules active and performing above 80%"

Measurement: Metric value at start vs current vs target
Best for: Improvement goals with a baseline and target
```

### Type 4: System Goal
```
Definition: Performance targets for the AI Employee system itself

Examples:
  - "Watcher uptime > 98% per month"
  - "Vault stays below 200 MB (Bronze tier)"
  - "Zero CRITICAL incidents this quarter"
  - "Queue depth never exceeds 20 tasks"

Measurement: Continuous monitoring against threshold
Best for: Operational reliability and capacity goals
```

### Type 5: Business Goal
```
Definition: Real-world outcomes the human wants to achieve

Examples:
  - "Close 5 new clients this quarter"
  - "Launch website redesign by April 1"
  - "Reduce invoice payment delays by 50%"
  - "Post 3 LinkedIn articles per week"

Measurement: Business KPI (revenue, clients, conversions)
Best for: Strategic objectives the AI supports but doesn't own
```

---

## Goal File Format

```markdown
# Goal: {title}

**ID**: GOAL-{YYYY}-{sequence}
**Created**: 2026-02-16
**Updated**: 2026-02-16
**Type**: outcome | process | learning | system | business
**Status**: ACTIVE | ON_TRACK | AT_RISK | OFF_TRACK | ACHIEVED | ABANDONED
**Owner**: Human | AI_Employee | Shared
**Horizon**: daily | weekly | monthly | quarterly | annual

---

## Objective

{Clear statement of what success looks like in 1-3 sentences}

---

## Success Criteria

| Criterion                    | Target       | Current      | Status  |
|------------------------------|--------------|--------------|---------|
| {measurable condition 1}     | {value}      | {value}      | GREEN   |
| {measurable condition 2}     | {value}      | {value}      | YELLOW  |
| {measurable condition 3}     | {value}      | {value}      | RED     |

**All criteria must be GREEN to mark ACHIEVED**

---

## Timeline

**Start**: 2026-02-01
**Target completion**: 2026-03-31
**Days remaining**: 44
**Percent of time elapsed**: 27%

---

## Milestones

| ID  | Milestone                     | Due        | Status     | Done  |
|-----|-------------------------------|------------|------------|-------|
| M1  | Baseline established          | 2026-02-07 | ACHIEVED   | ✓     |
| M2  | First improvement measurable  | 2026-02-21 | ON_TRACK   |       |
| M3  | Halfway to target             | 2026-03-01 | UPCOMING   |       |
| M4  | Final push                    | 2026-03-25 | UPCOMING   |       |
| M5  | Goal achieved                 | 2026-03-31 | UPCOMING   |       |

---

## Progress Journal

| Date       | Metric Value | Change   | Notes                          |
|------------|-------------|----------|--------------------------------|
| 2026-02-01 | 78%         | baseline | AI accuracy at project start   |
| 2026-02-08 | 82%         | +4%      | 2 new rules activated          |
| 2026-02-15 | 87%         | +5%      | Alice priority rule performing |
| 2026-02-16 | 89%         | +2%      | Bob coding rule added          |

---

## Current Status

**Progress**: 55% toward target (89% current, 95% target)
**Trajectory**: ON_TRACK (averaging +3.7% improvement per week)
**Forecast**: Will achieve target around 2026-03-02 (ahead of schedule)
**Blockers**: None

---

## Actions This Week

- [ ] Review 5 remaining rule proposals with low confidence
- [ ] Identify top 3 remaining error types to address
- [ ] Request human feedback on ambiguous categorizations

---

## Linked Tasks

- TASK-20260216-022 → Review rule proposals
- SCH-20260216-005 → Weekly accuracy check
```

---

## OKR Framework

### OKR Structure

```
Objectives and Key Results:

OBJECTIVE: {Inspiring, qualitative goal — what do we want to achieve?}
  KR1: {Specific, measurable result 1}  → {current} / {target}
  KR2: {Specific, measurable result 2}  → {current} / {target}
  KR3: {Specific, measurable result 3}  → {current} / {target}

OKR score: avg(KR1%, KR2%, KR3%)
  0-30%:  OFF_TRACK
  31-60%: AT_RISK
  61-85%: ON_TRACK
  86-100%:ACHIEVED (100% = perfect delivery)
```

### Example OKR: Bronze → Silver Readiness

```markdown
# OKR: Q1 2026 — Achieve Silver Tier Readiness

**Objective**: Build a reliable, intelligent AI Employee foundation
ready for Silver tier capabilities

**KR1**: AI decision accuracy ≥ 95%
  Current: 89% | Target: 95% | Progress: 73%

**KR2**: Watcher uptime ≥ 98% for the quarter
  Current: 97.8% | Target: 98% | Progress: 91%

**KR3**: Zero CRITICAL incidents in March
  Current: 1 (in Jan), 0 (in Feb) | Target: 0 in March | Progress: 80%

**KR4**: Vault storage < 200 MB (Bronze healthy zone)
  Current: 173 MB | Target: < 200 MB | Progress: 85%

**Overall OKR Score**: 82% → ON_TRACK

**Quarterly Review**: 2026-03-31
```

---

## Progress Tracking

### How Progress is Measured

```
For OUTCOME goals:
  Progress % = (current_value - start_value) / (target_value - start_value) × 100

  Example: AI accuracy 78% → target 95%
  Current: 89%
  Progress = (89 - 78) / (95 - 78) × 100 = 11/17 × 100 = 64.7%

For PROCESS goals:
  Progress % = (days_compliant / total_days) × 100
  Streak = consecutive_compliant_days

  Example: Daily Dashboard review (20/28 days compliant)
  Progress = 20/28 × 100 = 71.4%
  Streak = 7 (current streak)

For SYSTEM goals:
  Progress % = (target - current_deficit) / target × 100
  OR simply: threshold maintained = 100%, threshold breached = 0%

  Example: Uptime > 98%
  Current: 97.8% → below target → progress toward target
  Time in compliance: 25/28 days = 89.3%
```

### Drift Detection

```
Calculate expected progress at this point in time:

Expected progress = (days_elapsed / total_days) × 100

Compare to actual progress:
  IF actual >= expected               → ON_TRACK (green)
  IF actual >= expected - 10%         → SLIGHT_DRIFT (yellow)
  IF actual >= expected - 25%         → AT_RISK (orange)
  IF actual < expected - 25%          → OFF_TRACK (red)

Example:
  Goal: 90-day goal
  Day 30 elapsed (33% of time used)
  Expected progress: 33%
  Actual progress: 25%
  Gap: -8% → SLIGHT_DRIFT (yellow — watch but not alarming)

Drift alerts:
  SLIGHT_DRIFT → INFO log + mention in weekly report
  AT_RISK      → WARNING notification + recommend action
  OFF_TRACK    → HIGH notification + escalate to human + recovery plan
```

---

## Milestone Management

### Milestone States

```
UPCOMING   → Not yet due, not started
IN_PROGRESS→ Active work happening toward this milestone
ON_TRACK   → Work in progress, expected to hit deadline
AT_RISK    → Behind, intervention may be needed
ACHIEVED   → Milestone completed on or before due date
MISSED     → Due date passed, not completed
DEFERRED   → Moved to new date (with reason)
```

### Milestone Review Process

```
Weekly milestone review (every Monday):

For each UPCOMING or IN_PROGRESS milestone:
  1. Check due date vs today
  2. Assess current progress toward this milestone
  3. Identify tasks needed to hit milestone
  4. Update status (ON_TRACK / AT_RISK / MISSED)
  5. If AT_RISK → create recovery plan
  6. If MISSED → document reason, defer or abandon

Milestone health summary for Dashboard:
  ✓ M1 Baseline — ACHIEVED (Feb 7)
  → M2 First improvement — ON_TRACK (due Feb 21, progress 78%)
  ⚠️ M3 Halfway target — AT_RISK (due Mar 1, behind by 3%)
  ○ M4 Final push — UPCOMING (due Mar 25)
```

---

## Goal Status Determination

### Status Rules

```
ACTIVE    → Goal created, work not yet assessed
ON_TRACK  → Progress ≥ expected AND no missed milestones
AT_RISK   → Progress 10-25% behind expected OR 1 milestone missed
OFF_TRACK → Progress > 25% behind expected OR 2+ milestones missed
ACHIEVED  → All success criteria GREEN AND final milestone reached
ABANDONED → Human decided to stop pursuing this goal
DEFERRED  → Goal paused, will resume at future date

Auto-update status weekly based on drift calculation
Always notify human when status degrades (ON_TRACK → AT_RISK)
Always celebrate when status improves (AT_RISK → ON_TRACK)
```

---

## Goal Dashboard Section

```markdown
## Goals Overview

**Updated**: 2026-02-16
**Active Goals**: 5
**On Track**: 3
**At Risk**: 1
**Achieved This Quarter**: 2

---

### Active Goals

| Goal                           | Type    | Due      | Progress | Status    |
|--------------------------------|---------|----------|----------|-----------|
| AI Accuracy ≥ 95%              | Learning| Mar 31   | 65%      | ON_TRACK  |
| Watcher Uptime ≥ 98%          | System  | Mar 31   | 91%      | ON_TRACK  |
| Process 100% Inbox Same-Day   | Process | Ongoing  | 87%      | ON_TRACK  |
| Vault < 200 MB (Bronze)        | System  | Mar 31   | 85%      | AT_RISK   |
| Q1 OKR: Silver Readiness       | Business| Mar 31   | 82%      | ON_TRACK  |

---

### Milestone This Week

| Milestone                  | Goal            | Due    | Status     |
|----------------------------|-----------------|--------|------------|
| First improvement measured | AI Accuracy     | Feb 21 | ON_TRACK   |
| 30-day uptime check        | Watcher Uptime  | Feb 20 | ON_TRACK   |

---

### Recently Achieved

| Goal                           | Achieved   | Result              |
|--------------------------------|------------|---------------------|
| Zero incidents in February     | Feb 16     | 0 CRITICAL events   |
| Baseline established           | Feb 07     | All metrics logged  |
```

---

## Recovery Plans

### When a Goal is AT_RISK

```
Trigger: Status changes to AT_RISK or OFF_TRACK

Step 1: Diagnose the gap
  → How far behind are we?
  → What caused the drift? (missed tasks, slower than expected, external?)
  → Is the target still realistic?

Step 2: Generate recovery options
  Option A: Accelerate effort
    → Prioritize goal-related tasks above others
    → Add resources or reduce scope elsewhere
    → Estimated catch-up time: {n} days

  Option B: Adjust milestone dates
    → Keep final target, shift intermediate milestones
    → Viable if gap is not too large
    → Updated timeline: {new dates}

  Option C: Revise the target
    → Reduce ambition to what is achievable
    → Document the revised target and reason
    → New target: {revised value}

  Option D: Abandon the goal
    → If recovery would require unacceptable trade-offs
    → Document rationale clearly
    → Capture lessons learned

Step 3: Present to human (Decision Skill)
  → AT_RISK → notify, present options, recommend
  → OFF_TRACK → escalate, recovery plan required

Step 4: Execute chosen option
  → Update goal file with new plan
  → Adjust linked tasks and milestones
  → Monitor weekly for recovery
```

---

## Goal Review Cadence

### Daily (Automated)
```
- Check system goals against real-time metrics
- Update progress journal entry for active goals
- Flag any milestone due within 48 hours
- Alert if any goal transitions to AT_RISK
```

### Weekly (Monday Morning)
```
- Calculate progress % for all goals
- Run drift detection against expected progress
- Review milestone status for the week
- Update goal statuses
- Add weekly summary to progress journal
- Generate goal section for weekly report
- Celebrate any milestones achieved this week
```

### Monthly (1st of Month)
```
- Comprehensive goal review for all active goals
- Archive achieved goals to Knowledge/decisions/
- Initiate recovery plans for OFF_TRACK goals
- Set new monthly milestones
- Review if any goals should be abandoned
- Generate monthly goal report
```

### Quarterly (End of Quarter)
```
- OKR scoring and retrospective
- Close out quarterly goals (ACHIEVED or ABANDONED)
- Set next quarter's OKRs
- Extract lessons from both achieved and failed goals
- Archive full goal history
- Update Company_Handbook with key learnings
```

---

## Achieved Goal Record

```markdown
# Goal Achieved: Zero CRITICAL Incidents in February

**GOAL-2026-003**
**Achieved**: 2026-02-28
**Duration**: 28 days (full month)
**Final status**: ACHIEVED

---

## What Was Achieved

Zero CRITICAL system incidents in February 2026.
Previous month (January): 2 CRITICAL incidents.

---

## How It Was Achieved

Key factors:
  - Self-healing playbooks executed successfully for 3 near-misses
  - Monitoring thresholds adjusted after January incidents
  - Optimization Skill switched to emergency mode 2x (prevented escalation)
  - Disk managed at < 85% all month (archive ran twice)

---

## Lessons Learned

1. Early warning (WARNING alerts) consistently preceded CRITICAL events
   → Action: Lower WARNING threshold from 80% to 75% disk
2. Monday mornings had highest incident risk (file volume spike)
   → Action: Pre-run optimization check Sunday night

---

## What to Do Differently

- Run preventive checks before high-volume periods
- Lower alert thresholds earlier than feels necessary

---

## Archived

**Archived to**: Knowledge/decisions/2026-02.md
**Achievement noted in**: Dashboard, Weekly Report, Monthly Report
```

---

## Integration with Other Skills

### With Analytics Skill
```
analytics → supplies → goal-tracking with:
  Current metric values for progress calculation
  Trend data for forecast accuracy
  Anomaly alerts that may explain drift
  Historical baselines for realistic target setting
```

### With Reporting Skill
```
goal-tracking → feeds → reporting with:
  Goal status section for weekly/monthly reports
  OKR scores for quarterly reports
  Achievement records for celebration
  At-risk goals for exception reports
```

### With Task Management Skill
```
goal-tracking → creates tasks via → task-management for:
  Weekly goal-related action items
  Milestone delivery tasks
  Recovery plan tasks
  Goal review tasks (scheduled)
```

### With Scheduler Skill
```
scheduler → triggers → goal-tracking for:
  Daily progress checks (automated)
  Weekly goal reviews (Monday)
  Monthly milestone reviews (1st)
  Quarterly OKR scoring (end of quarter)
```

### With Notification Skill
```
goal-tracking → triggers → notification for:
  Goal status degradation (AT_RISK → HIGH alert)
  Milestone achieved (INFO — celebrate)
  Goal achieved (INFO — celebrate)
  Goal OFF_TRACK (CRITICAL if time-sensitive)
  Milestone due within 48 hours (WARNING)
```

### With Decision Skill
```
goal-tracking → uses → decision for:
  Choosing recovery option when AT_RISK
  Deciding whether to abandon an OFF_TRACK goal
  Prioritizing goal-related tasks above others
  Setting realistic targets during goal creation
```

### With Learning Skill
```
goal-tracking → feeds → learning with:
  Which behaviors drove goal achievement
  Which patterns caused drift
  Time estimates for similar goals in future
  Success factors to replicate
```

### With Knowledge Base Skill
```
goal-tracking → writes → knowledge-base on:
  Achieved goals (decision records)
  Lessons from failed or adjusted goals
  Effective milestone structures for goal types
  OKR patterns that worked
```

---

## Best Practices

### Setting Goals
```
DO:
  - Make targets specific and measurable (not "improve accuracy")
  - Set a baseline before setting a target
  - Break every goal into milestones (max 30-day gaps)
  - Assign clear ownership (human vs AI vs shared)
  - Define exactly what ACHIEVED looks like upfront
  - Set goals that stretch but are achievable (70-80% confidence)

DON'T:
  - Set goals without measurable success criteria
  - Skip the milestone structure (makes drift invisible)
  - Set too many goals simultaneously (max 5 active)
  - Set goals that depend entirely on external factors
  - Set vague goals like "get better at X"
```

### Tracking Goals
```
DO:
  - Update progress journal every week without fail
  - Run drift detection proactively (don't wait for problems)
  - Alert human when status degrades (don't hide bad news)
  - Celebrate milestones (recognition drives motivation)
  - Capture lessons as you go (not just at the end)

DON'T:
  - Go more than 7 days without updating a goal
  - Ignore AT_RISK status (it becomes OFF_TRACK fast)
  - Adjust the target downward silently (be transparent)
  - Mark goals ACHIEVED before all criteria are green
  - Abandon goals without documenting the reason
```

---

## Quick Reference: Goal Status → Action

```
Status      | Action                                | Notification
------------|---------------------------------------|-------------
ACTIVE      | Establish baseline, create milestones | INFO
ON_TRACK    | Monitor weekly, update journal        | INFO (weekly)
SLIGHT_DRIFT| Watch closely, mention in report      | INFO
AT_RISK     | Recovery plan, present options        | WARNING + human
OFF_TRACK   | Escalate, recovery mandatory          | HIGH + human
ACHIEVED    | Celebrate, archive, extract lessons   | INFO (celebration)
ABANDONED   | Document reason, archive, learn       | INFO (notify)
DEFERRED    | Set new date, note reason, reschedule | INFO
```

---

**Status**: Production Ready
**Priority**: HIGH (Ensures AI Employee moves toward meaningful outcomes)
**Goal Types**: 5 (Outcome, Process, Learning, System, Business)
**Hierarchy**: Vision → Strategic → Quarterly OKR → Monthly → Weekly → Daily
**Review Cadence**: Daily (auto), Weekly (Monday), Monthly (1st), Quarterly
**Max Active Goals**: 5 (focus over breadth)
**Drift Alert**: AT_RISK at -10%, OFF_TRACK at -25% vs expected progress

*Good goal tracking = Knowing exactly where you are, where you need to be, and what to do next*
