# Event Bus Skill

## Purpose
Provide a central event system where any part of the AI Employee can publish events (something happened) and any other part can subscribe and react. Decouples producers from consumers — the file watcher doesn't need to know who cares about new files, it just fires an event.

---

## Core Functions

1. **Publish Events** — Any skill or agent announces something happened
2. **Subscribe to Events** — Skills/agents declare what events they care about
3. **Route Events** — Deliver each event to all matching subscribers
4. **Persist Events** — Write events to disk so none are lost
5. **Replay Events** — Catch up on missed events after restart
6. **Dead Letter Handling** — Events no subscriber processed go to dead letter queue

---

## Event Structure

### Event Format
Every event follows this standard structure:

```
EVENT
ID:          EVT-20260216-000147
Type:        FILE_DETECTED
Timestamp:   2026-02-16 14:30:00
Source:      watcher/filesystem_watcher
Priority:    HIGH
Payload:
  file_path: AI_Employee_Vault/Inbox/proposal.pdf
  file_size: 245000
  file_type: PDF
  detected_at: 2026-02-16 14:30:00
Status:      PENDING
Attempts:    0
```

### Event Fields
| Field | Description | Required |
|-------|-------------|----------|
| ID | Unique event identifier | Yes |
| Type | What kind of event (see Event Catalog) | Yes |
| Timestamp | When it was published (ISO format) | Yes |
| Source | Which skill/agent/watcher published it | Yes |
| Priority | CRITICAL / HIGH / MEDIUM / LOW | Yes |
| Payload | Event-specific data (key-value pairs) | Yes |
| Status | PENDING / DELIVERED / FAILED / DEAD | Yes |
| Attempts | How many delivery attempts made | Yes |

### Event ID Format
```
EVT-{YYYYMMDD}-{6-digit sequence}
Example: EVT-20260216-000147
```

---

## Event Catalog

### System Events
| Event Type | Trigger | Priority |
|-----------|---------|----------|
| `SYSTEM_STARTED` | AI Employee session begins | HIGH |
| `SYSTEM_STOPPING` | Graceful shutdown initiated | HIGH |
| `SYSTEM_MODE_CHANGED` | Mode switches (NORMAL→BURST etc.) | MEDIUM |
| `HEALTH_CHECK_PASSED` | Validation check succeeds | LOW |
| `HEALTH_CHECK_FAILED` | Validation check fails | HIGH |
| `STATE_RECOVERED` | Recovery after crash/restart | HIGH |

### File Events
| Event Type | Trigger | Priority |
|-----------|---------|----------|
| `FILE_DETECTED` | New file appears in Inbox | HIGH |
| `FILE_PROCESSED` | File moved to Done | MEDIUM |
| `FILE_FAILED` | File processing failed | HIGH |
| `FILE_UNKNOWN_TYPE` | Unrecognized file extension | MEDIUM |
| `INBOX_EMPTY` | Inbox has no more files | LOW |
| `INBOX_SURGE` | 5+ files arrive within 10 minutes | HIGH |

### Task Events
| Event Type | Trigger | Priority |
|-----------|---------|----------|
| `TASK_CREATED` | New task file in Needs_Action | HIGH |
| `TASK_CLAIMED` | Agent claims a task | MEDIUM |
| `TASK_COMPLETED` | Task moved to Done | MEDIUM |
| `TASK_FAILED` | Task processing failed | HIGH |
| `TASK_BLOCKED` | Task waiting on dependency | MEDIUM |
| `TASK_OVERDUE` | Task past its SLA | HIGH |

### Agent Events
| Event Type | Trigger | Priority |
|-----------|---------|----------|
| `AGENT_SPAWNED` | New agent created | MEDIUM |
| `AGENT_ACTIVATED` | Agent begins work | LOW |
| `AGENT_COMPLETED` | Agent finishes its mission | MEDIUM |
| `AGENT_CRASHED` | Agent missed heartbeats | CRITICAL |
| `AGENT_OFFLINE` | Agent declared offline | HIGH |
| `AGENT_RECOVERED` | Crashed agent restored | MEDIUM |

