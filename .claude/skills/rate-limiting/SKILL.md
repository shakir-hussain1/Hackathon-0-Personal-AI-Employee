# Rate Limiting Skill

## Purpose
Control how fast the AI Employee performs actions — file writes, API calls, notifications, agent spawns, pipeline starts. Prevent overload, respect external service limits, protect system resources, and ensure no single burst of activity floods downstream systems or exhausts quotas.

---

## Core Functions

1. **Limit Enforcement** — Block or delay actions that exceed defined rates
2. **Quota Tracking** — Count actions against rolling time windows
3. **Throttling** — Slow down approaching-limit actions before hard blocking
4. **Backoff** — Wait intelligently when limits are hit
5. **Per-Resource Limits** — Different rules for files, APIs, notifications, agents
6. **Burst Allowance** — Let short bursts through within safe boundaries
7. **Limit Monitoring** — Track usage, warn on approach, alert on breach

---

## Rate Limit Strategies

### Strategy 1: Fixed Window
Count actions within a fixed time window (e.g., per minute, per hour, per day).

```
Window: 1 hour
Limit: 60 actions
Counter resets: At the start of each new hour

Behavior:
  - 60 actions in first 5 minutes → BLOCKED for rest of hour
  - 60 actions spread across hour → OK
Problem: Burst at window boundary (59 at end of hour 1 + 59 at start of hour 2 = 118 in 2 min)
Use for: Daily quotas, simple per-hour limits
```

### Strategy 2: Sliding Window
Count actions within a rolling window relative to NOW.

```
Window: Last 60 minutes (rolling)
Limit: 60 actions

Behavior:
  - Always counts last 60 minutes of activity
  - Smooth — no boundary burst problem
  - More accurate than fixed window
Use for: API calls, notification sending
```

### Strategy 3: Token Bucket
Start with a bucket of tokens. Each action costs 1 token. Tokens refill at a steady rate.

```
Bucket Size: 10 tokens (max burst)
Refill Rate: 1 token per 30 seconds

Behavior:
  - Burst of 10 actions allowed immediately (uses all tokens)
  - Then 1 action every 30 seconds as tokens refill
  - Idle time accumulates tokens (up to bucket max)
Use for: File writes, agent spawning, pipeline starts
```

### Strategy 4: Leaky Bucket
Actions enter a bucket and leak out at a fixed rate — smooths bursts into steady stream.

```
Leak Rate: 1 action per 10 seconds
Bucket Size: 20 (overflow = rejected)

Behavior:
  - No matter how fast actions arrive, output is steady
  - Excess actions wait in bucket (up to bucket size)
  - If bucket overflows → action rejected or queued
Use for: Dashboard writes, log writes, audit entries
```

---

## Rate Limit Registry

**Location:** `AI_Employee_Vault/.rate_limits/registry.md`

```
# Rate Limit Registry
Last Updated: 2026-02-16 14:30:00

| Limit ID | Resource              | Strategy       | Limit    | Window    | Burst | Status  |
|----------|-----------------------|----------------|----------|-----------|-------|---------|
| RL-001   | file_writes           | Token Bucket   | —        | —         | 10    | OK      |
| RL-002   | notifications_total   | Sliding Window | 20/hour  | 60 min    | 5     | OK      |
| RL-003   | notifications_human   | Sliding Window | 5/hour   | 60 min    | 2     | OK      |
| RL-004   | agent_spawns          | Token Bucket   | —        | —         | 3     | OK      |
| RL-005   | pipeline_starts       | Fixed Window   | 10/hour  | 60 min    | —     | OK      |
| RL-006   | dashboard_writes      | Leaky Bucket   | 1/30s    | —         | 5     | OK      |
| RL-007   | log_writes            | Leaky Bucket   | 1/5s     | —         | 20    | OK      |
| RL-008   | gmail_api             | Fixed Window   | 250/day  | 24 hours  | —     | SILVER+ |
| RL-009   | gmail_send            | Fixed Window   | 100/day  | 24 hours  | —     | SILVER+ |
| RL-010   | linkedin_post         | Fixed Window   | 10/day   | 24 hours  | —     | GOLD+   |
| RL-011   | kb_writes             | Token Bucket   | —        | —         | 15    | OK      |
| RL-012   | snapshot_creates      | Fixed Window   | 48/day   | 24 hours  | —     | OK      |
| RL-013   | event_publishes       | Token Bucket   | —        | —         | 50    | OK      |
| RL-014   | state_writes          | Token Bucket   | —        | —         | 10    | OK      |
```

