# 🛡️ Risk Detection Skill

**Purpose**: Detect and flag risky operations before execution
**Type**: Security & Safety Skill
**Action**: Stop → Flag → Require Approval

---

## 🎯 What It Detects

### 1. 💰 Financial Operations
- Payment processing
- Money transfers
- Invoice operations
- Salary/compensation changes
- Budget modifications
- Credit card operations

### 2. ⚖️ Legal Terms
- Contract language
- Liability clauses
- Legal agreements
- Compliance requirements
- Terms of service
- Non-disclosure agreements

### 3. 🗑️ Large Deletions
- Multiple file deletions (>5 files)
- Entire folder deletions
- Database drops
- Bulk record removal
- Permanent data loss operations

### 4. 📧 New Recipients
- Emails to new/unknown contacts
- External email domains
- First-time recipients
- Bulk email operations
- External sharing

### 5. 🔐 Sensitive Data
- API keys, passwords, tokens
- Social security numbers
- Credit card numbers
- Personal identification
- Confidential information
- Private keys

---

## 🚦 Risk Levels

| Level | Color | Action | Examples |
|-------|-------|--------|----------|
| **LOW** | 🟢 | Allow | Reading files, viewing data |
| **MEDIUM** | 🟡 | Log + Allow | Creating files, basic edits |
| **HIGH** | 🟠 | Flag + Confirm | Deletions, external emails |
| **CRITICAL** | 🔴 | Stop + Approval | Financial ops, data wipes |

---

## 🛑 Workflow

```
Operation Requested
    ↓
Risk Detection
    ↓
Risk Level?
    ↓
├─ LOW/MEDIUM → Allow (log it)
└─ HIGH/CRITICAL → STOP
         ↓
    Flag for Approval
         ↓
    Human Reviews
         ↓
    Approved? → Execute
    Denied? → Cancel
```

---

## 🔧 Core Functions

### `detect_risk(content, operation)`
Analyze content and operation for risks.

**Returns**: Dict with `risk_level`, `risk_types`, `details`

### `classify_risk_level(risk_types)`
Determine overall risk level from detected risks.

**Returns**: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"

### `should_require_approval(risk_level)`
Check if approval is needed.

**Returns**: Boolean

### `flag_for_approval(operation, risk_details)`
Create approval request.

**Returns**: Approval task file path

---

## 📝 Usage

```python
from risk_detection import detect_risk, should_require_approval, flag_for_approval

# Check operation
content = "Transfer $5000 to john@example.com"
operation = "send_email"

risk = detect_risk(content, operation)

if should_require_approval(risk['risk_level']):
    # STOP and flag
    approval_path = flag_for_approval(operation, risk)
    print(f"🛑 Operation requires approval: {approval_path}")
    exit(1)
else:
    # Safe to proceed
    print("✅ Operation allowed")
    execute_operation()
```

---

## 🔍 Detection Patterns

### Financial Keywords
`payment`, `transfer`, `invoice`, `$`, `amount`, `credit card`, `bank account`, `paypal`, `venmo`, `salary`, `compensation`

### Legal Keywords
`contract`, `agreement`, `liability`, `terms`, `confidential`, `NDA`, `legal`, `lawsuit`, `clause`

### Sensitive Patterns
- API Keys: `api_key=`, `token=`, `bearer `
- SSN: `\d{3}-\d{2}-\d{4}`
- Credit Cards: `\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}`
- Passwords: `password=`, `pwd=`

### Deletion Indicators
`delete`, `remove`, `drop`, `rm -rf`, `truncate`, `purge`, `wipe`

---

## 🎯 Integration Points

### With AI Employee Vault
```python
# Before processing task
task_content = read_task_file("task.md")
risk = detect_risk(task_content, "process_task")

if risk['risk_level'] in ['HIGH', 'CRITICAL']:
    flag_for_approval("process_task", risk)
    update_dashboard_with_warning()
```

### With Email Operations
```python
# Before sending email
recipients = extract_recipients(email)
new_recipients = identify_new_recipients(recipients, known_contacts)

if new_recipients:
    risk = {'risk_level': 'HIGH', 'risk_types': ['new_recipients']}
    flag_for_approval("send_email", risk)
```

### With File Operations
```python
# Before deletion
files_to_delete = get_file_list()

if len(files_to_delete) > 5:
    risk = {'risk_level': 'HIGH', 'risk_types': ['bulk_deletion']}
    flag_for_approval("delete_files", risk)
```

---

## 🔐 Safety Rules

1. **Default Deny**: If unsure, require approval
2. **Log Everything**: All risk checks logged
3. **No Bypassing**: No --force or --skip-approval flags
4. **Human Final Say**: AI recommends, human decides
5. **Audit Trail**: Complete record of approvals

---

## ⚡ Quick Examples

### Example 1: Safe Operation
```python
risk = detect_risk("Read meeting notes from yesterday", "read_file")
# Result: {'risk_level': 'LOW', 'risk_types': []}
# Action: Allow
```

### Example 2: Risky Operation
```python
risk = detect_risk("Delete all files in archive/", "delete_files")
# Result: {'risk_level': 'HIGH', 'risk_types': ['bulk_deletion']}
# Action: Require approval
```

### Example 3: Critical Operation
```python
risk = detect_risk("Process payment of $10,000", "financial_operation")
# Result: {'risk_level': 'CRITICAL', 'risk_types': ['financial']}
# Action: Stop and require approval
```

---

## 📊 Approval File Format

```markdown
# 🛑 Approval Required

**Operation**: send_email
**Risk Level**: 🔴 CRITICAL
**Detected**: 2026-02-16 10:30:00

## Risk Details
- Financial operation detected
- Amount: $5000
- New recipient: unknown@domain.com

## Operation Details
To: john@example.com
Subject: Payment Transfer
Body: [content preview]

## Actions
- [ ] ✅ APPROVE - I authorize this operation
- [ ] ❌ DENY - Cancel this operation

**Decision**: [PENDING]
**Approved By**: [name]
**Approved At**: [timestamp]
```

---

**Status**: Ready to Implement
**Priority**: HIGH (Security Critical)
