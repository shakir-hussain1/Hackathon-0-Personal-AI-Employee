# Collaboration Skill

**Purpose**: Enable the AI Employee to work effectively with humans, teams, and other AI agents
**Storage**: Markdown-based collaboration records, shared workspaces, team context, handoff notes
**Scope**: Human-AI teamwork, multi-agent coordination, shared task ownership, team awareness, handoff management

---

## Core Functions

### 1. Share Context
Ensure everyone working on a task has the same information

### 2. Coordinate Tasks
Prevent conflicts when multiple parties work on related items

### 3. Manage Handoffs
Transfer work cleanly between AI, human, and external parties

### 4. Track Shared Work
Know who is doing what, progress, and blockers

### 5. Resolve Conflicts
Handle when two parties make contradictory changes

### 6. Build Team Awareness
Maintain a shared view of what is happening across the system

---

## Collaboration Modes

### Mode 1: AI Assists Human
```
Description:
  AI does the groundwork, human makes final decisions
  Most common mode for Bronze tier

AI responsibilities:
  - Gather and organize information
  - Draft outputs for human review
  - Flag items needing human judgment
  - Execute approved actions
  - Track progress and report

Human responsibilities:
  - Review AI outputs
  - Make final decisions on ambiguous items
  - Approve outbound actions
  - Provide feedback that improves AI accuracy

Handoff pattern:
  AI works → Human reviews → Human approves/edits → AI executes
```

### Mode 2: Human Leads, AI Supports
```
Description:
  Human drives the work, AI handles logistics and execution

AI responsibilities:
  - Schedule and track tasks
  - Organize files and documents
  - Send reminders and follow-ups
  - Log all activities
  - Handle routine sub-tasks

Human responsibilities:
  - Define goals and priorities
  - Make strategic decisions
  - Handle stakeholder relationships
  - Provide new inputs and direction

Handoff pattern:
  Human decides → AI executes → AI reports result → Human next step
```

### Mode 3: Fully Autonomous (AI leads)
```
Description:
  AI handles a task end-to-end within approved boundaries
  Only for well-defined, low-risk, reversible tasks

AI responsibilities:
  - Complete task without human input
  - Log all decisions and actions
  - Alert human on completion
  - Escalate if anything unexpected occurs

Human responsibilities:
  - Define the task boundaries upfront
  - Review completion summary
  - Provide feedback if result was wrong

Handoff pattern:
  Human defines task → AI completes → AI reports → Human reviews
```

### Mode 4: Multi-Agent Collaboration (Gold+)
```
Description:
  Multiple AI agents work together, each with specialized roles

Agents:
  - Orchestrator agent: coordinates overall workflow
  - Specialist agents: handle specific domains (email, accounting, social)
  - Monitor agent: tracks health, detects conflicts

AI-to-AI responsibilities:
  - Share context packages via vault files
  - Signal readiness / completion via status files
  - Never overwrite another agent's active files
  - Lock files when writing (release immediately after)
  - Log all inter-agent communications

Handoff pattern:
  Agent A completes step → writes output → signals Agent B → B picks up
```

---

## Shared Workspace

### Structure

```
Common/AI_Employee_Vault/Plans/collaboration/
├── active/                    # Ongoing collaborative tasks
│   ├── COLLAB_001.md         # Active collaboration record
│   └── COLLAB_002.md
├── handoffs/                  # Pending handoffs (waiting for other party)
│   ├── HANDOFF_AI_TO_HUMAN_001.md
│   └── HANDOFF_HUMAN_TO_AI_001.md
├── shared_context/            # Context files shared across parties
│   ├── team_context.md       # Who is doing what right now
│   ├── project_status.md     # Current project states
│   └── blockers.md           # What is blocking progress
└── history/                   # Completed collaborations (archived)
```

---

## Collaboration Record Format

