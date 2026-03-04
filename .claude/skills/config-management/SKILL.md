# Config Management Skill

## Purpose
Store, validate, load, and update all configuration values that control how the AI Employee behaves. Provide a single source of truth for every setting — from watcher intervals to resource limits to tier-specific features — so no value is ever hardcoded in a skill or agent.

---

## Core Functions

1. **Config Storage** — Keep all settings in structured, human-readable files
2. **Config Loading** — Provide correct values to any skill or agent on demand
3. **Config Validation** — Reject bad values before they cause runtime failures
4. **Secret References** — Point to credentials without storing them in plaintext
5. **Tier Overrides** — Apply Bronze/Silver/Gold/Platinum-specific settings
6. **Change Tracking** — Log every config change with who changed it and why
7. **Hot Reload** — Apply non-critical config changes without full restart

---

## Config Hierarchy

Settings are resolved in this order (highest wins):

```
1. EMERGENCY overrides     (active only during Emergency mode)
2. Session overrides       (set at runtime, not persisted)
3. Tier config             (Bronze / Silver / Gold / Platinum)
4. Environment config      (local / cloud)
5. Base config             (defaults, always present)
```

If a setting is not found at any level → use the hardcoded fallback default.

---

## Config File Structure

```
AI_Employee_Vault/.config/
├── base.md              # Default values for all settings
├── bronze.md            # Bronze-tier overrides
├── silver.md            # Silver-tier overrides
├── gold.md              # Gold-tier overrides
├── platinum.md          # Platinum-tier overrides
├── local.md             # Machine-specific overrides (not committed)
├── secrets.md           # Secret references only (NO plaintext values)
├── session.md           # Runtime overrides (reset each session)
└── change_log.md        # History of all config changes
```

---

## Base Config (`base.md`)

```
# Base Configuration
Version: 1.0
Last Updated: 2026-02-16
Updated By: human

## Watcher Settings
watcher.check_interval_seconds: 30
watcher.max_file_size_mb: 50
watcher.supported_extensions: [.txt, .pdf, .docx, .xlsx, .csv, .md, .png, .jpg]
watcher.ignore_patterns: [.tmp, .lock, ~$*, .DS_Store]
watcher.inbox_path: AI_Employee_Vault/Inbox
watcher.done_path: AI_Employee_Vault/Done
watcher.needs_action_path: AI_Employee_Vault/Needs_Action

## Agent Settings
agent.max_concurrent: 3
agent.heartbeat_interval_seconds: 60
agent.heartbeat_timeout_seconds: 180
agent.max_task_runtime_minutes: 10
agent.max_spawn_depth: 3

## Pipeline Settings
pipeline.max_concurrent_runs: 2
pipeline.default_timeout_minutes: 15
pipeline.stage_retry_count: 2
pipeline.stage_retry_delay_seconds: 10

## Scheduler Settings
scheduler.daily_report_time: "18:00"
scheduler.weekly_review_day: "Sunday"
scheduler.weekly_review_time: "09:00"
scheduler.health_check_interval_minutes: 5
scheduler.snapshot_interval_minutes: 30

## Event Bus Settings
eventbus.max_retry_attempts: 3
eventbus.retry_delay_seconds: 60
eventbus.ack_timeout_seconds: 60
eventbus.replay_max_hours: 24
eventbus.dead_letter_alert: true

## Resource Limits
resources.mode: NORMAL
resources.max_ram_mb: 400
resources.max_log_size_mb: 10
resources.log_retention_days: 30
resources.snapshot_retention_count: 48
resources.done_archive_after_days: 90

## Notification Settings
notification.dashboard_update: true
notification.file_drop: true
notification.windows_toast: false
notification.email_draft: false
notification.dedup_window_minutes: 5

## Security Settings
security.scan_on_ingest: true
security.block_executable_extensions: [.exe, .bat, .ps1, .sh, .vbs]
security.max_path_depth: 10
security.pii_detection: true

## Dashboard Settings
dashboard.path: AI_Employee_Vault/Dashboard.md
dashboard.refresh_on_task_complete: true
dashboard.show_last_n_tasks: 10

## Knowledge Base Settings
knowledge.confidence_threshold_store: OBSERVED
knowledge.dedup_enabled: true
knowledge.max_entries_per_category: 500
```

---

## Tier Config (`bronze.md`)

