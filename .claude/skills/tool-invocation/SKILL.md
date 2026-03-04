# 🔧 Tool Invocation Skill

**Purpose**: Safely execute tools and API calls with validation
**Core Function**: Validate → Log → Execute (or DRY_RUN)
**Safety**: Input validation, output verification, complete audit trail

---

## 🎯 Core Capabilities

### 1. Safe Tool Calls
Execute tools with safety checks and error handling

### 2. Input Validation
Verify all parameters before execution

### 3. Output Logging
Record all invocations and results

### 4. DRY_RUN Mode
Test without executing (simulation mode)

---

## 🔄 Invocation Flow

```
1. RECEIVE REQUEST
   ↓
2. VALIDATE INPUTS
   ✓ Required params present?
   ✓ Types correct?
   ✓ Values in range?
   ✓ Safe to execute?
   ↓
3. CHECK MODE
   ├─→ DRY_RUN: Simulate & log
   └─→ EXECUTE: Run & log
   ↓
4. VERIFY OUTPUT
   ✓ Execution successful?
   ✓ Output as expected?
   ✓ No errors?
   ↓
5. LOG RESULT
   - Timestamp
   - Inputs
   - Outputs
   - Status
```

---

## 🛡️ Safety Checks

### Pre-Execution Validation

**1. Parameter Validation**
```markdown
Check each parameter:
- Is required parameter present?
- Is type correct? (string/int/bool/etc)
- Is value in allowed range?
- Is format valid? (email, URL, path)
- Is value safe? (no injection attempts)

Example:
email = "user@example.com"
✓ Present: YES
✓ Type: string
✓ Format: Valid email
✓ Safe: No SQL/code injection
→ VALID
```

**2. Permission Check**
```markdown
Verify authorization:
- Does user have permission?
- Is operation allowed in current context?
- Are credentials valid?
- Is rate limit okay?

Example:
Operation: delete_file
User: AI Employee
Permission: delete_files = TRUE
Rate limit: 5/hour, used: 2
→ AUTHORIZED
```

**3. Dependency Check**
```markdown
Verify prerequisites:
- Are required services available?
- Are dependencies met?
- Is system in valid state?
- Are resources available?

Example:
Tool: send_email
Check: SMTP server reachable? YES
Check: Email queue not full? YES
Check: Recipient valid? YES
→ DEPENDENCIES MET
```

---

## 📋 Input Validation Rules

### String Validation

```markdown
Parameter: email
Rules:
- Required: YES
- Type: string
- Min length: 5
- Max length: 255
- Pattern: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
- No SQL keywords
- No script tags

Examples:
"user@example.com" → ✅ VALID
"admin" → ❌ INVALID (not email format)
"'; DROP TABLE--" → ❌ INVALID (SQL injection attempt)
```

### Number Validation

```markdown
Parameter: amount
Rules:
- Required: YES
- Type: number (float/int)
- Min: 0
- Max: 10000
- Decimals: 2
- Not negative

Examples:
100.50 → ✅ VALID
-50 → ❌ INVALID (negative)
10001 → ❌ INVALID (exceeds max)
```

### Boolean Validation

```markdown
Parameter: confirmed
Rules:
- Required: YES
- Type: boolean
- Values: true/false only

Examples:
true → ✅ VALID
false → ✅ VALID
"yes" → ❌ INVALID (not boolean)
1 → ❌ INVALID (not boolean)
```

### File Path Validation

```markdown
Parameter: file_path
Rules:
- Required: YES
- Type: string (valid path)
- Must exist: YES
- Readable: YES
- No path traversal (../)
- Within allowed directories

Examples:
"data/file.txt" → ✅ VALID
"../../../etc/passwd" → ❌ INVALID (path traversal)
"C:\Windows\System32" → ❌ INVALID (restricted)
```

### URL Validation

```markdown
Parameter: api_url
Rules:
- Required: YES
- Type: string (valid URL)
- Protocol: https only
- Domain: whitelist only
- No localhost/private IPs

Examples:
"https://api.example.com/v1" → ✅ VALID
"http://example.com" → ❌ INVALID (not HTTPS)
"https://localhost:8080" → ❌ INVALID (localhost)
```

---

## 📊 DRY_RUN Mode

### What is DRY_RUN?

**Definition**: Simulation mode - validate and log without executing

**Use cases**:
- Testing new tools/APIs
- Debugging workflows
- Validating inputs
- Previewing results
- Training/demos

### DRY_RUN vs EXECUTE

