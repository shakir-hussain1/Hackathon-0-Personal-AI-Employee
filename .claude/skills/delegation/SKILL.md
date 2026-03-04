# Delegation Skill

**Purpose**: Assign the right task to the right skill, agent, or human — at the right time
**Storage**: Markdown-based delegation records, assignment logs, capability registry
**Scope**: Skill routing, task handoff, human escalation, load balancing, delegation tracking

---

## Core Functions

### 1. Identify Who Should Handle This
Match task requirements to the best available handler

### 2. Assign Tasks
Formally hand off work with full context and instructions

### 3. Track Delegations
Know what was handed off, to whom, and what happened

### 4. Follow Up
Check that delegated work was completed correctly

### 5. Reassign
Redirect tasks when the original handler fails or is unavailable

### 6. Close the Loop
Confirm completion, log outcomes, update records

---

## Delegation Hierarchy

```
Level 0: Fully Automated (no delegation needed)
  → Simple, known tasks handled by a single skill
  → Example: Move file from Inbox to Done

Level 1: Skill-to-Skill Delegation
  → Task requires a different skill's capability
  → Example: Decision Skill delegates priority to Context Skill

Level 2: Workflow Delegation
  → Task requires multiple skills in sequence
  → Delegated to Workflow Skill as orchestrator

Level 3: Human Delegation (Input Needed)
  → AI cannot decide or act alone
  → Task handed to human with full context and options

Level 4: Human Delegation (Full Ownership)
  → Task is outside AI competence entirely
  → Human takes full ownership, AI tracks and reminds

Level 5: External Delegation (Silver+)
  → Task handed to external person or system
  → Example: Email sent to vendor, task in Odoo assigned
```

---

## Capability Registry

### What Each Skill Can Handle