```
# Bronze Tier Configuration
Tier: BRONZE
Inherits: base.md

## Overrides
agent.max_concurrent: 3
pipeline.max_concurrent_runs: 2
watcher.check_interval_seconds: 30
resources.max_ram_mb: 400
notification.windows_toast: false
notification.email_draft: false

## Disabled Features (not available in Bronze)
gmail_watcher.enabled: false
calendar_watcher.enabled: false
linkedin_integration.enabled: false
odoo_integration.enabled: false
cloud_sync.enabled: false

## Bronze Limits
agent.max_spawn_depth: 2
resources.max_log_size_mb: 10
knowledge.max_entries_per_category: 200
```

---

## Secrets Config (`secrets.md`)

**IMPORTANT: This file stores REFERENCES only. Never store actual passwords, API keys, or tokens here.**

```
# Secrets Configuration
Last Updated: 2026-02-16
WARNING: Store actual secrets in environment variables or .env file (never committed)

## Secret References
# Format: setting_name: ENV_VAR_NAME or VAULT_PATH

## Silver+ Only
gmail.client_id: ENV:GMAIL_CLIENT_ID
gmail.client_secret: ENV:GMAIL_CLIENT_SECRET
gmail.refresh_token: ENV:GMAIL_REFRESH_TOKEN

## Gold+ Only
linkedin.api_key: ENV:LINKEDIN_API_KEY
odoo.db_password: ENV:ODOO_DB_PASSWORD

## Platinum+ Only
cloud.api_key: ENV:CLOUD_SYNC_API_KEY

## How to Set Environment Variables (Windows)
# setx GMAIL_CLIENT_ID "your-value-here"
# Or create .env file (listed in .gitignore)

## Validation
# On startup, check all required secrets for current tier are set
# Bronze: no secrets required
# Silver: GMAIL_* required if gmail_watcher.enabled = true
```

---

## Config Loading

### How a Skill Reads Config
Any skill needing a config value follows this pattern:

```
Step 1: IDENTIFY needed setting
        Name: watcher.check_interval_seconds

Step 2: CHECK session overrides (.config/session.md)
        → Found: use it

Step 3: CHECK tier config (.config/{tier}.md)
        → Found: use it

Step 4: CHECK base config (.config/base.md)
        → Found: use it

Step 5: USE hardcoded fallback
        → watcher.check_interval_seconds default = 30

Step 6: CACHE the value for this session
        Avoid repeated file reads for same setting
```

### Config Read Format
Skills reference config as: `CONFIG:{setting_name}`

Examples:
- `CONFIG:watcher.check_interval_seconds` → returns `30`
- `CONFIG:agent.max_concurrent` → returns `3`
- `CONFIG:resources.max_ram_mb` → returns `400`

---

## Config Validation

### Validation Rules Per Setting Type

**Integer settings:**
```
Rule: Must be a positive integer
Rule: Must be within allowed range
Example: watcher.check_interval_seconds → min: 10, max: 3600
```

**String settings:**
```
Rule: Must not be empty
Rule: Must match allowed values if enum type
Example: resources.mode → allowed: [NORMAL, IDLE, BURST, EMERGENCY]
```

**Boolean settings:**
```
Rule: Must be true or false only
Example: security.scan_on_ingest → true or false
```

**Path settings:**
```
Rule: Must be valid relative path within vault
Rule: Must not contain .. (path traversal)
Example: watcher.inbox_path → must start with AI_Employee_Vault/
```

**List settings:**
```
Rule: Must be valid comma-separated or bracket list
Rule: Each item must pass individual item validation
Example: watcher.supported_extensions → each must start with .
```

### Validation Triggers
- **On startup** — validate entire config before any work begins
- **On config change** — validate the changed setting immediately
- **On tier switch** — re-validate full config for new tier

### Validation Result
```
CONFIG VALIDATION REPORT
Timestamp: 2026-02-16 09:00:00
Tier: BRONZE
Result: PASSED

Checks:
✅ base.md loaded (47 settings)
✅ bronze.md loaded (12 overrides)
✅ All integer ranges valid
✅ All path settings safe (no traversal)
✅ All boolean settings valid
✅ No secrets in plaintext
✅ Bronze secrets: none required ✅

Warnings:
⚠️ watcher.check_interval_seconds = 30 (consider 60 for low RAM mode)
```

---

## Config Change Protocol

### How to Change a Setting
```
Step 1: IDENTIFY the config file to update
        (base.md for permanent, session.md for temporary)

Step 2: READ current value and log it

Step 3: VALIDATE the new value
        Reject immediately if invalid

Step 4: WRITE new value to config file

Step 5: LOG the change to change_log.md
        Format: {timestamp} | {setting} | {old} → {new} | {reason} | {changed_by}

Step 6: APPLY the change
        For hot-reload settings: apply immediately
        For restart-required settings: flag and notify
```

