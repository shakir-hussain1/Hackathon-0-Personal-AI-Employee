# State Management Skill

## Purpose
Track, persist, share, and restore the complete state of the AI Employee system at all times. Ensure every agent, task, workflow, and pipeline knows exactly where things stand — even after crashes, restarts, or context loss.

---

## Core Functions

1. **State Capture** — Snapshot the full system state at any moment
2. **State Persistence** — Write state to disk so it survives restarts
3. **State Sharing** — Make current state accessible to all agents
4. **State Transitions** — Move state forward in a controlled, logged way
5. **State Recovery** — Restore last known good state after failure
6. **State Validation** — Detect corrupted, stale, or inconsistent state

---

## What is "State"?

State is everything the system needs to know to answer:
- **What is happening right now?** (active tasks, running agents, open pipelines)
- **What happened before?** (completed work, past decisions, history)
- **What is waiting?** (queued tasks, pending approvals, blocked items)
- **What is the system's health?** (resource usage, error counts, last heartbeat)

---

## State Layers

### Layer 1: System State (Global)
The overall health and mode of the entire AI Employee.

**Location:** `AI_Employee_Vault/.state/system.md`

```
# System State
Last Updated: 2026-02-16 14:30:00
Version: 47

## Mode
Current Mode: NORMAL
Previous Mode: IDLE
Mode Changed At: 2026-02-16 09:00:00

## Health
Status: HEALTHY
Last Health Check: 2026-02-16 14:29:00
Active Agents: 2
Running Pipelines: 1
Pending Tasks: 4
Error Count (last hour): 0

## Session
Session ID: SESSION-20260216-001
Session Started: 2026-02-16 09:00:00
Uptime: 5h 30m
```

### Layer 2: Task State
The lifecycle position of every task.

**Location:** `AI_Employee_Vault/.state/tasks.md`

```
# Task State Registry
Last Updated: 2026-02-16 14:30:00

| Task ID   | Status      | Owner Agent  | Priority | Created At  | Updated At  |
|-----------|-------------|--------------|----------|-------------|-------------|
| TASK-045  | COMPLETED   | AGENT-FP-001 | HIGH     | 14:10:00    | 14:22:00    |
| TASK-046  | COMPLETED   | AGENT-FP-002 | MEDIUM   | 14:15:00    | 14:28:00    |
| TASK-047  | IN_PROGRESS | AGENT-FP-003 | HIGH     | 14:20:00    | 14:30:00    |
| TASK-048  | QUEUED      | —            | LOW      | 14:25:00    | 14:25:00    |
| TASK-049  | BLOCKED     | —            | MEDIUM   | 14:28:00    | 14:29:00    |
```

### Layer 3: Agent State
What every agent is doing right now.

**Location:** `AI_Employee_Vault/.state/agents.md`

```
# Agent State
Last Updated: 2026-02-16 14:30:00

| Agent ID         | Status   | Current Task | Current Stage   | Progress | Last Heartbeat |
|------------------|----------|--------------|-----------------|----------|----------------|
| AGENT-COORD-001  | ACTIVE   | —            | MONITORING      | —        | 14:30:00       |
| AGENT-FP-003     | WORKING  | TASK-047     | ANALYZE (4/8)   | 50%      | 14:29:55       |
```

### Layer 4: Pipeline State
Which stage each running pipeline is on.

**Location:** `AI_Employee_Vault/.state/pipelines.md`

```
# Pipeline State
Last Updated: 2026-02-16 14:30:00

| Run ID     | Pipeline      | Current Stage | Stage # | Total | Status      |
|------------|---------------|---------------|---------|-------|-------------|
| RUN-0047   | INBOX_TO_DONE | ANALYZE       | 4       | 8     | IN_PROGRESS |
```

### Layer 5: Context State
What the system knows and remembers about entities and patterns.

**Location:** `AI_Employee_Vault/.state/context.md`

```
# Context State
Last Updated: 2026-02-16 14:30:00

## Active Entity Context
- Files being processed: proposal.pdf, contract.docx
- Known senders: (none — Bronze tier)
- Current focus domain: business documents

## Active Rules
- 3 learned rules active (see learning skill)
- Last rule update: 2026-02-15

## Memory Pressure
- Context entries: 12
- Memory budget: 80% used
- Next purge: 2026-02-16 18:00
```

---

## State Transitions

### Valid State Transitions Per Layer

**Task State Machine:**
```
CREATED → QUEUED → IN_PROGRESS → COMPLETED
                ↓              ↓
            BLOCKED       CANCELLED
                ↓
          IN_PROGRESS (unblocked)
```

