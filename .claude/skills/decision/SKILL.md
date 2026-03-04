# Decision Skill

**Purpose**: Make clear, consistent, explainable decisions — and know when NOT to decide alone
**Storage**: Markdown-based decision logs, decision trees, escalation records
**Scope**: Priority decisions, routing decisions, approval triggers, ambiguity resolution, confidence-gated autonomy

---

## Core Functions

### 1. Evaluate Options
Weigh available choices using defined criteria

### 2. Apply Decision Rules
Use known rules from Company_Handbook and learned rules to decide

### 3. Assess Confidence
Know how sure the AI is — and act accordingly

### 4. Escalate Uncertainty
Route low-confidence decisions to human before acting

### 5. Explain Decisions
Always document why a decision was made

### 6. Learn from Outcomes
Feed decision results back to the Learning Skill

---

## Decision Framework

```
Every decision follows this sequence:

1. IDENTIFY     → What is the decision to be made?
2. GATHER       → What information is available?
3. CHECK RULES  → Does an existing rule cover this?
4. EVALUATE     → Score each option against criteria
5. ASSESS       → How confident is the AI in this choice?
6. DECIDE       → If confident enough → choose and log
7. ESCALATE     → If not confident enough → ask human
8. EXPLAIN      → Record the reasoning, not just the outcome
9. OBSERVE      → Track if the decision turned out correct
```

---

## Decision Types

### Type 1: Routing Decision
```
Question: Where should this file/task go?

Examples:
  - Which folder does this file belong in?
  - Is this a task or just an FYI?
  - Which workflow should handle this?
  - Which skill is responsible?

Inputs:   file type, sender, content summary, priority
Rules:    file-understanding, context, learned rules
Autonomy: HIGH (low risk, reversible)
```

### Type 2: Priority Decision
```
Question: How urgent is this?

Examples:
  - Is this HIGH, MEDIUM, or LOW priority?
  - Should this jump the queue?
  - Does this need same-day processing?

Inputs:   sender profile, content keywords, file type, time of day
Rules:    Company_Handbook priority rules, learned priority rules
Autonomy: HIGH for known senders, MEDIUM for unknowns
```

### Type 3: Action Decision
```
Question: What should be done with this?

Examples:
  - Should the AI summarize, flag, or forward this?
  - Does this need a response?
  - Should a task be created or just logged?

Inputs:   content analysis, sender intent, context, history
Rules:    Company_Handbook action rules
Autonomy: MEDIUM (depends on action impact)
```

### Type 4: Approval Decision
```
Question: Does this need human sign-off before proceeding?

Examples:
  - Is this email safe to send?
  - Should this file be deleted?
  - Is this payment amount within normal range?

Inputs:   risk level, action type, amount/scope, sender
Rules:    Security Skill rules, Approval Handling rules
Autonomy: LOW — approval decisions almost always need human
```

### Type 5: Escalation Decision
```
Question: Should the AI handle this or involve a human?

Examples:
  - Is this within the AI's competence?
  - Is the confidence too low to act safely?
  - Does this break any established pattern?
  - Is the potential downside too high?

Inputs:   confidence score, risk level, reversibility, urgency
Rules:    Confidence thresholds (see below)
Autonomy: Meta-decision — determines all other autonomy levels
```

### Type 6: Exception Decision
```
Question: What to do when something unexpected happens?

Examples:
  - File is corrupted — process partially or skip?
  - Duplicate task found — merge, link, or ignore?
  - Contradictory instructions — which to follow?
  - Emergency condition — override normal rules?

Inputs:   nature of exception, past similar exceptions, risk
Rules:    Error Recovery, Self-Healing, escalation threshold
Autonomy: LOW — exceptions often warrant human review
```

---

## Decision Rules

### Rule Set 1: Priority Assignment

```
IF sender is in HIGH_PRIORITY_SENDERS list
  → priority = HIGH (always)

IF filename contains any of: [urgent, critical, asap, deadline, emergency]
  → priority = HIGH (override)

IF file_type = .exe OR .bat OR .ps1
  → priority = QUARANTINE (security, not task priority)

IF sender is UNKNOWN AND file is first contact
  → priority = MEDIUM (default for unknowns)

IF content contains financial keywords AND amount > threshold
  → priority = HIGH

IF file arrived after business hours AND sender = known_important
  → priority = HIGH (important enough to send after hours)

IF file_type = .txt AND size < 1KB AND sender = unknown
  → priority = LOW (likely spam or noise)

DEFAULT:
  → priority = MEDIUM
```

