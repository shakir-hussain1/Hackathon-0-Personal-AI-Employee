# Version Control Skill

**Purpose**: Track changes to vault files, enable rollback, maintain history, and prevent data loss
**Storage**: Markdown-based change logs, snapshots, diff records, rollback points
**Scope**: Vault file versioning, change tracking, rollback, conflict detection, backup, history search

---

## Core Functions

### 1. Track Changes
Record what changed, when, who changed it, and why

### 2. Snapshot
Create point-in-time copies of critical files before changes

### 3. Diff
Show exactly what is different between two versions

### 4. Rollback
Restore a file or set of files to any previous state

### 5. Protect Critical Files
Prevent accidental overwrites on key vault files

### 6. Search History
Find when and why something changed in the past

---

## What Gets Versioned

### Always Version (Critical Files)
```
Common/AI_Employee_Vault/Dashboard.md
Common/AI_Employee_Vault/Company_Handbook.md
Common/AI_Employee_Vault/Plans/schedule.md
Common/AI_Employee_Vault/Plans/integrations.md
Common/AI_Employee_Vault/Knowledge/facts/policies.md
Common/AI_Employee_Vault/Knowledge/lessons/active_rules.md
Common/AI_Employee_Vault/Knowledge/people/contacts.md

Why: These files drive AI behavior — corruption or wrong
     change has immediate system-wide impact
Snapshot: Before every write (automatic)
History:  Keep all versions indefinitely
```

### Version on Change (Important Files)
```
All files in Knowledge/
All files in Plans/workflows/definitions/
All files in Plans/collaboration/active/
All files in Plans/reports/ (final versions)
Company_Handbook.md updates

Why: Important reference data, wrong change affects decisions
Snapshot: Before every write
History:  Keep last 20 versions, older → compress to summary
```

### Log Only (Operational Files)
```
All files in Logs/
All files in Needs_Action/ (task files)
All files in Done/ (completed tasks)
Plans/task_queue.md

Why: High churn, low criticality — full versioning wasteful
Action:  Log changes in change_log.md (no snapshot)
History: 30-day log retention, then summary only
```

### Do Not Version (Volatile Files)
```
Logs/metrics.md          → Updated every 60s (too frequent)
Logs/health.md           → Updated every 60s (too frequent)
Logs/*.log               → Append-only (no versioning needed)
Plans/task_queue.md      → High-frequency updates (log only)

Why: Too much churn to version, and rollback not meaningful
```

---

## Version Storage Structure

```
Common/AI_Employee_Vault/.versions/
│
├── snapshots/                     # Full file copies at point in time
│   ├── Dashboard/
│   │   ├── Dashboard_v001_20260216_0900.md
│   │   ├── Dashboard_v002_20260216_1430.md
│   │   └── Dashboard_v003_20260216_1600.md
│   ├── Company_Handbook/
│   │   ├── Company_Handbook_v001_20260101.md
│   │   └── Company_Handbook_v002_20260216.md
│   ├── schedule/
│   └── active_rules/
│
├── diffs/                         # Compact change records
│   ├── Dashboard_diff_log.md
│   ├── Company_Handbook_diff_log.md
│   └── active_rules_diff_log.md
│
├── rollback_points/               # Named restore points
│   ├── RP_20260216_before_cleanup.md
│   ├── RP_20260215_stable_state.md
│   └── index.md
│
└── change_log.md                  # Master change log (all files)
```

---

## Snapshot Format

### File Snapshot
```
Naming convention:
  {filename}_v{version_padded}_{YYYYMMDD}_{HHMM}.{ext}
  Example: Dashboard_v007_20260216_1430.md

Snapshot header (prepended to each snapshot):
─────────────────────────────────────────────
SNAPSHOT: Dashboard.md
Version:  v007
Captured: 2026-02-16 14:30:00
Reason:   Pre-write (Optimization Skill cleanup)
Changed by: optimization-skill
Hash:     sha256:a3f8c2...
Size:     4,821 bytes
─────────────────────────────────────────────
[original file content below]
```