```markdown
# Collaboration: COLLAB-20260216-003

**Created**: 2026-02-16 09:00
**Task**: Q1 Financial Report Review
**Type**: AI Assists Human (Mode 1)
**Status**: IN_PROGRESS

---

## Parties Involved

| Party       | Role                | Responsibilities                    | Status    |
|-------------|---------------------|-------------------------------------|-----------|
| AI Employee | Analyst / Organizer | Summarize report, flag key items    | WORKING   |
| Human       | Decision Maker      | Review summary, approve response    | WAITING   |
| Alice       | Report Author       | Provided report (external)          | DONE      |

---

## Task Breakdown

| Step | Owner    | Task                          | Status      | Deadline |
|------|----------|-------------------------------|-------------|----------|
| 1    | AI       | Read and summarize report     | COMPLETE    | 09:15    |
| 2    | AI       | Flag action items             | COMPLETE    | 09:20    |
| 3    | Human    | Review summary                | PENDING     | EOD      |
| 4    | Human    | Approve or edit response      | BLOCKED(3)  | EOD      |
| 5    | AI       | Send approved response        | BLOCKED(4)  | Tomorrow |

---

## Shared Context

**Report**: Done/report_q1.pdf
**Summary**: Plans/collaboration/active/COLLAB_003_summary.md
**Key findings**:
  - Revenue up 12% YoY
  - Expenses up 8% YoY
  - 3 action items flagged (see summary)

---

## Communication Log

| Time  | From    | To      | Message                                          |
|-------|---------|---------|--------------------------------------------------|
| 09:15 | AI      | Human   | Summary ready. 3 action items need your review.  |
| 09:20 | AI      | Human   | Reminder: response to Alice due by EOD.          |

---

## Blockers

| Blocker                      | Blocking Step | Waiting On | Since |
|------------------------------|---------------|------------|-------|
| Human review not started     | Steps 4, 5    | Human      | 09:20 |

---

## History

- 09:00 Collaboration created
- 09:05 AI started reading report_q1.pdf
- 09:15 AI completed summary (3 action items identified)
- 09:15 Handoff created → Human (review needed)
```

---

## Handoff Management

### Handoff Types

```
Type 1: AI → Human (Input Needed)
  When: AI completed its part, needs human decision
  Contains: What AI did, what human needs to do, options, deadline

Type 2: Human → AI (Continue Work)
  When: Human completed their part, AI should continue
  Contains: Human's decision or edit, AI's next steps

Type 3: AI → AI (Agent-to-Agent, Gold+)
  When: One agent finishes, another should pick up
  Contains: Output data, state snapshot, next agent instructions

Type 4: AI → External (Outbound)
  When: Task handed to external party (email sent, task created)
  Contains: What was sent, what is expected back, follow-up schedule

Type 5: External → AI (Inbound)
  When: External party responds (email received, file dropped)
  Contains: What was received, how it connects to original task
```

### Handoff Record Format

```markdown
# Handoff: HANDOFF-20260216-005

**Type**: AI → Human (Type 1)
**Created**: 2026-02-16 09:15
**From**: AI Employee
**To**: Human Owner
**Status**: PENDING

---

## What Was Completed (AI's Part)

- Read report_q1.pdf (12 pages)
- Extracted key financial figures
- Identified 3 action items requiring human decision
- Drafted response to Alice

**Output files**:
  - Summary: Plans/collaboration/active/COLLAB_003_summary.md
  - Draft response: Plans/email_drafts/DRAFT_alice_q1_response.md

---

## What You Need to Do

1. Review summary: Plans/collaboration/active/COLLAB_003_summary.md
   (estimated 5 minutes)

2. Review draft response to Alice:
   Plans/email_drafts/DRAFT_alice_q1_response.md
   - Edit if needed
   - Change status to APPROVED when ready

3. Decide on action item #2 (budget reallocation — AI cannot decide)
   Details in summary file, section "Action Items"

---

## Deadline

Response to Alice expected by: **Today EOD**
If not actioned by 16:00 → AI will send reminder

---

## How to Signal Completion

Edit the draft file status:
  **Status**: APPROVED  ← change this
AI will detect the change and send the email.
```

---

## Team Context File

### Location
```
Common/AI_Employee_Vault/Plans/collaboration/shared_context/team_context.md
```

### Format
```markdown
# Team Context

**Updated**: 2026-02-16 14:00
**Active Collaborations**: 3
**Pending Handoffs**: 2

---

## Who Is Doing What Right Now

| Party       | Current Task                    | Status     | Since | ETA   |
|-------------|----------------------------------|------------|-------|-------|
| AI Employee | Processing 4 inbox files         | WORKING    | 13:45 | 14:00 |
| Human       | Reviewing Q1 report summary      | PENDING    | 09:15 | EOD   |
| Alice       | Waiting for response to report   | EXTERNAL   | Feb 15| Today |

---

## Active Projects

| Project     | Owner  | AI Status          | Human Status       | Next Action |
|-------------|--------|--------------------|--------------------|-------------|
| Q1 Review   | Human  | Complete (summary) | Review needed      | Human reviews|
| Inbox batch | AI     | In progress        | -                  | AI completes |
| Acme invoice| Both   | Drafted response   | Approval pending   | Human approves|

---

## Blockers

| Blocker                      | Affects          | Since | Priority |
|------------------------------|------------------|-------|----------|
| Q1 summary awaiting review   | Alice response   | 09:15 | HIGH     |
| Acme approval not received   | Invoice response | Yesterday| MEDIUM |

---

## Completed Today

| Task                  | Completed By | Time  | Result    |
|-----------------------|-------------|-------|-----------|
| Process sales_data.csv| AI          | 09:45 | Done      |
| Process report_q1.pdf | AI + Human  | 11:00 | Approved  |
```

