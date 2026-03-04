# 🥇 Gold Tier - Personal AI Employee

**Status**: ✅ Built & Tested
**Time to Implement**: 40+ hours
**Complexity**: High
**Prerequisites**: Silver Tier Complete

---

## 📋 Overview

Gold tier is the Autonomous Employee. It adds social media automation (Twitter/X, Facebook, Instagram), Odoo accounting integration, Ralph Wiggum autonomous loop, weekly CEO Briefing, multi-process watchdog, and full JSON audit logging — all with human-in-the-loop safeguards and DRY_RUN safety mode.

---

## ✅ What's Built

| Component | File | Status |
|-----------|------|--------|
| Gold Orchestrator | `orchestrator/orchestrator.py` | ✅ Complete |
| Ralph Wiggum Loop | `orchestrator/ralph_wiggum.py` | ✅ Complete |
| Weekly CEO Briefing | `orchestrator/weekly_audit.py` | ✅ Complete |
| JSON Audit Logger | `orchestrator/audit_logger.py` | ✅ Complete |
| Error Handler | `orchestrator/error_handler.py` | ✅ Complete |
| Watchdog Process | `orchestrator/watchdog.py` | ✅ Complete |
| Twitter/X MCP | `mcp-servers/twitter_x/server.py` | ✅ Complete |
| Facebook + Instagram MCP | `mcp-servers/facebook_instagram/server.py` | ✅ Complete |
| Odoo Connector MCP | `mcp-servers/odoo_connector/server.py` | ✅ Complete |
| Odoo Docker | `docker/docker-compose.odoo.yml` | ✅ Complete |
| Virtual Environment | `venv/` | ✅ Installed |
| Dependencies | `requirements.txt` | ✅ Complete |
| Config Template | `.env.example` | ✅ Complete |
| Launch Script | `start_gold.bat` | ✅ Complete |

---

## 🎯 What Gold Tier Does

1. **Runs Silver** — inherits all Silver features (Gmail, Calendar, LinkedIn, WhatsApp, Reasoning Loop)
2. **Ralph Wiggum Loop** — Stop hook keeps Claude working autonomously until a task file moves to `Done/`
3. **Twitter/X** — posts tweets, fetches engagement summaries (HITL approval)
4. **Facebook + Instagram** — posts content, generates reach/engagement summaries (HITL)
5. **Odoo Accounting** — creates invoices, logs transactions, fetches summaries via JSON-RPC MCP
6. **Weekly CEO Briefing** — every Sunday at 20:00, auto-generates `Briefings/YYYY-MM-DD_Monday_Briefing.md`
7. **Watchdog** — monitors Gold + Silver + Bronze processes, auto-restarts on crash
8. **JSON Audit Logs** — every action logged to `Logs/YYYY-MM-DD.json`, 90-day retention

---

## 📁 Structure

```
Gold-Tier/
├── orchestrator/
│   ├── orchestrator.py       # Main coordinator + scheduler (runs Silver too)
│   ├── ralph_wiggum.py       # Autonomous loop (file-movement completion)
│   ├── weekly_audit.py       # CEO Briefing generator
│   ├── audit_logger.py       # JSON structured audit log
│   ├── error_handler.py      # safe_run() wrapper + retry logic
│   └── watchdog.py           # Multi-process health monitor + auto-restart
├── mcp-servers/
│   ├── twitter_x/
│   │   └── server.py         # Twitter API v2 (post, search, summary)
│   ├── facebook_instagram/
│   │   └── server.py         # Meta Graph API (FB + IG post, summary)
│   └── odoo_connector/
│       └── server.py         # Odoo JSON-RPC (invoices, partners, accounting)
├── watchers/
│   └── base_watcher.py       # Abstract base (Silver watchers extend this)
├── docker/
│   └── docker-compose.odoo.yml  # Odoo Community 17 local instance
├── venv/                     # Python 3.13 virtual environment
├── requirements.txt
├── .env.example              # All variables documented
├── start_gold.bat            # Launch script (Docker check + memory check)
└── README-Gold.md
```

---

## 🔑 Key Feature: Ralph Wiggum Autonomous Loop

The Stop hook pattern that keeps Claude working on multi-step tasks without human re-triggering.

**How it works:**
```
1. Orchestrator writes state file → In_Progress/.ralph_state.json
2. Claude works on task
3. Claude tries to exit
4. Stop hook runs ralph_wiggum.py
5. Hook checks: is task file in Done/?
   YES → allow exit ✅
   NO  → re-inject prompt, Claude continues 🔄
6. Repeat until Done/ or max_iterations (default: 10)
```

**Start a loop:**
```python
from orchestrator.ralph_wiggum import start_ralph_loop

start_ralph_loop(
    task_file="Needs_Action/EMAIL_client_invoice.md",
    prompt="Process this email task fully and move to Done when complete.",
    max_iterations=10
)
```

**Two completion strategies:**
- `Status: COMPLETED` in task file content (promise-based)
- Task file physically moved to `Done/` (file-movement — more reliable)

---

## 📊 Key Feature: Monday Morning CEO Briefing

Every Sunday at 20:00 (configurable), Gold auto-generates a business briefing.

**Reads:**
- `Business_Goals.md` — revenue targets, KPIs, active projects
- `Done/` — completed tasks this week
- `Accounting/` — income, expenses, transactions
- `Social_Media/` — Facebook/Instagram/Twitter engagement
- `Logs/*.json` — system health and errors

**Writes:**
```
Briefings/2026-02-24_Monday_Briefing.md
```

