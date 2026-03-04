# 🔄 Error Recovery Skill

**Purpose**: Handle failures gracefully and recover automatically
**Type**: Resilience & Reliability Skill
**Principle**: Fail-safe, not fail-fast

---

## 🎯 What We Handle

### 1. 🌐 Network Failures
- Connection timeout
- DNS resolution failure
- Network unreachable
- Connection refused
- SSL/TLS errors

### 2. ⏱️ API Timeouts
- Request timeout
- Response timeout
- Rate limit exceeded
- Gateway timeout (504)
- Service unavailable (503)

### 3. 📁 File Corruption
- Malformed JSON/YAML
- Incomplete file writes
- Permission errors
- File not found
- Invalid encoding

### 4. 💥 Script Crashes
- Unhandled exceptions
- Out of memory
- Infinite loops
- Deadlocks
- Resource exhaustion

---

## 🛠️ Recovery Strategies

### 1. **Retry with Exponential Backoff**

```
Attempt 1: Immediate
Attempt 2: Wait 1s
Attempt 3: Wait 2s
Attempt 4: Wait 4s
Attempt 5: Wait 8s
Max: Give up after 5 attempts
```

**When to use**: Network errors, API timeouts, transient failures

**Pattern**:
```python
max_retries = 5
base_delay = 1  # seconds

for attempt in range(1, max_retries + 1):
    try:
        result = risky_operation()
        return result  # Success!
    except TransientError as e:
        if attempt == max_retries:
            log_error("All retries exhausted")
            raise

        delay = base_delay * (2 ** (attempt - 1))
        log_warning(f"Attempt {attempt} failed, retrying in {delay}s")
        sleep(delay)
```

---

### 2. **Circuit Breaker Pattern**

```
States:
- CLOSED: Normal operation
- OPEN: Stop trying (too many failures)
- HALF_OPEN: Test if recovered

Flow:
CLOSED → (failures) → OPEN → (timeout) → HALF_OPEN → (success) → CLOSED
                                        → (failure) → OPEN
```

**When to use**: Prevent cascading failures, protect downstream services

**Implementation**:
- Track failure count
- Open circuit after N consecutive failures
- Stay open for X seconds
- Try one request (half-open)
- Close if success, reopen if failure

---

### 3. **Graceful Degradation**

**Levels**:
```
Level 1: Full functionality (all systems working)
Level 2: Core functionality (some features disabled)
Level 3: Read-only mode (no writes)
Level 4: Safe mode (basic operations only)
Level 5: Maintenance mode (display message)
```

**When to use**: Partial system failures, maintain availability

**Example**:
- Gmail down? Fall back to file-based queue
- Database unreachable? Use cached data
- API rate limited? Use stale data + warning

---

### 4. **Checkpoint & Resume**

**Pattern**:
```
1. Before operation: Save checkpoint
2. Execute operation
3. If crash: Resume from checkpoint
4. On success: Delete checkpoint
```

**When to use**: Long-running operations, batch processing

