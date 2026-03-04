# Agent Skill: Create Plan (Reasoning Loop)

## Purpose
Analyze pending tasks in `Needs_Action/` and create structured `Plan_*.md` files in `Plans/` using Claude's reasoning. This is the Silver-Tier autonomous reasoning loop.

## When to Use
- New task files appear in `Needs_Action/` with no corresponding Plan
- User asks "what should we do about X?"
- Orchestrator triggers the reasoning loop on schedule

## Automated Trigger
The orchestrator runs `reasoning_loop.run_reasoning_loop()` every 30 minutes automatically if `ANTHROPIC_API_KEY` is set in `.env`.

## Manual Workflow

### Step 1 — List pending tasks
```
List all .md files in Needs_Action/ that do NOT have a corresponding Plan_*.md in Plans/
```

### Step 2 — For each unplanned task, read it
Read the full task file content.

### Step 3 — Reason through the task
For every task, think through:
1. **What exactly happened or is being requested?**
2. **What are the key facts, priorities, and constraints?**
3. **What ordered actions should be taken?** (be specific, refer to names/dates/numbers)
4. **Who needs to be involved or notified?**
5. **What is the single most important next step RIGHT NOW?**

### Step 4 — Write the Plan file
Create `Plans/Plan_{task_stem}_{YYYYMMDD_HHMMSS}.md` with this structure:

```markdown
# Plan: {task name}
Generated: {timestamp}
Source Task: {task filename}

---

## Summary
{1-2 sentence summary of what the task requires}

## Key Facts
- {fact 1}
- {fact 2}
- {fact 3}

## Action Plan
1. {First action — specific, actionable}
2. {Second action}
3. {Third action}
...

## Immediate Next Step
{The ONE thing that should happen right now, and who should do it}

## Estimated Effort
{Low / Medium / High} — {one sentence justification}
```

### Step 5 — Log and update
- Log plan creation to `Logs/YYYY-MM-DD.log`
- Optionally update the source task file: add a "Plan:" reference line

## Configuration
Set in `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
REASONING_MODEL=claude-opus-4-6    # or claude-sonnet-4-5-20250929
```

The automated loop uses these values. If `ANTHROPIC_API_KEY` is not set, the loop skips silently and logs a warning — it will not crash the orchestrator.
