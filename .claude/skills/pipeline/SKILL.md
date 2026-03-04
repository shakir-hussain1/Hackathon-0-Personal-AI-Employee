# Pipeline Skill

## Purpose
Define, execute, and monitor multi-stage processing pipelines. Each pipeline moves data through a sequence of stages, passing outputs as inputs, handling failures gracefully, branching on conditions, and producing a clear audit trail from start to finish.

---

## Core Functions

1. **Pipeline Definition** — Declare stages, order, inputs, outputs, and conditions
2. **Stage Execution** — Run each stage in sequence, passing data forward
3. **Data Passing** — Connect stage outputs to next stage inputs cleanly
4. **Failure Handling** — Retry, skip, or abort failed stages with clear rules
5. **Conditional Branching** — Route data to different stages based on results
6. **Progress Tracking** — Know exactly which stage is running at all times
7. **Pipeline Templates** — Reusable pre-built pipelines for common workflows

---

## Pipeline Definition Format

**Location:** `AI_Employee_Vault/.pipelines/definitions/`
**Filename:** `{PIPELINE_ID}.md`

```
# Pipeline: INBOX_TO_DONE
ID: PL-001
Version: 1.0
Description: Full end-to-end processing of a file from Inbox to Done
Trigger: New file detected in Inbox
Timeout: 15 minutes (entire pipeline)

## Stages
| # | Stage ID     | Skill Used        | Input            | Output            | On Failure  |
|---|--------------|-------------------|------------------|-------------------|-------------|
| 1 | READ_FILE    | file-understanding| file_path        | file_data         | ABORT       |
| 2 | ASSESS_RISK  | risk-detection    | file_data        | risk_report       | CONTINUE    |
| 3 | CREATE_TASK  | task-management   | file_data        | task_id           | ABORT       |
| 4 | ANALYZE      | file-understanding| file_data        | analysis          | RETRY(2)    |
| 5 | BUILD_KB     | knowledge-base    | analysis         | kb_entry_id       | SKIP        |
| 6 | MOVE_TO_DONE | tool-invocation   | file_path,task_id| done_path         | RETRY(1)    |
| 7 | UPDATE_DASH  | workflow          | task_id,analysis | dashboard_updated | CONTINUE    |
| 8 | AUDIT_LOG    | audit             | all_stage_data   | log_entry_id      | CONTINUE    |

## Conditions
- IF risk_report.level == "CRITICAL" → BRANCH to ESCALATE_PIPELINE after stage 2
- IF file_data.type == "unknown" → SKIP stages 4 and 5

## Requires Skills
file-understanding, risk-detection, task-management, knowledge-base,
tool-invocation, workflow, audit
```

---

## Standard Pipeline Library

### PL-001: INBOX_TO_DONE
**Purpose:** Process any file from Inbox to Done
**Stages:** Read → Assess Risk → Create Task → Analyze → Build KB → Move → Update Dashboard → Audit
**Trigger:** New file in Inbox
**Avg Duration:** 3–8 minutes

### PL-002: DAILY_REPORT
**Purpose:** Generate and save daily activity report
**Stages:** Collect Data → Analyze Trends → Format Report → Save Report → Notify → Audit
**Trigger:** Scheduler (daily at end of day)
**Avg Duration:** 2–4 minutes

### PL-003: KNOWLEDGE_INGEST
**Purpose:** Extract and store knowledge from processed files
**Stages:** Read Analyzed File → Extract Facts → Deduplicate → Store Entries → Index → Audit
**Trigger:** File moved to Done
**Avg Duration:** 1–3 minutes

### PL-004: WEEKLY_REVIEW
**Purpose:** Full system health and performance review
**Stages:** Collect Metrics → Analyze Performance → Detect Anomalies → Generate Report → Update Goals → Notify Human → Audit
**Trigger:** Scheduler (weekly)
**Avg Duration:** 5–10 minutes