### Snapshot Index
```
Location: .versions/snapshots/{filename}/index.md

Format:
# Snapshot Index: Dashboard.md

| Version | Timestamp           | Reason                        | Size    | Hash     |
|---------|---------------------|-------------------------------|---------|----------|
| v001    | 2026-02-16 09:00    | Initial creation              | 3.2 KB  | a1b2c3.. |
| v002    | 2026-02-16 11:30    | Post-processing update        | 3.8 KB  | d4e5f6.. |
| v003    | 2026-02-16 14:00    | Weekly briefing added         | 4.1 KB  | g7h8i9.. |
| v004    | 2026-02-16 14:30    | Emergency cleanup update      | 4.8 KB  | a3f8c2.. |

Latest: v004 (2026-02-16 14:30)
Oldest: v001 (2026-02-16 09:00)
Total snapshots: 4
Storage used: 15.9 KB
```

---

## Change Tracking

### Change Log Format

```
Location: .versions/change_log.md

# Master Change Log

**Updated**: 2026-02-16 14:30
**Total Changes Today**: 28
**Total Changes This Week**: 147

---

## 2026-02-16

### 14:30 — Dashboard.md
- **Change type**: UPDATE
- **Changed by**: optimization-skill
- **Reason**: Post-cleanup metrics refresh
- **Fields changed**: Disk usage (66% → 54%), Last updated timestamp
- **Snapshot**: Dashboard_v004_20260216_1430.md
- **Rollback available**: YES

### 14:00 — active_rules.md
- **Change type**: APPEND
- **Changed by**: learning-skill
- **Reason**: RULE-007 activated (Alice HIGH priority)
- **Fields changed**: Added RULE-007 entry (8 lines)
- **Snapshot**: active_rules_v003_20260216_1400.md
- **Rollback available**: YES

### 13:45 — Company_Handbook.md
- **Change type**: UPDATE
- **Changed by**: Human
- **Reason**: Updated email tone preference
- **Fields changed**: Communication section, line 87
- **Snapshot**: Company_Handbook_v002_20260216_1345.md
- **Rollback available**: YES

### 09:15 — FILE_014.md (Needs_Action/)
- **Change type**: CREATE
- **Changed by**: file-understanding
- **Reason**: New task from report_q1.pdf
- **Log only** (no snapshot — operational file)
```

---

## Diff Records

### Diff Format

```
Location: .versions/diffs/Dashboard_diff_log.md

# Diff Log: Dashboard.md

---

## v003 → v004 (2026-02-16 14:00 → 14:30)

Changed by: optimization-skill
Reason: Post-cleanup update

CHANGED:
  Line 12: | Disk Vault | 66% | 75% | GREEN |
  →         | Disk Vault | 54% | 75% | GREEN |

  Line 24: **Updated**: 2026-02-16 14:00
  →         **Updated**: 2026-02-16 14:30

  Line 31: Active Cleanup: NO
  →         Active Cleanup: COMPLETE (ran 14:28-14:30)

ADDED:
  Lines 45-48: Cleanup summary section (new)
    > Cleanup ran: freed 12 MB
    > Files archived: 34 Done/ tasks
    > Next cleanup: scheduled 2026-03-01

REMOVED:
  Nothing removed

Summary: 3 lines changed, 4 lines added, 0 lines removed
```

---

## Rollback System

### Rollback Types

#### Type 1: Single File Rollback
```
Purpose: Restore one file to a previous version

When to use:
  - File was accidentally corrupted
  - Wrong change was made to a specific file
  - Human wants to undo AI's last edit to a file

Process:
  1. List available versions for the file
  2. Human (or AI with approval) selects target version
  3. Current file → saved as emergency snapshot
  4. Target version → copied to file location
  5. Log rollback event in change_log.md
  6. Notify human of successful rollback

Command format (Dashboard instruction):
  "Rollback Dashboard.md to version v002 (2026-02-16 11:30)"
```

#### Type 2: Rollback Point Restore
```
Purpose: Restore multiple related files to a named safe state

When to use:
  - A system-wide change went wrong
  - Multiple files need to be restored together
  - After a bad batch update affected many files

Named rollback points:
  RP_before_major_change_YYYYMMDD
  RP_stable_state_YYYYMMDD
  RP_pre_rule_activation_YYYYMMDD

Process:
  1. Read rollback_point/index.md
  2. Identify target rollback point
  3. List all files included in that point
  4. Require human approval (high impact operation)
  5. Create emergency snapshot of all current files first
  6. Restore all files from rollback point
  7. Log each file restored
  8. Notify human with full restoration summary
```