### Pipeline Events
| Event Type | Trigger | Priority |
|-----------|---------|----------|
| `PIPELINE_STARTED` | New pipeline run begins | MEDIUM |
| `PIPELINE_STAGE_COMPLETED` | One stage finishes | LOW |
| `PIPELINE_COMPLETED` | All stages done successfully | MEDIUM |
| `PIPELINE_FAILED` | Pipeline aborted due to error | HIGH |
| `PIPELINE_STALLED` | Pipeline no progress for >5 min | HIGH |

### Knowledge Events
| Event Type | Trigger | Priority |
|-----------|---------|----------|
| `KNOWLEDGE_ADDED` | New KB entry created | LOW |
| `KNOWLEDGE_UPDATED` | Existing entry modified | LOW |
| `KNOWLEDGE_CONFLICT` | Contradicting entries detected | MEDIUM |

### Alert Events
| Event Type | Trigger | Priority |
|-----------|---------|----------|
| `ALERT_LOW_DISK` | Disk space <10% free | HIGH |
| `ALERT_HIGH_MEMORY` | RAM usage >85% | HIGH |
| `ALERT_ERROR_SPIKE` | >5 errors in 10 minutes | CRITICAL |
| `ALERT_HUMAN_NEEDED` | Action requires human decision | HIGH |

---

## Subscription Registry

### What is a Subscription?
A declaration: "When event type X occurs, notify me."

**Location:** `AI_Employee_Vault/.events/subscriptions.md`

```
# Event Subscriptions
Last Updated: 2026-02-16 09:00:00

| Subscription ID | Subscriber         | Event Types                        | Filter               | Action |
|-----------------|--------------------|------------------------------------|----------------------|--------|
| SUB-001         | pipeline-skill     | FILE_DETECTED                      | priority >= HIGH     | SPAWN_PIPELINE(PL-001) |
| SUB-002         | notification-skill | AGENT_CRASHED, ALERT_*             | —                    | NOTIFY_HUMAN |
| SUB-003         | self-healing-skill | AGENT_CRASHED, PIPELINE_STALLED    | —                    | TRIGGER_RECOVERY |
| SUB-004         | monitoring-skill   | HEALTH_CHECK_FAILED, ALERT_*       | —                    | LOG_AND_ALERT |
| SUB-005         | reporting-skill    | TASK_COMPLETED, FILE_PROCESSED     | —                    | UPDATE_DAILY_STATS |
| SUB-006         | dashboard-skill    | TASK_CREATED, TASK_COMPLETED       | —                    | REFRESH_DASHBOARD |
| SUB-007         | learning-skill     | TASK_COMPLETED, TASK_FAILED        | —                    | EXTRACT_LESSON |
| SUB-008         | audit-skill        | *                                  | —                    | LOG_ALL_EVENTS |
| SUB-009         | scheduler-skill    | SYSTEM_STARTED                     | —                    | LOAD_SCHEDULE |
| SUB-010         | knowledge-skill    | FILE_PROCESSED                     | —                    | INGEST_KNOWLEDGE |
```

### Subscription Filters
Subscribers can filter by:
- **Priority:** `priority >= HIGH` — only receive HIGH and CRITICAL
- **Source:** `source == watcher/*` — only from watchers
- **Payload field:** `file_type == PDF` — only PDF file events
- **Wildcard:** `ALERT_*` — all events starting with ALERT_

---

## Event Lifecycle

```
PUBLISHER                    EVENT BUS                    SUBSCRIBER
    │                            │                             │
    │── publish(FILE_DETECTED) ──►│                             │
    │                            │ validate event format        │
    │                            │ assign EVT-ID                │
    │                            │ write to event_queue.md      │
    │                            │ match subscriptions          │
    │                            │── deliver(EVT) ─────────────►│
    │                            │                             │ process event
    │                            │◄── ACK ─────────────────────│
    │                            │ mark DELIVERED               │
    │                            │ write to event_log.md        │
```

---

## Publish Protocol

