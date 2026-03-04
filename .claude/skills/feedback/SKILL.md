# Feedback Skill

**Purpose**: Collect, process, store, and act on feedback from humans to continuously improve AI Employee behavior
**Storage**: Markdown-based feedback records, correction logs, preference profiles, improvement tracking
**Scope**: Human corrections, approvals, rejections, explicit instructions, implicit signals, satisfaction tracking

---

## Core Functions

### 1. Capture Feedback
Detect and record all signals — explicit and implicit — from human interactions

### 2. Classify Feedback
Identify what type of feedback it is and what it applies to

### 3. Process Signals
Convert raw feedback into actionable improvement data

### 4. Route to Skills
Send feedback to the right skill — Learning, Decision, Knowledge Base, Communication

### 5. Track Impact
Measure whether acting on feedback actually improved things

### 6. Close the Loop
Confirm to the human that their feedback was received and applied

---

## Feedback Signal Types

### Signal 1: Explicit Positive (Approval)
```
Definition: Human directly accepts or confirms AI output

Detection patterns:
  - Human approves a draft without changes → task status = APPROVED
  - Human marks task as "looks good"
  - Human uses AI output verbatim (no edits)
  - Human explicitly says "yes", "correct", "that's right"
  - Approval Handling records APPROVED status

Strength: MEDIUM (positive but could be passive acceptance)
Action:   Reinforce the behavior that led to this output
          Increase confidence on any rules applied
          Log as positive signal in feedback.md
```

### Signal 2: Explicit Negative (Rejection)
```
Definition: Human directly refuses or cancels AI output

Detection patterns:
  - Human sets status = REJECTED on draft
  - Human cancels a proposed action
  - Human explicitly says "no", "wrong", "don't do this"
  - Human deletes AI-created file
  - Human overrides entire AI recommendation

Strength: HIGH (clear negative signal)
Action:   Record what was rejected and why (if stated)
          Reduce confidence on rules applied
          Flag for Learning Skill review
          After 3 rejections of same type → propose rule change
          Log as strong negative signal in feedback.md
```

### Signal 3: Correction
```
Definition: Human changes something AI did without fully rejecting it

Detection patterns:
  - Human edits priority field in task file
  - Human changes category of a task
  - Human rewrites AI summary
  - Human adjusts email draft before approving
  - Human changes status or owner

Strength: HIGH (specific, actionable signal)
Action:   Record exact field changed: what AI set vs what human set
          Extract the correction as a learning signal
          Feed to Learning Skill as pattern observation
          Update entity profile if correction is sender-specific
          Log with full before/after context
```

### Signal 4: Instruction
```
Definition: Human explicitly tells AI to do something differently

Detection patterns:
  - Human writes note in task file or Dashboard
  - Human sends direct command: "always do X for Y"
  - Human adds rule to Company_Handbook.md
  - Human says "next time, please..."
  - Human corrects AI in conversation

Strength: VERY HIGH (deliberate, explicit teaching)
Action:   Parse instruction immediately
          Create knowledge entry with confidence = HIGH
          Apply to all future similar situations
          Confirm receipt: "Understood — will do X for Y going forward"
          Log as authoritative instruction
```

### Signal 5: Override
```
Definition: Human takes manual action instead of using AI output

Detection patterns:
  - Human processes a file manually that AI should have handled
  - Human creates a task file directly
  - Human moves files without using AI workflow
  - Human sends email manually instead of using AI draft

Strength: VERY HIGH (AI failed to meet expectations here)
Action:   Flag as strong negative signal
          Investigate: why did human bypass AI?
          Was AI output wrong? Too slow? Not produced?
          Propose improvement to prevent future bypass
          Log as override event with investigation note
```

### Signal 6: Implicit Positive (No Action Needed)
```
Definition: Human takes no corrective action — AI output is accepted passively

Detection patterns:
  - Task completed, human does not change anything
  - Report generated, no feedback given
  - Email sent, no complaint received
  - Several days pass with no corrections

Strength: LOW (passive — could be missed, not necessarily endorsed)
Action:   Treat as weak positive signal
          Do not increase confidence aggressively on single passive signal
          Accumulate: 5+ passive approvals → treat as medium positive
          Log as implicit approval in feedback.md
```

