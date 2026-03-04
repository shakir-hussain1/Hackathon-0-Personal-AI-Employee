# File Understanding Skill

Parse and validate markdown task files with metadata extraction.

## Core Functions

### `read_metadata(file_path)`
Extract all metadata from markdown file (YAML frontmatter + inline).

**Returns**: Dict with status, priority, owner, created, tags

### `validate_task(file_path)`
Validate task file format and required fields.

**Returns**: Dict with `valid`, `errors`, `warnings`

### `extract_status(file_path)`
Get normalized task status.

**Returns**: "PENDING" | "IN_PROGRESS" | "COMPLETED" | "DELETED"

### `extract_priority(file_path)`
Get normalized task priority.

**Returns**: "HIGH" | "MEDIUM" | "LOW" | "NEEDS_REVIEW"

### `extract_owner(file_path)`
Get task owner.

**Returns**: Owner name string or None

## Supported Formats

**YAML Frontmatter:**
```yaml
---
status: IN_PROGRESS
priority: HIGH
owner: john
---
```

**Inline Markdown:**
```markdown
**Status**: ⏳ PENDING
**Priority**: 🟡 MEDIUM
**Owner**: alice
```

## Status Mapping
- ⏳ PENDING → "PENDING"
- 🔄 IN_PROGRESS → "IN_PROGRESS"
- ✅ COMPLETED → "COMPLETED"
- ❌ DELETED → "DELETED"

## Priority Mapping
- 🔴 HIGH → "HIGH"
- 🟡 MEDIUM → "MEDIUM"
- 🟢 LOW → "LOW"
- 🟣 NEEDS_REVIEW → "NEEDS_REVIEW"

## Usage

```python
from file_understanding import read_metadata, validate_task, extract_status

# Validate task
result = validate_task("task.md")
if result['valid']:
    print("✓ Valid task file")

# Get metadata
metadata = read_metadata("task.md")
print(f"Status: {metadata['status']}")
print(f"Priority: {metadata['priority']}")

# Quick status check
status = extract_status("task.md")
if status == "COMPLETED":
    print("Task done!")
```

## Integration

Use with AI Employee vault to:
- Scan Needs_Action folder
- Validate task files before processing
- Extract priorities for task routing
- Generate status reports