#### Type 3: Field-Level Rollback
```
Purpose: Undo a specific field change without reverting whole file

When to use:
  - Task priority was changed incorrectly — restore priority only
  - One section of Company_Handbook was wrongly updated
  - A single rule was activated and needs to be deactivated

Process:
  1. Read diff log to find the specific change
  2. Extract the original value from diff
  3. Apply only that field back to current file
  4. Log as partial rollback
  5. Re-snapshot the file after field restoration

Safer than full file rollback (preserves other valid changes)
```

---

## Rollback Point Management

### Creating a Rollback Point

```
Create rollback point BEFORE:
  - Any major rule activation
  - Running emergency cleanup
  - Modifying Company_Handbook.md
  - Updating schedule with many changes
  - Any operation touching > 5 files at once
  - Upgrading to a new tier

Format:
  1. Identify files to include (usually: critical files list)
  2. Snapshot each file to rollback_points/{name}/
  3. Write index file with file list, timestamps, hashes
  4. Log rollback point creation in change_log.md

Rollback point index format:
  # Rollback Point: RP_20260216_pre_cleanup

  **Created**: 2026-02-16 14:28
  **Reason**: Before emergency disk cleanup
  **Created by**: optimization-skill

  ## Files Included
  | File                   | Version | Hash      | Size   |
  |------------------------|---------|-----------|--------|
  | Dashboard.md           | v003    | g7h8i9..  | 4.1 KB |
  | active_rules.md        | v002    | j1k2l3..  | 2.8 KB |
  | schedule.md            | v005    | m4n5o6..  | 3.5 KB |
  | Company_Handbook.md    | v002    | p7q8r9..  | 18.2 KB|
```

### Rollback Point Retention

```
Keep rollback points:
  Last 7 days: ALL rollback points
  7-30 days:   One per day (daily best state)
  30-90 days:  One per week (weekly best state)
  90+ days:    One per month (monthly summary only)

Auto-cleanup:
  Run weekly — remove excess rollback points per above schedule
  Never remove the "last known good" point (always keep 1 recent)
  Never remove rollback points created by human explicitly
```

---

## Conflict Detection

### Conflict Scenarios

#### Scenario 1: Concurrent Write Conflict
```
Detection: Two writes to same file within same minute
  AI wrote Dashboard.md at 14:30:05
  Human wrote Dashboard.md at 14:30:08

Response:
  1. Read both versions
  2. Generate diff between them
  3. Merge: preserve both sets of changes where possible
  4. Flag conflicting lines (same line changed differently)
  5. Write merged version with conflict markers
  6. Notify human of conflict and resolution

Conflict marker format:
  <<<<<<< AI version (14:30:05)
  | Disk Vault | 54% | GREEN |
  ======= Human version (14:30:08)
  | Disk Vault | 55% | GREEN |
  >>>>>>> Merged: AI version used (human's change was similar)
```

#### Scenario 2: Stale Read Conflict
```
Detection: File was read, then changed, then written back with old data

Prevention:
  Before every write:
    1. Read current file hash
    2. Compare to hash at time of last read
    3. IF hash changed → stale read detected → abort write
    4. Re-read latest version, re-apply changes, retry write

Response on detection:
  Log: "[VC] Stale read prevented on Dashboard.md"
  Action: Re-read + re-apply (transparent to human)
```

#### Scenario 3: Rule Conflict
```
Detection: New rule in active_rules.md contradicts existing rule

Example:
  RULE-001: Alice → HIGH priority
  RULE-012: Files from company.com domain → MEDIUM priority
  (Alice's email ends in @company.com → contradiction)

Response:
  1. Flag conflict in active_rules.md
  2. Apply more specific rule (RULE-001 wins — entity > domain)
  3. Notify Learning Skill of conflict
  4. Log conflict and resolution for human review
  5. Propose rule clarification if ambiguous
```

---

## Hash-Based Integrity

### File Integrity Checking