---

## Per-Resource Limits (Detail)

### File System Operations
```
Resource: file_writes (RL-001)
Strategy: Token Bucket
Bucket Size: 10 tokens
Refill Rate: 1 token per 5 seconds
Purpose: Prevent disk I/O storms

Resource: dashboard_writes (RL-006)
Strategy: Leaky Bucket
Leak Rate: 1 write per 30 seconds
Bucket Size: 5
Purpose: Dashboard updates are expensive — batch them
```

### Agent & Pipeline Operations
```
Resource: agent_spawns (RL-004)
Strategy: Token Bucket
Bucket Size: 3 tokens
Refill Rate: 1 token per 2 minutes
Purpose: Prevent runaway agent spawning

Resource: pipeline_starts (RL-005)
Strategy: Fixed Window
Limit: 10 per hour
Purpose: Prevent pipeline cascade from file surge
```

### Notification Operations
```
Resource: notifications_total (RL-002)
Strategy: Sliding Window
Limit: 20 per hour
Burst: 5 at once
Purpose: Don't flood human with alerts

Resource: notifications_human (RL-003)
Strategy: Sliding Window
Limit: 5 per hour
Burst: 2 at once
Purpose: Human attention is the scarcest resource — protect it
```

### External API Operations (Silver+ / Gold+)
```
Resource: gmail_api (RL-008)
Strategy: Fixed Window
Limit: 250 read operations per day
Reset: Midnight UTC
Source: Gmail API quota

Resource: gmail_send (RL-009)
Strategy: Fixed Window
Limit: 100 emails per day
Reset: Midnight UTC
Source: Gmail sending quota

Resource: linkedin_post (RL-010)
Strategy: Fixed Window
Limit: 10 posts per day
Reset: Midnight UTC
Source: LinkedIn API terms
```

---

## Rate Limit State Files

**Location:** `AI_Employee_Vault/.rate_limits/state/`
**One file per rate limit resource**

```
# Rate Limit State: notifications_human (RL-003)
Strategy: Sliding Window
Limit: 5 per hour
Last Updated: 2026-02-16 14:30:00

## Usage Log (last 60 minutes)
2026-02-16 13:45:00 | action: HUMAN_ALERT | agent: monitoring-skill
2026-02-16 14:10:00 | action: HUMAN_ALERT | agent: self-healing-skill
2026-02-16 14:25:00 | action: HUMAN_ALERT | agent: notification-skill

## Current State
Actions in window: 3
Remaining: 2
Next slot opens at: 2026-02-16 14:45:00 (oldest entry expires)
Status: OK
```

```
# Rate Limit State: agent_spawns (RL-004)
Strategy: Token Bucket
Bucket Size: 3
Refill Rate: 1 per 2 minutes
Last Updated: 2026-02-16 14:30:00

## Current State
Tokens Available: 1
Last Refill: 2026-02-16 14:28:00
Next Refill: 2026-02-16 14:30:00
Status: LOW (1 token remaining)
```

---

## Check-Before-Act Protocol

Every skill MUST check the rate limit before performing a limited action:

```
Step 1: IDENTIFY the action type
        What am I about to do? → notifications_human

Step 2: LOAD rate limit state
        Read .rate_limits/state/notifications_human.md

Step 3: EVALUATE availability
        → Token Bucket: tokens_available >= cost (usually 1)?
        → Sliding Window: actions_in_window < limit?
        → Fixed Window: actions_in_window < limit?
        → Leaky Bucket: bucket_level < bucket_size?

Step 4a: AVAILABLE → proceed
         Deduct token / increment counter
         Write updated state
         Perform action

Step 4b: NOT AVAILABLE → apply response policy
         (see Response Policies below)

Step 5: LOG the check result
        Action | Allowed/Denied | Current Usage | Remaining
```

