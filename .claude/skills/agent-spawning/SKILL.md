# Agent Spawning Skill

## Purpose
Dynamically create, configure, launch, and terminate agents on demand. Spawn the right agent for the right job, track its lifecycle, manage parent-child relationships, and reclaim resources when work is done.

---

## Core Functions

1. **Spawn Agents** — Instantiate new agents from blueprints based on workload
2. **Configure Capabilities** — Assign skills, scope, and permissions at spawn time
3. **Lifecycle Management** — Track every agent from birth to termination
4. **Parent-Child Relationships** — Maintain spawn tree for accountability
5. **Resource Allocation** — Assign memory and task budgets per agent
6. **Graceful Termination** — Shut down agents cleanly with full handoff

---

## Agent Blueprints

### What is a Blueprint?
A blueprint is a pre-defined agent template. Spawning an agent means picking a blueprint, filling in runtime parameters, and registering the live instance.

### Blueprint Registry
**Location:** `AI_Employee_Vault/.sync/blueprints/`

### Blueprint Format
**Filename:** `{blueprint_id}.md`

```
# Blueprint: FILE_PROCESSOR
ID: BP-001
Version: 1.0
Description: Processes a single file from Inbox to Done

## Assigned Skills
- file-understanding
- risk-detection
- task-management
- audit
- error-recovery

## Scope
- READ:  AI_Employee_Vault/Inbox/
- WRITE: AI_Employee_Vault/Needs_Action/
- WRITE: AI_Employee_Vault/Done/
- WRITE: AI_Employee_Vault/Logs/
- READ:  AI_Employee_Vault/Company_Handbook.md

## Resource Limits
- Max Tasks: 1 (single-file processor)
- Max Runtime: 10 minutes
- Memory Budget: LOW (reads one file at a time)

## Spawn Trigger
- Condition: New file detected in Inbox
- Max Concurrent Instances: 3

## Auto-Terminate When
- Task file moved to Done
- Runtime limit exceeded
- Unrecoverable error
```

---

## Standard Blueprints

| Blueprint ID | Name | Purpose | Max Instances |
|---|---|---|---|
| BP-001 | FILE_PROCESSOR | Process one Inbox file end-to-end | 3 |
| BP-002 | REPORT_GENERATOR | Generate scheduled reports | 1 |
| BP-003 | INBOX_WATCHER | Monitor Inbox for new arrivals | 1 |
| BP-004 | DASHBOARD_UPDATER | Refresh Dashboard stats | 1 |
| BP-005 | KNOWLEDGE_BUILDER | Extract and store knowledge | 2 |
| BP-006 | HEALTH_MONITOR | Watch system vitals | 1 |
| BP-007 | EMAIL_DRAFTER | Draft outbound emails | 2 |
| BP-008 | ANALYST | Run analytics on vault data | 1 |
| BP-009 | COORDINATOR | Orchestrate multi-step workflows | 1 |
| BP-010 | EMERGENCY_RESPONDER | Handle critical failures | 1 |

---

## Spawn Protocol

### Step-by-Step Spawn Process

```
Step 1: EVALUATE NEED
        - Why is a new agent needed?
        - Is this workload within current agents' capacity?
        - Is max concurrent instances limit reached for this blueprint?
        → If limit reached: queue the work, do NOT spawn

Step 2: SELECT BLUEPRINT
        - Match task type to blueprint
        - Verify blueprint exists and is valid
        - Check resource headroom (RAM, task slots)

Step 3: GENERATE AGENT ID
        Format: AGENT-{BLUEPRINT_CODE}-{DATE}-{SEQUENCE}
        Example: AGENT-FP-20260216-003
        (FP = File Processor, 003 = third spawned today)

Step 4: CREATE SPAWN RECORD
        Location: AI_Employee_Vault/.sync/spawn_records/
        Filename: {AGENT_ID}.md
        (see Spawn Record Format below)

Step 5: REGISTER IN AGENT REGISTRY
        Add row to AI_Employee_Vault/.sync/agents.md
        Status: STARTING

Step 6: PASS CONTEXT
        Write task assignment to agent's context file
        Location: AI_Employee_Vault/.sync/contexts/{AGENT_ID}.md

Step 7: AGENT ACTIVATES
        Agent reads its context file
        Agent updates status: ACTIVE
        Agent begins work

Step 8: LOG SPAWN EVENT
        Write to AI_Employee_Vault/Logs/{DATE}.log
        Entry: "SPAWNED {AGENT_ID} from {BLUEPRINT_ID} by {PARENT_AGENT_ID}"
```

---

## Spawn Record Format

**Location:** `AI_Employee_Vault/.sync/spawn_records/{AGENT_ID}.md`