```
For every critical file, maintain hash record:

Location: .versions/hashes.md

# File Integrity Hashes

**Updated**: 2026-02-16 14:30

| File                    | Last Hash    | Last Verified       | Status  |
|-------------------------|--------------|---------------------|---------|
| Dashboard.md            | a3f8c2...    | 2026-02-16 14:30    | OK      |
| Company_Handbook.md     | p7q8r9...    | 2026-02-16 14:30    | OK      |
| active_rules.md         | j1k2l3...    | 2026-02-16 14:30    | OK      |
| schedule.md             | m4n5o6...    | 2026-02-16 14:30    | OK      |

Verification interval: Every 5 minutes
On mismatch: Alert Security Skill (possible tampering)
```

### Hash Verification Process

```
Every 5 minutes:
  1. Read each critical file
  2. Calculate current hash
  3. Compare to stored hash in hashes.md
  4. IF match → update "Last Verified" timestamp
  5. IF mismatch:
     a. Check change_log.md for expected change
     b. IF change was logged by AI → update stored hash (expected)
     c. IF no corresponding log entry → ALERT SECURITY SKILL
     d. Log: "[VC] Hash mismatch on Dashboard.md — unexpected change"
```

---

## History Search

### How to Search Version History

```
Search by date:
  "Show all changes to active_rules.md in February"
  → Scan change_log.md filtered by file + date range
  → List all change entries with timestamps

Search by actor:
  "Show all changes made by human this week"
  → Scan change_log.md filtered by changed_by = Human
  → List files, timestamps, change types

Search by change type:
  "Show all rules that were added or removed"
  → Scan diffs/active_rules_diff_log.md
  → List all ADDED/REMOVED entries

Search by content:
  "When was Alice's priority rule first added?"
  → Full text search across all diff logs
  → Find first occurrence of "alice" + "HIGH" + "RULE"

Search by rollback point:
  "What was the state of the vault on Feb 10?"
  → Find rollback point nearest to Feb 10
  → List all file versions in that point
```

### History Query Results Format

```
# History Query Results

**Query**: Changes to active_rules.md in February 2026
**Results**: 6 changes found

---

| # | Date              | Changed by     | Type   | Summary                        |
|---|-------------------|----------------|--------|--------------------------------|
| 1 | Feb 02 10:00      | learning-skill | APPEND | Added RULE-001 (Alice HIGH)    |
| 2 | Feb 05 14:00      | learning-skill | APPEND | Added RULE-002 (Acme invoice)  |
| 3 | Feb 10 09:00      | Human          | UPDATE | Modified RULE-002 condition    |
| 4 | Feb 12 11:00      | learning-skill | APPEND | Added RULE-003 (Bob Friday)    |
| 5 | Feb 15 16:00      | learning-skill | REMOVE | Retired RULE-004 (stale)       |
| 6 | Feb 16 14:00      | learning-skill | APPEND | Added RULE-007 (Alice)         |

**To view diff for any entry**: Check .versions/diffs/active_rules_diff_log.md
**To rollback to entry #3 state**: Rollback active_rules.md to v003
```

---

## Backup Strategy

### Backup Levels

```
Level 1: In-vault snapshots (real-time)
  What:    Critical file snapshots before every write
  Where:   .versions/snapshots/
  When:    Before every write to versioned files
  Cost:    Low (markdown files are small)
  Restore: Instant (files in vault)

Level 2: Daily vault backup (Bronze)
  What:    Full copy of entire vault
  Where:   .versions/daily_backups/vault_YYYYMMDD.zip
  When:    Daily at 02:00 (low activity)
  Retain:  Last 7 days
  Restore: Minutes (extract zip)

Level 3: Weekly vault backup (Silver+)
  What:    Full copy synced to cloud
  Where:   Cloud storage (Platinum tier)
  When:    Weekly on Sunday
  Retain:  Last 4 weeks
  Restore: Requires network + cloud access
```

### Daily Backup Process

```
Daily at 02:00:
  1. Create rollback point (snapshot all critical files)
  2. Compress vault to .zip (exclude .versions/ to avoid recursion)
  3. Save to .versions/daily_backups/vault_{YYYYMMDD}.zip
  4. Verify backup (test zip integrity)
  5. Delete oldest backup if > 7 days retained
  6. Log: "[VC] Daily backup created: vault_{YYYYMMDD}.zip ({size})"
  7. Update hashes.md with fresh verification
```