**Agent State Machine:**
```
STARTING → ACTIVE → WORKING → COMPLETING → TERMINATED
              ↓         ↓
           PAUSED     ERROR → RECOVERING → ACTIVE
```

**Pipeline State Machine:**
```
QUEUED → RUNNING → STAGE_N → COMPLETED
                ↓
            FAILED → RETRYING → STAGE_N
                ↓
            ABORTED
```

### Transition Rules
1. State MUST be written to disk before the transition is considered complete
2. Every transition gets a log entry (who changed it, from what, to what, why)
3. Illegal transitions are rejected and logged as violations
4. No state can go backwards without a Recovery or Rollback event

---

## State Persistence

### Write Protocol
Every state change follows this sequence:

```
Step 1: READ current state file
Step 2: VALIDATE current state is consistent
Step 3: APPLY change to in-memory state
Step 4: INCREMENT version counter
Step 5: WRITE updated state to .state/ file
Step 6: WRITE transition log entry
Step 7: CONFIRM write succeeded
       → If write fails: retry 3 times, then ALERT
```

### State File Update Frequency
| State Layer | Update Trigger | Max Staleness |
|------------|---------------|---------------|
| System State | Every 60 seconds + on mode change | 2 minutes |
| Task State | Every task status change | Immediate |
| Agent State | Every heartbeat (60s) | 2 minutes |
| Pipeline State | Every stage completion | Immediate |
| Context State | On context update | 5 minutes |

---

## State Snapshot

### What is a Snapshot?
A complete copy of all state layers at a single point in time — used for recovery, auditing, and debugging.

### Snapshot Format
**Location:** `AI_Employee_Vault/.state/snapshots/`
**Filename:** `SNAP_{YYYYMMDD}_{HHMM}.md`

```
# State Snapshot
Captured At: 2026-02-16 14:30:00
Snapshot ID: SNAP-20260216-1430
Trigger: SCHEDULED (every 30 minutes)
Version: 47

## System State (at capture)
Mode: NORMAL | Status: HEALTHY | Active Agents: 2

## Task State (at capture)
COMPLETED: 45, 46
IN_PROGRESS: 47
QUEUED: 48
BLOCKED: 49

## Agent State (at capture)
AGENT-COORD-001: ACTIVE
AGENT-FP-003: WORKING on TASK-047 (50%)

## Pipeline State (at capture)
RUN-0047: IN_PROGRESS at stage 4/8

## Integrity Hash
SHA256: a3f7c9d2...
```

### Snapshot Schedule
- **Automatic:** Every 30 minutes
- **On-demand:** Before any high-risk operation
- **On mode change:** System → Emergency, NORMAL → BURST
- **Retention:** Last 48 snapshots (24 hours worth)

---

## State Recovery

### Recovery Scenarios

**Scenario 1: Agent Crash (missed heartbeat)**
```
Detect:  Agent heartbeat >3 minutes old
Action:
  1. Read last known agent state from .state/agents.md
  2. Identify task agent was working on
  3. Read task file — what stage was it at?
  4. Mark task as NEEDS_REASSIGNMENT
  5. Remove agent from active registry
  6. Coordinator reassigns task to available agent
  7. Log: "Recovered TASK-047 from crashed AGENT-FP-003"
```

**Scenario 2: System Restart (full shutdown)**
```
Detect:  Session ID in system.md does not match current session
Action:
  1. Read last system.md state
  2. Read task state — find all IN_PROGRESS tasks
  3. Reset IN_PROGRESS → QUEUED (they were interrupted)
  4. Read pipeline state — find all RUNNING pipelines
  5. Reset RUNNING → QUEUED at last completed stage
  6. Clear all agent state (all agents are new on restart)
  7. Start fresh session with recovered queue
  8. Log: "System recovery from shutdown — N tasks re-queued"
```

**Scenario 3: Corrupted State File**
```
Detect:  State file hash mismatch OR unreadable content
Action:
  1. Load most recent valid snapshot
  2. Apply any transition logs written after the snapshot
  3. Reconstruct state to closest known good point
  4. Flag affected tasks for manual review
  5. Alert human: "State file corrupted — recovered from snapshot SNAP-20260216-1400"
```

**Scenario 4: Stale State (outdated but uncorrupted)**
```
Detect:  Last Updated timestamp >10 minutes old without expected updates
Action:
  1. Trigger health check on all active agents
  2. Re-sync state from agent heartbeats
  3. Reconcile with filesystem (actual files in Done/, Needs_Action/, etc.)
  4. Update state to match reality
  5. Log: "State re-synced after staleness detected"
```

