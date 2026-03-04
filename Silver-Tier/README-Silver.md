# 🥈 Silver Tier - Personal AI Employee

**Status**: ✅ Built & Ready (credentials required)
**Time to Implement**: 20-30 hours
**Complexity**: Medium
**Prerequisites**: Bronze Tier Complete

---

## 📋 Overview

Silver tier enhances Bronze with Gmail monitoring, email drafting + sending (MCP), LinkedIn posting, Calendar awareness, WhatsApp watching, Claude reasoning loop (Plan.md), and human-in-the-loop approval workflows.

---

## ✅ What's Built

| Component | File | Status |
|-----------|------|--------|
| Orchestrator | `orchestrator/orchestrator.py` | ✅ Complete |
| Reasoning Loop | `orchestrator/reasoning_loop.py` | ✅ Complete |
| Gmail Watcher | `watchers/gmail_watcher.py` | ✅ Complete |
| Calendar Watcher | `watchers/calendar_watcher.py` | ✅ Complete |
| LinkedIn Watcher | `watchers/linkedin_watcher.py` | ✅ Complete |
| WhatsApp Watcher | `watchers/whatsapp_watcher.py` | ✅ Complete |
| Email Sender MCP | `mcp-servers/email_sender/server.py` | ✅ Complete |
| LinkedIn Poster MCP | `mcp-servers/linkedin_poster/server.py` | ✅ Complete |
| Agent Skills | `skills/` (5 skills) | ✅ Complete |
| Virtual Environment | `venv/` | ✅ Installed |
| Dependencies | `requirements.txt` | ✅ Complete |
| Config Template | `.env.example` | ✅ Complete |

---

## 🎯 What Silver Tier Does

1. **Gmail Monitoring** — Polls inbox every 15 min, creates `EMAIL_*.md` tasks in `Needs_Action/`
2. **Claude Reasoning Loop** — Reads pending tasks, calls Claude API to create `Plan_*.md` files
3. **Email Sending (HITL)** — Drafts go to `Plans/email_drafts/`, human approves, MCP sends
4. **LinkedIn Posting** — Watches `Done/` for business content, queues posts, human approves
5. **Calendar Monitoring** — Creates tasks for upcoming events in `Needs_Action/`
6. **WhatsApp Watcher** — Playwright-based keyword monitoring (optional, requires QR scan)
7. **Scheduling** — All checks run on configurable intervals via `schedule` library

---

## 📁 Structure

```
Silver-Tier/
├── watchers/
│   ├── base_watcher.py          # Abstract base class
│   ├── gmail_watcher.py         # Gmail inbox monitoring
│   ├── calendar_watcher.py      # Google Calendar events
│   ├── linkedin_watcher.py      # LinkedIn content queue
│   └── whatsapp_watcher.py      # WhatsApp Web (Playwright)
├── orchestrator/
│   ├── orchestrator.py          # Main coordinator + scheduler
│   └── reasoning_loop.py        # Claude API → Plan.md creation
├── mcp-servers/
│   ├── email_sender/
│   │   ├── server.py            # Gmail send MCP server
│   │   ├── config.json
│   │   └── templates/
│   └── linkedin_poster/
│       └── server.py            # LinkedIn post MCP server
├── skills/
│   ├── process_email.md
│   ├── draft_reply.md
│   ├── create_plan.md
│   ├── linkedin_post.md
│   └── schedule_task.md
├── venv/                        # Python 3.13 virtual environment
├── requirements.txt
├── .env.example                 # Copy → .env and fill credentials
├── start_silver.bat             # Launch script
└── README-Silver.md
```

---

## ⚙️ Setup (5 steps)

### Step 1 — Google Cloud Setup (required for Gmail + Calendar)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project → Enable **Gmail API** + **Google Calendar API**
3. Create **OAuth 2.0 credentials** (Desktop app type)
4. Download JSON → save as `Silver-Tier\credentials.json`

### Step 2 — Configure `.env`

```cmd
cd E:\Hackathon-0-Personal-AI-Employee\Silver-Tier
copy .env.example .env
notepad .env
```

Fill in:
- `ANTHROPIC_API_KEY` — from claude.ai (for reasoning loop)
- `LINKEDIN_ACCESS_TOKEN` — from LinkedIn Developer Portal
- `LINKEDIN_AUTHOR_URN` — your LinkedIn person URN
- Leave `ENABLE_WHATSAPP=false` unless you want WhatsApp

### Step 3 — Start Silver

```cmd
start_silver.bat
```

First run will open a browser for Google OAuth — approve both Gmail and Calendar scopes.
Tokens are cached (`.gmail_token.json`, `.calendar_token.json`) — only needed once.

---

## 🔄 How It Works

```
Gmail Inbox
    ↓ (every 15 min)
gmail_watcher.py → Needs_Action/EMAIL_*.md
    ↓ (every 30 min)
reasoning_loop.py → Plans/Plan_*.md  (Claude API)
    ↓ (Claude Code skill)
draft_reply.md skill → Plans/email_drafts/DRAFT_*.md
    ↓ (human reviews)
Move to Approved/
    ↓ (every 5 min)
email_sender/server.py → sends via Gmail API → Done/
```

---

## 🔧 Feature Toggles (`.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_GMAIL` | `true` | Gmail inbox monitoring |
| `ENABLE_CALENDAR` | `true` | Google Calendar events |
| `ENABLE_EMAIL_SENDER` | `true` | Send approved email drafts |
| `ENABLE_LINKEDIN` | `true` | LinkedIn post suggestions |
| `ENABLE_WHATSAPP` | `false` | WhatsApp keyword monitoring |
| `CHECK_INTERVAL_MINUTES` | `15` | Gmail poll frequency |

---

## 🔐 Security

- `credentials.json` — never committed (in `.gitignore`)
- `*.json` token files — never committed
- `.env` — never committed
- All email sends require **human approval** (file moved to `/Approved/`)
- LinkedIn posts require human approval (move to `LinkedIn_Approved/`)
- `DRY_RUN` mode available — no real sends until you remove it

---

## 📊 Schedules (default)

| Task | Interval |
|------|----------|
| Gmail check | every 15 min |
| Calendar check | every 60 min |
| Email sender | every 5 min |
| Reasoning loop | every 30 min |
| LinkedIn watcher | every 60 min |
| WhatsApp watcher | every 60 sec (if enabled) |
| Dashboard update | every 30 min |

---

## 🧪 Quick Test (no Google credentials needed)

```cmd
cd E:\Hackathon-0-Personal-AI-Employee\Silver-Tier
venv\Scripts\activate.bat

REM Test orchestrator starts (Gmail will warn but not crash)
python orchestrator\orchestrator.py
```

Expected output:
```
Silver Tier Orchestrator Starting
Vault: E:\...\AI_Employee_Vault
Gmail:          ENABLED
Reasoning Loop: DISABLED (set ANTHROPIC_API_KEY)
...
Schedules configured
```

---

## 🎯 Silver Tier Success Criteria

- [x] Orchestrator runs and schedules all watchers
- [x] Gmail watcher creates EMAIL_*.md tasks (requires credentials)
- [x] Claude reasoning loop creates Plan.md files (requires ANTHROPIC_API_KEY)
- [x] Email MCP drafts and sends on approval (requires credentials)
- [x] LinkedIn watcher queues post suggestions
- [x] WhatsApp watcher monitors keywords (optional)
- [x] Human-in-the-loop for all sends
- [x] Comprehensive audit logging
