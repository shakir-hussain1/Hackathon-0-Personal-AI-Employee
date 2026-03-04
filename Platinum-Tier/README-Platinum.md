# 💎 Platinum Tier - Personal AI Employee

**Status**: ✅ Built (cloud VM deploy required for 24/7 operation)
**Time to Implement**: 60+ hours
**Complexity**: Very High
**Prerequisites**: Gold Tier Complete

---

## 📋 Overview

Platinum tier transforms the AI Employee from a local tool into a production-grade, always-on system. A cloud VM runs 24/7 doing email triage and drafting while your laptop handles approvals, sends, and sensitive actions. They communicate through a Git-synced vault — no direct network connection needed between the two.

---

## ✅ What's Built

| Component | File | Status |
|-----------|------|--------|
| Vault Sync (Git) | `shared/vault_sync.py` | ✅ Complete |
| Claim Manager | `shared/claim_manager.py` | ✅ Complete |
| Cloud Orchestrator | `cloud/cloud_orchestrator.py` | ✅ Complete |
| Health Monitor | `cloud/health_monitor.py` | ✅ Complete |
| Dockerfile | `cloud/Dockerfile` | ✅ Complete |
| Docker Compose | `cloud/docker-compose.yml` | ✅ Complete |
| Cloud `.env` template | `cloud/.env.cloud.example` | ✅ Complete |
| Local Orchestrator | `local/local_orchestrator.py` | ✅ Complete |
| Setup Script | `setup/setup_platinum.py` | ✅ Complete |
| Local launch script | `start_platinum_local.bat` | ✅ Complete |
| Dependencies | `requirements.txt` | ✅ Complete |
| Local `.env` template | `.env.example` | ✅ Complete |

---

## 🎯 What Platinum Adds Over Gold

| Feature | Gold | Platinum |
|---------|------|----------|
| Always-on 24/7 | ❌ Manual start | ✅ Cloud VM + Docker |
| Cloud-Local split | ❌ | ✅ Two separate agents |
| Vault sync (Git) | ❌ | ✅ Bidirectional, every cycle |
| Claim-by-move rule | ❌ | ✅ No double-work |
| Health auto-restart | Basic watchdog | ✅ psutil + max restarts/hr |
| Dashboard single-writer | ❌ | ✅ Only Local writes it |
| Secrets-never-sync | Partial | ✅ .gitignore enforced by setup |
| Domain-namespaced folders | ❌ | ✅ Needs_Action/email/, /social/ |
| Cloud update pipeline | ❌ | ✅ Updates/ → Dashboard merge |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                  CLOUD VM (24/7)                     │
│                                                      │
│  cloud_orchestrator.py        health_monitor.py      │
│  ┌─────────────────────┐      ┌───────────────────┐  │
│  │ 1. Gmail → detect   │      │ Monitor processes  │  │
│  │ 2. Claim task       │      │ Auto-restart crash │  │
│  │ 3. Draft reply      │      │ Write health report│  │
│  │ 4. Write approval   │      └───────────────────┘  │
│  │ 5. Write Updates/   │                             │
│  │ 6. Git push vault   │                             │
│  └─────────────────────┘                             │
└──────────────── Git Sync (private repo) ─────────────┘
                          ↕
