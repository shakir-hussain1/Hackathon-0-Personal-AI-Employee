# Queue Management Skill

## Purpose
Manage all work queues in the AI Employee system. Control what gets processed next, in what order, at what time, and by whom. Prevent overload, ensure fairness, and guarantee no work item is ever lost or silently skipped.

---

## Core Functions

1. **Enqueue** — Add work items to the correct queue
2. **Dequeue** — Pull the next highest-priority item for processing
3. **Prioritize** — Order items by urgency, type, and age
4. **Delay** — Hold items until a future time or condition
5. **Requeue** — Return failed items for retry
6. **Monitor** — Track depth, age, and throughput of every queue
7. **Drain** — Safely empty a queue during shutdown

---

## Queue Types

### Type 1: Priority Queue
Items ordered by priority level, then by arrival time within the same priority.

```
Use for: Task Queue, Alert Queue
Ordering: CRITICAL → HIGH → MEDIUM → LOW → (within same level: oldest first)
```

### Type 2: FIFO Queue (First In, First Out)
Items processed strictly in arrival order.

```
Use for: Event Log Queue, Audit Queue
Ordering: Arrival timestamp — oldest item always next
```

### Type 3: Scheduled Queue
Items held until their scheduled time, then released to the priority queue.

```
Use for: Scheduler Queue
Ordering: Scheduled time — earliest release time first
```

### Type 4: Delayed Retry Queue
Failed items held for a cooling-off period before being retried.

```
Use for: Retry Queue (pipeline stages, event delivery)
Ordering: Retry-after timestamp — earliest eligible first
```

### Type 5: Dead Letter Queue
Items that exhausted all retries and need human review.

```
Use for: Unprocessable tasks, undeliverable events
Ordering: FIFO — oldest dead letter reviewed first
```

---

## Queue Registry

**Location:** `AI_Employee_Vault/.queues/registry.md`

```
# Queue Registry
Last Updated: 2026-02-16 14:30:00

| Queue ID    | Name              | Type       | Max Depth | Current Depth | Status  |
|-------------|-------------------|------------|-----------|---------------|---------|
| Q-001       | Task Queue        | PRIORITY   | 100       | 4             | HEALTHY |
| Q-002       | Event Queue       | FIFO       | 500       | 12            | HEALTHY |
| Q-003       | Scheduled Queue   | SCHEDULED  | 50        | 3             | HEALTHY |
| Q-004       | Retry Queue       | DELAYED    | 30        | 1             | HEALTHY |
| Q-005       | Dead Letter Queue | FIFO       | 100       | 2             | WARNING |
| Q-006       | Agent Work Queue  | PRIORITY   | 20        | 2             | HEALTHY |
| Q-007       | Audit Log Queue   | FIFO       | 1000      | 47            | HEALTHY |
| Q-008       | Notification Queue| PRIORITY   | 50        | 0             | IDLE    |
```

---

## Queue Item Format

Every item in any queue uses this standard format:

```
# Queue Item
Item ID:        QI-20260216-000892
Queue:          Q-001 (Task Queue)
Type:           TASK
Priority:       HIGH
Status:         PENDING

## Payload
task_id:        TASK-047
file_path:      AI_Employee_Vault/Inbox/proposal.pdf
file_type:      PDF
created_by:     filesystem_watcher

## Timing
Enqueued At:    2026-02-16 14:25:00
Scheduled For:  — (immediate)
Retry After:    — (not in retry)
Expires At:     2026-02-16 15:25:00 (1 hour TTL)

## Processing
Attempts:       0
Max Attempts:   3
Assigned To:    —
Started At:     —

## History
2026-02-16 14:25:00 | ENQUEUED by filesystem_watcher
```

### Item ID Format
```
QI-{YYYYMMDD}-{6-digit sequence}
Example: QI-20260216-000892
```

---

## Queue File Structure

```
AI_Employee_Vault/
└── .queues/
    ├── registry.md              # All queues overview
    ├── task_queue/
    │   ├── pending/             # Items waiting to be processed
    │   ├── in_progress/         # Items currently being worked
    │   └── completed/           # Done (short-term retention)
    ├── event_queue/
    │   ├── pending/
    │   └── delivered/
    ├── scheduled_queue/
    │   └── pending/             # All items, sorted by scheduled_for
    ├── retry_queue/
    │   └── pending/             # Items with retry_after timestamp
    ├── dead_letter_queue/
    │   └── items/               # Permanently failed items
    ├── agent_work_queue/
    │   └── pending/
    ├── notification_queue/
    │   └── pending/
    └── metrics.md               # Queue performance statistics
```

---

## Core Operations

### ENQUEUE — Add Item to Queue

```
Step 1: CREATE queue item record (standard format above)
Step 2: ASSIGN Item ID (QI-{date}-{sequence})
Step 3: VALIDATE item (required fields present, priority valid, TTL set)
Step 4: ACQUIRE write lock on target queue folder
Step 5: WRITE item file to {queue}/pending/
Step 6: RELEASE lock
Step 7: UPDATE registry.md (increment current depth)
Step 8: PUBLISH event: ITEM_ENQUEUED (for monitoring)
Step 9: LOG enqueue action in item history
```

### DEQUEUE — Pull Next Item for Processing

```
Step 1: ACQUIRE read lock on queue pending folder
Step 2: SCAN all items in pending/
Step 3: SORT by queue type rules:
        Priority queue → sort by: priority DESC, enqueued_at ASC
        FIFO queue     → sort by: enqueued_at ASC
        Scheduled queue→ filter scheduled_for <= NOW, then sort by scheduled_for ASC
        Retry queue    → filter retry_after <= NOW, then sort by retry_after ASC
Step 4: SELECT top item
        → If queue is empty: return EMPTY signal
Step 5: CHECK expiry: if expires_at < NOW → move to dead_letter, dequeue next
Step 6: MOVE item from pending/ to in_progress/
Step 7: UPDATE item: Status = IN_PROGRESS, Started At = NOW, Assigned To = {agent_id}
Step 8: RELEASE lock
Step 9: UPDATE registry.md (depth unchanged — item still "in" queue)
Step 10: RETURN item to caller
```

### COMPLETE — Mark Item as Done

```
Step 1: MOVE item from in_progress/ to completed/
Step 2: UPDATE item: Status = COMPLETED, Completed At = NOW
Step 3: UPDATE registry.md (decrement current depth)
Step 4: PUBLISH event: ITEM_COMPLETED
Step 5: CLEANUP: delete completed/ items older than 24 hours
```

### FAIL — Item Processing Failed

```
Step 1: READ item from in_progress/
Step 2: INCREMENT attempts counter
Step 3: CHECK attempts vs max_attempts:
        attempts < max_attempts → REQUEUE with delay
        attempts >= max_attempts → DEAD LETTER

Step 4a: REQUEUE path
         Calculate retry_after = NOW + (attempts × retry_delay_seconds)
         Move item to retry_queue/pending/
         Update status: RETRY_PENDING

Step 4b: DEAD LETTER path
         Move item to dead_letter_queue/items/
         Update status: DEAD
         PUBLISH event: ITEM_DEAD
         NOTIFY: human review needed

Step 5: UPDATE registry.md
Step 6: LOG failure reason in item history
```

### PEEK — Inspect Without Removing

```
Step 1: READ pending/ folder without acquiring write lock
Step 2: SORT per queue rules
Step 3: RETURN top N items (default: 5) without moving them
Step 4: No state changes — peek is always read-only
```

### REORDER — Change an Item's Priority

```
Step 1: FIND item in pending/ by Item ID
Step 2: ACQUIRE write lock
Step 3: UPDATE priority field in item file
Step 4: LOG: "Priority changed: {old} → {new} by {agent}"
Step 5: RELEASE lock
Note: Reorder only works on PENDING items, never IN_PROGRESS
```

---

## Priority Ordering

### Priority Levels and Weights

| Priority | Weight | Max Wait Before Escalation |
|----------|--------|---------------------------|
| CRITICAL | 1000 | None — process immediately |
| HIGH | 100 | 5 minutes |
| MEDIUM | 10 | 30 minutes |
| LOW | 1 | 2 hours |

### Age Escalation
To prevent starvation, items gain priority weight over time:

```
Every 10 minutes waiting: +5 weight points
MEDIUM item waiting 30 min: weight 10 + 15 = 25
(Still below HIGH at 100, but gaining on new LOW items at 1)

MEDIUM item waiting 2 hours: weight 10 + 60 = 70
(Now competing with some HIGH items)

Escalation cap: Never exceeds next priority tier's base weight
```

---

## Queue Capacity Management

### What Happens When a Queue is Full

| Queue | At 80% Capacity | At 100% Capacity |
|-------|----------------|-----------------|
| Task Queue | WARN human | Reject new items, ALERT |
| Event Queue | WARN system | Drop LOW events, keep HIGH+ |
| Notification Queue | No action | Drop LOW notifications |
| Dead Letter Queue | ALERT human | CRITICAL alert to human |
| Retry Queue | WARN system | Fast-fail retries to dead letter |

### Capacity Alerts
```
Q-001 (Task Queue): depth 80/100 → WARNING: Task queue at 80% capacity
Q-001 (Task Queue): depth 100/100 → CRITICAL: Task queue FULL — new items rejected
```

---

## Queue Monitoring

### Queue Health Check (every 5 minutes)

For each queue, check:
```
1. DEPTH OK?        current_depth / max_depth < 0.8
2. OLDEST OK?       oldest pending item age < SLA for its priority
3. STUCK ITEMS?     any IN_PROGRESS item with started_at > max_processing_time
4. DEAD LETTERS?    dead_letter count > 0 → flag for human review
5. RETRY BUILDUP?   retry_queue depth growing → possible systemic failure
```

### Queue Metrics (`metrics.md`)