**Checkpoint data**:
- Current position (file #, row #)
- Processed items list
- Pending items queue
- Operation state
- Timestamp

---

### 5. **Timeout Protection**

**Strategy**:
```
operation_timeout = 30s
connection_timeout = 10s
read_timeout = 20s

with timeout(operation_timeout):
    result = long_running_operation()
```

**When to use**: Prevent hanging, bound execution time

**Levels**:
- Connection timeout (establishing connection)
- Read timeout (waiting for response)
- Operation timeout (total time limit)

---

## 📝 Logging Strategy

### Log Levels

**ERROR** (🔴): Operation failed, needs attention
```
[ERROR] Failed to send email after 5 retries
- Recipient: user@example.com
- Error: Connection timeout
- Action: Email queued for manual review
```

**WARNING** (🟡): Recoverable issue, temporary failure
```
[WARNING] API rate limit hit, backing off
- Retry in: 60s
- Attempt: 3/5
- Action: Automatic retry scheduled
```

**INFO** (🟢): Normal operation, successful recovery
```
[INFO] Operation succeeded after retry
- Attempts: 2
- Total time: 3.5s
- Action: Continued processing
```

**DEBUG** (⚪): Detailed diagnostics
```
[DEBUG] Retry attempt details
- Backoff delay: 2s
- Error type: ConnectionError
- Stack trace: [...]
```

---

## 🚨 Alerting Rules

### When to Alert Human

**IMMEDIATE** (🔴 Critical):
- All retries exhausted
- Data corruption detected
- Security breach suspected
- System crash (multiple times)
- Financial operation failed

**DELAYED** (🟡 Warning):
- Circuit breaker opened
- High error rate (>10% failures)
- Resource approaching limits
- Repeated warnings

**NO ALERT** (🟢 Normal):
- Single retry succeeded
- Transient network blip
- Expected errors (rate limits)
- Automatic recovery worked

---

## 🔐 Fail-Safe Design Principles

### 1. **Default to Safe State**
```
If unsure → Don't execute
If error → Preserve data
If conflict → Ask human
```

### 2. **Idempotent Operations**
```
Execute once = Execute N times
- Use unique IDs
- Check before create
- Safe to retry
```

**Example**:
```
❌ BAD: counter += 1  (not idempotent)
✅ GOOD: counter = 5  (idempotent)

❌ BAD: send_email()  (might send twice)
✅ GOOD: send_email_once(msg_id)  (checks if already sent)
```

### 3. **Atomic Operations**
```
All-or-nothing
- Start transaction
- Execute steps
- Commit if all succeed
- Rollback if any fail
```

### 4. **Defensive Validation**
```
Before operation:
- Validate inputs
- Check preconditions
- Verify resources

After operation:
- Validate results
- Check postconditions
- Verify consistency
```

### 5. **Fail Early, Fail Clearly**
```
✅ Validate early
✅ Clear error messages
✅ Specific exceptions
✅ Actionable feedback

❌ Silent failures
❌ Generic errors
❌ Unclear state
```

---

## 🏗️ Error Handling Architecture

### Layer 1: Operation Level
```
try:
    result = risky_operation()
except SpecificError as e:
    log_error(e)
    retry_with_backoff()
```

### Layer 2: Module Level
```
try:
    process_batch()
except BatchError as e:
    save_checkpoint()
    alert_human()
    graceful_shutdown()
```

### Layer 3: System Level
```
try:
    run_application()
except SystemError as e:
    emergency_backup()
    notify_admin()
    safe_mode()
```

---

## 📊 Error Classification

### Transient Errors (Retry)
- Network timeouts
- API rate limits
- Temporary unavailability
- Connection refused
- DNS resolution

**Action**: Retry with backoff

### Permanent Errors (Don't Retry)
- 404 Not Found
- 401 Unauthorized
- Invalid input
- File not found
- Malformed data

**Action**: Log and alert, don't retry

### Ambiguous Errors (Investigate)
- 500 Internal Server Error
- Generic exceptions
- Timeout (could be either)
- Unknown errors

**Action**: Limited retries, then alert

---

## 🔍 Specific Error Handlers

### Network Failure Handler
```
Pattern: Retry with exponential backoff
Max retries: 5
Base delay: 1s
Max delay: 32s
Fallback: Offline mode / Queue for later
```

### API Timeout Handler
```
Pattern: Retry with jitter (random delay)
Max retries: 3
Timeout increase: 2x each retry
Fallback: Use cached data + warning
```

### File Corruption Handler
```
Pattern: Try alternate format / backup
Steps:
1. Try parsing file
2. If corrupted, try .backup file
3. If backup corrupted, try recovery
4. If all fail, alert + manual review
```

### Script Crash Handler
```
Pattern: Automatic restart with limit
Max restarts: 3 within 10 minutes
Cooldown: 2 minutes between restarts
If exceeded: Stay down + alert
```

---

## 🎯 Recovery Patterns by Scenario

### Scenario 1: Email Sending Failed
```
Error: SMTP timeout
Recovery:
1. Retry immediately (maybe server blip)
2. Wait 30s, retry
3. Wait 2min, retry
4. Queue email for later
5. Alert: "Email queued, will retry in 1h"
```

### Scenario 2: Database Connection Lost
```
Error: Connection refused
Recovery:
1. Try reconnect (3 attempts, 5s apart)
2. Switch to read-only mode (cached data)
3. Queue write operations
4. Alert: "Database unavailable, read-only mode"
5. Retry connection every 5 min
```

### Scenario 3: File Write Failed
```
Error: Disk full
Recovery:
1. Check disk space
2. Clean temporary files
3. Rotate old logs
4. Retry write
5. If still fails: Alert "Critical: Disk full"
```

### Scenario 4: API Rate Limited
```
Error: 429 Too Many Requests
Recovery:
1. Read Retry-After header
2. Wait specified time
3. Reduce request rate (throttle)
4. Continue with slower processing
5. Log: "Rate limited, throttling"
```

---

## 📋 Implementation Checklist

### For Every Risky Operation:

- [ ] Wrapped in try-except
- [ ] Specific exception handling
- [ ] Retry logic (if appropriate)
- [ ] Timeout protection
- [ ] Logging (error details)
- [ ] Graceful degradation path
- [ ] Alert rules defined
- [ ] Recovery tested

### For Every Module:

- [ ] Error handling strategy documented
- [ ] Recovery procedures defined
- [ ] Checkpointing implemented (if needed)
- [ ] Fallback mode available
- [ ] Alert thresholds configured
- [ ] Test error scenarios

### For Entire System:

- [ ] Global exception handler
- [ ] Crash recovery mechanism
- [ ] Health check endpoint
- [ ] Monitoring/alerting setup
- [ ] Runbook for common errors
- [ ] Recovery playbook

---

## 🧪 Testing Error Recovery

### Test Scenarios

1. **Network Failure Simulation**
   - Disconnect network mid-operation
   - Verify retry behavior
   - Check recovery time

2. **API Timeout Simulation**
   - Delay responses artificially
   - Verify timeout triggers
   - Check backoff strategy

3. **File Corruption Simulation**
   - Create malformed files
   - Verify detection
   - Check recovery/fallback

4. **Crash Recovery Simulation**
   - Kill process mid-operation
   - Restart
   - Verify checkpoint resume

### Test Criteria

✅ **Success**: System recovers automatically
✅ **Success**: No data loss
✅ **Success**: Appropriate alerts sent
✅ **Success**: Logs contain diagnostic info
✅ **Success**: Recovery time < 5 minutes

---

## 📚 Best Practices

### DO ✅

- **Log before retry**: Capture error details
- **Use exponential backoff**: Prevent thundering herd
- **Add jitter**: Randomize retry timing
- **Set max retries**: Don't retry forever
- **Validate after recovery**: Ensure correct state
- **Monitor recovery rate**: Track success/failure
- **Document error codes**: Clear meanings
- **Test failure modes**: Chaos engineering

### DON'T ❌

- **Retry without delay**: Overwhelms failing service
- **Retry forever**: Resource exhaustion
- **Ignore transient errors**: May indicate bigger issue
- **Silent failures**: Lost operations
- **Generic error handling**: Masks specific issues
- **Retry permanent errors**: Waste resources
- **Skip logging**: Lost debugging info
- **Panic on first error**: Could be transient

---

## 🔧 Integration with AI Employee

### Bronze Tier Integration

```
File Watcher Error:
- If file access fails → Retry 3x
- If still fails → Skip file, log error
- Continue monitoring other files

Processing Error:
- If task processing fails → Mark as error
- Move to Done/Errors/
- Create error report
- Continue with next task

Dashboard Update Error:
- If update fails → Use stale data
- Retry next cycle
- Log warning
```

### Silver Tier Integration

```
Gmail API Error:
- Rate limit → Respect Retry-After header
- Network error → Retry with backoff
- Auth error → Refresh token, retry once
- Other errors → Alert human

Email Send Error:
- SMTP timeout → Queue for retry
- Invalid recipient → Mark as bounce
- Size limit → Compress/split email
```

### Gold Tier Integration

```
Social Media API Error:
- Rate limit → Throttle requests
- Network error → Queue posts
- Auth error → Require re-authorization
- Post scheduled for later

Accounting Integration Error:
- Connection lost → Switch to local DB
- Sync failed → Queue transactions
- Conflict → Alert for manual resolution
```

---

## 🎓 Learning from Failures

### Post-Error Analysis

After each error:
1. **What happened?** (root cause)
2. **Why did it happen?** (contributing factors)
3. **How did we recover?** (what worked)
4. **What can we improve?** (prevention)
5. **Update runbook** (for next time)

### Failure Database

Track:
- Error type
- Frequency
- Recovery success rate
- Average recovery time
- Cost (time/resources)
- Prevention opportunities

### Continuous Improvement

- Review error logs weekly
- Identify patterns
- Improve error handling
- Update documentation
- Test new scenarios

---

## 📖 Example Runbook Entry

```markdown
## Error: SMTP Connection Timeout

**Symptoms**: Email sending fails with timeout
**Frequency**: Occasional (< 1% of emails)
**Impact**: Medium (email delayed but not lost)

**Root Causes**:
- SMTP server overloaded
- Network congestion
- Temporary firewall block

**Recovery Steps**:
1. Automatic retry (3 attempts, exponential backoff)
2. If all fail: Queue email in outbox/
3. Log error with recipient + timestamp
4. Alert if queue size > 10

**Prevention**:
- Monitor SMTP server health
- Use connection pooling
- Implement local email queue

**Last Updated**: 2026-02-16
**Success Rate**: 95% (auto-recovery)
```

---

## 🚀 Quick Reference

### Error → Recovery Map

| Error Type | Strategy | Max Retries | Backoff | Fallback |
|------------|----------|-------------|---------|----------|
| Network timeout | Exponential | 5 | 1s → 32s | Queue |
| API rate limit | Linear | 3 | From header | Throttle |
| File corrupt | Alternative | 2 | None | Backup file |
| Auth failed | Refresh | 1 | 5s | Re-auth |
| Disk full | Cleanup | 1 | None | Alert |
| Memory error | Restart | 3 | 60s | Safe mode |

---

## 🎯 Success Metrics

**Good Error Recovery**:
- 95%+ automatic recovery rate
- < 1% data loss
- < 5 min recovery time
- Clear audit trail
- Minimal human intervention

**Monitoring**:
- Error rate trend
- Recovery success rate
- Mean time to recovery (MTTR)
- Error types distribution
- Alert response time

---

**Status**: Ready to Implement
**Priority**: HIGH (Foundation for reliability)
**Integration**: All tiers benefit

*Error recovery is not optional - it's essential for production systems.*