---

## Version Control Metrics

### Track Weekly

```
Snapshots created:              {n}
Rollbacks performed:            {n}
Conflicts detected:             {n}
Conflicts resolved automatically:{n}
Conflicts needing human:         {n}
Hash mismatches (unexpected):    {n}
Backup success rate:             {%}
Storage used by .versions/:      {MB}
Oldest snapshot retained:        {date}
```

---

## Integration with Other Skills

### With Security Skill
```
version-control → alerts → security when:
  Hash mismatch detected (unexpected file change)
  Rollback point altered without logged reason
  Critical file changed without AI action log
  .versions/ folder accessed or modified unexpectedly
```

### With Self-Healing Skill
```
self-healing → uses → version-control for:
  Restoring Dashboard.md from snapshot after corruption
  Rolling back bad rule activation after failure
  Providing file state at time of crash for diagnosis
  Creating rollback point before every recovery attempt
```

### With Learning Skill
```
version-control → protects → learning outputs:
  Snapshot active_rules.md before every rule activation
  Provide rollback if newly activated rule causes problems
  Track history of rule changes over time
```

### With Workflow Skill
```
workflow → uses → version-control for:
  Create rollback point at start of multi-step workflows
  Use rollback during workflow failure (undo completed steps)
  Track which workflow step caused which file change
```

### With Audit Skill
```
version-control → feeds → audit:
  Change log entries (who changed what and when)
  Rollback events (what needed to be undone)
  Hash verification results (integrity status)
  Backup success/failure history
```

### With Monitoring Skill
```
monitoring → watches → version-control for:
  .versions/ folder growing too large (storage alert)
  Daily backup not created (missed backup alert)
  Hash mismatch count (tampering signal)
  Snapshot frequency abnormal (too many writes = instability)
```

### With Collaboration Skill
```
version-control → supports → collaboration:
  Detect concurrent edits (human + AI same time)
  Provide merge capability for collaborative files
  Show human what AI changed in shared files
  Rollback human's accidental overwrites
```

---

## Best Practices

### DO
```
- Snapshot before every write to critical files (automatic)
- Create named rollback points before major operations
- Log every change with actor, reason, and timestamp
- Verify hashes on schedule (integrity checks)
- Keep rollback points rotated (7 days all, then thin out)
- Test rollback occasionally (ensure it actually works)
- Search history before diagnosing a problem (check what changed)
- Back up daily (even if everything seems fine)
```

### DON'T
```
- Version high-churn operational files (logs, metrics)
- Store .versions/ inside git (can expose sensitive data)
- Delete snapshots without updating the index
- Skip creating rollback points for "quick" changes
- Perform multi-file rollback without human approval
- Let .versions/ grow without pruning (storage impact)
- Assume hash match means no change (check actor + reason too)
- Rollback without creating an emergency snapshot first
```

---

## Quick Reference: Operation → Version Control Action

```
Operation                       | VC Action                        | Approval Needed?
--------------------------------|----------------------------------|----------------
Write to Dashboard.md           | Auto-snapshot before write       | No
Write to Company_Handbook.md    | Auto-snapshot + log              | No (log only)
Activate new learning rule      | Rollback point + snapshot        | No
Run emergency cleanup           | Rollback point (multi-file)      | No (auto)
Modify schedule.md              | Auto-snapshot                    | No
Delete a task file              | Log only (operational)           | No
Rollback single file            | Emergency snapshot first         | YES (human)
Rollback point restore          | Emergency snapshot of all first  | YES (human)
Detect hash mismatch            | Alert security + log             | No (auto)
Daily backup                    | Full vault zip                   | No (scheduled)
```

---

**Status**: Production Ready
**Priority**: HIGH (Data safety foundation for all operations)
**Critical Files**: Always versioned (unlimited history)
**Important Files**: Last 20 versions (older compressed)
**Operational Files**: Logged only (no snapshot)
**Backup**: Daily (last 7 days), Weekly (cloud — Silver+)
**Rollback**: Single file, field-level, or named rollback point
**Integrity**: Hash verification every 5 minutes on critical files

*Good version control = Nothing is ever truly lost — every mistake can be undone*