| Aspect | DRY_RUN | EXECUTE |
|--------|---------|---------|
| Validates inputs | ✅ YES | ✅ YES |
| Checks permissions | ✅ YES | ✅ YES |
| Executes tool | ❌ NO | ✅ YES |
| Makes changes | ❌ NO | ✅ YES |
| Logs invocation | ✅ YES | ✅ YES |
| Returns result | 🔍 Simulated | ✅ Real |

### Enabling DRY_RUN

**Method 1: Global flag**
```markdown
Set at start of session:
DRY_RUN = true

All tool calls will be simulated
```

**Method 2: Per-call flag**
```markdown
invoke_tool(
  name="send_email",
  params={...},
  dry_run=true  ← Override
)
```

**Method 3: Environment variable**
```markdown
TOOL_DRY_RUN=true
```

### DRY_RUN Output

```markdown
DRY_RUN SIMULATION

Tool: send_email
Mode: DRY_RUN (not executed)

Inputs:
  to: user@example.com
  subject: "Hello"
  body: "Test message"

Validation: ✅ PASSED
  ✓ Email format valid
  ✓ Recipient exists
  ✓ SMTP available

Would execute: send_email()
Would send to: user@example.com
Would attach: []

Simulated result: SUCCESS
Actual result: NOT EXECUTED (DRY_RUN)

Logged: 2026-02-16 15:30:00
```

---

## 📝 Logging System

### Log Entry Format

```markdown
[TIMESTAMP] [LEVEL] [TOOL] [STATUS] - Message

Example:
[2026-02-16 15:30:00] [INFO] [send_email] [SUCCESS] - Email sent to user@example.com
```

### Log Levels

**DEBUG** (detailed info):
```markdown
[DEBUG] Validating email parameter: user@example.com
[DEBUG] Email format check: PASSED
[DEBUG] SMTP connection established
[DEBUG] Email queued for sending
```

**INFO** (normal operations):
```markdown
[INFO] Tool invoked: send_email
[INFO] Validation passed
[INFO] Email sent successfully
```

**WARNING** (potential issues):
```markdown
[WARNING] Email send delayed (queue full)
[WARNING] Recipient mailbox near full
[WARNING] Attachment size large (4.5 MB)
```

**ERROR** (failures):
```markdown
[ERROR] Email send failed: SMTP timeout
[ERROR] Invalid recipient: nonexistent@domain.com
[ERROR] Attachment too large (exceeded 5 MB limit)
```

---

### Complete Log Entry

```markdown
===============================================
TOOL INVOCATION LOG
===============================================

Timestamp: 2026-02-16 15:30:00.123
Invocation ID: INV-2026-02-16-001
Mode: EXECUTE (not DRY_RUN)

---

TOOL DETAILS
Name: send_email
Category: Communication
Version: 1.0
Risk Level: HIGH (external communication)

---

INPUT PARAMETERS
{
  "to": "user@example.com",
  "subject": "Project Update",
  "body": "Please find attached...",
  "attachments": ["report.pdf"],
  "cc": [],
  "bcc": []
}

---

VALIDATION RESULTS
✅ PASSED (6/6 checks)

Email format: ✅ VALID
Recipient exists: ✅ VERIFIED
SMTP available: ✅ ONLINE
Attachment size: ✅ 2.1 MB (under 5 MB limit)
Permissions: ✅ AUTHORIZED
Rate limit: ✅ 3/10 today

---

EXECUTION RESULTS
Status: ✅ SUCCESS
Duration: 1.23 seconds
Message ID: <abc123@smtp.example.com>

Response:
{
  "status": "sent",
  "message_id": "abc123",
  "timestamp": "2026-02-16T15:30:01Z"
}

---

OUTPUT VERIFICATION
✅ Email sent successfully
✅ Recipient acknowledged
✅ Message ID received
✅ No errors reported

---

AUDIT TRAIL
Requested by: AI Employee (automated)
Approved by: N/A (auto-approved)
Executed by: SMTP Service
Completed: 2026-02-16 15:30:01

---

RELATED LOGS
Previous invocation: INV-2026-02-15-089
Related task: TASK-2026-02-16-005
Dashboard updated: YES

===============================================
```

---

## 🔧 Tool Registry

### Registered Tools

**Format**:
```markdown
Tool: [name]
Category: [category]
Risk: [LOW/MEDIUM/HIGH/CRITICAL]
Requires approval: [YES/NO]
DRY_RUN supported: [YES/NO]
```

