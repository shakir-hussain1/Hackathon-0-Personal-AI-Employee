# Template Engine Skill

## Purpose
Define, store, and render reusable document templates. Any skill that needs to produce structured output — task files, reports, notifications, knowledge entries, emails — uses the Template Engine to fill a pre-defined template with live data instead of constructing documents from scratch every time.

---

## Core Functions

1. **Template Library** — Store all reusable templates in one place
2. **Variable Substitution** — Replace `{{variable}}` placeholders with real values
3. **Conditional Sections** — Include or exclude blocks based on conditions
4. **Template Inheritance** — Build complex templates from simpler base templates
5. **Render to File** — Write the filled template to the correct vault location
6. **Template Validation** — Catch missing variables before rendering fails

---

## Template Syntax

### Variables
Replace a placeholder with a dynamic value:
```
{{variable_name}}
```

Examples:
```
{{task_id}}           → TASK-047
{{file_name}}         → proposal.pdf
{{timestamp}}         → 2026-02-16 14:30:00
{{agent_id}}          → AGENT-FP-20260216-003
{{priority}}          → HIGH
```

### Conditional Blocks
Include a section only if a condition is true:
```
{{IF condition}}
  ...content shown when true...
{{END IF}}
```

```
{{IF NOT condition}}
  ...content shown when false...
{{END IF}}
```

Examples:
```
{{IF risk_level == "CRITICAL"}}
⚠️ CRITICAL RISK DETECTED — Human review required
{{END IF}}

{{IF has_summary}}
## Summary
{{summary}}
{{END IF}}

{{IF NOT has_attachments}}
No attachments detected.
{{END IF}}
```

### Loops
Repeat a block for each item in a list:
```
{{FOR item IN list}}
  ...content using {{item.field}}...
{{END FOR}}
```

Example:
```
{{FOR flag IN risk_flags}}
- {{flag.severity}}: {{flag.description}}
{{END FOR}}
```

### Includes
Embed another template inside this one:
```
{{INCLUDE template_name}}
```

Example:
```
{{INCLUDE footer_standard}}
{{INCLUDE header_with_status}}
```

### Filters
Transform a variable's value at render time:
```
{{variable | filter}}
```

Available filters:
| Filter | Effect | Example |
|--------|--------|---------|
| `upper` | Uppercase | `{{priority \| upper}}` → HIGH |
| `lower` | Lowercase | `{{status \| lower}}` → completed |
| `date` | Format as date | `{{timestamp \| date}}` → 2026-02-16 |
| `time` | Format as time | `{{timestamp \| time}}` → 14:30 |
| `truncate(N)` | Limit to N chars | `{{summary \| truncate(100)}}` |
| `default(X)` | Use X if empty | `{{owner \| default("Unassigned")}}` |
| `count` | Count list items | `{{flags \| count}}` → 3 |
| `yes_no` | Boolean to Yes/No | `{{has_risk \| yes_no}}` → Yes |

---

## Template Library

**Location:** `AI_Employee_Vault/.templates/`

```
AI_Employee_Vault/.templates/
├── tasks/
│   ├── task_file.md          # Needs_Action task record
│   ├── task_summary.md       # Brief task status line
│   └── task_completion.md    # Done record
├── reports/
│   ├── daily_report.md       # End-of-day summary
│   ├── weekly_report.md      # Weekly review
│   ├── exception_report.md   # Error/alert report
│   └── on_demand_report.md   # Ad-hoc report
├── notifications/
│   ├── alert_human.md        # Human attention needed
│   ├── task_ready.md         # Task ready for pickup
│   ├── system_status.md      # System health update
│   └── escalation.md        # Escalated issue
├── knowledge/
│   ├── kb_entry.md           # Standard knowledge entry
│   ├── person_profile.md     # Person entity record
│   ├── decision_record.md    # Decision log entry
│   └── lesson_learned.md     # Learning capture
├── emails/
│   ├── email_draft.md        # Outbound email draft
│   ├── follow_up.md          # Follow-up email
│   └── acknowledgment.md     # Receipt confirmation
├── dashboard/
│   ├── dashboard_full.md     # Complete dashboard
│   ├── status_section.md     # Status block only
│   └── stats_table.md        # Stats table only
└── partials/
    ├── header_standard.md    # Reusable header
    ├── footer_standard.md    # Reusable footer
    ├── risk_banner.md        # Risk level banner
    └── metadata_block.md     # Standard metadata rows
```