### Hot-Reload Settings (apply immediately)
- `dashboard.refresh_on_task_complete`
- `notification.*`
- `scheduler.health_check_interval_minutes`
- `eventbus.dedup_window_minutes`
- `resources.mode`

### Restart-Required Settings (flag for next session)
- `watcher.check_interval_seconds`
- `watcher.inbox_path`
- `agent.max_concurrent`
- `pipeline.max_concurrent_runs`
- `security.*`

---

## Change Log (`change_log.md`)

```
# Config Change Log

| Timestamp           | Setting                          | Old Value | New Value | Reason                    | Changed By   |
|---------------------|----------------------------------|-----------|-----------|---------------------------|--------------|
| 2026-02-16 09:00:00 | resources.mode                   | IDLE      | NORMAL    | Session start             | system       |
| 2026-02-16 11:30:00 | scheduler.health_check_interval  | 5         | 3         | Increased monitoring freq | human        |
| 2026-02-16 14:00:00 | resources.mode                   | NORMAL    | BURST     | Inbox surge detected      | monitoring   |
| 2026-02-16 14:45:00 | resources.mode                   | BURST     | NORMAL    | Surge cleared             | monitoring   |
```

---

## Session Config (`session.md`)

Runtime overrides that reset every session — not persisted to base or tier config.

```
# Session Configuration
Session ID: SESSION-20260216-001
Started At: 2026-02-16 09:00:00
WARNING: These values reset on next session start

## Active Session Overrides
resources.mode: NORMAL
agent.debug_mode: false

## Flags Set This Session
first_run_today: true
inbox_surge_cleared: true
```

---

## Config for Each Tier

| Setting | Bronze | Silver | Gold | Platinum |
|---------|--------|--------|------|----------|
| max_concurrent_agents | 3 | 8 | 20 | 50 |
| max_concurrent_pipelines | 2 | 5 | 15 | 40 |
| watcher_check_interval (s) | 30 | 15 | 10 | 5 |
| max_ram_mb | 400 | 800 | 2000 | 8000 |
| log_retention_days | 30 | 90 | 180 | 365 |
| snapshot_retention_count | 48 | 168 | 720 | 2160 |
| gmail_watcher | ❌ | ✅ | ✅ | ✅ |
| linkedin_integration | ❌ | ❌ | ✅ | ✅ |
| cloud_sync | ❌ | ❌ | ❌ | ✅ |
| windows_toast | ❌ | ✅ | ✅ | ✅ |
| email_draft | ❌ | ✅ | ✅ | ✅ |

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|-----------------|
| Optimization | Reads resource limits from config |
| Watcher | Reads check_interval, paths, extensions |
| Agent Spawning | Reads max_concurrent, max_spawn_depth |
| Pipeline | Reads timeout, retry settings |
| Scheduler | Reads report times, review schedule |
| Security | Reads blocked extensions, PII detection flag |
| Notification | Reads enabled channels |
| Monitoring | Reads health check interval |
| Version Control | Config changes logged and versioned |
| Event Bus | Publishes CONFIG_CHANGED events on updates |

---

## Quick Reference

```
BASE CONFIG:        .config/base.md
TIER CONFIG:        .config/{bronze|silver|gold|platinum}.md
SECRETS:            .config/secrets.md (references only)
SESSION OVERRIDES:  .config/session.md
CHANGE LOG:         .config/change_log.md

READ SETTING:       CONFIG:{setting.name}
CHANGE SETTING:     validate → write → log → apply
HOT RELOAD:         notification.*, dashboard.*, resources.mode
RESTART REQUIRED:   watcher.*, agent.max_concurrent, security.*

CURRENT TIER:       BRONZE
VALIDATION:         Run on startup + on every change
SECRET RULE:        References only — never plaintext in any config file
```

---

## Best Practices

1. **No hardcoded values** — every tunable value lives in config, never in skill logic
2. **Secrets = references** — config files point to `ENV:VAR_NAME`, never the actual value
3. **Validate before use** — always validate a config value before trusting it
4. **Log every change** — who changed what and why is always recorded
5. **Base config = safe defaults** — base.md should work for Bronze tier out of the box
6. **Tier config = additions only** — tier files override specific settings, not replace entire base
7. **Session config = temporary** — runtime experiments go in session.md, not base.md
8. **Human-readable always** — config files are markdown, not JSON/YAML, so humans can edit and read them naturally
9. **One source of truth** — if the same setting appears in two files, the hierarchy resolves it; never duplicate with different values in same-level files
10. **Config is documentation** — comments in config files explain why a value is what it is