### Signal 7: Escalation Request
```
Definition: Human asks AI to involve someone else or handle differently

Detection patterns:
  - "Can you cc Bob on this?"
  - "This should go to Alice first"
  - "Flag this as HIGH, not MEDIUM"
  - "Get approval from finance before proceeding"

Strength: MEDIUM (process correction, not quality rejection)
Action:   Execute the specific request immediately
          Update routing knowledge for this scenario
          Feed to Learning Skill as routing pattern
          Log as routing feedback
```

---

## Feedback Capture Methods

### Method 1: File-Based Detection
```
Monitor for changes in task files:

Check every task file in Needs_Action/ and Done/:
  - Was priority field changed since AI set it?
  - Was status changed by human vs AI?
  - Was owner field changed?
  - Were action items added or removed?
  - Was the summary section rewritten?

Compare: current file state vs last_AI_written state
IF difference detected → classify and log as correction

Check interval: Every 5 minutes on active task files
```

### Method 2: Approval Outcome Tracking
```
After every approval request:
  Track: APPROVED / REJECTED / MODIFIED

IF MODIFIED:
  Compare original vs approved version
  Extract all differences
  Classify each diff (tone change, content change, data change)
  Feed each diff as correction signal

IF REJECTED:
  Record: what type of content was rejected
  Record: reason if human provided one
  Classify rejection type (wrong content, wrong timing, wrong format)
```

### Method 3: Explicit Feedback Form
```
Location: Common/AI_Employee_Vault/Plans/feedback_form.md

Format:
# Feedback for AI Employee

**Date**: [fill in]
**About**: [task ID or general]

## What went well
[Write here]

## What could be better
[Write here]

## Specific change requests
[Write here — "Please always do X when Y"]

## Priority of this feedback
[ ] Low — would be nice
[ ] Medium — would improve my day
[ ] High — this is blocking me
[ ] Critical — this must change

Human fills this out → AI detects update → processes feedback
```

### Method 4: Dashboard Annotation
```
Human can add notes directly to Dashboard.md:

## Feedback Notes (Human)
- 2026-02-16: Alice's files should always be HIGH — currently getting MEDIUM sometimes
- 2026-02-15: Email drafts are too formal — please use casual professional tone
- 2026-02-14: Stop creating tasks for files from newsletter@spam.com

AI scans Dashboard feedback section on every read
Processes annotations as explicit instructions
Marks annotations as "processed" when acted on
```

---

## Feedback Classification

### Classification Dimensions

```
Dimension 1: Scope
  GLOBAL    → Applies to all future situations ("always use bullet points")
  ENTITY    → Applies to specific person/company ("for Alice, always HIGH")
  FILE_TYPE → Applies to specific file type ("for invoices, always flag amount")
  ONE_TIME  → Only for this specific instance (no rule change)

Dimension 2: Domain
  PRIORITY    → How urgency is assessed
  CATEGORY    → How content is classified
  FORMAT      → How output is structured
  TONE        → How messages are written
  ROUTING     → Where tasks or messages go
  TIMING      → When things happen
  CONTENT     → What information is included
  SECURITY    → What is flagged or blocked

Dimension 3: Strength
  AUTHORITATIVE → Explicit instruction ("always do X")
  STRONG        → Repeated correction or direct rejection
  MODERATE      → Single correction or modification
  WEAK          → Implicit acceptance or passive approval

Dimension 4: Sentiment
  POSITIVE → Approval, confirmation, praise
  NEGATIVE → Rejection, correction, complaint
  NEUTRAL  → Request, routing, structural change
```

### Classification → Action Map

```
AUTHORITATIVE + GLOBAL:
  → Create AUTHORITATIVE knowledge entry immediately
  → Apply to Company_Handbook.md if relevant
  → Activate rule immediately (no waiting for pattern)
  → Confirm to human: "Got it — applying immediately"

STRONG + ENTITY:
  → Update entity profile in Knowledge/people/
  → Create OBSERVED lesson (3 corrections = CONFIDENT)
  → Propose rule to Learning Skill
  → Apply tentatively from next interaction

MODERATE + FILE_TYPE:
  → Log as observation
  → If 3+ similar corrections → propose rule
  → Apply tentatively while building confidence

WEAK + ONE_TIME:
  → Log only
  → Do not change behavior yet
  → Monitor for recurrence
```