---

## Response Policies

When a rate limit is hit, the skill chooses one of these responses:

### Policy 1: WAIT (Throttle)
Pause and retry after the next slot opens.
```
Use when: Action is time-sensitive but not urgent
Wait time: Until next token refills OR oldest window entry expires
Max wait: 2 minutes
After max wait: Escalate to QUEUE
```

### Policy 2: QUEUE
Place the action in the Queue Management system to be processed when limit resets.
```
Use when: Action can be delayed safely
Add to: Appropriate queue with priority preserved
Note in queue item: "Rate limited — waiting for RL-003 reset"
```

### Policy 3: DROP
Discard the action entirely.
```
Use when: Action is LOW priority and already redundant
Example: Dropping a 5th duplicate dashboard refresh in 30 seconds
Log: "Action dropped due to rate limit: {action} | Limit: {limit_id}"
```

### Policy 4: ESCALATE
Notify human that rate limit is preventing required action.
```
Use when: CRITICAL action cannot be delayed or dropped
Example: CRITICAL alert blocked by notification rate limit
Action: Write directly to Dashboard.md (bypasses notification limit)
        AND queue the notification for when limit resets
```

### Policy Map by Priority

| Action Priority | Response Policy |
|----------------|----------------|
| CRITICAL | ESCALATE (never drop, never wait >30s) |
| HIGH | WAIT then QUEUE |
| MEDIUM | QUEUE |
| LOW | DROP if duplicate, QUEUE otherwise |

---

## Throttling Zone

Before hitting the hard limit, enter the throttling zone at 80%:

```
Example: notifications_human limit = 5/hour
Throttling zone: ≥ 4 actions in window (80%)

In throttling zone:
  → Add minimum 15-minute gap between human notifications
  → Batch related alerts into single notification if possible
  → Log: "Approaching rate limit RL-003: 4/5 used — throttling active"
  → Publish event: RATE_LIMIT_APPROACHING

At hard limit (5/5):
  → Apply response policy
  → Log: "Rate limit RL-003 reached: 5/5 — policy: WAIT"
  → Publish event: RATE_LIMIT_REACHED
```

---

## Backoff Strategy

When waiting for a rate limit to reset, use exponential backoff:

```
Attempt 1: Wait 10 seconds
Attempt 2: Wait 20 seconds
Attempt 3: Wait 40 seconds
Attempt 4: Wait 80 seconds (cap at 2 minutes)
Attempt 5+: Wait 120 seconds (2 minutes, stays here)

After 5 attempts total → escalate to QUEUE or ESCALATE policy
```

### Jitter (prevent thundering herd)
Add random jitter to backoff times so multiple agents don't retry at the exact same moment:
```
Actual wait = base_wait + random(0, base_wait × 0.2)
Example: 40 seconds + random(0, 8) = 40-48 seconds
```

---

## Burst Handling

Some limits allow a burst allowance — a small number of extra actions above the rate:

```
Example: notifications_total
Limit: 20/hour
Burst: 5

Normal: 20 notifications per hour
Burst: Up to 25 notifications allowed if:
  - At least 10 minutes have passed since last burst use
  - System is in BURST or EMERGENCY mode
  - Burst tokens are available (separate bucket, refills hourly)

Burst Usage Log:
  2026-02-16 09:00:00 | Burst used: 3 extra notifications | Reason: Inbox surge
  2026-02-16 09:00:00 | Burst tokens remaining: 2
```

---

## Daily Quota Tracking

For external APIs with daily limits:

**Location:** `AI_Employee_Vault/.rate_limits/daily_quotas.md`

```
# Daily Quota Tracker — 2026-02-16

| Resource       | Limit/Day | Used | Remaining | Reset At     | Status  |
|----------------|-----------|------|-----------|--------------|---------|
| gmail_api      | 250       | 47   | 203       | 00:00 UTC    | OK      |
| gmail_send     | 100       | 12   | 88        | 00:00 UTC    | OK      |
| linkedin_post  | 10        | 3    | 7         | 00:00 UTC    | OK      |

## Warnings
- gmail_api: >200 used → WARN (approaching daily limit)
- gmail_send: >80 used → WARN
- linkedin_post: >8 used → WARN
```

