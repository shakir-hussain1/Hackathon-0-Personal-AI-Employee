---
name: weekly-audit
description: |
  Run the comprehensive weekly business and accounting audit.
  Analyzes Done/ tasks, Accounting/ transactions, Social_Media/ engagement,
  and system health logs to generate the Monday Morning CEO Briefing.
  Use on Sunday evenings or when asked for a weekly business summary.
---

# Weekly Audit Skill

**Purpose**: Comprehensive weekly audit of business performance + CEO Briefing generation
**Tier**: Gold
**Output**: `Briefings/YYYY-MM-DD_Monday_Briefing.md`
**Automated**: Every Sunday 20:00 via Gold orchestrator
**Dependencies**: Business_Goals.md, Accounting/ logs, Done/ tasks

---

## When to Use

- Sunday evening preparation for Monday
- User asks "how did we do this week?"
- Pre-meeting business summary needed
- End-of-month review
- Investor/partner reporting

---

## Full Audit Workflow

### Step 1 — Check data availability
```
1. Read Business_Goals.md → get revenue target
2. List Done/ (last 7 days) → count completed tasks
3. Read Accounting/transactions_*.json → sum income/expenses
4. Read Social_Media/*.md → engagement metrics
5. Read Logs/*.json (last 7 days) → error rate and action counts
6. Check Pending_Approval/ → items awaiting review
```

### Step 2 — Analyze performance

For each section, compare actual vs target:

**Revenue:**
- Calculate weekly income from Accounting/
- Compare to weekly_target = monthly_target / 4
- Flag if below 80% of weekly target

**Tasks:**
- Count tasks completed (moved to Done/ this week)
- Identify any HIGH priority tasks still in Needs_Action (overdue?)
- Note any tasks with ERROR status

**Social Media:**
- Aggregate likes, comments, shares across platforms
- Compare to previous week if data available
- Flag posts with 0 engagement

**System Health:**
- Error rate from JSON audit logs
- Any failed actions or circuit breaker trips
- Watchdog restart events

**Subscriptions:**
- Scan Accounting/ for recurring expense patterns
- Flag subscriptions matching SUBSCRIPTION_PATTERNS keywords
- Note any cost increases

### Step 3 — Generate CEO Briefing

Write to `Briefings/{date}_Monday_Briefing.md`:

```markdown
# Monday Morning CEO Briefing
Generated: {timestamp}
Period: {week}

## Executive Summary
{Overall health — 2 sentences}

## Revenue & Financials
| Income | {amount} |
| Expenses | {amount} |
| Net | {amount} |
| MTD | {%} of target |

## Completed Tasks ({n})
- [x] {task}

## Social Media
{platform summaries}

## System Health
{error rate, top actions}

## Subscription Audit
{flagged subscriptions}

## Pending Approvals ({n} items)
{list}
```

### Step 4 — Notify via Dashboard

```
Append to Dashboard.md:
> CEO Briefing ready: Briefings/{date}_Monday_Briefing.md
```

### Step 5 — Log audit

```python
audit_log(
    'weekly_audit_complete',
    parameters={'income': n, 'tasks': n, 'errors': n}
)
```

---

## Run Manually

```bash
cd Gold-Tier
venv\Scripts\activate
python orchestrator\weekly_audit.py
```

Or from Claude:
```
Run the weekly audit and generate this week's CEO Briefing.
```

---

## Configure Audit Schedule

In `Gold-Tier/.env`:
```env
WEEKLY_AUDIT_DAY=sunday       # Day of week
WEEKLY_AUDIT_TIME=20:00       # Time (24h)
ENABLE_WEEKLY_AUDIT=true      # Enable/disable
```

---

## Accounting Data Format

Transactions logged via `odoo_log_transaction` MCP tool:
```json
{"date": "2026-02-20", "amount": 50000, "type": "income", "client": "ABC Corp", "description": "Invoice payment"}
{"date": "2026-02-20", "amount": 2500, "type": "expense", "description": "Anthropic API"}
```

To log a transaction manually:
```
Tool: odoo_log_transaction
MCP: odoo-connector
Arguments:
  description: "Client payment received"
  amount: 50000
  type: income
  client: "ABC Corp"
  reference: "INV-2026-042"
```

---

**Status**: Production Ready
**Tier**: Gold
**Script**: `Gold-Tier/orchestrator/weekly_audit.py`
**Output**: `Briefings/YYYY-MM-DD_Monday_Briefing.md`
**Related**: `ceo-briefing` skill (manual generation), `odoo-accounting` skill
