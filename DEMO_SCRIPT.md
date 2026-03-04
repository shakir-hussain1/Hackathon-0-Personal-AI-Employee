# 🎬 Demo Video Script
# Personal AI Employee — All 4 Tiers
# Hackathon-0: Building Autonomous FTEs in 2026
# Target Duration: 7–8 minutes

---

## 🖥️ RECORDING SETUP (Do This Before Hitting Record)

**Screen Layout:**
- Left half: VS Code (Markdown preview of Dashboard.md open)
- Right half: Terminal / Windows Explorer

**Pre-recording checklist:**
- [ ] Font size 16+ in VS Code and Terminal (readable on video)
- [ ] Focus Assist ON (no notification popups)
- [ ] Close browser, Slack, all irrelevant windows
- [ ] `Dashboard.md` open in VS Code with `Ctrl+Shift+V` preview active
- [ ] 3 terminals pre-opened and cleared (`cls`)
- [ ] Demo test files ready on Desktop (see bottom of this file)
- [ ] Bronze venv activated and ready
- [ ] All terminals at correct directories

**Recording tool:** OBS Studio (free) or Windows Game Bar (`Win+G`)
**Resolution:** 1920×1080, 30fps
**Upload:** YouTube unlisted or Google Drive link

---

## ⏱️ TIMING GUIDE

| Scene | Time | What to Show |
|-------|------|-------------|
| 1. Hook | 0:00–0:30 | The problem — one line pitch |
| 2. Architecture | 0:30–1:00 | Project structure in VS Code |
| 3. Bronze LIVE | 1:00–2:45 | Drop file → detect → Claude processes |
| 4. Silver | 2:45–4:15 | Orchestrator start + skills + LinkedIn draft |
| 5. Gold | 4:15–6:00 | CEO Briefing + audit log + Ralph Wiggum |
| 6. Platinum | 6:00–7:00 | Architecture + local agent live |
| 7. Close | 7:00–7:30 | All 4 running + wrap up |
| **Total** | **~7:30** | |

---

## SCENE 1 — THE HOOK (0:00 – 0:30)

**[Show: Desktop — project folder icon]**

**Narration (speak slowly and clearly):**
> "Ek human employee 40 ghante kaam karta hai hafte mein.
> Ek Digital FTE — 168 ghante. Har hafte. Bina thake.
>
> Aaj main aapko dikhaunga — Personal AI Employee.
> Yeh aapki Gmail monitor karta hai, invoices banata hai,
> LinkedIn pe post karta hai, aur har Monday CEO briefing deta hai.
>
> Sab kuch local — aapke laptop pe. Koi cloud subscription nahi."

**[Pause 1 second — let it sink in]**

---

## SCENE 2 — PROJECT STRUCTURE (0:30 – 1:00)

**[Show: VS Code Explorer — project root open]**

**Narration:**
> "Project four tiers mein build hua hai."

**[ACTION: Expand folder tree slowly in VS Code]**

> "Bronze — file system monitoring. Foundation.
> Silver — Gmail, Calendar, LinkedIn automation.
> Gold — Odoo accounting, social media, CEO briefing.
> Platinum — always-on cloud deployment with local approval."

**[Show: Common/AI_Employee_Vault/ folder]**

> "Yeh sab ek shared vault ke through communicate karte hain —
> Obsidian-compatible markdown files. Human-readable. Audit-ready."

**[ACTION: Click Dashboard.md — preview visible]**

> "Yeh AI ka real-time dashboard hai. Chalo live demo shuru karte hain."

---

## SCENE 3 — BRONZE: LIVE DEMO (1:00 – 2:45)

**[Show: Terminal 1 — Bronze-Tier]**

**Narration:**
> "Bronze tier — file system watcher. Start karte hain."

**[ACTION: Type in terminal]**
```
cd E:\Hackathon-0-Personal-AI-Employee\Bronze-Tier
start_bronze.bat
```

**[Bronze watcher output appears:]**
```
Bronze Tier AI Employee Starting
[OK] Vault folder exists.
Activating virtual environment...
Starting Bronze Tier File System Watcher...
[INFO] Vault: ...\AI_Employee_Vault
[INFO] Drop files into Inbox\ to trigger the AI employee.
```

> "Watcher chal raha hai. Har 30 second mein Inbox check karta hai."

**[ACTION: Open Windows Explorer — navigate to Inbox folder]**
**[ACTION: Copy `meeting_notes_client_xyz.md` from Desktop into Inbox/]**

> "Main yeh meeting notes file Inbox mein daal raha hoon..."

**[Switch to Bronze terminal — wait max 30 seconds]**

```
[INFO] New file detected: meeting_notes_client_xyz.md
[INFO] Created task: FILE_meeting_notes_client_xyz_XXXXXX.md [Priority: MEDIUM]
```

> "Detected! Priority MEDIUM — .md file ke liye."

**[ACTION: Drop `invoice_demo.txt` into Inbox/]**

```
[INFO] New file detected: invoice_demo.txt
[INFO] Created task: FILE_invoice_demo_XXXXXX.md [Priority: HIGH]
```

> "Invoice file — automatically HIGH priority. 'Invoice' keyword detect hua."

**[ACTION: In VS Code — open Needs_Action/ folder, click on task file]**

> "Yeh task file ban gayi — AI ke liye complete instructions.
> Filename, priority, timestamp, suggested actions — sab kuch."

**[ACTION: New terminal — Claude Code session]**
```
cd "E:\Hackathon-0-Personal-AI-Employee\Common\AI_Employee_Vault"
claude
```

**[In Claude session:]**
```
Please process all tasks in Needs_Action/ according to Company_Handbook.md
```

**[Show Claude working — reading, analyzing, writing]**

**[After 30–45 seconds:]**

> "Claude ne process kar diya. Dekho —"

**[Show in VS Code:]**
- Needs_Action/ — empty ✅
- Done/ — files moved here ✅
- Dashboard.md preview — stats updated ✅

> "Files Done mein hain. Dashboard updated. Log file create hui.
> Yeh Bronze tier — working foundation."

---

## SCENE 4 — SILVER: ORCHESTRATOR + SKILLS (2:45 – 4:15)

**[Show: Terminal 2 — Silver-Tier]**

**Narration:**
> "Silver tier — Gmail, Calendar, LinkedIn, WhatsApp. Start karte hain."

**[ACTION:]**
```
cd E:\Hackathon-0-Personal-AI-Employee\Silver-Tier
start_silver.bat
```

**[Silver output appears:]**
```
Silver Tier Orchestrator Starting
Vault: ...\AI_Employee_Vault
Gmail:          ENABLED
Calendar:       ENABLED
Email Sender:   ENABLED
LinkedIn:       ENABLED
WhatsApp:       DISABLED (set ENABLE_WHATSAPP=true)
Reasoning Loop: ENABLED
Schedules configured:
  Gmail check:    every 15 minutes
  Reasoning loop: every 30 minutes
  LinkedIn:       every 60 minutes
```

> "Sab features enabled hain. Gmail se email aane pe automatically
> task file ban jaayegi — credentials add karne ke baad fully live."

**[ACTION: Switch to VS Code — open `.claude/skills/` folder]**

> "Silver ke 6 Agent Skills hain — Claude Code automatically discover karta hai."

**[Slowly scroll through skill files:]**
```
process-email/SKILL.md    ← Gmail emails process karo
draft-reply/SKILL.md      ← Professional reply draft karo
linkedin-post/SKILL.md    ← LinkedIn post queue karo
create-plan/SKILL.md      ← Autonomous Plan.md banao
schedule-task/SKILL.md    ← Windows Task Scheduler setup
whatsapp-watcher/SKILL.md ← WhatsApp keywords monitor karo
```

**[ACTION: In Claude session:]**
```
/linkedin-post
```

**[Show Claude drafting a LinkedIn post based on Done/ content]**

> "LinkedIn skill chalaya — Claude ne Done/ folder se business content uthaya,
> professional post draft ki, aur LinkedIn_Queue mein rakh di human approval ke liye.
> Koi post directly nahi hoti — HITL. Human in the Loop."

**[Show: LinkedIn_Queue/ folder — draft file visible]**