```
# Spawn Record: AGENT-FP-20260216-003

## Identity
Agent ID:       AGENT-FP-20260216-003
Blueprint:      BP-001 (FILE_PROCESSOR)
Spawned By:     AGENT-COORD-20260216-001
Spawned At:     2026-02-16 14:45:00
Purpose:        Process Inbox/proposal.pdf

## Assignment
Task ID:        TASK-047
Source File:    AI_Employee_Vault/Inbox/proposal.pdf
Target:         AI_Employee_Vault/Done/

## Skills Loaded
- file-understanding
- risk-detection
- task-management
- audit
- error-recovery

## Permissions
READ:  AI_Employee_Vault/Inbox/
WRITE: AI_Employee_Vault/Needs_Action/
WRITE: AI_Employee_Vault/Done/
WRITE: AI_Employee_Vault/Logs/

## Resource Allocation
Max Runtime:    10 minutes
Max Tasks:      1
Memory Budget:  LOW

## Lifecycle
Status:         ACTIVE
Started At:     2026-02-16 14:45:02
Completed At:   —
Terminated At:  —
Exit Reason:    —

## Outputs
Files Created:  —
Files Modified: —
Files Moved:    —
```

---

## Agent Context File

**Location:** `AI_Employee_Vault/.sync/contexts/{AGENT_ID}.md`

```
# Agent Context: AGENT-FP-20260216-003

## Your Mission
Process the file: AI_Employee_Vault/Inbox/proposal.pdf
Create task record, analyze content, move to Done, update logs.

## Your Constraints
- Only touch files listed in your Permissions
- Do not spawn sub-agents without approval
- Terminate yourself when task is complete
- Max runtime: 10 minutes

## Your Skills
Use these skills in this order:
1. file-understanding → analyze proposal.pdf
2. risk-detection → flag any concerns
3. task-management → update TASK-047
4. audit → log all actions
5. error-recovery → handle any failures

## Parent Agent
Report completion to: AGENT-COORD-20260216-001
Completion signal: Write DONE to .sync/signals/{AGENT_ID}_complete.md

## Current State
Status: STARTING
Last Updated: 2026-02-16 14:45:00
```

---

## Lifecycle State Machine

```
              SPAWN REQUEST
                   │
                   ▼
             [QUEUED] ──── capacity full ────► [WAITING]
                   │                                │
                   │ capacity available ◄───────────┘
                   ▼
            [STARTING] ← blueprint loaded, context written
                   │
                   ▼
             [ACTIVE] ← heartbeat every 60s
                   │
           ┌───────┼───────┐
           │       │       │
           ▼       ▼       ▼
       [PAUSED] [ERROR] [WORKING]
           │       │       │
           │  recover│      │ done
           └───────►│       │
                   │       ▼
                   ▼  [COMPLETING]
             [FAILED]      │
                   │       ▼
                   └──► [TERMINATED]
                              │
                              ▼
                        [ARCHIVED]
```

---

## Termination Protocol

### Normal Termination (Task Complete)
```
Step 1: Agent signals completion
        Write: .sync/signals/{AGENT_ID}_complete.md
        Contents: COMPLETE | {TASK_ID} | {timestamp} | SUCCESS

Step 2: Agent releases all locks
        Delete all files in .sync/locks/ owned by this agent

Step 3: Agent updates its spawn record
        Set: Completed At, Exit Reason: TASK_COMPLETE

Step 4: Agent updates agent registry
        Set status: TERMINATED

Step 5: Parent agent reads completion signal
        Parent logs: "AGENT-FP-20260216-003 completed TASK-047"
        Parent assigns next task or marks workflow done

Step 6: Cleanup (after 1 hour)
        Move spawn record to .sync/archive/
        Delete context file
        Delete signal file
```

### Forced Termination (Timeout / Error)
```
Step 1: Monitor detects agent exceeded runtime limit
        OR agent enters FAILED state

Step 2: Terminator (Coordinator or Monitor) writes:
        .sync/signals/{AGENT_ID}_terminate.md
        Contents: TERMINATE | REASON: {timeout/error} | {timestamp}

Step 3: Agent reads terminate signal on next loop iteration
        Agent saves current state to spawn record
        Agent releases all locks

Step 4: If task was in progress:
        Mark task: NEEDS_REASSIGNMENT in task file
        Parent re-evaluates: retry or escalate

Step 5: Log termination event
        AI_Employee_Vault/Logs/{DATE}.log
        Entry: "TERMINATED {AGENT_ID} | Reason: {reason} | Task: {TASK_ID}"
```

---

## Spawn Tree

### What is the Spawn Tree?
A record of which agent spawned which, forming a parent-child hierarchy.

**Location:** `AI_Employee_Vault/.sync/spawn_tree.md`