---

## Standard Templates

### Template: Task File (`tasks/task_file.md`)
Used by: Task Management Skill, Pipeline, Watcher

```
# Task: {{task_id}}
Created: {{created_at}}
Priority: {{priority | upper}}
Status: {{status}}

{{IF claimed_by}}
CLAIMED BY: {{claimed_by}}
CLAIMED AT: {{claimed_at}}
{{END IF}}

## Source
File: {{source_file}}
File Type: {{file_type}}
File Size: {{file_size_kb}} KB

{{IF risk_level == "CRITICAL"}}
{{INCLUDE risk_banner}}
{{END IF}}

## What Needs To Happen
{{action_description}}

## Analysis
{{IF has_analysis}}
{{analysis_summary}}
{{ELSE}}
Analysis pending.
{{END IF}}

## Risk Assessment
Risk Level: {{risk_level}}
{{IF risk_flags}}
Flags:
{{FOR flag IN risk_flags}}
- [{{flag.severity}}] {{flag.description}}
{{END FOR}}
{{END IF}}

## Actions Taken
{{IF actions_taken}}
{{FOR action IN actions_taken}}
- {{action.timestamp}}: {{action.description}}
{{END FOR}}
{{ELSE}}
No actions taken yet.
{{END IF}}

{{INCLUDE metadata_block}}
```

---

### Template: Daily Report (`reports/daily_report.md`)
Used by: Reporting Skill, Scheduler

```
# Daily Report — {{report_date}}
Generated: {{generated_at}}
Period: {{period_start}} to {{period_end}}

## Summary
- Files Processed: {{files_processed}}
- Tasks Completed: {{tasks_completed}}
- Tasks Failed: {{tasks_failed}}
- Avg Processing Time: {{avg_processing_time}}

## Performance
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Files Processed | {{files_processed}} | {{target_files}} | {{files_status}} |
| Success Rate | {{success_rate}}% | >90% | {{success_status}} |
| Avg Duration | {{avg_duration}} | <5 min | {{duration_status}} |
| Errors | {{error_count}} | 0 | {{error_status}} |

{{IF has_completed_tasks}}
## Completed Tasks
{{FOR task IN completed_tasks}}
- {{task.id}} — {{task.file_name}} ({{task.duration}}) {{task.status_icon}}
{{END FOR}}
{{END IF}}

{{IF has_failed_tasks}}
## Failed Tasks
{{FOR task IN failed_tasks}}
- {{task.id}} — {{task.file_name}}: {{task.failure_reason}}
{{END FOR}}
{{END IF}}

{{IF has_alerts}}
## Alerts
{{FOR alert IN alerts}}
- [{{alert.severity}}] {{alert.message}} at {{alert.time}}
{{END FOR}}
{{END IF}}

## Knowledge Added
{{IF knowledge_added > 0}}
{{knowledge_added}} new entries added to knowledge base.
{{ELSE}}
No new knowledge entries today.
{{END IF}}

---
*Generated by AI Employee — {{agent_id}}*
```

---

### Template: Alert Human (`notifications/alert_human.md`)
Used by: Notification Skill