> "Yeh file LinkedIn_Approved mein move karoge tab post hogi. Pehle review, phir action."

---

## SCENE 5 — GOLD: CEO BRIEFING + AUDIT + RALPH (4:15 – 6:00)

**[Show: Terminal 3 — Gold-Tier]**

**Narration:**
> "Gold tier — autonomous employee ka full implementation."

**[ACTION:]**
```
cd E:\Hackathon-0-Personal-AI-Employee\Gold-Tier
start_gold.bat
```

**[Gold output:]**
```
Gold Tier AI Employee Starting
DRY_RUN: True  (safe mode)
Ralph Loop:     ENABLED
Weekly Briefing: sunday 20:00
Odoo:       DISABLED (set ENABLE_ODOO=true)
Facebook:   DISABLED
Twitter:    DISABLED
Schedules configured.
```

> "Gold chal raha hai — DRY_RUN=true matlab safe mode. Credentials add karo,
> DRY_RUN=false karo — live ho jata hai."

**[ACTION: Open Briefings/ folder — CEO Briefing file click karein]**

> "Yeh Monday Morning CEO Briefing hai — AI ne khud generate ki hai.
> Business_Goals.md padha, done tasks analyze kiye, accounting check ki."

**[Read key sections aloud while scrolling:]**
- Revenue this week
- Completed tasks
- Action required items
- Proactive suggestions

> "Har Sunday raat yeh automatically generate hoti hai — Monday subah ready."

**[ACTION: Open Logs/ folder — click JSON audit log file]**

```json
{
  "timestamp": "2026-02-20T14:25:41",
  "action_type": "SYSTEM_TEST",
  "actor": "gold_orchestrator",
  "target": "Gold-Tier",
  "approval_status": "auto",
  "result": "OK"
}
```

> "Har action JSON mein log hoti hai — timestamp, actor, approval status, result.
> 90 din ka retention. Full audit trail. Hackathon spec Section 6.3 compliant."

**[ACTION: In Claude session:]**
```
/ralph-wiggum
```

**[Show Claude starting a ralph loop or explain:]**

> "Ralph Wiggum — Gold tier ka persistence mechanism.
> Claude ko ek complex task dete hain. Jab Claude kaam khatam karne ke baad
> exit karna chahta hai, Stop hook check karta hai — task file Done mein gayi?
> Nahi gayi toh Claude ko wapas kaam pe lagata hai.
> Automatically. Jab tak task Done nahi hota."

**[ACTION: Briefly show Gold MCP server files in VS Code]**

```
Gold-Tier/mcp-servers/
├── odoo_connector/server.py    ← Invoice banao, transactions log karo
├── twitter_x/server.py         ← Tweets post karo
└── facebook_instagram/server.py ← FB + Instagram pe post karo
```

> "5 MCP servers register hain — Claude ke haath hain yeh. External world se connect."

---

## SCENE 6 — PLATINUM: ALWAYS-ON ARCHITECTURE (6:00 – 7:00)

**[Show: VS Code — Platinum-Tier/ folder structure]**

**Narration:**
> "Platinum tier — production deployment. Cloud 24/7 + local approval."

**[Show architecture diagram on screen — draw/type it:]**
```
☁️  CLOUD VM (Oracle Free / AWS)          💻  YOUR LAPTOP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ←git→   ━━━━━━━━━━━━━━━━━━━━━
cloud_orchestrator.py                     local_orchestrator.py
  Gmail detect → task file                  Git pull
  Claim task (claim-by-move)                Merge Updates → Dashboard
  Draft reply → Plans/                      Watch Approved/ folder
  Write approval → Pending_Approval/        Execute sends via MCP
  Write status → Updates/                   Log audit trail
  Git push                                  Git push
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━           ━━━━━━━━━━━━━━━━━━━━━
DRAFT ONLY. Never sends.                  EXECUTES after human OK.
```

> "Cloud sirf drafts banata hai — kabhi directly send nahi karta.
> Local machine pe tum approve karte ho, phir local agent actual email bhejta hai.
> Secrets — .env, tokens, credentials — kabhi sync nahi hote."