---

## Feedback Record Format

```markdown
# Feedback Record

**ID**: FB-20260216-007
**Captured**: 2026-02-16 14:30
**Type**: Correction
**Strength**: STRONG
**Scope**: ENTITY
**Domain**: PRIORITY

---

## Raw Signal

**Task**: TASK-20260216-014 (report_q1.pdf from Alice)
**AI set**: Priority = MEDIUM
**Human changed to**: Priority = HIGH
**Changed at**: 2026-02-16 14:30 (15 minutes after task created)
**Human comment**: None provided

---

## Classification

Scope:   ENTITY (specific to Alice Johnson)
Domain:  PRIORITY (priority assignment)
Strength: STRONG (5th correction of same type)
Pattern: alice@company.com → MEDIUM corrected to HIGH (5/5 times)

---

## Action Taken

1. Logged as observation +1 (PAT-007 now at 5 occurrences)
2. Confidence: 92% → ESTABLISHED threshold reached
3. Rule proposal: RULE-PROP-007 drafted for human review
4. Entity profile updated: Alice priority note added
5. Learning Skill notified
6. Human notification: "I've noticed Alice's files are always HIGH
   priority — I'll propose a rule to handle this automatically."

---

## Follow-Up

Rule proposed: RULE-PROP-007 (pending human approval)
Expected approval: 2026-02-17
If approved: Will auto-assign HIGH to Alice's files going forward
Impact estimate: Saves ~1 correction per Alice file (avg 3/week)
```

---

## Feedback Processing Pipeline

```
Step 1: CAPTURE
  Detect feedback signal from one of 4 methods
  Record raw signal immediately (timestamp, source, content)
  Do not process yet — just capture

Step 2: CLASSIFY
  Determine: type, scope, domain, strength, sentiment
  Check: is this a duplicate of a recent feedback?
  IF duplicate within 24h → merge with existing record

Step 3: STORE
  Write to Knowledge/feedback.md (permanent log)
  Write to Logs/observations.log (Learning Skill input)
  Update relevant entity profile if entity-specific

Step 4: ROUTE
  Send to appropriate skill based on classification:
    PRIORITY feedback    → Learning Skill (priority rules)
    FORMAT feedback      → Communication Skill (templates)
    ROUTING feedback     → Delegation Skill (handler rules)
    SECURITY feedback    → Security Skill (threat rules)
    PROCESS feedback     → Workflow Skill (workflow rules)
    ENTITY feedback      → Knowledge Base (person profile)
    GENERAL feedback     → Learning Skill (general rules)

Step 5: RESPOND
  Close the loop with human:
    Simple correction → log silently (no response needed)
    Instruction → confirm: "Understood — will do X going forward"
    Rejection → acknowledge: "Noted — I'll handle differently next time"
    Explicit feedback form → full response with action plan

Step 6: TRACK
  Monitor if the feedback was acted on correctly
  Compare AI behavior before vs after feedback applied
  Report improvement in weekly analytics
```

---

## Feedback Log

### Location
```
Common/AI_Employee_Vault/Knowledge/feedback.md
```

### Log Format

```markdown
# Feedback Log

**Updated**: 2026-02-16 14:30
**Total Feedback This Month**: 47
**Acted On**: 43 (91.5%)
**Pending Action**: 4
**Rules Proposed from Feedback**: 6
**Rules Activated from Feedback**: 4

---

## This Week's Feedback

| Date  | ID       | Type        | Domain   | Scope  | Strength | Status   |
|-------|----------|-------------|----------|--------|----------|----------|
| Feb 16| FB-014   | Correction  | Priority | Entity | STRONG   | ACTED_ON |
| Feb 16| FB-013   | Approval    | Format   | Global | WEAK     | LOGGED   |
| Feb 15| FB-012   | Instruction | Tone     | Global | AUTH     | APPLIED  |
| Feb 15| FB-011   | Rejection   | Content  | Entity | STRONG   | REVIEW   |
| Feb 14| FB-010   | Override    | Routing  | Type   | VERY_HIGH| INVEST.  |

---

## Pending Action

| ID     | Feedback                           | Waiting For          |
|--------|------------------------------------|-----------------------|
| FB-011 | Email tone too formal (Alice)      | Rule proposal review |
| FB-010 | Human bypassed AI for invoices     | Root cause analysis  |
| FB-009 | Priority correction (Bob)          | 3rd occurrence (2/3) |
| FB-008 | Summary too long (general)         | Pattern confirmation |
```