```
# ⚠ Action Required — {{alert_title}}
Time: {{timestamp}}
Severity: {{severity | upper}}
Source: {{source_skill}}

## What Happened
{{description}}

{{IF has_context}}
## Context
{{context}}
{{END IF}}

## Recommended Action
{{recommended_action}}

{{IF has_options}}
## Options
{{FOR option IN options}}
{{option.number}}. **{{option.label}}** — {{option.description}}
{{END FOR}}

To respond: Add your choice to AI_Employee_Vault/Needs_Action/HUMAN_RESPONSE_{{event_id}}.md
{{END IF}}

{{IF auto_resolves}}
**Auto-resolves in:** {{auto_resolve_timeout}} if no response
{{END IF}}

---
Task ID: {{task_id | default("N/A")}}
Event ID: {{event_id}}
```

---

### Template: Knowledge Base Entry (`knowledge/kb_entry.md`)
Used by: Knowledge Base Skill

```
# {{entry_title}}
Entry ID: {{entry_id}}
Type: {{entry_type}}
Confidence: {{confidence_level}}
Created: {{created_at}}
Last Updated: {{updated_at}}
Source: {{source_file | default("Unknown")}}

## Content
{{content}}

{{IF has_tags}}
## Tags
{{FOR tag IN tags}}#{{tag}} {{END FOR}}
{{END IF}}

{{IF has_related}}
## Related Entries
{{FOR related IN related_entries}}
- [{{related.id}}] {{related.title}}
{{END FOR}}
{{END IF}}

{{IF has_validation_notes}}
## Validation Notes
{{validation_notes}}
{{END IF}}

---
*Confidence: {{confidence_level}} | Reviewed: {{reviewed | yes_no}}*
```

---

### Template: Partial — Metadata Block (`partials/metadata_block.md`)
Included in most documents:

```
---
**Metadata**
Created: {{created_at}}
Updated: {{updated_at}}
Agent: {{agent_id | default("System")}}
Session: {{session_id}}
Version: {{version | default("1")}}
```

---

### Template: Email Draft (`emails/email_draft.md`)
Used by: Communication Skill (Silver+)

```
# Email Draft — {{draft_id}}
Status: DRAFT — Pending Human Approval
Created: {{created_at}}

## Envelope
To: {{recipient_email}}
Subject: {{subject}}
{{IF cc_list}}Cc: {{cc_list}}{{END IF}}

## Body
{{email_body}}

{{IF has_attachments}}
## Attachments
{{FOR attachment IN attachments}}
- {{attachment.name}} ({{attachment.size_kb}} KB)
{{END FOR}}
{{END IF}}

---
**Approval Required**
To send: Move this file to AI_Employee_Vault/Approved/
To discard: Move this file to AI_Employee_Vault/Done/
```

---

## Render Protocol

### How to Render a Template

```
Step 1: SELECT template
        Identify which template to use based on document type
        Load from .templates/{category}/{template_name}.md

Step 2: COLLECT variables
        Gather all values needed for {{variable}} placeholders
        Check which are required vs optional

Step 3: VALIDATE variables
        Verify all REQUIRED variables are present and non-empty
        For missing optional variables: apply default() filter or skip block

Step 4: RESOLVE includes
        Load any {{INCLUDE partial_name}} files
        Substitute includes before main rendering

Step 5: EVALUATE conditions
        Process all {{IF}} / {{END IF}} blocks
        Remove false blocks entirely from output

Step 6: EXECUTE loops
        Process all {{FOR}} / {{END FOR}} blocks
        Expand each item in the list

Step 7: SUBSTITUTE variables
        Replace all remaining {{variable}} and {{variable | filter}} placeholders
        Flag any unresolved {{variable}} as a render warning

Step 8: WRITE output
        Write rendered document to target file path
        Log: "Rendered {template_name} → {output_path}"
```

---

## Variable Requirements Per Template

| Template | Required Variables | Optional Variables |
|----------|-------------------|-------------------|
| `task_file` | task_id, created_at, priority, status, source_file, file_type, action_description, risk_level | claimed_by, analysis_summary, risk_flags, actions_taken |
| `daily_report` | report_date, generated_at, files_processed, tasks_completed, success_rate | completed_tasks, failed_tasks, alerts |
| `alert_human` | alert_title, timestamp, severity, source_skill, description, recommended_action, event_id | context, options, task_id, auto_resolve_timeout |
| `kb_entry` | entry_id, entry_title, entry_type, confidence_level, created_at, content | tags, related_entries, validation_notes |
| `email_draft` | draft_id, created_at, recipient_email, subject, email_body | cc_list, attachments |