---

## Conflict Resolution

### Conflict Types

#### Conflict 1: Simultaneous Edit
```
Situation: AI and human both modify the same file at the same time

Detection:
  AI checks file hash before writing
  IF hash changed since last read → conflict detected

Resolution steps:
  1. AI stops its write
  2. AI reads the human's version
  3. AI merges: keep human's changes + add AI's new content
  4. AI saves merged version with conflict note
  5. AI notifies human: "Merged your changes with mine — please review"

Merge note format:
  <!-- MERGE NOTE 2026-02-16 14:30: Human and AI edited simultaneously.
       Human changes preserved. AI additions appended. Please review. -->
```

#### Conflict 2: Contradictory Decisions
```
Situation: AI made a decision, human made a different decision about the same thing

Detection:
  Human changes a field AI already set (priority, category, status)

Resolution:
  Human's decision ALWAYS wins
  AI records the override in learning signal
  AI updates its rule if pattern repeats 3x
  AI does NOT revert or question human's override

Log entry:
  [COLLAB] Override: AI set priority=MEDIUM, Human set priority=HIGH
  [LEARNING] Override recorded (+1 for alice→HIGH pattern)
```

#### Conflict 3: Duplicate Work
```
Situation: Two parties start the same task independently

Detection:
  Task file already has owner = "AI" when human starts
  OR human started task that AI already completed

Resolution:
  IF AI already completed → show human the completed work
  IF both in progress → merge outputs, flag duplicates
  IF human prefers their version → archive AI's version

Prevention:
  Always check owner field before starting any task
  AI claims ownership immediately when starting a task
  Human tasks labeled "HUMAN" in status
```

#### Conflict 4: Stale Handoff
```
Situation: Handoff is pending but context has changed since it was created

Detection:
  Handoff created > 24 hours ago with no response
  AND source file or context has been updated

Resolution:
  AI re-evaluates: is handoff still valid?
  IF context changed significantly → update handoff + re-notify
  IF handoff is now irrelevant → close with note
  IF still relevant → send follow-up reminder with updated context
```

---

## Collaboration Protocols

### Protocol 1: Claiming a Task
```
Before working on any shared task:

1. Read task file: check owner field
   IF owner = "" or "UNASSIGNED" → proceed to step 2
   IF owner = "HUMAN" → do not touch (human is working on it)
   IF owner = "AI" → AI already working, check if stuck

2. Claim the task:
   Write to task file: Owner: AI Employee
   Write to task file: Status: IN_PROGRESS
   Timestamp the claim

3. Begin work immediately after claiming
   Do not claim without intention to work on it

4. Release claim on completion or if blocked:
   Write: Owner: HUMAN (if handing off to human)
   Write: Status: PENDING_REVIEW (if awaiting human)
   Write: Status: BLOCKED (if stuck, explain why)
```

### Protocol 2: Signaling Completion
```
When AI finishes its part of a collaborative task:

1. Update task file:
   Status: PENDING_REVIEW
   Owner: HUMAN
   Completed_by_AI: {timestamp}
   AI_output: {link to output file}

2. Create handoff record in collaboration/handoffs/
3. Notify human via notification + dashboard update
4. Set follow-up reminder (4 hours if no response)
5. Do NOT continue to next step until human responds
```

### Protocol 3: Receiving Human Input
```
When human responds to a handoff or makes a change:

1. Detect the change:
   File modified since last check?
   Status changed to APPROVED / REJECTED / EDITED?
   New instruction added?

2. Acknowledge:
   Log: "[COLLAB] Human input received for COLLAB-003"
   Update collaboration record

3. Continue workflow:
   IF APPROVED → execute next step
   IF REJECTED → archive, notify, stop
   IF EDITED → incorporate edits, re-evaluate next step
   IF NEW INSTRUCTION → re-plan if needed, confirm understanding

4. Close handoff record:
   Status: RESOLVED
   Human_responded_at: {timestamp}
   Human_decision: {what they decided}
```