**Includes:**
- Revenue this week vs target
- Completed tasks summary
- Bottlenecks and delays
- Subscription cost flags (unused software)
- Upcoming deadlines
- Proactive suggestions

---

## 🔒 Key Feature: JSON Audit Logging

Every action logged in structured format (Section 6.3 of spec):

```json
{
  "timestamp": "2026-02-24T10:30:00",
  "action_type": "tweet_post",
  "actor": "gold_orchestrator",
  "target": "@handle",
  "parameters": {"text": "..."},
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

- Location: `Logs/YYYY-MM-DD.json`
- Retention: 90 days (auto-purge configurable)
- Used by: CEO Briefing, security audit, debugging

---

## 🐕 Key Feature: Watchdog

Monitors all three tier processes and restarts on crash:

| Process | Command monitored |
|---------|------------------|
| Gold orchestrator | `python orchestrator/orchestrator.py` |
| Silver orchestrator | `python Silver-Tier/orchestrator/orchestrator.py` |
| Bronze watcher | `python Bronze-Tier/watchers/filesystem_watcher.py` |

Run separately: `python orchestrator/watchdog.py`

---

## ⚙️ Setup

### Step 1 — Start Odoo (optional, for accounting)

```cmd
docker-compose -f Gold-Tier\docker\docker-compose.odoo.yml up -d
```

Odoo available at: `http://localhost:8069`
Default login: `admin` / `admin`

### Step 2 — Configure `.env`

```cmd
cd E:\Hackathon-0-Personal-AI-Employee\Gold-Tier
copy .env.example .env
notepad .env
```

Fill in credentials as needed (see table below). **Start with all `ENABLE_*=false`** and enable one at a time after testing.

### Step 3 — Start Gold

```cmd
start_gold.bat
```

The bat file will:
1. Check Docker (for Odoo)
2. Create venv + install deps (first run only)
3. Install Playwright Chromium (for WhatsApp)
4. Show memory usage tip
5. Start the orchestrator

---

## 🔧 Feature Toggles (`.env`)

| Variable | Default | Enables |
|----------|---------|---------|
| `DRY_RUN` | `true` | **Safety** — no real external actions |
| `ENABLE_ODOO` | `false` | Odoo invoice/accounting MCP |
| `ENABLE_FACEBOOK` | `false` | Facebook page posting |
| `ENABLE_INSTAGRAM` | `false` | Instagram business posting |
| `ENABLE_TWITTER` | `false` | Twitter/X API v2 posting |
| `ENABLE_WEEKLY_AUDIT` | `true` | Sunday CEO Briefing |
| `ENABLE_RALPH_LOOP` | `true` | Ralph Wiggum Stop hook |
| `ENABLE_SILVER_INTEGRATION` | `true` | Run Silver checks too |
| `ENABLE_WATCHDOG_GOLD` | `true` | Monitor Gold process |
| `ENABLE_WATCHDOG_SILVER` | `true` | Monitor Silver process |

---

## 🔑 Credentials Needed

| Service | Variables | Where to get |
|---------|-----------|-------------|
| Twitter/X | `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET`, `TWITTER_BEARER_TOKEN` | [developer.twitter.com](https://developer.twitter.com) |
| Facebook | `FB_PAGE_ID`, `FB_PAGE_ACCESS_TOKEN` | [developers.facebook.com](https://developers.facebook.com) |
| Instagram | `IG_ACCOUNT_ID` | Meta Business Suite |
| Odoo | `ODOO_URL`, `ODOO_DB`, `ODOO_USER`, `ODOO_PASSWORD` | Local Docker (defaults work) |
| Claude API | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |

---

## 🔐 Security

- `DRY_RUN=true` by default — no real posts/invoices until explicitly enabled
- All social posts require human approval (HITL — move to `LinkedIn_Approved/` or `Approved/`)
- All payment/invoice actions flagged for human review
- `.env` never committed (`.gitignore` enforced)
- Audit log captures every action with approval status
- Permission boundaries from spec enforced in MCP servers

---

## 📅 Schedules (default)

| Task | Schedule |
|------|----------|
| Silver checks (Gmail, Calendar, etc.) | Per Silver settings |
| Social media summary (FB + IG + Twitter) | Every 6 hours |
| Weekly CEO Briefing | Sunday at 20:00 |
| Audit log purge (90+ day old logs) | Daily |
| Watchdog health check | Every 60 seconds |

---

## 🧪 Quick Test (no credentials needed)

```cmd
cd E:\Hackathon-0-Personal-AI-Employee\Gold-Tier
venv\Scripts\activate.bat
python orchestrator\orchestrator.py
```

Expected output (with all features disabled):
```
Gold Tier Orchestrator Starting
Vault: E:\...\AI_Employee_Vault
DRY_RUN: True
Odoo:      DISABLED
Facebook:  DISABLED
Twitter:   DISABLED
Ralph:     ENABLED
Audit:     ENABLED
Weekly:    ENABLED (sunday 20:00)
...
All schedules configured.
```

---

## 🎯 Gold Tier Success Criteria

- [x] Orchestrator runs, schedules all tasks
- [x] Inherits all Silver features
- [x] Ralph Wiggum loop keeps Claude working until Done/
- [x] CEO Briefing generated every Sunday
- [x] JSON audit log captures all actions with 90-day retention
- [x] Twitter/X posts via MCP after approval
- [x] Facebook + Instagram posts via MCP after approval
- [x] Odoo invoice creation via MCP (local Docker)
- [x] Watchdog monitors + restarts crashed processes
- [x] DRY_RUN safe mode prevents accidents
- [x] Human-in-the-loop for all sensitive actions