**[ACTION: In terminal — run setup]**
```
cd E:\Hackathon-0-Personal-AI-Employee\Platinum-Tier
python setup\setup_platinum.py
```

**[Output:]**
```
  ✓ Needs_Action/email/
  ✓ Needs_Action/social/
  ✓ In_Progress/cloud/
  ✓ In_Progress/local/
  ✓ Updates/
  ✓ Signals/
✓ .gitignore updated (secrets excluded from sync)
✓ Git repo initialized in vault
✓ Setup complete!
```

> "Setup complete. Cloud VM pe Docker image deploy karo — 24/7 chal ta rahega.
> Laptop pe local agent — approval sunta rahega."

**[ACTION: Quickly show Dockerfile]**

```dockerfile
FROM python:3.13-slim
# Secrets mounted at runtime — never baked into image
CMD ["python", "cloud_orchestrator.py"]
```

> "Docker image mein koi secret nahi — runtime pe mount hota hai. Secure."

---

## SCENE 7 — CLOSING (7:00 – 7:30)

**[Show: All 3 tier terminals running + VS Code Dashboard preview]**

**Narration:**
> "Yeh hai Personal AI Employee.
>
> Bronze — files detect karta hai, organize karta hai.
> Silver — Gmail, Calendar, LinkedIn — autonomously handle karta hai.
> Gold — accounting, social media, CEO briefing — har hafte.
> Platinum — 24/7 cloud pe, local approval ke saath.
>
> Human employee: 40 hours/week. Cost: Rs 40,000+/month.
> Digital FTE: 168 hours/week. Cost: API calls only.
>
> Yeh sirf ek hackathon project nahi —
> yeh ek working blueprint hai production AI employee ka."

**[Pause — show Dashboard.md with completed tasks visible]**

> "Thank you."

**[END RECORDING]**

---

## 📋 PRE-RECORDING CHECKLIST (Full)

**Files to prepare on Desktop:**

**`meeting_notes_client_xyz.md`**
```markdown
# Client Meeting Notes — XYZ Corp
Date: 2026-02-24
Attendees: CEO, Client Team

## Key Points
- Q1 project scope finalized
- Budget: Rs 2,00,000
- Deadline: March 31, 2026

## Action Items
- Send proposal by Feb 28
- Schedule follow-up call next week
```

**`invoice_demo.txt`**
```
Invoice #INV-2026-002
Client: ABC Corporation
Amount: Rs 50,000
Due Date: March 5, 2026
Services: AI Integration - Phase 1
```

**Terminal windows to pre-open:**
| Terminal | Directory | Command ready |
|----------|-----------|---------------|
| T1 | Bronze-Tier/ | `start_bronze.bat` |
| T2 | Silver-Tier/ | `start_silver.bat` |
| T3 | Gold-Tier/ | `start_gold.bat` |
| T4 | AI_Employee_Vault/ | `claude` |

**VS Code tabs to pre-open:**
- `Dashboard.md` (Ctrl+Shift+V — preview mode)
- `Company_Handbook.md`
- `Business_Goals.md`
- `Briefings/` folder
- `.claude/skills/` folder

---

## 🎬 POST-RECORDING CHECKLIST

- [ ] Trim dead air at start and end
- [ ] Add text overlay at each scene change (e.g. "🥉 Bronze Tier — File Monitoring")
- [ ] Zoom in on terminal output — font may be small on video
- [ ] Add captions for key narration lines
- [ ] Export: 1080p, 30fps, MP4
- [ ] Upload: YouTube (unlisted) or Google Drive
- [ ] Paste link in submission form

---

## ⚠️ COMMON RECORDING MISTAKES TO AVOID

| Mistake | Fix |
|---------|-----|
| Terminal font too small | Set to 16pt before recording |
| Talking while typing | Type first, then narrate |
| Long pauses while waiting | Pre-run watcher — drop files you already know will trigger |
| Showing error screens | Test entire flow once before recording |
| Going over 10 minutes | Practice run with a timer first |
| Forgetting to show Dashboard update | Keep VS Code preview open entire time |

---

*Script for Hackathon-0 — Personal AI Employee*
*Submission tier: Platinum (all 4 tiers built)*