```markdown
# Skill Capability Registry

## file-understanding
Capabilities:
  - Parse markdown task files
  - Read YAML frontmatter
  - Extract status, priority, owner
  - Validate task format
  - Detect file type from extension + content
Accepts: file_path, task_file_path
Returns: metadata, type, status, priority, owner
Best for: Any task involving reading or classifying files

## risk-detection
Capabilities:
  - Detect financial operations
  - Identify legal terms
  - Flag sensitive data
  - Classify risk level (LOW/MEDIUM/HIGH/CRITICAL)
Accepts: content, action_description
Returns: risk_level, risk_reasons, recommendation
Best for: Before any outbound or destructive action

## error-recovery
Capabilities:
  - Retry with backoff
  - Circuit breaker management
  - Checkpoint and resume
  - Graceful degradation
Accepts: error_type, error_context, attempt_count
Returns: recovery_action, retry_schedule
Best for: Any task that fails and needs retry logic

## memory-management
Capabilities:
  - Index vault content
  - Archive old tasks
  - Compress archives
  - Find duplicates
  - Clean vault
Accepts: target_folder, days_threshold, compression_level
Returns: files_archived, space_freed, index_updated
Best for: Storage operations, archival, vault maintenance

## planning
Capabilities:
  - Break complex tasks into steps
  - Detect dependencies
  - Identify critical path
  - Generate checklists
Accepts: goal_description, constraints, deadline
Returns: plan_steps, dependencies, timeline
Best for: Any complex multi-step task

## approval-handling
Capabilities:
  - Submit items for approval
  - Track approval status
  - Handle expiry and escalation
  - Enforce blocking on unapproved actions
Accepts: item_description, approver, expiry_hours
Returns: approval_status (PENDING/APPROVED/REJECTED/EXPIRED)
Best for: Any action requiring human sign-off

## tool-invocation
Capabilities:
  - Safely call external tools and APIs
  - Validate inputs before calling
  - Log outputs
  - Support DRY_RUN mode
Accepts: tool_name, parameters, mode
Returns: tool_output, invocation_log
Best for: Any external API or tool call

## audit
Capabilities:
  - Analyze logs
  - Track failures
  - Measure performance
  - Generate audit reports
Accepts: log_path, period, metric_type
Returns: analysis, failure_list, performance_kpis
Best for: System health review, compliance, reporting

## optimization
Capabilities:
  - Reduce RAM usage
  - Tune check intervals
  - Auto-clean vault
  - Switch operating modes
Accepts: resource_threshold, target_mode
Returns: actions_taken, resources_freed
Best for: Performance issues, disk/RAM pressure

## scheduler
Capabilities:
  - Schedule recurring tasks
  - Manage task queue
  - Handle missed jobs
  - Priority-based execution
Accepts: task_definition, schedule_type, priority
Returns: schedule_id, next_run_time
Best for: Time-based or condition-based task triggering

## notification
Capabilities:
  - Send Dashboard alerts
  - Write to notification log
  - Trigger Windows toast
  - Create email drafts (Silver+)
Accepts: level, title, message, channels
Returns: notification_sent, channels_used
Best for: Alerting human of events, status, issues

## reporting
Capabilities:
  - Generate daily/weekly/monthly reports
  - Exception reports on demand
  - Trend analysis
  - ASCII charts
Accepts: report_type, period, data_sources
Returns: report_file_path, key_metrics
Best for: Generating human-readable summaries

## self-healing
Capabilities:
  - Detect component failures
  - Execute recovery playbooks
  - Manage escalation
  - Track incidents
Accepts: component_name, failure_type
Returns: recovery_status, actions_taken
Best for: System failures, crashes, stuck processes

## integration
Capabilities:
  - Connect to external services
  - Read from Gmail, Calendar (Silver+)
  - Write to social, accounting (Gold+)
  - Sync with cloud (Platinum+)
Accepts: integration_id, operation, payload
Returns: operation_result, sync_status
Best for: Cross-system data flow

## security
Capabilities:
  - Scan files for threats
  - Detect credential leaks
  - Identify prompt injection
  - Quarantine suspicious files
Accepts: file_path, content, action_description
Returns: scan_result, threat_list, recommended_action
Best for: Any incoming file, any outbound action

## workflow
Capabilities:
  - Run multi-step processes
  - Branch on conditions
  - Handle human handoffs
  - Rollback on failure
Accepts: workflow_id, input_data
Returns: run_id, status, output_data
Best for: Any multi-step coordinated process

## context
Capabilities:
  - Load entity profiles
  - Detect patterns
  - Resolve ambiguity
  - Inject relevant history
Accepts: entity_name, task_type, file_path
Returns: context_package, confidence_level
Best for: Any task needing background knowledge

## learning
Capabilities:
  - Detect patterns from observations
  - Propose new rules
  - Track rule accuracy
  - Update behavior based on feedback
Accepts: observation_log, feedback_signal
Returns: patterns_detected, rules_proposed
Best for: Improving accuracy over time

## decision
Capabilities:
  - Evaluate options with scoring
  - Assess confidence
  - Gate actions by autonomy level
  - Escalate uncertainty
Accepts: decision_type, options, context
Returns: chosen_option, confidence, reasoning
Best for: Any branching point or routing decision

## delegation (this skill)
Capabilities:
  - Match tasks to handlers
  - Assign with context
  - Track delegation outcomes
  - Reassign on failure
Accepts: task_description, requirements, constraints
Returns: handler_assigned, delegation_record
Best for: Orchestrating work across skills and humans
```

---

## Delegation Decision Logic

### How to Choose a Handler

```
Step 1: Extract task requirements
  → What capability is needed?
  → What is the input?
  → What is the expected output?
  → What is the risk level?
  → What is the urgency?

Step 2: Match to capability registry
  → Find all skills that can handle this requirement
  → If multiple matches → rank by:
      1. Specialization (most specific wins)
      2. Current load (less busy wins)
      3. Past accuracy for this task type
      4. Risk level (higher risk → more capable handler)

Step 3: Check handler availability
  → Is the skill currently running?
  → Is there a queue backlog?
  → Is the skill suspended (self-healing event)?

Step 4: Delegate with context
  → Pass: task data + relevant context + instructions
  → Set: expected completion time
  → Log: delegation record

Step 5: If no skill can handle
  → Escalate to human (Level 3 or 4 delegation)
```

### Delegation Matching Table