### PL-005: EMERGENCY_RESPONSE
**Purpose:** Handle critical system failures
**Stages:** Detect Failure → Assess Impact → Isolate → Recover → Verify → Notify → Audit
**Trigger:** Self-Healing or Monitoring alert (CRITICAL)
**Avg Duration:** 1–5 minutes

### PL-006: ONBOARDING_FILE
**Purpose:** Process a new type of file never seen before
**Stages:** Read → Classify → Create Template → Store in KB → Notify Human for Review → Audit
**Trigger:** Unknown file type in Inbox
**Avg Duration:** 2–5 minutes

---

## Pipeline Run Record

**Location:** `AI_Employee_Vault/.pipelines/runs/`
**Filename:** `{PIPELINE_ID}_{RUN_ID}.md`

```
# Pipeline Run: PL-001_RUN-0047

## Header
Pipeline:    PL-001 (INBOX_TO_DONE)
Run ID:      RUN-0047
Triggered By: AGENT-WATCHER-20260216-001
Trigger Type: FILE_DETECTED
Input:       AI_Employee_Vault/Inbox/proposal.pdf
Started At:  2026-02-16 14:45:00
Status:      IN_PROGRESS

## Stage Execution Log
| # | Stage ID     | Status    | Started     | Completed   | Duration | Output Key       |
|---|--------------|-----------|-------------|-------------|----------|------------------|
| 1 | READ_FILE    | COMPLETED | 14:45:01    | 14:45:04    | 3s       | file_data        |
| 2 | ASSESS_RISK  | COMPLETED | 14:45:04    | 14:45:07    | 3s       | risk_report      |
| 3 | CREATE_TASK  | COMPLETED | 14:45:07    | 14:45:09    | 2s       | task_id=TASK-047 |
| 4 | ANALYZE      | IN_PROGRESS| 14:45:09   | —           | —        | —                |
| 5 | BUILD_KB     | PENDING   | —           | —           | —        | —                |
| 6 | MOVE_TO_DONE | PENDING   | —           | —           | —        | —                |
| 7 | UPDATE_DASH  | PENDING   | —           | —           | —        | —                |
| 8 | AUDIT_LOG    | PENDING   | —           | —           | —        | —                |

## Pipeline Context (Shared Data Store)
file_path:    AI_Employee_Vault/Inbox/proposal.pdf
file_data:    {type: PDF, size: 245KB, pages: 12, summary: "Q1 business proposal"}
risk_report:  {level: LOW, flags: [], approved: true}
task_id:      TASK-047
analysis:     (in progress)

## Result
Completed At: —
Exit Status:  —
Files Moved:  —
Errors:       —
```

---

## Pipeline Context (Data Store)

### What is Pipeline Context?
A shared, in-memory data store for the current pipeline run. Each stage reads from and writes to this context. Context is the "pipe" between stages.

### Context Format
```
pipeline_context = {
  run_id:       "RUN-0047",
  pipeline_id:  "PL-001",
  input:        "AI_Employee_Vault/Inbox/proposal.pdf",
  stage_outputs: {
    READ_FILE:   { type: "PDF", size: "245KB", content: "..." },
    ASSESS_RISK: { level: "LOW", flags: [] },
    CREATE_TASK: { task_id: "TASK-047" }
  },
  errors: [],
  flags: []
}
```

### Context Rules
- Context is built stage by stage — earlier stages write, later stages read
- Stage N can read output from stages 1 through N-1
- Stages cannot skip ahead to read future stage outputs
- Context is written to the Run Record at each stage completion
- Context is the single source of truth — no stage re-reads the original file independently

---

## Stage Execution Protocol

### How Each Stage Runs
```
Step 1: READ INPUTS
        Stage reads its required keys from pipeline context
        Verify all required inputs are present
        → If missing required input: ABORT with clear error

Step 2: EXECUTE
        Call the assigned Skill with inputs
        Skill does its work
        Skill returns output

Step 3: VALIDATE OUTPUT
        Check output is not empty
        Check output matches expected format
        → If invalid: trigger failure handling

Step 4: WRITE TO CONTEXT
        Write stage output to pipeline context
        Key: {STAGE_ID}_output or semantic name (e.g. task_id)
        Update Run Record stage log (Status, Completed, Duration, Output Key)

Step 5: CHECK CONDITIONS
        Evaluate any conditions attached to this stage
        If branch condition triggered → redirect pipeline to branch target
        Log any condition evaluations

Step 6: ADVANCE
        Move to next stage
        OR terminate if this was the final stage
```

