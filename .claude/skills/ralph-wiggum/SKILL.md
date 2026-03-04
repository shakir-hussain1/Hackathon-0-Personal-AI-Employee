---
name: ralph-wiggum
description: |
  Start and manage the Ralph Wiggum autonomous loop — keeps Claude working on a multi-step
  task until the task file moves to Done/ or max iterations reached.
  This is the Gold-Tier persistence mechanism that prevents Claude from stopping mid-task.
  Use when a task requires multiple steps and Claude should not stop until complete.
---

# Ralph Wiggum Skill

**Purpose**: Keep Claude autonomously working until a multi-step task is fully complete
**Tier**: Gold
**Mechanism**: Stop hook checks Done/ folder — re-injects prompt if task not finished
**State file**: `AI_Employee_Vault/In_Progress/.ralph_state.json`

---

## When to Use

- A task has 5+ steps and Claude might stop mid-way
- End-to-end automation: detect → plan → act → approve → complete
- User says "work on this until done, don't stop"
- Processing a batch of tasks in Needs_Action/
- Any task that must reach Done/ before Claude stops

---

## How It Works

```
1. You or orchestrator creates a state file with the task + prompt
     ↓
2. Claude starts working on the task
     ↓
3. Claude tries to stop (session ends)
     ↓
4. Stop hook runs: .claude/hooks/ralph_wiggum_stop.py
     ↓
5. Hook checks: Is the task file in Done/?
     ↓
   YES → Allow exit (task complete)
   NO  → Output re-injection prompt → Claude continues
     ↓
6. Loop repeats until Done/ or max_iterations hit
```

---

## Starting a Ralph Loop

### Method 1 — Via Python (orchestrator)

```python
from Gold-Tier.orchestrator.ralph_wiggum import start_ralph_loop

state = start_ralph_loop(
    task_file="Common/AI_Employee_Vault/Needs_Action/FILE_invoice_abc.md",
    prompt="Process the invoice task. Read the file, draft an invoice in Odoo, create approval request. Move task to Done/ when complete.",
    max_iterations=10,
)
print(f"Ralph loop started: {state}")
```

### Method 2 — Via Claude (manual)

Ask Claude to start a Ralph loop:
```
Start a Ralph Wiggum loop for task file:
  Needs_Action/WHATSAPP_client_a_20260220.md

Prompt: "Process this WhatsApp task. Identify if a reply is needed, draft it using draft-reply skill, create approval request. Move task to Done/ when complete."

Max iterations: 8
```

Claude will write the state file to `In_Progress/.ralph_state.json`.

---

## State File Format

```json
{
  "task_file": "E:\\...\\Needs_Action\\FILE_task.md",
  "task_name": "FILE_task.md",
  "prompt": "Original task instructions...",
  "max_iterations": 10,
  "current_iteration": 3,
  "started_at": "2026-02-20T09:00:00",
  "status": "running"
}
```

---

## Completion Signals

The loop ends when ANY of these conditions are true:
1. **File moved to Done/**: `Done/` or any subdirectory contains the task filename
2. **TASK_COMPLETE in file**: Task file contains `TASK_COMPLETE` or `Status: COMPLETED`
3. **Max iterations**: Safety limit reached (default: 10)
4. **File deleted**: Task file no longer exists in Needs_Action

---

## Safety Rules

- Max iterations default: **10** (configurable via `RALPH_MAX_ITERATIONS` in .env)
- On hook error: Claude exits normally (fail-safe)
- State persists across Claude restarts (In_Progress/ folder)
- To force stop: delete `In_Progress/.ralph_state.json`

---

## Typical Ralph Loop Tasks

| Task Type | Typical Iterations | Completion Signal |
|-----------|-------------------|-------------------|
| Email processing | 2-3 | Task moved to Done/ |
| Invoice creation | 3-5 | Approval file created + moved |
| Social media post | 2-3 | Post queued for approval |
| WhatsApp response | 2-4 | Reply drafted + task moved |
| Weekly audit | 1-2 | Briefing file written |
| Multi-step plan | 5-10 | All plan steps checked off |

---

## Stop Loop Manually

```python
# Delete state file to stop the loop
from pathlib import Path
state = Path("Common/AI_Employee_Vault/In_Progress/.ralph_state.json")
if state.exists():
    state.unlink()
    print("Ralph loop stopped")
```

Or from terminal:
```bash
del "E:\Hackathon-0-Personal-AI-Employee\Common\AI_Employee_Vault\In_Progress\.ralph_state.json"
```

---

**Status**: Production Ready
**Tier**: Gold
**Hook**: `.claude/hooks/ralph_wiggum_stop.py` (registered in `.claude/settings.local.json`)
**State**: `In_Progress/.ralph_state.json`
