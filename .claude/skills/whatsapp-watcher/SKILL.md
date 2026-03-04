---
name: whatsapp-watcher
description: |
  Monitor WhatsApp Web for unread messages containing urgent business keywords.
  Uses Playwright persistent browser context to avoid repeated QR code scans.
  Creates WHATSAPP_*.md task files in Needs_Action/ for matching messages.
  Use to set up WhatsApp monitoring or troubleshoot the WhatsApp watcher.
---

# WhatsApp Watcher Skill

**Purpose**: Set up and operate WhatsApp Web monitoring for urgent business messages
**Tier**: Silver
**Script**: `Silver-Tier/watchers/whatsapp_watcher.py`
**Output**: `WHATSAPP_*.md` task files in `Needs_Action/`

---

## When to Use

- Setting up WhatsApp monitoring for the first time
- Troubleshooting WhatsApp watcher issues
- Testing if a WhatsApp message triggered a task
- User asks "monitor WhatsApp for urgent messages"

---

## First-Time Setup (QR Code Scan)

### Step 1 — Install Playwright

```bash
cd Silver-Tier
venv\Scripts\activate
pip install playwright
playwright install chromium
```

### Step 2 — Enable in `.env`

```env
ENABLE_WHATSAPP=true
WHATSAPP_HEADLESS=false   ← set to false for first run (shows browser)
WHATSAPP_INTERVAL_SECONDS=60
```

### Step 3 — Scan QR Code

```bash
cd Silver-Tier
venv\Scripts\activate
python watchers\whatsapp_watcher.py
```

A browser window opens → scan the QR code with your phone.

Once logged in:
- Session is saved to `Silver-Tier/.whatsapp_session/`
- Set `WHATSAPP_HEADLESS=true` in `.env` for future runs

### Step 4 — Verify Session Saved

```bash
dir Silver-Tier\.whatsapp_session
```

Should contain browser profile files. If empty, scan QR again.

---

## How It Works

```
WhatsApp Watcher checks every 60 seconds:
    ↓
Opens WhatsApp Web in persistent Playwright context
    ↓
Finds chats with unread message badge
    ↓
Checks each chat text for urgent keywords:
    urgent, asap, emergency, invoice, payment,
    deadline, help, problem, meeting, call me
    ↓
For matching messages → creates WHATSAPP_*.md in Needs_Action/
    ↓
Orchestrator / Claude processes the task
```

---

## Urgent Keywords

The watcher triggers on these keywords (case-insensitive):
```
urgent, asap, emergency, critical
invoice, payment, overdue, deadline
help, problem, issue, fix, broken
meeting, call me, call us
```

To customize, edit `URGENT_KEYWORDS` in `Silver-Tier/watchers/whatsapp_watcher.py`.

---

## Task File Format

When a matching message is found, the watcher creates:
`Needs_Action/WHATSAPP_{sender}_{timestamp}.md`

```markdown
# WhatsApp Task: {sender name}
Created: {timestamp}
Priority: HIGH
Status: PENDING
Source: WhatsApp Watcher

## Message Preview
From: {sender}
Keywords Detected: urgent, invoice

{message preview text}

## What To Do
1. Review the WhatsApp message from {sender}
2. Determine if action or reply is required
3. Use draft-reply skill or respond directly on WhatsApp
4. Move to Done/ when handled
```

---

## Running via Orchestrator

The orchestrator calls `check_whatsapp()` on schedule when `ENABLE_WHATSAPP=true`.

To check schedule status:
```bash
# In orchestrator log:
type Silver-Tier\orchestrator_*.log | findstr /i whatsapp
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `playwright not installed` | `pip install playwright && playwright install chromium` |
| QR code keeps reappearing | Session not saved — check `.whatsapp_session/` permissions |
| "chat-list not found" | WhatsApp not logged in — run headless=false and scan QR |
| No messages found despite unread | Keywords may not match — check `URGENT_KEYWORDS` list |
| Browser fails to open | Try: `playwright install --with-deps chromium` |

---

## Session Management

- Session path: `Silver-Tier/.whatsapp_session/` (auto-created)
- Session persists across restarts (no QR scan needed again)
- If session expires (WhatsApp logs out): re-run with `WHATSAPP_HEADLESS=false`
- To reset session: delete `Silver-Tier/.whatsapp_session/` folder

---

## Configuration Reference

```env
# Silver-Tier/.env
ENABLE_WHATSAPP=true              # Enable in orchestrator
WHATSAPP_HEADLESS=true            # false = show browser (needed for QR scan)
WHATSAPP_INTERVAL_SECONDS=60      # Check every N seconds
WHATSAPP_SESSION_PATH=Silver-Tier\.whatsapp_session   # override if needed
```

---

**Status**: Production Ready
**Tier**: Silver
**Requires**: `playwright` package + `playwright install chromium`
**Related**: `process-email` skill (similar workflow for WHATSAPP_ tasks)