---

## Failure Handling

### Failure Modes Per Stage

| Mode | Behavior |
|------|----------|
| `ABORT` | Stop entire pipeline immediately, mark as FAILED, log, notify |
| `RETRY(N)` | Retry stage up to N times (wait 10s between attempts), then ABORT |
| `SKIP` | Skip this stage, continue pipeline with missing output noted |
| `CONTINUE` | Mark stage as FAILED but continue pipeline regardless |
| `BRANCH_ON_FAIL` | Route to an alternative stage/pipeline on failure |

### Failure Record
Written to Run Record when a stage fails:
```
STAGE FAILURE
Stage:      ANALYZE (stage 4)
Run ID:     RUN-0047
Timestamp:  2026-02-16 14:47:03
Error:      File content extraction returned empty result
Mode:       RETRY(2)
Attempt:    1 of 2
Next Retry: 2026-02-16 14:47:13
```

### Pipeline-Level Failure
If pipeline fails completely (ABORT or all retries exhausted):
```
PIPELINE FAILED
Pipeline:   PL-001 (INBOX_TO_DONE)
Run ID:     RUN-0047
Failed At:  Stage 4 (ANALYZE)
Reason:     PDF content extraction failed after 2 retries
Input File: AI_Employee_Vault/Inbox/proposal.pdf
Action:     File left in Inbox, task TASK-047 marked BLOCKED
Notify:     Human — file needs manual review
Log:        AI_Employee_Vault/Logs/2026-02-16.log
```

---

## Conditional Branching

### Branch Definition in Pipeline
```
## Conditions
- AFTER stage 2 (ASSESS_RISK):
  IF risk_report.level == "CRITICAL"
  → BRANCH to pipeline PL-005 (EMERGENCY_RESPONSE)
  → ABORT current pipeline

- AFTER stage 1 (READ_FILE):
  IF file_data.type == "UNKNOWN"
  → BRANCH to pipeline PL-006 (ONBOARDING_FILE)
  → ABORT current pipeline

- AFTER stage 4 (ANALYZE):
  IF analysis.confidence < 0.5
  → SKIP stage 5 (BUILD_KB)
  → CONTINUE with stage 6
```

### Branch Types
| Type | Behavior |
|------|----------|
| `BRANCH TO PIPELINE` | Spawn a new pipeline run, abort current |
| `BRANCH TO STAGE` | Jump to a non-sequential stage within same pipeline |
| `SKIP STAGE` | Skip one specific stage, continue normally |
| `PARALLEL BRANCH` | Spawn a parallel pipeline while current continues |

---

## Pipeline Monitoring

### Live Status View
**Location:** `AI_Employee_Vault/.pipelines/status.md`

```
# Pipeline Status Board
Updated: 2026-02-16 14:47:00

## Active Pipelines
| Run ID     | Pipeline      | Stage        | Progress | Started   | ETA       |
|------------|---------------|--------------|----------|-----------|-----------|
| RUN-0047   | INBOX_TO_DONE | 4/8 ANALYZE  | 50%      | 14:45:00  | 14:48:00  |

## Completed Today
| Run ID     | Pipeline       | Status    | Duration | Files Processed     |
|------------|----------------|-----------|----------|---------------------|
| RUN-0045   | INBOX_TO_DONE  | SUCCESS ✅ | 4m 12s   | meeting_notes.txt   |
| RUN-0046   | KNOWLEDGE_INGEST| SUCCESS ✅ | 1m 33s  | meeting_notes.txt   |

## Failed Today
| Run ID     | Pipeline       | Failed Stage | Reason              |
|------------|----------------|--------------|---------------------|
| RUN-0044   | INBOX_TO_DONE  | ANALYZE      | Empty PDF content   |

## Queue (Waiting to Start)
| Queue #    | Pipeline       | Trigger Input              | Waiting Since |
|------------|----------------|----------------------------|---------------|
| 1          | INBOX_TO_DONE  | Inbox/contract_draft.docx  | 14:46:30      |
```