---

## Rate Limit Monitoring

### Metrics Tracked Per Limit
```
- Current usage (count in window OR tokens available)
- Peak usage (highest point in last 24 hours)
- Times limit was reached (today)
- Times action was dropped (today)
- Times action was queued (today)
- Times WAIT policy was applied (today)
- Avg time spent waiting (when WAIT policy applied)
```

### Monitoring Alerts
```
RATE_LIMIT_APPROACHING:  Usage >= 80% of limit
RATE_LIMIT_REACHED:      Usage = 100% of limit
RATE_LIMIT_CRITICAL:     CRITICAL action was blocked by rate limit
QUOTA_WARNING:           Daily quota >= 80% consumed
QUOTA_EXHAUSTED:         Daily quota fully consumed
```

---

## Rate Limits by System Mode

| Mode | Effect on Rate Limits |
|------|----------------------|
| NORMAL | Standard limits apply |
| IDLE | Limits relaxed — lower urgency, refill rates slower |
| BURST | Burst allowances activated, some limits raised temporarily |
| EMERGENCY | CRITICAL actions bypass rate limits; all others queued |

### Emergency Bypass
In EMERGENCY mode only:
```
CRITICAL priority actions: bypass rate limit check
All other priorities: queue without attempting, process when emergency clears
Log all bypasses: "Rate limit bypassed: {limit_id} | Mode: EMERGENCY | Action: {action}"
```

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|-----------------|
| Notification | Checks RL-002 (total) and RL-003 (human) before every alert |
| Agent Spawning | Checks RL-004 before spawning any agent |
| Pipeline | Checks RL-005 before starting any pipeline run |
| Integration | Checks API-specific limits (RL-008 to RL-014) before every API call |
| Queue Management | Receives queued actions when rate limit policy = QUEUE |
| Monitoring | Publishes RATE_LIMIT_* events for tracking |
| Event Bus | Checks RL-013 before publishing bursts of events |
| Optimization | Reads rate limit usage to adjust system mode |
| Config Management | Rate limit values read from config (adjustable per tier) |

---

## Quick Reference

```
CHECK LIMIT:       Load state → evaluate → proceed or apply policy
STRATEGIES:        Token Bucket / Sliding Window / Fixed Window / Leaky Bucket
THROTTLE ZONE:     80% usage → add gaps, batch, warn
HARD LIMIT:        100% → WAIT / QUEUE / DROP / ESCALATE
BACKOFF:           10s → 20s → 40s → 80s → 120s (+ jitter)
BURST:             Extra allowance for BURST/EMERGENCY mode
EMERGENCY BYPASS:  CRITICAL actions only, all others queued
DAILY QUOTAS:      .rate_limits/daily_quotas.md
LIMIT STATES:      .rate_limits/state/{resource}.md
REGISTRY:          .rate_limits/registry.md

PRIORITY → POLICY:
  CRITICAL → ESCALATE
  HIGH     → WAIT then QUEUE
  MEDIUM   → QUEUE
  LOW      → DROP (if duplicate) or QUEUE
```

---

## Best Practices

1. **Check before act** — never perform a limited action without checking the rate limit first
2. **Protect human attention first** — `notifications_human` is the most precious limit; never drop CRITICAL alerts
3. **Batch when throttling** — combine related actions into one instead of firing them separately
4. **Jitter always** — add random jitter to all backoff waits to prevent synchronized retries
5. **Log every denial** — every dropped or queued action must be logged with reason
6. **Monitor trends** — a rate limit hit once is normal; hit consistently means the limit needs tuning
7. **Emergency = bypass sparingly** — EMERGENCY bypass is for true emergencies only; log every use
8. **Daily quota buffer** — stop at 80% of daily quotas, not 100% — leave headroom for urgent needs
9. **Burst is not free** — burst tokens have their own pool; once spent, they refill slowly
10. **Tune via config** — rate limit values live in Config Management, not hardcoded here