---

## Satisfaction Tracking

### Satisfaction Signals

```
High satisfaction signals:
  - No corrections needed for 7+ consecutive tasks
  - Human explicitly says "great", "perfect", "exactly right"
  - Approval rate > 90% this week
  - Human override rate dropping week over week
  - Feedback form submitted with positive comments

Low satisfaction signals:
  - Correction rate > 20% this week
  - Human override rate increasing
  - Multiple rejections in same domain within 48h
  - Human submits feedback form with critical items
  - Human bypasses AI for more than 2 tasks in a day
```

### Weekly Satisfaction Score

```
Score (0-100):

Base:           50 points

Add:
  +2 per task approved without correction (max +30)
  +5 per explicit positive comment
  +5 per week with no overrides
  +3 per feedback acted on within 24h

Subtract:
  -3 per correction (deduct per instance)
  -5 per rejection
  -10 per override (human bypassed AI)
  -5 per feedback unacted on after 48h
  -10 per explicit negative comment

Interpretation:
  80-100: EXCELLENT — AI meeting expectations well
  60-79:  GOOD — Minor improvements needed
  40-59:  FAIR — Noticeable gaps, active improvement needed
  20-39:  POOR — Significant misalignment, review with human
  0-19:   CRITICAL — AI not meeting needs, immediate intervention

Report score in weekly analytics
Alert human if score drops below 40 (POOR)
```

---

## Closing the Loop

### Response Templates

#### After Simple Correction (Silent)
```
No response needed for routine corrections.
Just log and act.
Human does not need confirmation for minor field changes.
```

#### After Repeated Correction (Propose Rule)
```
Dashboard note:
  "I've noticed [FIELD] for [ENTITY/TYPE] has been corrected [N] times.
   I've drafted a rule to handle this automatically going forward.
   Please review: Knowledge/rules_proposed.md → RULE-PROP-{id}"
```

#### After Explicit Instruction
```
Dashboard note:
  "Understood. I'll [INSTRUCTION] for [SCOPE] going forward.
   This is now saved as a rule and will apply from the next task.
   Rule reference: KB-{id}"
```

#### After Rejection
```
Dashboard note:
  "Noted — the [TYPE] for [TASK] was not right.
   I've logged this feedback and will handle it differently next time.
   If you have a moment to say what was wrong, that helps me improve faster."
```

#### After Override (Investigation)
```
Dashboard note:
  "I noticed you handled [TASK] manually.
   I want to make sure I can do this for you next time.
   Was there something wrong with my approach, or did I not produce output?
   Your input here will help me improve."
```

#### After Feedback Form Submission
```
Dashboard note:
  "Thank you for the feedback on [DATE].
   Here's what I'm doing with it:
     1. [Item 1] → [Action being taken]
     2. [Item 2] → [Action being taken]
     3. [Item 3] → [Needs more info before acting — will watch]
   I'll report back on improvement in next week's report."
```

---

## Feedback-Driven Improvement Tracking

### Before / After Comparison

```
For each feedback acted on, measure before vs after:

Example: "Email tone too formal" feedback (Feb 15)

Before (Feb 1-14):
  Email drafts modified by human: 8/10 (80% modification rate)
  Human comments: "too stiff", "not like me"

After rule applied (Feb 15-28):
  Email drafts modified by human: 2/10 (20% modification rate)
  Human comments: None (passive approval)

Improvement: 60% reduction in email draft modifications
Feedback effectiveness: HIGH

Report in weekly analytics:
  "Email tone feedback from Feb 15 reduced draft modification rate by 60%"
```

