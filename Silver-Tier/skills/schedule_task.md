# Agent Skill: Schedule Task

## Purpose
Create scheduled recurring tasks using Windows Task Scheduler or Python schedule library.

## When to Use
- User requests automated recurring processing
- Setting up daily/weekly reports
- Configuring regular Gmail checks
- Scheduling any repeating AI action

## Steps

### Option A: Windows Task Scheduler (Recommended for production)
1. **Identify task:** What runs, when, how often
2. **Create batch launcher:** Silver-Tier/start_{task_name}.bat
3. **Register with Task Scheduler:**
   ```
   schtasks /create /tn "AI Employee - {task_name}" /tr "path\to\script.bat" /sc {frequency} /st {time}
   ```
4. **Verify:** Check Task Scheduler GUI or run:
   ```
   schtasks /query /tn "AI Employee - {task_name}"
   ```
5. **Log:** Record scheduled task in Dashboard

### Option B: Python schedule library (Built into orchestrator)
1. **Add to orchestrator.py** under setup_schedules():
   ```python
   schedule.every({N}).{unit}.do({function})
   ```
2. **Ensure orchestrator is running** (via Task Scheduler or manually)

## Common Schedules
- Gmail check: every 15 minutes
- Calendar check: every 60 minutes
- Email sender poll: every 5 minutes
- Daily report: 18:00 daily
- Weekly review: Sunday 09:00
- Dashboard refresh: every 30 minutes

## Output
- Task Scheduler entry (Option A) OR updated orchestrator.py (Option B)
- Log entry confirming schedule created
- Dashboard update: "Scheduled: {task_name} at {schedule}"
