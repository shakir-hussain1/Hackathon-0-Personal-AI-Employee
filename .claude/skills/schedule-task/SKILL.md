---
name: schedule-task
description: |
  Set up automated recurring tasks using Windows Task Scheduler or the Python schedule library.
  Use when the user wants to automate recurring AI actions, set up daily/weekly reports,
  configure monitoring intervals, or add scheduled jobs to the orchestrator.
---

# Schedule Task Skill

**Purpose**: Create and manage recurring automated tasks for the AI Employee
**Tier**: Silver
**Input**: Task name, script path, frequency, time
**Output**: Scheduled task (Task Scheduler entry or orchestrator schedule entry)

---

## When to Use

- User wants something to run automatically at a fixed interval
- Setting up daily/weekly reports or summaries
- Configuring how often Gmail/Calendar/WhatsApp checks run
- Adding new recurring jobs to the Silver orchestrator

---

## Two Options

### Option A: Windows Task Scheduler (Recommended for reliability)

Best for: Tasks that must run even if the orchestrator is stopped.

#### Step 1 — Identify the task
- What script or command runs?
- When and how often? (daily at 9am, every 15 min, weekly on Monday, etc.)
- Should it run even when not logged in?

#### Step 2 — Create a batch launcher

Create `Silver-Tier/start_{task_name}.bat`:
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python {script_path} >> logs\{task_name}.log 2>&1
```

#### Step 3 — Register with Task Scheduler

```powershell
# Run in PowerShell as Administrator

# Example: run every 15 minutes
schtasks /create `
  /tn "AI Employee - {TaskName}" `
  /tr "E:\Hackathon-0-Personal-AI-Employee\Silver-Tier\start_{task_name}.bat" `
  /sc MINUTE /mo 15 `
  /st 00:00 `
  /ru SYSTEM

# Example: run daily at 6pm
schtasks /create `
  /tn "AI Employee - DailyReport" `
  /tr "E:\...\Silver-Tier\start_daily_report.bat" `
  /sc DAILY /st 18:00
```

#### Step 4 — Verify

```powershell
schtasks /query /tn "AI Employee - {TaskName}" /v /fo LIST
```

#### Step 5 — Log and update Dashboard

```
[{timestamp}] [SCHEDULER] Created Windows Task: AI Employee - {TaskName} | Runs: {frequency}
```

---

### Option B: Python schedule library (Built into orchestrator)

Best for: Tasks managed within the Silver orchestrator.

#### Step 1 — Open `Silver-Tier/orchestrator/orchestrator.py`

#### Step 2 — Add function
```python
def run_{task_name}():
    """Run {task description}."""
    try:
        # your code here
        logger.info("{task_name} complete")
    except Exception as e:
        logger.error(f"{task_name} failed: {e}")
```

#### Step 3 — Register in `setup_schedules()`
```python
# Common patterns:
schedule.every(15).minutes.do(run_{task_name})
schedule.every().hour.do(run_{task_name})
schedule.every().day.at("09:00").do(run_{task_name})
schedule.every().monday.at("08:00").do(run_{task_name})
```

#### Step 4 — Add to initial run (optional)
```python
def run():
    # ... existing code ...
    run_{task_name}()   # ← add this line
    setup_schedules()
```

#### Step 5 — Restart orchestrator
```
start_silver.bat
```

---

## Common Schedule Patterns

| What | Pattern | Frequency |
|------|---------|-----------|
| Gmail check | `schedule.every(15).minutes` | 15 min |
| Calendar check | `schedule.every(60).minutes` | 1 hour |
| Email sender poll | `schedule.every(5).minutes` | 5 min |
| Dashboard refresh | `schedule.every(30).minutes` | 30 min |
| LinkedIn watcher | `schedule.every(60).minutes` | 1 hour |
| Daily report | `schedule.every().day.at("18:00")` | Daily 6pm |
| Weekly briefing | `schedule.every().sunday.at("09:00")` | Sunday 9am |

---

## Verify Active Schedules

```powershell
# List all AI Employee tasks in Windows Task Scheduler
schtasks /query /fo TABLE | findstr "AI Employee"

# Check orchestrator log to see schedule setup
type Silver-Tier\orchestrator_*.log | findstr "Schedule"
```

---

## Remove a Schedule

```powershell
# Windows Task Scheduler
schtasks /delete /tn "AI Employee - {TaskName}" /f

# Python schedule — remove from setup_schedules() and restart orchestrator
```

---

**Status**: Production Ready
**Tier**: Silver
**Requirements**: Python schedule library (installed), or admin access for Task Scheduler