┌──────────────────────────────────────────────────────┐
│              LOCAL MACHINE (your laptop)             │
│                                                      │
│  local_orchestrator.py                               │
│  ┌─────────────────────────────────────────────┐     │
│  │ 1. Git pull vault                           │     │
│  │ 2. Merge Updates/ → Dashboard.md            │     │  ← sole writer
│  │ 3. Watch Approved/ → execute via MCP        │     │
│  │ 4. Log actions → Logs/audit.jsonl           │     │
│  │ 5. Git push vault                           │     │
│  └─────────────────────────────────────────────┘     │
│                                                      │
│  WhatsApp session | Banking | Payments               │  ← LOCAL ONLY
└──────────────────────────────────────────────────────┘
```

### The 5 Iron Rules

| # | Rule | Why |
|---|------|-----|
| 1 | **Cloud = draft-only** | Never sends email, never posts, never pays |
| 2 | **Local = executor** | All real actions happen after human approval |
| 3 | **Single-writer rule** | Only Local writes `Dashboard.md` |
| 4 | **Claim-by-move** | First agent to move file to `In_Progress/` owns it |
| 5 | **Secrets never sync** | `.env`, tokens, credentials stay machine-local |

---

## 📁 File Structure

```
Platinum-Tier/
├── shared/
│   ├── vault_sync.py         # Git push/pull + .gitignore enforcement
│   └── claim_manager.py      # Claim-by-move rule (atomic file move)
├── cloud/
│   ├── cloud_orchestrator.py # 24/7 cloud agent (draft-only)
│   ├── health_monitor.py     # psutil process monitor + auto-restart
│   ├── Dockerfile            # Python 3.13-slim + git
│   ├── docker-compose.yml    # cloud-orchestrator + health-monitor services
│   └── .env.cloud.example    # Cloud VM environment template
├── local/
│   └── local_orchestrator.py # Approval watcher + MCP executor + Dashboard merger
├── setup/
│   └── setup_platinum.py     # One-time: creates folders, git init, .gitignore
├── start_platinum_local.bat  # Launch local agent on Windows
├── requirements.txt          # python-dotenv, psutil, google-auth, requests
└── .env.example              # Local machine environment template
```

---

## 📂 Vault Folder Structure (Platinum additions)

```
AI_Employee_Vault/
├── Needs_Action/
│   ├── email/              ← Cloud drops email tasks here
│   ├── social/             ← Cloud drops social draft tasks here
│   └── file/               ← File-drop tasks (Bronze, still works)
├── Plans/
│   ├── email/              ← Cloud writes draft replies here
│   └── social/             ← Cloud writes social post drafts here
├── Pending_Approval/
│   ├── email/              ← Cloud writes approval requests (email)
│   └── social/             ← Cloud writes approval requests (social)
├── In_Progress/
│   ├── cloud/              ← Tasks claimed by cloud agent
│   └── local/              ← Tasks claimed by local agent
├── Updates/                ← Cloud writes status summaries here
│   ├── health/             ← Health monitor reports (HEALTH_LATEST.md)
│   └── processed/          ← Archived updates after local merges them
├── Signals/                ← Inter-agent coordination signals
├── Approved/               ← Human moves approval files here → local executes
├── Rejected/               ← Human moves here → task cancelled
└── Done/                   ← Both agents move completed tasks here
```

---

## 🔑 Key Feature: VaultSync

Git-based bidirectional sync. Both agents share state through a private GitHub repo — no direct network connection required between cloud and laptop.

```python
from shared.vault_sync import VaultSync