```
Task Type                    | Primary Handler      | Backup Handler
-----------------------------|----------------------|-------------------
New file arrives             | file-understanding   | workflow (WF-001)
File has security concern    | security             | human (Level 3)
Task needs priority set      | decision             | context
Multi-step process needed    | workflow             | planning
Error occurred               | error-recovery       | self-healing
Disk getting full            | optimization         | memory-management
Human approval needed        | approval-handling    | notification
Report requested             | reporting            | audit
Pattern learning opportunity | learning             | decision
External API call needed     | tool-invocation      | integration
System component down        | self-healing         | human (Level 4)
Context about sender needed  | context              | file-understanding
Alert needed immediately     | notification         | dashboard (direct)
Schedule a recurring task    | scheduler            | workflow
Ambiguous task               | decision             | human (Level 3)
Financial operation          | risk-detection then approval-handling | human
```

---

## Delegation Record Format

```markdown
# Delegation Record: DEL-20260216-014

**Created**: 2026-02-16 09:15
**Task**: Process report_q1.pdf from Alice Johnson
**Delegated by**: Workflow WF-001 Step 2
**Delegated to**: file-understanding
**Level**: Level 1 (Skill-to-Skill)

---

## Assignment Details

**Input provided**:
  - file_path: Inbox/report_q1.pdf
  - sender: alice@company.com
  - context: entity profile for Alice (HIGH priority sender)

**Expected output**:
  - file_type: classified type
  - priority: assigned priority
  - metadata: extracted metadata

**Expected completion**: Within 30 seconds
**Deadline**: 09:15:30 (hard — part of active workflow)

---

## Status Tracking

| Time     | Status      | Detail                              |
|----------|-------------|-------------------------------------|
| 09:15:00 | ASSIGNED    | Delegated to file-understanding     |
| 09:15:04 | ACCEPTED    | Skill acknowledged                  |
| 09:15:06 | COMPLETED   | type=document, priority=HIGH        |

**Outcome**: SUCCESS
**Duration**: 6 seconds
**Output**: file_type=document, priority=HIGH, metadata extracted

---

## Feedback to Learning
  - Delegation success: +1 for file-understanding (document tasks)
  - Duration: 6s (within 30s target) ✓
```

---

## Human Delegation Format

### Level 3: Human Input Needed

```markdown
# Human Task: HT-20260216-003

**Created**: 2026-02-16 10:30
**Priority**: HIGH
**Assigned to**: Human (you)
**Delegated by**: Decision Skill (confidence 42%)
**Reason**: New vendor, first contact, ambiguous content

---

## What Needs Your Decision

A file arrived from an unknown sender that the AI cannot confidently classify.

**File**: unknown_proposal.xlsx
**From**: vendor@newcompany.com (first contact — no history)
**Size**: 2.3 MB
**Content preview**: Appears to be a sales proposal with pricing tables

---

## Options

| # | Action              | AI will do                        | Risk |
|---|---------------------|-----------------------------------|------|
| A | Process normally    | Summarize and create task         | LOW  |
| B | Flag for review     | Create task marked NEEDS_REVIEW   | LOW  |
| C | Ignore / discard    | Move to Done without task         | LOW  |
| D | Quarantine          | Move to quarantine folder         | NONE |

**AI recommendation**: B (Flag for review) — safest given no history

---

## How to Respond

Edit this file and add your choice below:

**Your choice**: ___
**Notes** (optional): ___

Or update the task file directly: Needs_Action/FILE_015.md

**No expiry** — AI will wait for your response.
```

---

### Level 4: Human Full Ownership

```markdown
# Human Task: HT-20260216-007

**Created**: 2026-02-16 14:00
**Priority**: HIGH
**Assigned to**: Human (full ownership)
**Delegated by**: Self-Healing Skill (escalated after 3 failed attempts)
**Reason**: Watcher keeps crashing — code-level bug, AI cannot fix

---

## What Happened

The file watcher (filesystem_watcher.py) has crashed 3 times in 4 hours.
Auto-recovery attempted 3 times — all failed.
This requires developer-level investigation.

**Error log**: Logs/2026-02-16.log (lines 145–180)
**Last error**: MemoryError at line 89 of base_watcher.py

---

## What AI Has Done
- Cleaned stale .watcher.pid (3x)
- Restarted watcher (3x)
- Switched to Emergency mode (disk/RAM monitoring reduced)
- Paused all inbox processing

---

## What You Need to Do
- [ ] Review error log: Logs/2026-02-16.log
- [ ] Fix base_watcher.py memory issue
- [ ] Test watcher locally before restarting
- [ ] Restart watcher when fixed
- [ ] Mark this task RESOLVED when done

---

## AI Will
- Monitor for watcher recovery
- Resume inbox processing automatically when watcher is back
- Log all activity during downtime

**Reminder**: AI will re-notify after 4 hours if not resolved.
```