### Steps to Publish an Event
```
Step 1: CREATE event record
        Assign EVT-ID (sequential)
        Fill all required fields
        Set Status: PENDING

Step 2: VALIDATE event
        Event type must be in Event Catalog (or custom registered)
        Payload must match expected fields for that type
        Priority must be set

Step 3: WRITE to event queue
        Append to AI_Employee_Vault/.events/queue.md
        (atomic append — use lock)

Step 4: BUS PROCESSES queue
        Read all PENDING events
        For each event:
          → Find matching subscriptions
          → Deliver to each subscriber
          → Mark DELIVERED or FAILED

Step 5: ARCHIVE
        Move DELIVERED events to event_log.md
        Keep queue.md lean (only PENDING/FAILED)
```

---

## Delivery Protocol

### How Events Are Delivered
Events are file-based — delivery means writing a notification file the subscriber reads.

**Delivery File Location:** `AI_Employee_Vault/.events/inbox/{SUBSCRIBER_ID}/`
**Delivery Filename:** `{EVT_ID}.md`

```
# Event Delivery
Event ID:      EVT-20260216-000147
Event Type:    FILE_DETECTED
Delivered At:  2026-02-16 14:30:05
For:           pipeline-skill (SUB-001)
Priority:      HIGH

## Payload
file_path: AI_Employee_Vault/Inbox/proposal.pdf
file_type: PDF
detected_at: 2026-02-16 14:30:00

## Required Action
SPAWN_PIPELINE(PL-001) with input: file_path
```

### Subscriber Reading Events
Each subscriber checks its inbox folder on every cycle:
```
Step 1: Scan .events/inbox/{my_id}/ for new delivery files
Step 2: Read each delivery file in priority order (CRITICAL first)
Step 3: Execute the required action
Step 4: Write ACK file: .events/inbox/{my_id}/{EVT_ID}.ack
Step 5: Event Bus reads ACK, marks event DELIVERED, deletes delivery file
```

---

## Failure Handling

### Delivery Failure
If a subscriber fails to ACK within its timeout:

```
Attempt 1: Deliver → wait 60 seconds for ACK
Attempt 2: Re-deliver → wait 60 seconds for ACK
Attempt 3: Re-deliver → wait 60 seconds for ACK
After 3 failures: Move event to DEAD LETTER QUEUE
```

### Dead Letter Queue
**Location:** `AI_Employee_Vault/.events/dead_letter.md`

```
# Dead Letter Queue
Last Updated: 2026-02-16 14:45:00

| Event ID            | Type          | Failed Subscriber  | Attempts | Reason              |
|---------------------|---------------|--------------------|----------|---------------------|
| EVT-20260216-000143 | FILE_DETECTED | pipeline-skill     | 3        | No ACK received     |
| EVT-20260216-000139 | TASK_CREATED  | dashboard-skill    | 3        | Subscriber offline  |
```

### Dead Letter Resolution
- Human reviews dead_letter.md
- Options: Manual retry / Skip / Reassign to different subscriber
- CRITICAL priority dead letters → immediate human notification

---

## Event Log

### Persistent Event History
**Location:** `AI_Employee_Vault/.events/event_log.md`

```
# Event Log — 2026-02-16
Total Events: 147 | Delivered: 145 | Failed: 2 | Dead: 0

| Time     | Event ID            | Type               | Source           | Status    |
|----------|---------------------|--------------------|------------------|-----------|
| 14:30:00 | EVT-20260216-000147 | FILE_DETECTED      | filesystem_watcher| DELIVERED |
| 14:30:05 | EVT-20260216-000148 | PIPELINE_STARTED   | pipeline-skill   | DELIVERED |
| 14:30:07 | EVT-20260216-000149 | TASK_CREATED       | task-mgmt-skill  | DELIVERED |
| 14:38:00 | EVT-20260216-000150 | PIPELINE_COMPLETED | pipeline-skill   | DELIVERED |
| 14:38:02 | EVT-20260216-000151 | TASK_COMPLETED     | agent-fp-003     | DELIVERED |
| 14:38:04 | EVT-20260216-000152 | FILE_PROCESSED     | pipeline-skill   | DELIVERED |
```

---

## Event Replay

### Why Replay?
After a system restart or agent crash, subscribers may have missed events. Replay lets them catch up.