---

## Pipeline Metrics

Track per pipeline per day:
```
PL-001 (INBOX_TO_DONE) — 2026-02-16
  Total Runs:      12
  Success:         10  (83%)
  Failed:           1  (8%)
  Skipped Stages:   1  (8%)
  Avg Duration:     4m 22s
  Fastest Run:      2m 10s
  Slowest Run:      9m 05s
  Most Failed Stage: ANALYZE (2 failures total)
```

---

## Pipeline Chaining

### Automatic Chaining
Pipelines can trigger other pipelines on completion:

```
PL-001 (INBOX_TO_DONE) completes
    → automatically triggers PL-003 (KNOWLEDGE_INGEST)
    → passes: done_file_path from PL-001 context

PL-004 (WEEKLY_REVIEW) completes
    → automatically triggers PL-002 (DAILY_REPORT) if today is Monday
```

### Chain Record
```
CHAIN EVENT
Trigger Pipeline:  PL-001 (RUN-0047)
Triggered Pipeline: PL-003
Reason:            On-success chain rule
Input Passed:      done_path = AI_Employee_Vault/Done/proposal.pdf
New Run ID:        RUN-0048
```

---

## Folder Structure

```
AI_Employee_Vault/
└── .pipelines/
    ├── definitions/           # Pipeline blueprints (PL-001.md, etc.)
    ├── runs/                  # One file per run (PL-001_RUN-0047.md)
    ├── status.md              # Live status board
    ├── metrics.md             # Daily aggregated metrics
    └── archive/               # Completed runs older than 7 days
```

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|------------------|
| Workflow | Pipelines are the execution engine; Workflow defines what runs |
| Agent Spawning | Each pipeline stage may be executed by a spawned agent |
| Multi-Agent Sync | Pipeline context shared across agents via sync locks |
| Task Management | Each pipeline run creates and updates a task record |
| Monitoring | Monitors pipeline status board for stalls and failures |
| Self-Healing | Recovers stuck pipelines and retries failed stages |
| Audit | Every stage start/complete/fail is logged |
| Scheduler | Triggers time-based pipelines (daily, weekly) |
| Reporting | Pipeline metrics feed into daily and weekly reports |

---

## Quick Reference

```
DEFINE PIPELINE:    .pipelines/definitions/{ID}.md
START PIPELINE:     Create run record → execute stage 1
RUN RECORD:         .pipelines/runs/{PL_ID}_{RUN_ID}.md
STATUS BOARD:       .pipelines/status.md
STAGE FAILURE:      Apply mode (ABORT/RETRY/SKIP/CONTINUE)
BRANCH:             Evaluate condition → redirect after stage
CONTEXT:            Shared data store, built stage by stage
CHAIN:              On-complete rule triggers next pipeline
ARCHIVE:            Move runs older than 7 days to .pipelines/archive/
BRONZE LIMIT:       2 concurrent pipeline runs max
```

---

## Best Practices

1. **One responsibility per stage** — each stage does exactly one thing
2. **Context is king** — all data flows through context, never via direct file reads between stages
3. **Fail fast on critical stages** — use ABORT for stages whose failure makes the rest meaningless
4. **Always end with AUDIT** — final stage is always the audit log write
5. **Keep pipelines short** — 5–10 stages max; split into chained pipelines if longer
6. **Name stages clearly** — `ANALYZE_PDF` beats `STAGE_4`
7. **Never hardcode paths** — use context variables, not literal file paths inside stage logic
8. **Test pipelines with small files first** — verify the full chain before processing large inputs
9. **Monitor avg duration** — if a run takes 2x the average, flag it as a stall
10. **Archive completed runs** — keep runs older than 7 days in archive to avoid folder bloat