```
# Queue Metrics — 2026-02-16 14:30:00

## Task Queue (Q-001)
Current Depth: 4
Enqueued Today: 12
Completed Today: 8
Failed Today: 0
Dead Today: 0
Avg Wait Time: 2m 15s
Avg Processing Time: 4m 30s
Throughput: 8 tasks / day

## Event Queue (Q-002)
Current Depth: 12
Enqueued Today: 147
Delivered Today: 135
Failed Deliveries: 2
Avg Delivery Lag: 4s

## Dead Letter Queue (Q-005)
Current Depth: 2
Oldest Item: 2026-02-16 11:20:00 (3h 10m ago)
Action Required: YES — human review needed
```

---

## Queue SLAs

Maximum wait times before an item is considered overdue:

| Queue | Priority | SLA |
|-------|----------|-----|
| Task Queue | CRITICAL | 30 seconds |
| Task Queue | HIGH | 5 minutes |
| Task Queue | MEDIUM | 30 minutes |
| Task Queue | LOW | 2 hours |
| Event Queue | CRITICAL | Immediate |
| Event Queue | HIGH | 30 seconds |
| Notification Queue | CRITICAL | 1 minute |
| Notification Queue | HIGH | 5 minutes |
| Dead Letter Queue | Any | Human review within 24 hours |

### SLA Breach Response
```
SLA Breach Detected:
  Item: QI-20260216-000892
  Queue: Task Queue
  Priority: HIGH
  Enqueued: 14:25:00
  SLA: 5 minutes
  Current Wait: 7 minutes (2 min overdue)

Response:
  1. Escalate priority: HIGH → CRITICAL
  2. Publish event: TASK_OVERDUE
  3. Notification: Alert human if still unprocessed after 10 min
```

---

## Graceful Drain (Shutdown)

When the system is shutting down:

```
Step 1: STOP accepting new items to all queues
Step 2: FINISH all IN_PROGRESS items (allow up to 5 minutes)
Step 3: SNAPSHOT queue state for each queue
        Record: all pending items, their position, their data
Step 4: PERSIST pending items to disk (they are already in .queues/)
Step 5: MARK any abandoned IN_PROGRESS items as INTERRUPTED
        (they will be re-queued as PENDING on next startup)
Step 6: LOG: "Queue drain complete — N items preserved for next session"
```

### Startup Queue Recovery

On system start:
```
Step 1: READ all queue folders
Step 2: Find IN_PROGRESS items from last session → move to PENDING (top of queue)
Step 3: Find SCHEDULED items whose time has passed → move to priority queue immediately
Step 4: Find RETRY items whose retry_after has passed → move to priority queue
Step 5: Update registry depths from actual folder counts
Step 6: LOG: "Queue recovery: N items restored, M scheduled items promoted"
```

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|-----------------|
| Task Management | All tasks enter via Task Queue (Q-001) |
| Event Bus | Events flow through Event Queue (Q-002) |
| Scheduler | Scheduled jobs enter Scheduled Queue (Q-003) |
| Self-Healing | Monitors queue health, rescues stuck items |
| Monitoring | Watches queue depth, SLA breaches, dead letters |
| Pipeline | Pipeline runs queued when capacity full |
| Agent Spawning | Agent work assignments via Agent Work Queue (Q-006) |
| Notification | All alerts go through Notification Queue (Q-008) |
| State Management | Queue depths reflected in system state |
| Optimization | Adjusts queue processing rate by system mode |

---

## Quick Reference

```
ENQUEUE:            Write item to {queue}/pending/ (with write lock)
DEQUEUE:            Read + move top item pending/ → in_progress/
COMPLETE:           Move item in_progress/ → completed/
FAIL (retry):       Move item in_progress/ → retry_queue/pending/
FAIL (dead):        Move item in_progress/ → dead_letter_queue/items/
PEEK:               Read pending/ without moving anything
REORDER:            Update priority field on pending item

PRIORITY ORDER:     CRITICAL → HIGH → MEDIUM → LOW → (oldest first within same level)
AGE ESCALATION:     +5 weight per 10 min wait (cap at next tier)
SLA BREACH:         Escalate priority + publish TASK_OVERDUE event

QUEUE CAPACITY:     80% = WARN, 100% = REJECT/DROP
DRAIN ON SHUTDOWN:  Finish in-progress, persist pending, log interrupted
RECOVERY ON START:  Restore interrupted → PENDING, promote overdue scheduled
```

---

## Best Practices

1. **One queue per concern** — tasks, events, notifications each have their own queue
2. **Always set TTL** — every item must have an expires_at; nothing lives forever in a queue
3. **Peek before dequeue** — inspect queue state before committing to pull an item
4. **Never lose an item** — FAIL → RETRY → DEAD LETTER; items are always moved, never deleted silently
5. **SLA drives priority** — overdue items escalate automatically; no manual intervention needed
6. **Dead letters need eyes** — a growing dead letter queue is a sign of systemic failure
7. **Drain gracefully** — never kill the system with items in-progress; always finish or mark interrupted
8. **Monitor depth trends** — a slowly growing queue means processing is slower than arrival rate
9. **Lock before write** — all enqueue/dequeue operations acquire a lock to prevent race conditions
10. **Recovery on startup** — always restore queue state before starting any new work