---

## Template Versioning

Every template has a version. When a template changes, old renders are preserved.

```
## Template Version Header (inside template file)
TEMPLATE: daily_report
VERSION: 2.1
LAST_UPDATED: 2026-02-10
CHANGELOG: Added knowledge_added section
```

Rendered documents record which template version was used:
```
*Rendered with template: daily_report v2.1*
```

---

## Adding a New Template

```
Step 1: Create file in .templates/{category}/
Step 2: Use {{variable}} syntax for dynamic values
Step 3: Add TEMPLATE, VERSION, LAST_UPDATED header
Step 4: Document required and optional variables
Step 5: Test render with sample data
Step 6: Register in template index (.templates/index.md)
```

---

## Template Index (`.templates/index.md`)

```
# Template Index
Last Updated: 2026-02-16

| Template Name         | Category      | Version | Used By                    |
|-----------------------|---------------|---------|----------------------------|
| task_file             | tasks         | 1.2     | task-management, pipeline  |
| daily_report          | reports       | 2.1     | reporting, scheduler       |
| weekly_report         | reports       | 1.3     | reporting, scheduler       |
| alert_human           | notifications | 1.0     | notification               |
| kb_entry              | knowledge     | 1.1     | knowledge-base             |
| email_draft           | emails        | 1.0     | communication (Silver+)    |
| dashboard_full        | dashboard     | 3.0     | workflow, reporting        |
| header_standard       | partials      | 1.0     | (all templates)            |
| footer_standard       | partials      | 1.0     | (all templates)            |
| metadata_block        | partials      | 1.0     | (most templates)           |
| risk_banner           | partials      | 1.0     | task_file, alert_human     |
```

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|-----------------|
| Task Management | Uses `task_file` template for every Needs_Action file |
| Reporting | Uses `daily_report`, `weekly_report` templates |
| Notification | Uses `alert_human`, `system_status` templates |
| Knowledge Base | Uses `kb_entry`, `person_profile` templates |
| Communication | Uses `email_draft`, `follow_up` templates (Silver+) |
| Workflow | Uses `dashboard_full` template on refresh |
| Pipeline | Renders task and completion documents per run |
| Audit | Renders structured log entries |

---

## Quick Reference

```
TEMPLATES FOLDER:    AI_Employee_Vault/.templates/
VARIABLE SYNTAX:     {{variable_name}}
FILTER SYNTAX:       {{variable | filter}}
CONDITION SYNTAX:    {{IF condition}} ... {{END IF}}
LOOP SYNTAX:         {{FOR item IN list}} ... {{END FOR}}
INCLUDE SYNTAX:      {{INCLUDE partial_name}}
RENDER STEPS:        Select → Collect → Validate → Includes → Conditions → Loops → Substitute → Write
MISSING REQUIRED:    Stop render, log error
MISSING OPTIONAL:    Use default() or skip block
TEMPLATE INDEX:      .templates/index.md
```

---

## Best Practices

1. **Templates over construction** — never build a document by string concatenation in a skill; always use a template
2. **Required vs optional** — clearly mark which variables are required; optional ones must have safe defaults
3. **Partials for reuse** — common sections (headers, footers, metadata) go in partials and get `{{INCLUDE}}`d
4. **Keep templates readable** — a human must be able to read and edit a template file directly
5. **Version on change** — increment version number whenever a template's structure changes
6. **Validate before render** — catch missing required variables before writing any output
7. **Log every render** — which template, which output file, which agent, what timestamp
8. **Separate layout from logic** — templates contain structure only; skill code provides the data
9. **Test with edge cases** — empty lists, missing optional fields, very long strings — render must not break
10. **Index every template** — unregistered templates in index.md won't be found by other skills