### Replay Protocol
```
Step 1: Subscriber requests replay
        Writes: .events/replay_requests/{subscriber_id}.md
        Contents:
          FROM: 2026-02-16 14:00:00
          TO:   2026-02-16 14:30:00 (or "NOW")
          TYPES: FILE_DETECTED, TASK_CREATED (or "ALL")

Step 2: Event Bus reads replay request
        Searches event_log.md for matching events in time range

Step 3: Re-delivers matching events to subscriber inbox
        Marks as REPLAY (not original PENDING)

Step 4: Subscriber processes replay events
        Subscriber must be idempotent (same event twice = same result)
```

### Replay Rules
- Max replay window: **24 hours** back
- Replay events are labeled `REPLAY` so subscribers know
- Subscribers must handle duplicates gracefully (idempotency)
- CRITICAL events always replayed first

---

## Event Bus Folder Structure

```
AI_Employee_Vault/
└── .events/
    ├── queue.md                    # Pending events waiting for delivery
    ├── event_log.md                # Delivered event history (current day)
    ├── subscriptions.md            # All subscriber registrations
    ├── dead_letter.md              # Undeliverable events
    ├── inbox/                      # Per-subscriber delivery folders
    │   ├── pipeline-skill/         # Events waiting for pipeline-skill
    │   ├── notification-skill/     # Events waiting for notification-skill
    │   ├── self-healing-skill/     # Events waiting for self-healing-skill
    │   └── audit-skill/            # Events waiting for audit-skill
    ├── replay_requests/            # Pending replay requests
    └── archive/                    # Daily event logs older than today
        └── 2026-02-15_event_log.md
```

---

## Event Priority Processing Order

Events in queue are always processed in this order:
```
1. CRITICAL  → Process immediately, before anything else
2. HIGH      → Process next, within 30 seconds
3. MEDIUM    → Process within 2 minutes
4. LOW       → Process within 5 minutes
```

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|-----------------|
| Monitoring | Subscribes to all ALERT_* and HEALTH_CHECK_FAILED events |
| Self-Healing | Subscribes to AGENT_CRASHED, PIPELINE_STALLED, PIPELINE_FAILED |
| Pipeline | Subscribes to FILE_DETECTED to auto-start processing pipelines |
| Notification | Subscribes to CRITICAL and HIGH events for human alerts |
| Task Management | Publishes TASK_CREATED, TASK_COMPLETED, TASK_FAILED |
| Agent Spawning | Publishes AGENT_SPAWNED, AGENT_CRASHED |
| Audit | Subscribes to ALL events (wildcard) for full audit log |
| Learning | Subscribes to TASK_COMPLETED and TASK_FAILED to extract lessons |
| Scheduler | Publishes scheduled trigger events at defined times |
| State Management | Subscribes to state-changing events to update .state/ files |

---

## Quick Reference

```
PUBLISH EVENT:     Write to .events/queue.md (use WRITE lock)
SUBSCRIBE:         Add row to .events/subscriptions.md
CHECK INBOX:       Scan .events/inbox/{my_id}/ each cycle
ACK EVENT:         Write .events/inbox/{my_id}/{EVT_ID}.ack
DEAD LETTER:       .events/dead_letter.md
EVENT LOG:         .events/event_log.md
REPLAY:            Write to .events/replay_requests/{my_id}.md
MAX REPLAY:        24 hours back
RETRY LIMIT:       3 attempts before dead letter
CRITICAL SLA:      Process immediately
HIGH SLA:          Within 30 seconds
MEDIUM SLA:        Within 2 minutes
LOW SLA:           Within 5 minutes
```

---

## Best Practices

1. **Publish facts, not commands** — `FILE_DETECTED` not `PLEASE_PROCESS_FILE` — let subscribers decide what to do
2. **Be idempotent** — processing the same event twice must produce the same result
3. **Keep payloads small** — include references (file_path) not full content
4. **Always ACK** — subscribers must ACK every event, even if they chose to ignore it
5. **Never block the bus** — subscriber processing must not slow down event delivery
6. **Dead letters need attention** — review dead_letter.md daily
7. **Prioritize correctly** — CRITICAL is for true emergencies only; overuse makes it meaningless
8. **Audit subscribes to everything** — Audit Skill is the one subscriber that never filters
9. **One event per thing** — don't bundle multiple things into one event; publish separately
10. **Log before act** — event is written to log before subscriber action begins