**Example Registry**:
```markdown
### Communication Tools

send_email:
  Category: Communication
  Risk: HIGH (external)
  Approval: YES (external only)
  DRY_RUN: YES
  Params: to, subject, body, attachments

send_slack:
  Category: Communication
  Risk: MEDIUM
  Approval: NO (internal)
  DRY_RUN: YES
  Params: channel, message

### File Tools

read_file:
  Category: File
  Risk: LOW
  Approval: NO
  DRY_RUN: YES (returns sample)
  Params: file_path

delete_file:
  Category: File
  Risk: HIGH
  Approval: YES (>5 files)
  DRY_RUN: YES
  Params: file_path, confirm

### Data Tools

query_database:
  Category: Database
  Risk: MEDIUM
  Approval: NO (read only)
  DRY_RUN: YES (returns mock data)
  Params: query, limit

update_database:
  Category: Database
  Risk: HIGH
  Approval: YES
  DRY_RUN: YES
  Params: table, values, where

### API Tools

call_api:
  Category: API
  Risk: MEDIUM
  Approval: NO (GET only)
  DRY_RUN: YES
  Params: endpoint, method, body

webhook_trigger:
  Category: API
  Risk: HIGH (external)
  Approval: YES
  DRY_RUN: YES
  Params: url, payload
```

---

## 🎯 Safe Invocation Pattern

### Standard Invocation

```markdown
function invoke_tool_safely(tool_name, params, options={}):

  # 1. SETUP
  log_info(f"Invoking tool: {tool_name}")
  invocation_id = generate_id()
  start_time = now()

  # 2. VALIDATE INPUTS
  validation = validate_params(tool_name, params)
  if not validation.passed:
    log_error(f"Validation failed: {validation.errors}")
    return {
      success: false,
      error: "Invalid parameters",
      details: validation.errors
    }

  # 3. CHECK PERMISSIONS
  if not has_permission(tool_name):
    log_error(f"Permission denied: {tool_name}")
    return {
      success: false,
      error: "Unauthorized"
    }

  # 4. CHECK APPROVAL
  if requires_approval(tool_name, params):
    approval = check_approval(tool_name, params)
    if not approval.approved:
      log_warning(f"Approval required: {tool_name}")
      return {
        success: false,
        error: "Approval required",
        approval_id: approval.id
      }

  # 5. EXECUTE OR DRY_RUN
  if options.dry_run or global_dry_run:
    # SIMULATE
    log_info(f"DRY_RUN: {tool_name} (not executed)")
    result = simulate_tool(tool_name, params)
    result.dry_run = true
  else:
    # EXECUTE
    try:
      result = execute_tool(tool_name, params)
      log_info(f"Tool executed: {tool_name}")
    catch error:
      log_error(f"Execution failed: {error}")
      return {
        success: false,
        error: error.message
      }

  # 6. VERIFY OUTPUT
  verification = verify_output(tool_name, result)
  if not verification.passed:
    log_warning(f"Output verification failed: {verification.issues}")

  # 7. LOG COMPLETE
  log_invocation({
    id: invocation_id,
    tool: tool_name,
    params: params,
    result: result,
    duration: now() - start_time,
    dry_run: options.dry_run
  })

  # 8. RETURN RESULT
  return {
    success: true,
    result: result,
    invocation_id: invocation_id,
    dry_run: options.dry_run
  }
```

---

## 🔍 Error Handling

### Error Types

**1. Validation Errors**
```markdown
Error: Invalid parameter
Cause: Email format incorrect
Action: Fix parameter, retry
Severity: MEDIUM
Logged: YES
Retry: After fix
```

**2. Permission Errors**
```markdown
Error: Unauthorized
Cause: Missing permission
Action: Request permission
Severity: HIGH
Logged: YES
Retry: After authorization
```

**3. Execution Errors**
```markdown
Error: Tool execution failed
Cause: SMTP timeout
Action: Retry with backoff
Severity: MEDIUM
Logged: YES
Retry: 3 attempts
```

**4. Output Errors**
```markdown
Error: Invalid response
Cause: Malformed JSON
Action: Log and alert
Severity: HIGH
Logged: YES
Retry: NO (data issue)
```

---

### Error Response Format

```markdown
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "parameter": "to",
      "value": "invalid",
      "expected": "Valid email address",
      "pattern": "user@domain.com"
    },
    "timestamp": "2026-02-16T15:30:00Z",
    "invocation_id": "INV-2026-02-16-001",
    "retry_possible": true,
    "suggested_action": "Fix email format and retry"
  }
}
```

---

## 📊 Monitoring & Metrics

### Metrics to Track

**Invocation metrics**:
- Total invocations
- Success rate
- Failure rate
- Average duration
- DRY_RUN vs EXECUTE ratio

**Tool usage**:
- Most called tools
- Least called tools
- Tools with highest failure rate
- Tools requiring most approvals

**Performance**:
- Fastest tools
- Slowest tools
- Timeout occurrences
- Retry frequency

---

### Daily Report

```markdown
# Tool Invocation Report - 2026-02-16

## Summary
- Total invocations: 156
- Successful: 148 (94.9%)
- Failed: 8 (5.1%)
- DRY_RUN: 23 (14.7%)
- Average duration: 1.23s

## Top Tools
1. read_file: 45 calls (28.8%)
2. send_email: 34 calls (21.8%)
3. query_database: 28 calls (17.9%)

## Failures
- SMTP timeout: 3 occurrences
- Invalid parameter: 2 occurrences
- Permission denied: 2 occurrences
- Rate limit: 1 occurrence

## DRY_RUN Usage
- Testing new workflows: 15
- Validation checks: 5
- Training: 3

## Performance
- Fastest: read_file (0.05s avg)
- Slowest: webhook_trigger (3.2s avg)
- 99th percentile: 2.5s

## Recommendations
- Investigate SMTP timeout issue
- Review rate limits for send_email
- Consider caching for query_database
```

---

## 🎯 Best Practices

### DO ✅

**1. Always validate inputs**
```markdown
✅ Check all parameters
✅ Verify types and ranges
✅ Sanitize user input
✅ Test with edge cases
```

**2. Use DRY_RUN first**
```markdown
✅ Test new tools in DRY_RUN
✅ Validate workflows
✅ Verify outputs
✅ Then switch to EXECUTE
```

**3. Log everything**
```markdown
✅ Log all invocations
✅ Include parameters
✅ Record results
✅ Track errors
```

**4. Handle errors gracefully**
```markdown
✅ Catch all exceptions
✅ Return structured errors
✅ Suggest fixes
✅ Allow retries
```

**5. Verify outputs**
```markdown
✅ Check return values
✅ Validate response format
✅ Confirm side effects
✅ Log discrepancies
```

---

### DON'T ❌

**1. Don't skip validation**
```markdown
❌ Never trust input
❌ Don't assume format
❌ Can't skip type checks
❌ No unvalidated execution
```

**2. Don't ignore errors**
```markdown
❌ Don't suppress exceptions
❌ Don't retry blindly
❌ Don't hide failures
❌ Can't continue on error
```

**3. Don't execute without approval**
```markdown
❌ High-risk tools need approval
❌ Don't bypass checks
❌ Can't force execute
❌ No emergency shortcuts
```

**4. Don't forget logging**
```markdown
❌ Every call must log
❌ Include all details
❌ Don't skip errors
❌ Can't delete logs
```

**5. Don't mix DRY_RUN and EXECUTE**
```markdown
❌ Clear mode indication
❌ Don't confuse results
❌ Can't partially execute
❌ All or nothing
```

---

## 🔐 Security Considerations

### Input Sanitization

```markdown
Always sanitize:
- SQL queries (prevent injection)
- Shell commands (prevent execution)
- File paths (prevent traversal)
- URLs (prevent SSRF)
- User data (prevent XSS)
```

### Rate Limiting

```markdown
Enforce limits:
- Calls per minute: 60
- Calls per hour: 1000
- Calls per day: 10000
- Per tool limits: custom
```

### Audit Trail

```markdown
Maintain complete log:
- Who invoked?
- When invoked?
- What parameters?
- What result?
- Any errors?
```

---

## 📋 Quick Reference

### Invocation Template

```markdown
invoke_tool(
  name: "tool_name",
  params: {
    param1: value1,
    param2: value2
  },
  options: {
    dry_run: false,
    validate: true,
    log: true,
    timeout: 30
  }
)
```

### Validation Template

```markdown
validate_params(tool_name, params):
  for each param in params:
    - Check required
    - Check type
    - Check range
    - Check format
    - Check safety
  return validation_result
```

### Log Template

```markdown
log_invocation(
  id: "INV-YYYY-MM-DD-NNN",
  tool: "tool_name",
  params: {...},
  result: {...},
  duration: 1.23,
  success: true,
  dry_run: false
)
```

---

**Status**: Production Ready
**Core Function**: Safe tool/API execution with validation and logging
**DRY_RUN**: Full simulation support for testing

*Safe tool invocation: Validate → Log → Execute*
