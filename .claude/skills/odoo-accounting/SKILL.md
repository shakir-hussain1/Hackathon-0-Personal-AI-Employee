---
name: odoo-accounting
description: |
  Interact with Odoo Community accounting via the odoo-connector MCP server.
  Create invoices, view transactions, get accounting summaries, manage contacts.
  Odoo runs locally via Docker (http://localhost:8069). All write actions require
  human approval (HITL) before execution.
---

# Odoo Accounting Skill

**Purpose**: Manage business accounting via Odoo Community (self-hosted, local)
**Tier**: Gold
**MCP Server**: `odoo-connector`
**Requires**: Docker running + Odoo started via `docker-compose.odoo.yml`

---

## When to Use

- Client asks for an invoice
- Need to check payment status or overdue invoices
- Weekly/monthly accounting summary needed
- CEO Briefing generation (automated)
- Logging a business transaction

---

## Quick Start

### Check if Odoo is running
```bash
docker ps | grep odoo
# or: curl http://localhost:8069/web/health
```

### Start Odoo (if not running)
```bash
docker-compose -f Gold-Tier/docker/docker-compose.odoo.yml up -d
# Wait ~60 seconds for startup
```

---

## Available MCP Tools

### 1. `odoo_get_invoices`
Get recent customer invoices.

```
Tool: odoo_get_invoices
Arguments:
  state: posted    (draft/posted/cancel/all)
  limit: 20
```

### 2. `odoo_create_invoice` (requires approval)
Create a draft invoice — queued to `Pending_Approval/` for human review.

```
Tool: odoo_create_invoice
Arguments:
  partner_name: "ABC Corp"
  amount: 50000
  description: "Web Development Services — February 2026"
  currency: "PKR"
  due_date_days: 30
```

### 3. `odoo_get_accounting_summary`
Revenue, expenses, and net for a period.

```
Tool: odoo_get_accounting_summary
Arguments:
  period_days: 30
```

### 4. `odoo_get_partners`
Search for clients/contacts in Odoo.

```
Tool: odoo_get_partners
Arguments:
  search: "ABC"
  limit: 5
```

### 5. `odoo_create_partner`
Add a new client to Odoo contacts.

```
Tool: odoo_create_partner
Arguments:
  name: "XYZ Trading Co"
  email: "accounts@xyz.com"
  phone: "+92-300-1234567"
  is_company: true
```

### 6. `odoo_log_transaction`
Log any business transaction to vault `Accounting/` (always available, no Odoo needed).

```
Tool: odoo_log_transaction
Arguments:
  description: "Web dev invoice payment from ABC Corp"
  amount: 50000
  type: income       (income/expense/payment)
  client: "ABC Corp"
  reference: "INV-2026-042"
```

---

## Invoice Approval Workflow

```
odoo_create_invoice called
    ↓
Approval file created: Pending_Approval/INVOICE_{timestamp}.md
    ↓
Human reviews invoice details
    ↓
Human moves file → Approved/
    ↓
Gold orchestrator detects (every 5 min) → creates invoice in Odoo
    ↓
Invoice moved → Done/Communications/
```

---

## Accounting Summary for CEO Briefing

The weekly audit automatically calls:
1. `odoo_get_accounting_summary` (period_days=7)
2. Reads `Accounting/transactions_*.json` (always available)
3. Writes summary to `Briefings/YYYY-MM-DD_Monday_Briefing.md`

---

## Odoo Setup (First Time)

1. Start Docker: `docker-compose -f Gold-Tier/docker/docker-compose.odoo.yml up -d`
2. Open http://localhost:8069
3. Create database: `odoo` with master password from .env
4. Install modules: **Accounting** + **Contacts** (skip non-essential)
5. Set `ENABLE_ODOO=true` in `Gold-Tier/.env`
6. Restart Gold orchestrator

**Memory Note:** Odoo + PostgreSQL use ~2GB RAM. On 8GB system, close other apps.

---

**Status**: Production Ready
**Tier**: Gold
**Depends on**: Docker Desktop, Gold-Tier/docker/docker-compose.odoo.yml
**Config**: `Gold-Tier/.env` → ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD
