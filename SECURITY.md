# Security & Credential Handling
# Personal AI Employee — Hackathon-0

---

## TL;DR

> **No secrets are stored in this repository. All credentials are machine-local, never committed, never synced.**

---

## Credential Storage Rules

| Credential Type | Where Stored | Committed to Git? | Synced to Cloud? |
|-----------------|-------------|-------------------|------------------|
| Google OAuth credentials | `Silver-Tier/credentials.json` | ❌ Never | ❌ Never |
| Gmail token | `Silver-Tier/.gmail_token.json` | ❌ Never | ❌ Never |
| Calendar token | `Silver-Tier/.calendar_token.json` | ❌ Never | ❌ Never |
| LinkedIn access token | `.env` (local only) | ❌ Never | ❌ Never |
| Twitter/X API keys | `.env` (local only) | ❌ Never | ❌ Never |
| Facebook/Instagram tokens | `.env` (local only) | ❌ Never | ❌ Never |
| Odoo password | `.env` (local only) | ❌ Never | ❌ Never |
| Anthropic API key | `.env` (local only) | ❌ Never | ❌ Never |
| Vault Git SSH key | Machine SSH agent only | ❌ Never | ❌ Never |

---

## What the `.gitignore` Protects

The root `.gitignore` explicitly excludes:

```
.env
.env.local
.env.*.local
credentials.json
*.json          (token files)
*.session       (Playwright sessions)
*.key
*.pem
*.cert
secrets/
credentials/
venv/
__pycache__/
```

The Platinum tier `setup_platinum.py` additionally enforces these rules programmatically — it writes a vault-level `.gitignore` before any `git push` is possible, so credentials can never accidentally enter the vault sync repo.

---

## Human-in-the-Loop (HITL) for All Actions

This project implements a strict approval gate for every external action:

| Action | Approval Gate |
|--------|--------------|
| Send email | Human moves file from `Pending_Approval/` → `Approved/` |
| Post to LinkedIn | Human moves file from `LinkedIn_Queue/` → `LinkedIn_Approved/` |
| Post to Twitter/X | MCP server requires `DRY_RUN=false` + approval file |
| Post to Facebook/Instagram | HITL file move required |
| Create Odoo invoice | HITL review before execution |
| Any cloud-originated action | Local agent executes ONLY after human approval |

**No action is ever executed automatically on external systems.** Claude drafts; humans decide.

---

## DRY_RUN Safety Mode

All tiers default to `DRY_RUN=true`. This means:

- No real emails are sent
- No real social media posts are made
- No real invoices are created
- All "send" actions are logged as simulated only

To enable live actions, the user must:
1. Explicitly set `DRY_RUN=false` in their local `.env`
2. Provide valid API credentials
3. Approve each action individually via the HITL file-move workflow

---

## Platinum Tier: Secrets Never Sync

The Platinum tier uses Git to sync the vault between a cloud VM and the local machine. The security model:

```
Cloud VM                           Local Machine
─────────────────────────────      ──────────────────────────
credentials.json  ← NEVER SYNCED  credentials.json
.env              ← NEVER SYNCED  .env
Gmail tokens      ← NEVER SYNCED  Gmail tokens
SSH keys          ← NEVER SYNCED  SSH keys

What DOES sync:
*.md task files       ✅
Updates/ summaries    ✅
Signals/ coordination ✅
Logs/*.log            ✅
```

Cloud orchestrator has **no send/post/pay code** — it can only read and draft. All execution happens local.

---

## MCP Server Permission Boundaries

Each MCP server enforces its own permission boundary:

| MCP Server | Can Do | Cannot Do |
|------------|--------|-----------|
| `email-sender` | Draft emails, send approved emails | Access contacts outside approved list |
| `linkedin-poster` | Queue posts for approval, publish approved | Post without approval file |
| `odoo-connector` | Read invoices, create draft invoices | Delete records, change passwords |
| `twitter-x` | Post approved tweets, read timeline | Delete tweets, change account settings |
| `facebook-instagram` | Post approved content | Delete posts, modify page settings |

---

## Audit Trail

Every action executed by the system is logged:

- **Format**: JSON Lines (`*.jsonl`)
- **Location**: `Common/AI_Employee_Vault/Logs/YYYY-MM-DD_audit.jsonl`
- **Retention**: 90 days (configurable)
- **Contents**: timestamp, action_type, actor, target, approval_status, approved_by, result

```json
{
  "timestamp": "2026-02-24T10:30:00",
  "action_type": "email_send",
  "actor": "local_orchestrator",
  "target": "client@example.com",
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

This log is human-readable, immutable (append-only), and covers every external action taken by the AI employee.

---

## What This Project Does NOT Do

- Does **not** store credentials in code
- Does **not** commit `.env` files
- Does **not** send emails, post, or pay without human approval
- Does **not** run destructive operations (no `DELETE`, `DROP`, `rm -rf`)
- Does **not** expose credentials to the vault sync repo
- Does **not** bake secrets into Docker images
- Does **not** log credential values (only action results)

---

## Reporting Issues

If you discover a security concern in this project, please open an issue on the repository describing the concern. Do not include actual credentials or tokens in the issue.

---

*Personal AI Employee — Hackathon-0 Submission*
*Security model: local-first, human-in-the-loop, audit-logged*
