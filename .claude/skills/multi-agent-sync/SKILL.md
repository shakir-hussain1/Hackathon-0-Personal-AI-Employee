# Multi-Agent Sync Skill

## Purpose
Coordinate multiple AI agents working in the same vault, prevent conflicts, share task status in real time, and ensure smooth parallel workflow without stepping on each other's work.

---

## Core Functions

1. **Agent Registration** — Track which agents are active and what they own
2. **Conflict Prevention** — Lock files/tasks before touching them
3. **Status Broadcasting** — Publish agent state so others can adapt
4. **Work Distribution** — Split tasks across agents without overlap
5. **Consensus Building** — Resolve disagreements between agents
6. **Handoff Protocol** — Transfer ownership cleanly between agents

---

## Agent Registry

### Active Agents File
**Location:** `AI_Employee_Vault/.sync/agents.md`

```
# Active Agent Registry
Last Updated: {TIMESTAMP}

| Agent ID    | Name              | Status   | Current Task   | Locked Files         | Heartbeat           |
|-------------|-------------------|----------|----------------|----------------------|---------------------|
| AGENT-001   | Claude-Primary    | ACTIVE   | TASK-042       | Dashboard.md         | 2026-02-16 14:30:00 |
| AGENT-002   | Claude-Watcher    | IDLE     | —              | —                    | 2026-02-16 14:29:55 |
| AGENT-003   | Claude-Reporter   | WORKING  | RPT-WEEKLY-07  | Reports/weekly.md    | 2026-02-16 14:30:01 |
```

### Agent Status Values
| Status   | Meaning                                    |
|----------|--------------------------------------------|
| ACTIVE   | Running, has claimed work                  |
| IDLE     | Running, waiting for tasks                 |
| WORKING  | Deep in a task, do not interrupt           |
| PAUSED   | Temporarily suspended                      |
| OFFLINE  | Not responding (missed 3 heartbeats)       |
| ERROR    | Failed state, needs recovery               |

### Heartbeat Rule
- Each agent updates its heartbeat every **60 seconds**
- If heartbeat is **>3 minutes old** → agent is considered OFFLINE
- OFFLINE agent's locks are released after **5 minutes**

---

## Lock System

### How Locking Works
Before any agent reads/writes a file or claims a task, it MUST acquire a lock.

### Lock File Format
**Location:** `AI_Employee_Vault/.sync/locks/`
**Filename:** `{resource_id}.lock`

```
LOCK
Resource: AI_Employee_Vault/Dashboard.md
Locked By: AGENT-001
Locked At: 2026-02-16 14:25:00
Expires At: 2026-02-16 14:35:00
Lock Type: WRITE
Purpose: Updating daily stats
```

### Lock Types
| Type      | Behavior                                               |
|-----------|--------------------------------------------------------|
| READ      | Multiple agents can hold simultaneously                |
| WRITE     | Exclusive — only one agent at a time                   |
| CLAIM     | Task ownership — prevents double-processing            |
| ADVISORY  | Soft lock — signals intent, not enforced               |

### Lock Acquisition Protocol
```
Step 1: Check if lock file exists
        → If NO lock: create lock file, proceed
        → If READ lock + want READ: proceed (shared OK)
        → If WRITE lock: wait and retry

Step 2: Wait and retry
        → Wait: 5 seconds
        → Retry: up to 6 times (30 seconds total)
        → After 6 fails: escalate to Conflict Resolution

Step 3: Work with locked resource
        → Complete operation
        → Release lock immediately when done

Step 4: Release
        → Delete lock file
        → Update agents.md (remove from Locked Files)
```

### Lock Expiry
- Standard lock: **10 minutes** max
- Emergency lock: **30 minutes** max
- Expired locks are automatically released
- Stale locks (agent OFFLINE) released after **5 minutes**

---

## Task Ownership

### Claim Protocol
Before processing any task, agent must CLAIM it.

**Claim Record Location:** `AI_Employee_Vault/Needs_Action/{task_file}.md`

Add to task file header:
```
CLAIMED BY: AGENT-001
CLAIMED AT: 2026-02-16 14:25:00
ESTIMATED COMPLETION: 2026-02-16 14:35:00
```

### Anti-Double-Processing Rules
1. Agent scans Needs_Action folder
2. For each task file — check for CLAIMED BY header
3. If already claimed AND agent is ACTIVE/WORKING → **skip**
4. If claimed AND agent is OFFLINE → **take over** (log the takeover)
5. If unclaimed → acquire CLAIM lock, add header, proceed

### Task Queue Priority (Multi-Agent)
When multiple agents compete for tasks:
```
Priority 1: CRITICAL tasks → fastest available agent
Priority 2: HIGH tasks → agent with matching capability
Priority 3: MEDIUM tasks → any idle agent, round-robin
Priority 4: LOW tasks → least-loaded agent
```

---

## Status Broadcasting

### Shared Status Board
**Location:** `AI_Employee_Vault/.sync/status_board.md`

```
# Agent Status Board
Updated: 2026-02-16 14:30:00

## In Progress
- AGENT-001 → Processing TASK-042 (Inbox file: proposal.pdf) [60% done]
- AGENT-003 → Generating weekly report [30% done]

## Completed (Last Hour)
- AGENT-001 → TASK-040 completed at 14:15 ✅
- AGENT-002 → TASK-041 completed at 14:20 ✅

## Blocked
- AGENT-002 → Waiting for AGENT-001 to release Dashboard.md lock

## Queue Depth
- Needs_Action: 5 tasks pending
- 2 agents idle → assign immediately
```

### Status Update Triggers
An agent MUST update the status board when:
- It starts a new task
- It completes a task
- It becomes blocked
- Its progress crosses 25% / 50% / 75% / 100%
- It encounters an error
- It goes idle

---

## Conflict Resolution

### Conflict Types and Responses

**Type 1: Write Conflict (same file)**
```
Situation: Two agents try to write Dashboard.md simultaneously

Resolution:
1. First agent to acquire WRITE lock wins
2. Second agent waits (up to 30 seconds)
3. After wait: second agent reads updated file, applies its changes on top
4. Log conflict in .sync/conflict_log.md
```

**Type 2: Task Conflict (same task)**
```
Situation: Two agents claim the same task

Resolution:
1. Check CLAIMED BY timestamp
2. Earlier timestamp wins
3. Later claimant releases claim, moves to next task
4. Log: "AGENT-002 deferred TASK-042 to AGENT-001 (earlier claim)"
```

**Type 3: Resource Conflict (dependency)**
```
Situation: AGENT-002 needs output from AGENT-001's in-progress task

Resolution:
1. AGENT-002 registers dependency in status board
2. AGENT-002 picks up other available tasks while waiting
3. AGENT-001 signals completion in status board
4. AGENT-002 resumes when dependency is met
```

**Type 4: Decision Conflict (agents disagree)**
```
Situation: AGENT-001 wants to archive file; AGENT-002 wants to process it

Resolution:
1. More conservative action wins (process, not archive)
2. Log disagreement in conflict_log.md
3. Escalate to human if conflict repeats 3+ times
```

### Conflict Log Format
**Location:** `AI_Employee_Vault/.sync/conflict_log.md`

```
## 2026-02-16 14:27:00 | WRITE CONFLICT
Resource: Dashboard.md
Agents Involved: AGENT-001, AGENT-003
Resolution: AGENT-001 won lock (first to claim)
AGENT-003: waited 8 seconds, applied changes after release
Impact: None (resolved automatically)
```

---

## Handoff Protocol

### Clean Handoff Steps
When one agent transfers work to another:

```
Step 1: HANDOFF INITIATION
        Agent A writes handoff record to .sync/handoffs/

Step 2: HANDOFF RECORD FORMAT
        FROM: AGENT-001
        TO: AGENT-002
        TASK: TASK-042
        REASON: Scheduled shutdown / resource limit / specialization needed
        STATE: 60% complete — file read, analysis done, writing summary pending
        FILES: AI_Employee_Vault/Inbox/proposal.pdf (DO NOT MOVE YET)
        LOCKS TRANSFERRED: none (agent releases all locks first)
        NOTES: Sentiment is positive, priority is HIGH

Step 3: AGENT B ACKNOWLEDGMENT
        Agent B reads handoff record
        Agent B adds: ACCEPTED BY: AGENT-002 AT: {timestamp}
        Agent B updates agents.md

Step 4: AGENT A CLEANUP
        Agent A removes its entry from active tasks
        Agent A releases all locks
        Agent A marks itself IDLE or OFFLINE

Step 5: CONTINUITY
        Agent B continues from documented state
        Agent B does NOT restart from scratch
```

---

## Sync Folder Structure

```
AI_Employee_Vault/
└── .sync/
    ├── agents.md               # Live agent registry
    ├── status_board.md         # Real-time work status
    ├── conflict_log.md         # History of conflicts + resolutions
    ├── locks/                  # One .lock file per locked resource
    │   ├── Dashboard.lock
    │   └── TASK-042.lock
    └── handoffs/               # Pending and completed handoffs
        └── HO-001.md
```

---

## Coordination Patterns

### Pattern 1: Leader-Worker
```
One LEADER agent:
  - Scans Needs_Action
  - Assigns tasks to WORKER agents
  - Monitors status board
  - Handles Dashboard updates

WORKER agents:
  - Accept assignments from leader
  - Process tasks
  - Report completion
  - Never touch Dashboard (leader owns it)
```

### Pattern 2: Peer-to-Peer
```
All agents are equal:
  - Each claims unclaimed tasks independently
  - Lock system prevents overlap
  - Status board keeps everyone informed
  - Conflict resolution is automatic
```

### Pattern 3: Specialist Routing
```
Tasks routed by type:
  - File tasks → File Understanding Agent
  - Report tasks → Reporting Agent
  - Email tasks → Communication Agent
  - Monitoring tasks → Monitoring Agent
  - All agents check type before claiming
```

---

## Smooth Workflow Rules

### DO
- Always check status board before starting work
- Always acquire lock before writing
- Always release lock immediately after writing
- Always update heartbeat every 60 seconds
- Always claim task before processing
- Always log handoffs completely
- Prefer picking IDLE tasks over interrupting WORKING agents

### DO NOT
- Never write to a file without a WRITE lock
- Never process a task without a CLAIM
- Never hold a lock longer than necessary
- Never ignore another agent's WORKING status
- Never leave stale locks (always release on exit)
- Never skip the status board update on completion

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| Task Management | Task claim/release protocol |
| Version Control | Lock before versioned writes |
| Monitoring | Watch agent heartbeats, alert on OFFLINE |
| Self-Healing | Recover stale locks, revive crashed agents |
| Delegation | Route tasks to correct specialist agent |
| Audit | Log all agent actions and handoffs |
| Security | Validate agent identity before lock grant |
| Workflow | Multi-agent workflows use sync at each step |

---

## Quick Reference

```
REGISTER AGENT:    Add row to .sync/agents.md
HEARTBEAT:         Update heartbeat column every 60s
CLAIM TASK:        Add CLAIMED BY header to task file
LOCK FILE:         Create .sync/locks/{resource}.lock
RELEASE LOCK:      Delete .sync/locks/{resource}.lock
BROADCAST STATUS:  Update .sync/status_board.md
HANDOFF:           Write to .sync/handoffs/HO-{id}.md
CONFLICT:          Log to .sync/conflict_log.md
AGENT OFFLINE:     Release locks after 5 min, reassign tasks
```

---

## Best Practices

1. **Lock duration = minimum needed** — release the moment write is done
2. **Status board = always current** — stale status causes poor decisions
3. **Heartbeat = non-negotiable** — missed heartbeat = declared OFFLINE
4. **Claim first, work second** — never process an unclaimed task
5. **Conservative conflict resolution** — when in doubt, do less and log it
6. **Handoffs = complete context** — receiving agent must not need to re-read everything
7. **One dashboard owner** — designate one agent as dashboard writer to avoid write storms
8. **Graceful shutdown** — agent going offline must release all locks and update registry
