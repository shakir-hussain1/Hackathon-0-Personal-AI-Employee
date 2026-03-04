---
name: create-plan
description: |
  Analyze pending tasks in Needs_Action/ and create structured Plan_*.md files in Plans/.
  This is the Silver-Tier autonomous reasoning loop — it reads task files, reasons through them,
  and writes actionable plans. Use when new tasks need planning or user says "plan this task".
---

# Create Plan Skill (Reasoning Loop)

**Purpose**: Turn raw task files into structured, actionable Plan_*.md files
**Tier**: Silver
**Input**: `*.md` task files in `Needs_Action/`
**Output**: `Plans/Plan_{task}_{timestamp}.md` with full action plan

---

## When to Use

- New task files appear in `Needs_Action/` with no corresponding Plan
- User says "plan this", "what should we do about X?", "analyze this task"
- Manually triggering the reasoning loop
- Orchestrator schedules this every 30 minutes automatically (if `ANTHROPIC_API_KEY` is set)

---

## Automated Trigger

The orchestrator runs `reasoning_loop.run_reasoning_loop()` every 30 minutes if `ANTHROPIC_API_KEY` is configured in `.env`.

To enable:
```
# Silver-Tier/.env
ANTHROPIC_API_KEY=sk-ant-your-key-here
REASONING_MODEL=claude-opus-4-6
```

---

## Manual Workflow

### Step 1 — Find Unplanned Tasks

List all `.md` files in `Needs_Action/` that do NOT have a corresponding `Plans/Plan_{stem}_*.md`.

Skip task files that already have plans (idempotent — safe to run repeatedly).

### Step 2 — Read the Task

For each unplanned task, read the full file content including:
- Priority and status
- What was detected or requested
- Source file or email content
- Any notes or context

### Step 3 — Reason Through the Task

For every task, think through:
1. **What exactly happened or is being requested?** (state facts, not assumptions)
2. **What are the key facts, priorities, and constraints?** (dates, amounts, people)
3. **What ordered actions should be taken?** (be specific — refer to file names, people, deadlines)
4. **Who needs to be involved or notified?** (human, client, external party?)
5. **What is the single most important next step RIGHT NOW?**

### Step 4 — Write the Plan File

Create `Plans/Plan_{task_stem}_{YYYYMMDD_HHMMSS}.md`:

```markdown
# Plan: {task name}
Generated: {timestamp}
Source Task: {task filename}

---

## Summary
{1-2 sentence plain-language description of what this task requires}

## Key Facts
- {fact 1 — specific, verifiable}
- {fact 2}
- {fact 3}

## Action Plan
1. {First action — specific and actionable}
2. {Second action}
3. {Third action}
...

## Immediate Next Step
{The ONE thing that should happen right now, and who should do it}

## Estimated Effort
{Low / Medium / High} — {one sentence justification}
```

### Step 5 — Log and Update

Add to `Logs/YYYY-MM-DD.log`:
```
[{timestamp}] [REASONING_LOOP] Plan created: Plan_{task_stem}_{timestamp}.md | Source: {task_file}
```

Optionally update the source task file with a reference:
```markdown
**Plan**: Plans/Plan_{stem}_{timestamp}.md
```

---

## Plan Quality Rules

```
DO:
  - Write specific, actionable steps (not "investigate" but "read file X and check Y")
  - Include file paths, names, deadlines from the task
  - State the immediate next step clearly
  - Keep Summary to 1-2 sentences
  - Use ordered list for Action Plan (1, 2, 3...)

DON'T:
  - Write vague steps ("figure out the situation")
  - Repeat information already in the task
  - Create plans for tasks that already have plans
  - Include speculative information not in the task
```

---

## Example Plan

```markdown
# Plan: EMAIL_invoice_from_alice_20260219
Generated: 2026-02-19 14:30:00
Source Task: EMAIL_invoice_from_alice_20260219_143000.md

---

## Summary
Alice from Acme Corp sent an invoice for $2,400 for services rendered in January.
Action required: verify amount, draft acknowledgment reply, and flag for payment.

## Key Facts
- Invoice amount: $2,400
- Due date: 2026-03-01
- Sender: alice@acmecorp.com
- Service period: January 2026

## Action Plan
1. Cross-reference $2,400 against service agreement in Done/Contracts/acme_sla.md
2. Draft acknowledgment email using draft-reply skill
3. Add payment reminder to Plans/payments/march_2026.md (create if missing)
4. Move EMAIL task to Done/Communications/ after reply is drafted

## Immediate Next Step
Draft the acknowledgment reply — human should review and approve before March 1

## Estimated Effort
Low — straightforward acknowledgment, no dispute indicated
```

---

## Configuration

```env
# Silver-Tier/.env
ANTHROPIC_API_KEY=sk-ant-...
REASONING_MODEL=claude-opus-4-6    # or claude-sonnet-4-6, claude-haiku-4-5-20251001
```

The automated loop skips silently (logs a warning) if `ANTHROPIC_API_KEY` is not set — it will not crash the orchestrator.

---

**Status**: Production Ready
**Tier**: Silver
**Depends on**: `Silver-Tier/orchestrator/reasoning_loop.py`, `ANTHROPIC_API_KEY`
**Runs**: Every 30 min automatically, or manually via this skill