---

## Delegation Tracking Dashboard Section

```markdown
## Delegation Status

**Active delegations**: 3
**Completed today**: 28
**Escalated to human**: 2 (pending)

### Active Now
| ID              | Task                    | Handler          | Assigned | ETA     |
|-----------------|-------------------------|------------------|----------|---------|
| DEL-016         | Analyze invoice.pdf     | file-understanding| 14:30   | 14:31   |
| DEL-017         | Compress Feb logs       | memory-management | 14:28   | 14:35   |
| HT-007          | Watcher crash (Level 4) | HUMAN            | 14:00   | Open    |

### Pending Human Response
| ID     | Task                  | Waiting Since | Priority |
|--------|-----------------------|---------------|----------|
| HT-007 | Fix watcher crash     | 14:00         | HIGH     |
| HT-008 | Review vendor proposal| 10:30         | MEDIUM   |
```

---

## Reassignment Rules

### When to Reassign

```
Reassign when:
  - Handler did not complete within 2x expected time
  - Handler returned an error it cannot recover from
  - Handler is suspended (self-healing event)
  - Handler's output quality was rejected by next step
  - Human explicitly requests reassignment

Reassignment priority:
  1. Try backup handler from matching table
  2. If backup also fails → escalate to human (Level 3)
  3. If Level 3 escalation gets no response in 48h → Level 4

Log every reassignment with reason:
  [DELEGATION] DEL-016 reassigned: file-understanding → workflow
  Reason: file-understanding timed out after 90s (limit: 30s)
```

### Reassignment Limits

```
Max reassignments per task: 3
After 3 reassignments → Level 4 (human full ownership)
Cooldown before reassigning same skill: 30 minutes
Never reassign security tasks (always escalate directly)
```

---

## Follow-Up Schedule

```
Delegation type   | First check | Escalation | Give up
------------------|-------------|------------|--------
Skill-to-Skill    | 2x ETA      | 3x ETA     | 4x ETA
Level 3 (input)   | 4 hours     | 24 hours   | Never (wait)
Level 4 (owned)   | 4 hours     | 8 hours    | Never (wait)
External (email)  | 24 hours    | 48 hours   | 7 days

Follow-up actions:
  First check:  Log "still waiting"
  Escalation:   Notify human again (WARNING)
  Give up:      Mark STALLED, notify human (HIGH)
```

---

## Delegation Log

### Location
```
Common/AI_Employee_Vault/Logs/delegation.log
```

### Log Format
```
[2026-02-16 09:15:00] [DELEG] DEL-014 ASSIGNED  task=report_q1.pdf handler=file-understanding level=1
[2026-02-16 09:15:06] [DELEG] DEL-014 COMPLETED handler=file-understanding duration=6s outcome=SUCCESS
[2026-02-16 10:30:00] [DELEG] HT-003  ASSIGNED  task=unknown_proposal.xlsx handler=HUMAN level=3
[2026-02-16 10:30:00] [DELEG] HT-003  WAITING   reason=ambiguous_file confidence=42%
[2026-02-16 10:45:12] [DELEG] HT-003  COMPLETED handler=HUMAN duration=15m outcome=flag_for_review
[2026-02-16 14:00:00] [DELEG] HT-007  ASSIGNED  task=watcher_crash handler=HUMAN level=4
[2026-02-16 18:00:00] [DELEG] HT-007  FOLLOWUP  still_open duration=4h reminder_sent=YES
```

---

## Delegation Metrics

### Track Weekly