sync = VaultSync(vault_path="/path/to/vault", remote="git@github.com:user/vault.git")
sync.init()        # git init + add remote (run once)
sync.pull()        # fetch latest from cloud/local counterpart
sync.push("cloud: processed 3 emails")  # stage markdown + push
sync.sync()        # pull then push in one call
```

**What syncs:** `*.md`, `Logs/*.log`, `Updates/`, `Signals/`

**What NEVER syncs** (enforced by `.gitignore`):
`.env`, `credentials.json`, `*.session`, `*.json` tokens, `venv/`, `__pycache__/`

---

## 🔑 Key Feature: ClaimManager

Prevents both agents from processing the same task. Uses atomic `shutil.move()` — whichever agent moves the file first owns it.

```python
from shared.claim_manager import ClaimManager

cm = ClaimManager(vault_path, agent_name="cloud")

# Try to claim — returns None if another agent already claimed it
claimed = cm.claim(Path("Needs_Action/email/EMAIL_invoice.md"))
if claimed:
    # You own it — process safely
    cm.release(claimed, destination="Done")

# List what's available vs what's mine
pending = cm.list_pending("email")   # unclaimed tasks
mine    = cm.list_mine()             # my current claims
```

---

## 🔑 Key Feature: Health Monitor (Cloud)

Runs alongside `cloud_orchestrator.py` in Docker. Monitors process PIDs with `psutil`, restarts on crash, caps restarts per hour to prevent loops.

**Behaviour:**
- Checks every 60 seconds (configurable)
- Max 5 restarts/hour per process (safety cap)
- Writes `Updates/health/HEALTH_LATEST.md` after each check
- Local agent sees health report on next git pull

**Output in vault:**
```markdown
# Cloud Health Report
Updated: 2026-02-24 10:30:00

## Process Status
- ✅ **cloud_orchestrator** | pid=1234 | restarts=0
```

---

## 🔑 Key Feature: Dashboard Merge (Single-Writer Rule)

Cloud never writes directly to `Dashboard.md`. Instead it writes status files to `Updates/`. Local merges them.

```
Cloud writes:  Updates/UPDATE_20260224_103000.md
Local reads:   Updates/*.md
Local appends: Dashboard.md  ← sole writer, no conflicts
Local archives: Updates/processed/
```

---

## ⚙️ Setup: Step by Step

### Phase 1 — Local Machine (Start Here)

```cmd
cd E:\Hackathon-0-Personal-AI-Employee\Platinum-Tier

REM Step 1: Create Platinum vault folders + git init + .gitignore
python setup\setup_platinum.py

REM Step 2: Configure local environment
copy .env.example .env
notepad .env

REM Step 3: Start local agent
start_platinum_local.bat
```

### Phase 2 — Vault Git Sync (Private GitHub Repo)

```bash
# 1. Create a PRIVATE repo on GitHub: e.g. "ai-employee-vault"
# 2. In your vault directory:
cd "E:\Hackathon-0-Personal-AI-Employee\Common\AI_Employee_Vault"
git remote add origin git@github.com:youruser/ai-employee-vault.git
git push -u origin main

# 3. Set VAULT_GIT_REMOTE in both .env files
```

### Phase 3 — Cloud VM (Oracle Free Tier / AWS)

Oracle Cloud Always Free: 2 AMD cores, 1GB RAM — sufficient for cloud agent.

```bash
# SSH into VM
ssh ubuntu@YOUR_VM_IP

# Clone vault (git clone of your private vault repo)
git clone git@github.com:youruser/ai-employee-vault.git ~/AI_Employee_Vault

# Clone project
git clone YOUR_PROJECT_REPO ~/ai-employee

# Create secrets directory (NEVER commit these files)
mkdir -p ~/secrets
cp ~/ai-employee/Platinum-Tier/cloud/.env.cloud.example ~/secrets/.env
nano ~/secrets/.env    # Fill in VAULT_GIT_REMOTE, GMAIL_CREDENTIALS, etc.

# Deploy with Docker
cd ~/ai-employee/Platinum-Tier/cloud
docker-compose up -d

# Verify
docker logs platinum_cloud_orchestrator -f
docker logs platinum_health_monitor -f
```

---

## 🔧 Feature Toggles

### Local `.env`

| Variable | Default | Description |
|----------|---------|-------------|
| `VAULT_PATH` | auto-detected | Absolute path to vault |
| `VAULT_GIT_REMOTE` | _(empty)_ | Private GitHub repo SSH URL |
| `DRY_RUN` | `true` | No real email sends until false |
| `ENABLE_GMAIL_SEND` | `false` | Actually send approved emails via MCP |
| `CHECK_INTERVAL_SEC` | `30` | How often local polls for approvals |

### Cloud `.env` (on VM)

| Variable | Default | Description |
|----------|---------|-------------|
| `VAULT_PATH` | `/home/ubuntu/AI_Employee_Vault` | Vault clone path on VM |
| `VAULT_GIT_REMOTE` | _(required)_ | Private vault repo SSH URL |
| `GMAIL_CREDENTIALS` | `/secrets/credentials.json` | OAuth credentials (never synced) |
| `CHECK_INTERVAL_MIN` | `15` | Gmail poll frequency |
| `DRY_RUN` | `true` | Safe mode |
| `ENABLE_GMAIL` | `false` | Enable Gmail monitoring |
| `HEALTH_CHECK_INTERVAL_SEC` | `60` | Health monitor frequency |
| `MAX_RESTARTS_PER_HOUR` | `5` | Crash restart cap |

---

## 🚀 Demo: Platinum Minimum Passing Gate

> "Email arrives while Local is offline → Cloud drafts reply + writes approval
> → Local returns, human approves → Local sends via MCP → logs → Done"

| Step | Agent | Action | Vault change |
|------|-------|--------|-------------|
| 1 | Cloud | Gmail detects email | `Needs_Action/email/EMAIL_xxx.md` created |
| 2 | Cloud | Claims task | File moved → `In_Progress/cloud/EMAIL_xxx.md` |
| 3 | Cloud | Drafts reply | `Plans/email/PLAN_EMAIL_xxx.md` created |
| 4 | Cloud | Writes approval request | `Pending_Approval/email/APPROVAL_xxx.md` created |
| 5 | Cloud | Git push | Remote vault updated |
| 6 | Human | Laptop comes online, git pull | Sees approval file |
| 7 | Human | Reviews draft in Plans/email/ | Approves or edits |
| 8 | Human | Moves approval file | → `Approved/APPROVAL_xxx.md` |
| 9 | Local | Detects approved file | Sends email via MCP |
| 10 | Local | Logs action | `Logs/YYYY-MM-DD_audit.jsonl` entry |
| 11 | Local | Moves to Done | `Done/APPROVAL_xxx.md` |
| 12 | Local | Git push | Remote updated for cloud |

---

## 🔐 Security

| Rule | Implementation |
|------|---------------|
| Secrets never sync | `.gitignore` enforced by `setup_platinum.py` |
| Cloud = read + draft only | `cloud_orchestrator.py` has no send/post/pay code |
| HITL for all sends | Every action requires file in `Approved/` first |
| Audit trail | Every action → `Logs/YYYY-MM-DD_audit.jsonl` |
| Docker secrets mount | Credentials mounted read-only at runtime, not in image |
| No creds in repo | `Dockerfile` has no secrets; `.env` never committed |

---

## 📅 Schedules

| Agent | Task | Frequency |
|-------|------|-----------|
| Cloud | Gmail check + draft | Every 15 min |
| Cloud | Git push (after changes) | After each cycle |
| Health | Process health check | Every 60 sec |
| Health | Write health report to vault | Every 60 sec |
| Local | Git pull | Every 30 sec |
| Local | Check Approved/ | Every 30 sec |
| Local | Merge Updates/ → Dashboard | Every 30 sec (when updates exist) |

---

## 🧪 Quick Test (no cloud VM needed)

Test local agent on your laptop first:

```cmd
cd E:\Hackathon-0-Personal-AI-Employee\Platinum-Tier

REM Step 1: Setup folders
python setup\setup_platinum.py

REM Step 2: Start local agent
start_platinum_local.bat
```

Expected output:
```
Local Orchestrator starting (Platinum Tier)
Vault: E:\...\AI_Employee_Vault
DRY_RUN: True
Watching: /Approved/, /Updates/
```

**Simulate cloud sending an approval:**
1. Create any `.md` file in `Approved/` named `APPROVAL_test.md`
2. Local agent detects it within 30 seconds
3. Logs action to `Logs/YYYY-MM-DD_audit.jsonl`
4. Moves file to `Done/`

---

## 🎯 Success Criteria

- [x] `setup_platinum.py` creates all Platinum folders in vault
- [x] `vault_sync.py` — Git push/pull with `.gitignore` security enforcement
- [x] `claim_manager.py` — atomic claim-by-move, race condition handled
- [x] `cloud_orchestrator.py` — Gmail monitor + draft + approval writer (draft-only)
- [x] `health_monitor.py` — psutil process monitoring + auto-restart (max 5/hr)
- [x] `local_orchestrator.py` — approval watcher + MCP executor + Dashboard merger
- [x] `Dockerfile` + `docker-compose.yml` — cloud deployment ready
- [x] Domain-namespaced vault folders (`/email/`, `/social/`)
- [x] Single-writer rule for `Dashboard.md`
- [x] `DRY_RUN=true` by default — no real actions until explicitly enabled
- [x] Audit log for every local execution
- [x] Platinum demo gate scenario implementable end-to-end