### Rule Set 2: Routing

```
IF security_scan = QUARANTINED
  → route to: Inbox/quarantine/ (stop all further processing)

IF file_type IN [.exe, .bat, .cmd, .vbs, .ps1]
  → route to: Inbox/quarantine/ (dangerous type)

IF content_type = invoice AND sender IN known_vendors
  → route to: Plans/accounting/ (Gold+) OR flag HIGH in Needs_Action

IF content_type = meeting_notes OR calendar_event
  → route to: Plans/calendar.md update (Silver+) OR Needs_Action

IF sender = UNKNOWN AND content = SPAM_SIGNALS
  → route to: Done/spam/ (no task created)

IF file is duplicate (hash matches existing file)
  → route to: flag for merge/dedup review

DEFAULT:
  → route to: Needs_Action/ with standard task file
```

### Rule Set 3: Autonomy Gates

```
FULL AUTONOMY (act without asking):
  Conditions:
    - Confidence >= 85%
    - Action is reversible
    - Risk level = LOW
    - Pattern is ESTABLISHED (10+ occurrences)
  Examples:
    - Categorize a known sender's file
    - Assign priority using established rule
    - Move file from Inbox to Done after processing

SUPERVISED AUTONOMY (act but notify human):
  Conditions:
    - Confidence 65–84%
    - Action is reversible
    - Risk level = MEDIUM
  Examples:
    - Process a new file type from a known sender
    - Apply a CONFIDENT (not ESTABLISHED) rule
    - Create a task for an ambiguous file

GATED AUTONOMY (propose, wait for approval):
  Conditions:
    - Confidence 40–64%
    - OR action is irreversible
    - OR risk level = HIGH
  Examples:
    - Send an email on behalf of human
    - Delete a file permanently
    - Post to social media

NO AUTONOMY (always escalate):
  Conditions:
    - Confidence < 40%
    - OR risk level = CRITICAL
    - OR action involves money/legal/security
    - OR action is irreversible AND high impact
  Examples:
    - Approve a payment
    - Modify security rules
    - Respond to legal documents
    - Any first-ever action type
```

---

## Decision Scoring

### How to Score a Decision

```
Step 1: Identify options (usually 2-4 choices)
Step 2: Define criteria relevant to this decision type
Step 3: Score each option on each criterion (1-5 scale)
Step 4: Apply weights
Step 5: Calculate total score
Step 6: Select highest-scoring option IF score gap >= 20%
        Otherwise escalate (too close to call)
```

### Criteria by Decision Type

#### Priority Decision Criteria
```
Criterion          | Weight | Description
-------------------|--------|---------------------------------------------
Sender importance  | 35%    | Is sender known high-priority?
Content urgency    | 30%    | Does content signal urgency?
Time sensitivity   | 20%    | Is there a deadline mentioned?
File type signal   | 15%    | Does file type imply urgency?
```

#### Action Decision Criteria
```
Criterion          | Weight | Description
-------------------|--------|---------------------------------------------
Human benefit      | 30%    | Does this action help the human?
Risk of action     | 30%    | What is the downside if wrong?
Reversibility      | 25%    | Can this be undone if wrong?
Confidence         | 15%    | How sure are we?
```

#### Escalation Decision Criteria
```
Criterion          | Weight | Description
-------------------|--------|---------------------------------------------
Confidence level   | 40%    | How sure is the AI?
Risk if wrong      | 30%    | What is the cost of a bad decision?
Reversibility      | 20%    | Can the decision be undone?
Urgency            | 10%    | Does this need to happen NOW?
```

### Scoring Example

```
Decision: Should report_q1.pdf from Alice be HIGH or MEDIUM priority?

Option A: HIGH priority
Option B: MEDIUM priority

Scores:
Criterion          | Weight | A: HIGH | B: MEDIUM
-------------------|--------|---------|----------
Sender importance  | 35%    | 5 (Alice = known HIGH) | 2
Content urgency    | 30%    | 4 (Q1 report = time-sensitive) | 2
Time sensitivity   | 20%    | 4 (end of quarter) | 3
File type signal   | 15%    | 3 (PDF, standard) | 3

Weighted Score:
  A: (5×0.35)+(4×0.30)+(4×0.20)+(3×0.15) = 1.75+1.20+0.80+0.45 = 4.20
  B: (2×0.35)+(2×0.30)+(3×0.20)+(3×0.15) = 0.70+0.60+0.60+0.45 = 2.35

Score gap: 4.20 vs 2.35 = 44% gap (>20% threshold)
Decision: HIGH priority ✓
Confidence: HIGH (established rule + high score gap)
```

---

## Confidence Assessment

### Confidence Inputs

```
Starts at: 50% (neutral / unknown)

INCREASE confidence when:
  + Exact rule match exists          → +20%
  + ESTABLISHED pattern applies      → +15%
  + CONFIDENT pattern applies        → +10%
  + Known entity with full profile   → +10%
  + Similar past decisions went well → +10%
  + Multiple criteria agree          → +5%

DECREASE confidence when:
  - No matching rule found           → -20%
  - NEW_ENTITY (no history)          → -15%
  - TENTATIVE pattern only           → -10%
  - Contradictory signals present    → -15%
  - Recent exception to this pattern → -10%
  - High-risk action type            → -10%
  - Unusual timing or context        → -5%

Cap: 0% minimum, 98% maximum (never 100% certain)
```

### Confidence → Action Mapping

```
95–98%  → Act silently (no log noise for routine decisions)
85–94%  → Act, log decision with brief reason
65–84%  → Act, log full reasoning, notify human (INFO)
40–64%  → Propose to human, wait for approval
20–39%  → Escalate with recommendation, wait
0–19%   → Escalate with no recommendation, request guidance
```

---

## Decision Log

### Location
```
Common/AI_Employee_Vault/Logs/decisions.log
```

### Entry Format

```
[2026-02-16 09:15] [DECISION] [AUTO] task=FILE_014 type=priority
  Options: [HIGH, MEDIUM, LOW]
  Chosen: HIGH
  Confidence: 92%
  Reason: Rule RULE-001 (Alice = HIGH) + content urgency score 4/5
  Outcome: pending

[2026-02-16 09:20] [DECISION] [ESCALATED] task=FILE_015 type=action
  Options: [summarize, flag_for_review, create_task]
  Escalated: Confidence 48% (new file type from new sender)
  Recommended: flag_for_review (safest option)
  Human response: create_task (2026-02-16 09:35)
  Outcome: correct (human chose reasonable action)

[2026-02-16 14:30] [DECISION] [APPROVED] task=DRAFT_002 type=approval
  Options: [send, hold, reject]
  Submitted for approval: human
  Approved by: human (14:45)
  Outcome: sent, no issues
```

---

## Escalation Format

### When AI Escalates to Human

```markdown
## Decision Needed

**Task**: FILE_015 — unknown_report.xlsx
**Received**: 2026-02-16 09:15
**Sender**: first_contact@newvendor.com (NEW — no history)

**Decision Required**: How should this file be handled?

**AI Assessment**:
- File type: Excel spreadsheet (data)
- Content: Appears to be a sales proposal (detected keywords)
- Sender: Unknown vendor, first contact
- Confidence: 48% (new entity, no established pattern)

**Options**:
| Option | Action | Risk | AI Recommendation |
|--------|--------|------|-------------------|
| A | Create task, process normally | LOW | |
| B | Flag for review, hold | LOW | ← Recommended |
| C | Move to Done without processing | LOW | |
| D | Quarantine (treat as suspicious) | NONE | |

**Why AI is not deciding alone**:
No history with this sender. Content could be a legitimate proposal
or unsolicited sales material. Human judgment needed.

**To respond**: Edit this section or update FILE_015 task file
**Expires**: No expiry (AI will wait)
```

---

## Decision Tree: New Incoming File

```
New file detected in Inbox/
          │
          ▼
Security scan → QUARANTINED? ──YES──→ Quarantine, alert, STOP
          │
          NO
          ▼
Known sender?
  YES → Load entity profile
  NO  → Mark NEW_ENTITY, lower confidence by 15%
          │
          ▼
File type dangerous? (.exe, .bat...)
  YES → Quarantine, alert, STOP
  NO  → Continue
          │
          ▼
Known pattern for this sender + type?
  ESTABLISHED → Apply rule, confidence HIGH, act autonomously
  CONFIDENT   → Apply rule, confidence MEDIUM, log + notify
  TENTATIVE   → Apply with caution, flag for review
  NONE        → Default rules only, confidence LOW
          │
          ▼
Confidence >= 65%?
  YES → Create task, assign priority, process
  NO  → Escalate to human with options
          │
          ▼
Action reversible?
  YES → Proceed with logging
  NO  → Require human approval regardless of confidence
          │
          ▼
Log decision → Observe outcome → Feed back to Learning Skill
```