```
Total delegations:          {n}
By level:
  Level 0 (no delegation):  {n} ({%})
  Level 1 (skill-to-skill): {n} ({%})
  Level 2 (workflow):       {n} ({%})
  Level 3 (human input):    {n} ({%})
  Level 4 (human owned):    {n} ({%})

Success rate by handler:
  file-understanding:  {%} success
  decision:            {%} success
  workflow:            {%} success
  human (Level 3):     avg {min} response time
  human (Level 4):     avg {hours} to resolve

Reassignment rate:     {%} of tasks needed reassignment
Human escalation rate: {%} (target < 10%)
Stalled delegations:   {n} (target = 0)
```

---

## Integration with Other Skills

### With Workflow Skill
```
workflow → calls → delegation at:
  Every step that requires a different skill
  When a step fails and reassignment needed
  When human handoff is triggered
```

### With Decision Skill
```
decision → calls → delegation when:
  Confidence < 40% (escalate to human)
  Risk = CRITICAL (route to approval-handling)
  Exception type has no automated handler
```

### With Approval Handling Skill
```
delegation → routes HIGH-risk tasks → approval-handling:
  Any Level 3 delegation requiring sign-off
  Outbound actions requiring human approval
  Financial operations
```

### With Context Skill
```
delegation → attaches → context to every delegation:
  Entity profile for human delegations (so human has full picture)
  Task history for skill delegations (so skill has context)
  Active rules from Learning Skill relevant to this task
```

### With Audit Skill
```
delegation → logs to → audit:
  Every delegation event (assigned, completed, failed, reassigned)
  Human response times for Level 3/4 delegations
  Handler accuracy statistics
  Stalled delegations
```

### With Learning Skill
```
delegation → feeds → learning:
  Which handlers succeed for which task types
  Reassignment patterns (handler X keeps failing task type Y)
  Human override patterns (human prefers to handle Z themselves)
  Response time patterns per delegation level
```

### With Notification Skill
```
delegation → triggers → notification for:
  Level 3/4 delegations (human has action to take)
  Follow-up reminders (task still waiting)
  Stalled delegations (needs attention)
  Handler failures (reassignment in progress)
```

---

## Best Practices

### DO
```
- Always pass full context when delegating (handler should not need to re-gather)
- Set realistic expected completion times per handler
- Log every delegation immediately when assigned
- Follow up on open delegations on schedule
- Reassign quickly when handler fails (don't wait)
- Present human delegations clearly with options and recommendation
- Close delegations promptly after completion
- Feed outcomes to Learning Skill for capability improvement
```

### DON'T
```
- Delegate the same task to multiple handlers simultaneously
- Delegate without context (handler will do a worse job)
- Forget to follow up on Level 3/4 human delegations
- Reassign more than 3 times without escalating to Level 4
- Delegate security decisions to non-security handlers
- Let stalled delegations sit without alerting human
- Assume delegation = completion (always verify outcome)
- Skip closing the loop (log completion and outcome always)
```

---

## Quick Reference: Task → Handler

```
Task                          | Handler               | Level
------------------------------|----------------------|-------
Classify incoming file        | file-understanding   | 1
Set task priority             | decision + context   | 1
Run multi-step process        | workflow             | 2
Detect risk in action         | risk-detection       | 1
Handle system error           | error-recovery       | 1
Fix crashed component         | self-healing         | 1/4
Clean vault storage           | memory-management    | 1
Schedule recurring task       | scheduler            | 1
Send alert to human           | notification         | 1
Call external API             | tool-invocation + integration | 1
Scan file for threats         | security             | 1
Approve outbound action       | approval-handling    | 3
Full ambiguous case           | decision → human     | 3
Code-level bug or outage      | human               | 4
Legal or financial decision   | human               | 4
New contact from unknown      | decision → human     | 3
```

---

**Status**: Production Ready
**Priority**: HIGH (Ensures every task reaches the right handler)
**Delegation Levels**: 0–5 (Automated → External)
**Max Reassignments**: 3 before Level 4 human ownership
**Human Escalation Target**: < 10% of all delegations
**Follow-up**: Scheduled per delegation type, never dropped

*Good delegation = Every task handled by the most capable, available, appropriate handler — every time*