```
# Spawn Tree — 2026-02-16

AGENT-COORD-20260216-001 [COORDINATOR] ← ROOT (spawned by human/scheduler)
├── AGENT-FP-20260216-001 [FILE_PROCESSOR] — TASK-045 ✅
├── AGENT-FP-20260216-002 [FILE_PROCESSOR] — TASK-046 ✅
├── AGENT-FP-20260216-003 [FILE_PROCESSOR] — TASK-047 🔄
├── AGENT-RG-20260216-001 [REPORT_GENERATOR] — RPT-DAILY ✅
└── AGENT-KB-20260216-001 [KNOWLEDGE_BUILDER] — KB-UPDATE ⏳
```

### Spawn Tree Rules
- Maximum depth: **3 levels** (Root → Child → Grandchild)
- Grandchildren cannot spawn further agents
- Every agent knows its parent ID
- Root agent is always a COORDINATOR or human-initiated

---

## Concurrency Limits

### Global Limits
| Tier | Max Total Agents | Max Workers | Max Coordinators |
|------|-----------------|-------------|-----------------|
| Bronze | 3 | 2 | 1 |
| Silver | 8 | 6 | 2 |
| Gold | 20 | 16 | 4 |
| Platinum | 50 | 42 | 8 |

### Per-Blueprint Limits (Bronze)
| Blueprint | Max Instances |
|-----------|-------------|
| FILE_PROCESSOR | 2 |
| REPORT_GENERATOR | 1 |
| INBOX_WATCHER | 1 |
| DASHBOARD_UPDATER | 1 |
| All others | 1 each |

### When Limit Reached
1. New spawn request goes to WAITING queue
2. Coordinator checks every 30 seconds for available slots
3. When a slot opens → spawn queued agent
4. If waiting >5 minutes → log warning, notify human

---

## Spawn Decision Rules

### SPAWN when:
- Task volume exceeds current agent capacity
- A task requires specialist skills not in current agents
- Parallel processing would reduce total time significantly
- A workflow step is blocked waiting for a dedicated resource

### DO NOT SPAWN when:
- Existing idle agent can handle the task
- Max concurrent instances limit is reached
- Available memory is below LOW threshold
- Task is too small (< 2 minutes work) — handle inline instead
- Spawning would create depth > 3 in spawn tree

---

## Resource Budgets

### Memory Tiers
| Tier | RAM Budget | Suitable For |
|------|-----------|--------------|
| MINIMAL | < 10MB | Read-only analysis, small files |
| LOW | 10–50MB | Single file processing |
| MEDIUM | 50–150MB | Multi-file workflows, reports |
| HIGH | 150–300MB | Heavy analytics, large datasets |

### Bronze Tier Total Budget
- OS + VS Code: ~2.5GB
- Watcher: ~50MB
- Claude Primary: ~300MB
- Max 2 spawned agents × LOW = ~100MB
- **Headroom: ~5GB** ✅

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|------------------|
| Multi-Agent Sync | All spawned agents register and use lock system |
| Delegation | Delegation routes work; Spawning creates capacity |
| Monitoring | Watches heartbeats of all spawned agents |
| Self-Healing | Recovers crashed spawned agents automatically |
| Optimization | Enforces memory budgets at spawn time |
| Audit | Logs every spawn and termination event |
| Workflow | Workflow steps may trigger agent spawns |
| Task Management | Each spawned agent owns exactly one task (Bronze) |
| Scheduler | Scheduler triggers spawns at scheduled times |

---

## Quick Reference

```
SPAWN AGENT:       Select blueprint → generate ID → write spawn record → register
AGENT ID FORMAT:   AGENT-{BP_CODE}-{YYYYMMDD}-{SEQ}
CONTEXT FILE:      .sync/contexts/{AGENT_ID}.md
SPAWN RECORD:      .sync/spawn_records/{AGENT_ID}.md
COMPLETE SIGNAL:   .sync/signals/{AGENT_ID}_complete.md
TERMINATE SIGNAL:  .sync/signals/{AGENT_ID}_terminate.md
SPAWN TREE:        .sync/spawn_tree.md
MAX DEPTH:         3 levels (Root → Child → Grandchild)
HEARTBEAT:         Every 60 seconds (inherited from Multi-Agent Sync)
BRONZE MAX AGENTS: 3 total (1 coordinator + 2 workers)
```

---

## Best Practices

1. **Spawn for parallelism, not for isolation** — only spawn if tasks can genuinely run in parallel
2. **One task per spawned agent (Bronze)** — keep scope tight
3. **Always write context before activating** — agent must know its mission before it starts
4. **Parent is responsible for its children** — if child fails, parent handles reassignment
5. **Terminate promptly** — do not leave idle agents running; reclaim resources immediately
6. **Blueprint first** — never spawn a custom one-off agent; always use or extend a blueprint
7. **Log everything** — spawn, activate, complete, terminate all go to the audit log
8. **Respect depth limit** — 3 levels max, no exceptions; prevents runaway spawn cascades