---

## Decision Quality Metrics

### Track These Weekly

```
Total decisions made:       {n}
  - Fully autonomous:       {n} ({%})
  - Supervised (notified):  {n} ({%})
  - Escalated to human:     {n} ({%})

Decision accuracy:
  - Correct (human confirmed or no correction): {n} ({%})
  - Corrected by human:                         {n} ({%})
  - Overridden by human:                        {n} ({%})

Confidence calibration:
  - Decisions made at 85%+ confidence: {%} accurate
  - Decisions made at 65–84%:          {%} accurate
  - Decisions escalated:               {%} human agreed with AI recommendation

Target:
  Accuracy at 85%+ confidence: >= 95%
  Accuracy at 65–84%:          >= 80%
  Escalation rate:             < 15% of all decisions
```

---

## Integration with Other Skills

### With Context Skill
```
decision → requests → context for:
  Entity profile (who is this from?)
  Historical decisions for similar tasks
  Active learned rules relevant to this decision
  Environmental context (time, mode, urgency)
```

### With Learning Skill
```
decision → feeds → learning after every decision:
  What was decided and why
  Whether it turned out correct
  Confidence at time of decision
  Whether human overrode or confirmed
```

### With Approval Handling Skill
```
decision → triggers → approval-handling when:
  Confidence < 65% AND action is not trivially reversible
  Risk level = HIGH or CRITICAL
  Action type requires mandatory approval (outbound, destructive)
```

### With Security Skill
```
decision → defers to → security for:
  Any decision involving credentials, access, or permissions
  Any file with security concerns raised
  Routing decisions for quarantined files
```

### With Audit Skill
```
decision → logs to → audit:
  Every decision entry (type, options, chosen, confidence, reason)
  Escalation events
  Human overrides
  Decision accuracy retrospectives
```

### With Workflow Skill
```
workflow → calls → decision at:
  Step branching points (which path to take)
  Exception handling (what to do when step fails)
  Human handoff decision (is this worth pausing for?)
```

### With Reporting Skill
```
reporting → includes → decision metrics:
  Weekly decision accuracy in weekly report
  Escalation rate trends in monthly report
  Rules that trigger most decisions
```

---

## Best Practices

### DO
```
- Always log the reason, not just the outcome
- Use confidence scores consistently — don't skip them
- Escalate early rather than guessing wrong
- Present options clearly when escalating
- Track whether decisions turned out correct
- Feed outcomes back to Learning Skill
- Default to safer option when confidence is equal
- Respect hard rules even when confidence is high
```

### DON'T
```
- Make irreversible decisions with low confidence
- Skip the confidence assessment to save time
- Assume a decision is correct because rules said so
- Escalate everything (reduces AI value)
- Decide without logging the reasoning
- Override security rules using decision logic
- Make the same escalation twice without new information
- Treat 85% confidence as certainty (it is not)
```

---

## Quick Reference: Confidence → Behavior

```
Confidence  | Action           | Log Level | Human Notified?
------------|------------------|-----------|----------------
95–98%      | Act silently     | INFO      | No
85–94%      | Act + brief log  | INFO      | No
65–84%      | Act + full log   | INFO      | Yes (INFO)
40–64%      | Propose + wait   | WARNING   | Yes (needs input)
20–39%      | Escalate + hint  | WARNING   | Yes (needs decision)
0–19%       | Escalate, no rec | HIGH      | Yes (urgent input)
```

---

**Status**: Production Ready
**Priority**: CRITICAL (Every autonomous action passes through here)
**Confidence Threshold for Autonomy**: 85% (low-risk) / 65% (supervised)
**Mandatory Escalation**: Irreversible actions, CRITICAL risk, confidence < 40%
**Decision Log**: decisions.log — permanent record of all AI decisions

*Good decisions = AI that acts confidently when it should, and stops when it shouldn't*