### Feedback Impact Metrics

```
Track monthly:
  Total feedback received:           {n}
  Feedback acted on:                 {n} ({%})
  Feedback that improved a metric:   {n} ({%})
  Average time to act on feedback:   {hours}
  Satisfaction score trend:          {direction}
  Correction rate trend:             {direction}
  Override rate trend:               {direction}
  Rules created from feedback:       {n}
  Rules performing above 80%:        {n} ({%})
```

---

## Integration with Other Skills

### With Learning Skill
```
feedback → primary input for → learning:
  All correction signals (what AI got wrong)
  All approval signals (what AI got right)
  Pattern observations for rule proposals
  Strength signals for confidence calculation
```

### With Knowledge Base Skill
```
feedback → updates → knowledge-base:
  Person profiles (entity-specific corrections)
  Active rules (approved from feedback)
  Authoritative instructions (explicit human teaching)
  Decision records (rejected actions logged)
```

### With Communication Skill
```
feedback → improves → communication via:
  Tone corrections → update tone profiles
  Length corrections → update length rules
  Format corrections → update template defaults
  Close-the-loop messages written by Communication Skill
```

### With Analytics Skill
```
analytics → measures → feedback effectiveness:
  Satisfaction score weekly trend
  Correction rate before/after rule activation
  Override rate trend
  Feedback response time
```

### With Monitoring Skill
```
monitoring → watches for → feedback signals:
  Task file changes (correction detection)
  Dashboard annotation changes
  Approval outcome tracking
  Override events (human doing things manually)
```

### With Goal Tracking Skill
```
goal-tracking → uses → feedback data:
  Satisfaction score as a tracked metric
  Correction rate as quality KPI
  Override rate as automation coverage signal
  Feedback volume as engagement indicator
```

### With Reporting Skill
```
reporting → includes → feedback section in:
  Weekly report: feedback received, rules proposed, improvements
  Monthly report: satisfaction trend, top corrections, impact
  Exception report: satisfaction below threshold, override spike
```

---

## Best Practices

### DO
```
- Capture every feedback signal immediately (never delay)
- Classify accurately — wrong classification wastes effort
- Close the loop — humans need to know feedback was heard
- Act on strong signals quickly (< 24 hours)
- Track impact — did the feedback actually help?
- Celebrate when feedback leads to clear improvement
- Ask for clarification when rejection reason is unclear
- Prioritize feedback that affects the most frequent scenarios
```

### DON'T
```
- Ignore weak signals (they accumulate into patterns)
- Over-react to single corrections (wait for 3+ for rule changes)
- Change behavior based on one-time anomalies
- Let feedback pile up unprocessed (max 48 hours)
- Apply global rule from entity-specific feedback without checking
- Treat all feedback with equal urgency (classify first)
- Close the loop with lengthy explanations (keep it brief)
- Lose feedback data — it is the training signal for improvement
```

---

## Quick Reference: Signal → Response

```
Signal Type         | Strength  | Immediate Action           | Learning Action
--------------------|-----------|----------------------------|------------------
Approval (explicit) | MEDIUM    | Log positive signal        | Reinforce rule
Approval (implicit) | LOW       | Log (accumulate)           | Track count
Rejection           | HIGH      | Acknowledge + log          | Review rules (3x)
Correction          | HIGH      | Log before/after + route   | Feed to Learning
Instruction         | VERY HIGH | Apply now + confirm        | Create AUTH rule
Override            | VERY HIGH | Investigate + log          | Root cause fix
Escalation request  | MEDIUM    | Execute + log routing      | Update routing rule
Feedback form       | VARIES    | Full response + action plan| Prioritize by score
```

---

**Status**: Production Ready
**Priority**: HIGH (Primary signal for all AI improvement)
**Signal Types**: 7 (Approval, Rejection, Correction, Instruction, Override, Implicit, Escalation)
**Capture Methods**: 4 (File detection, Approval tracking, Feedback form, Dashboard annotation)
**Response Time**: < 24 hours for STRONG signals, < 48 hours for all
**Satisfaction Score**: Tracked weekly, alert if below 40/100

*Good feedback = AI Employee that listens, learns, and visibly improves every week*