### Protocol 4: Agent-to-Agent Handoff (Gold+)
```
When AI Agent A hands off to AI Agent B:

1. Agent A writes output to shared file:
   Location: Plans/collaboration/active/COLLAB_XXX_output.md
   Include: result data, state, next agent instructions

2. Agent A signals completion:
   Update status file: Plans/collaboration/active/COLLAB_XXX_status.md
   Write: step_completed = "Step 3", next_agent = "Agent B", timestamp

3. Agent B detects signal:
   Reads status file every check_interval
   IF next_agent = "me" → claim task, begin work

4. Agent B acknowledges:
   Updates status file: step_started = "Step 4", owner = "Agent B"

5. No direct agent-to-agent calls:
   All coordination via shared files (vault = shared memory)
```

---

## Collaboration Metrics

### Track Weekly

```
Active collaborations:             {n}
Completed collaborations:          {n}
Avg collaboration duration:        {hours}

Handoffs:
  AI → Human:                      {n} this week
  Human → AI:                      {n} this week
  Avg human response time:          {minutes}
  Stalled handoffs (>24h):          {n}

Conflicts:
  Simultaneous edits resolved:      {n}
  Human overrides:                  {n} (healthy signal)
  Duplicate work detected:          {n}

Collaboration health:
  Tasks completed without blocker:  {%}
  Handoffs requiring re-send:       {%}
  Human satisfaction (approvals):   {%}
```

---

## Integration with Other Skills

### With Delegation Skill
```
collaboration → uses → delegation for:
  Routing tasks to correct collaborative party
  Escalating blockers to appropriate handler
  Reassigning if one party is unavailable
```

### With Context Skill
```
collaboration → shares → context via:
  Team context file (who is doing what)
  Handoff notes (full picture for receiving party)
  Entity profiles (background on external parties)
```

### With Communication Skill
```
collaboration → uses → communication for:
  All handoff messages written by Communication Skill
  Team context updates formatted clearly
  Conflict resolution messages to human
  Follow-up reminders for stalled handoffs
```

### With Workflow Skill
```
workflow → uses → collaboration for:
  Human handoff steps in multi-step workflows
  Tracking who completed which workflow step
  Resolving conflicts when workflow step re-run
```

### With Approval Handling Skill
```
collaboration → feeds → approval-handling:
  Outbound items needing human approval (collaborative review)
  Multi-party approvals (both parties must approve)
  Escalating stalled approvals to next party
```

### With Learning Skill
```
collaboration → feeds → learning:
  Human response time patterns per task type
  Which handoff formats get fastest responses
  Common edits humans make to AI outputs
  Override patterns for behavior improvement
```

### With Audit Skill
```
collaboration → logs to → audit:
  Every handoff created and resolved
  Conflict detections and resolutions
  Stalled collaboration incidents
  Override events (human overrides AI decision)
```

---

## Best Practices

### DO
```
- Always claim tasks before starting (prevents duplicate work)
- Pass full context in every handoff (recipient should not re-gather)
- Signal completion clearly (change status field explicitly)
- Set realistic deadlines in handoffs (not "ASAP")
- Follow up on stalled handoffs (4h for human, 30s for AI)
- Human override always wins — never resist or question it
- Keep team_context.md updated in real time
- Close collaboration records promptly when complete
```

### DON'T
```
- Start work on a task claimed by another party
- Leave handoffs with vague instructions
- Assume human has seen a handoff without confirmation
- Allow stale handoffs to sit for >48 hours without re-notify
- Create conflicts by writing without checking current state
- Bypass collaboration protocol for "simple" tasks
- Leave team_context.md stale (>1 hour behind)
- Treat human silence as approval (always wait for explicit response)
```

---

## Quick Reference: Collaboration Patterns

```
Situation                     | Action                          | Record
------------------------------|----------------------------------|--------
Starting new collab task      | Claim + create COLLAB record    | COLLAB_XXX.md
Finishing AI part             | Create handoff → notify human   | HANDOFF_XXX.md
Human finishes their part     | Detect change → continue        | Update COLLAB
Conflict detected             | Stop → resolve → merge → notify | Conflict note
Handoff stalled >4h           | Send reminder → escalate @24h   | Communication log
Human overrides AI decision   | Accept → log → feed learning    | Learning signal
Task needs external party     | Create external handoff         | HANDOFF_XXX.md
Agent-to-agent (Gold+)        | Write to shared file → signal   | Status file
Collaboration complete        | Close record → archive          | Move to history/
```

---

**Status**: Production Ready
**Priority**: HIGH (Enables effective human-AI teamwork)
**Collaboration Modes**: 4 (AI Assists, Human Leads, Autonomous, Multi-Agent)
**Handoff Types**: 5 (AI→Human, Human→AI, AI→AI, AI→External, External→AI)
**Conflict Resolution**: Automatic merge + human-wins policy
**Stalled Handoff Timeout**: Follow-up at 4h, escalate at 24h, alert at 48h

*Good collaboration = AI Employee that works with humans, not around them*