---

## State Validation

### Validation Checks (run every 5 minutes)
```
Check 1: Filesystem Consistency
  → Count files in Inbox/, Needs_Action/, Done/
  → Compare with task state counts
  → Alert if mismatch > 1 file

Check 2: Agent Heartbeat Freshness
  → All ACTIVE/WORKING agents must have heartbeat <2 min old
  → Flag any agent with stale heartbeat

Check 3: Task Ownership Consistency
  → Every IN_PROGRESS task must have an ACTIVE/WORKING agent owner
  → Every ACTIVE agent must own at most 1 task (Bronze tier)

Check 4: Pipeline Stage Validity
  → Every RUNNING pipeline must be at a valid stage number
  → Stage number must not exceed total stages for that pipeline

Check 5: Version Counter Integrity
  → State version must be monotonically increasing
  → No version regression allowed

Check 6: State File Hash
  → Compare current hash with last known good hash
  → Alert if unexpected change detected
```

### Validation Result
**Location:** `AI_Employee_Vault/.state/validation.md`
```
# State Validation
Last Run: 2026-02-16 14:35:00
Result: PASSED

## Checks
- Filesystem Consistency: ✅ (Needs_Action: 1, Done: 46 — matches task state)
- Agent Heartbeat Freshness: ✅ (All agents current)
- Task Ownership Consistency: ✅ (TASK-047 owned by AGENT-FP-003)
- Pipeline Stage Validity: ✅ (Stage 4 of 8 valid)
- Version Counter Integrity: ✅ (v47, previous v46)
- State File Hash: ✅ (matches)
```

---

## State Diff (Change Detection)

### What Changed Since Last Snapshot?
Used for debugging, auditing, and reporting.

```
State Diff: v46 → v47
Timestamp: 2026-02-16 14:30:00

CHANGED:
  tasks.TASK-047.status: IN_PROGRESS (unchanged — still working)
  agents.AGENT-FP-003.progress: 40% → 50%
  pipelines.RUN-0047.current_stage: RISK_ASSESS → ANALYZE
  system.running_pipelines: 1 (unchanged)

ADDED:
  tasks.TASK-049.status: BLOCKED (new block detected)

REMOVED:
  nothing
```

---

## State Folder Structure

```
AI_Employee_Vault/
└── .state/
    ├── system.md           # Global system state
    ├── tasks.md            # All task statuses
    ├── agents.md           # All agent statuses
    ├── pipelines.md        # All pipeline run statuses
    ├── context.md          # Context and memory state
    ├── validation.md       # Last validation result
    ├── transition_log.md   # Chronological state changes
    └── snapshots/          # Point-in-time full snapshots
        ├── SNAP_20260216_1400.md
        └── SNAP_20260216_1430.md
```

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|-----------------|
| Multi-Agent Sync | Agent state feeds into sync registry |
| Agent Spawning | Spawn events update agent state immediately |
| Pipeline | Each stage completion updates pipeline state |
| Task Management | Task state transitions written here |
| Self-Healing | Reads state to detect and recover from failures |
| Monitoring | Monitors state staleness and validation results |
| Version Control | State snapshots are versioned |
| Audit | All state transitions logged in audit trail |
| Memory Management | Context state used to manage memory pressure |

---

## Quick Reference

```
SYSTEM STATE:      .state/system.md
TASK STATE:        .state/tasks.md
AGENT STATE:       .state/agents.md
PIPELINE STATE:    .state/pipelines.md
CONTEXT STATE:     .state/context.md
VALIDATION:        .state/validation.md
SNAPSHOT:          .state/snapshots/SNAP_{DATE}_{TIME}.md
TRANSITION LOG:    .state/transition_log.md

SNAPSHOT TRIGGER:  Every 30 min + before risky ops + on mode change
VALIDATION CYCLE:  Every 5 minutes
STALENESS ALERT:   >10 min without update
RECOVERY TRIGGER:  Crashed agent / system restart / corrupted file
```

---

## Best Practices

1. **Write before acting** — always persist state before starting work, not after
2. **Single writer per state file** — use Multi-Agent Sync locks to prevent write collisions
3. **Validate on startup** — first thing every session is a full state validation
4. **Snapshot before risk** — take a manual snapshot before any bulk operation
5. **Trust the filesystem, not memory** — always re-read state from disk, never assume in-memory is current
6. **Version everything** — every state update increments the version counter
7. **Fail safe** — if state is unreadable, stop work and alert human rather than proceeding blind
8. **Small diffs, frequent writes** — write small incremental changes often rather than large batches rarely
