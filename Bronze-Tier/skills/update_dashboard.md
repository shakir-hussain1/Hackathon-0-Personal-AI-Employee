# 📊 Agent Skill: Update Dashboard

**Purpose**: Refresh Dashboard statistics and activity summary
**Trigger**: After processing tasks or on-demand
**Vault**: AI_Employee_Vault

---

## 📋 Instructions for AI

When this skill is invoked, update the Dashboard with current system statistics.

### Step 1: Gather Current Statistics

Collect the following data:

#### File Counts
- **Files in Inbox**: Count all files in `Inbox/` folder
- **Tasks Pending**: Count all `.md` files in `Needs_Action/` folder
- **Tasks Completed Today**: Read from current Dashboard or count today's log entries
- **Total Files Processed**: Count all files in `Done/` folder and subdirectories

#### Watcher Status
- Check if a log entry exists from the last 5 minutes
- If yes: 🟢 Running
- If no: 🔴 Not Running (or can't determine)

#### Recent Activity
- Read today's log file from `Logs/[today].log`
- Extract the last 5-10 activities
- Format for display in Dashboard

### Step 2: Calculate Derived Metrics

- **Inbox Status**:
  - If 0 files: ✅ Clear
  - If 1-5 files: 🟡 Active
  - If >5 files: 🔴 Backlog

- **Task Status**:
  - If 0 pending: ✅ Clear
  - If 1-3 pending: 🟡 Active
  - If >3 pending: 🔴 Queue Building

### Step 3: Update Dashboard Sections

Open `Dashboard.md` and update these sections:

#### A. Header Section
```markdown
**Last Updated**: [Current timestamp: YYYY-MM-DD HH:MM:SS]
**Status**: [Overall system status emoji]
```

Status options:
- 🟢 All Clear: Inbox empty, no pending tasks
- 🟡 Active: Normal operation with some tasks
- 🔴 Attention Needed: High backlog or errors

#### B. System Status Table
```markdown
| Metric | Count | Status |
|--------|-------|--------|
| 📥 Files in Inbox | [count] | [status] |
| ⏳ Tasks Pending | [count] | [status] |
| ✅ Tasks Completed Today | [count] | - |
| 📁 Total Files Processed | [count] | - |
```

#### C. Active Watchers Section
Update the File System Watcher status:
- 🟢 Running (if recent log entries)
- 🔴 Not Running (if no recent activity)
- Update "Last Check" timestamp if available

#### D. Today's Activity Summary
Extract from today's log and format like:
```markdown
### Recent Tasks
1. ✅ [HH:MM] - Processed `filename.ext`
   - Type: [file type] | Priority: [level] | Result: Success
2. ✅ [HH:MM] - Processed `another_file.ext`
   - Type: [file type] | Priority: [level] | Result: Success
...
```

If no activity today:
```markdown
### Recent Tasks
*No tasks processed yet today. System ready for new files.*
```

### Step 4: Preserve Static Sections

**DO NOT modify** these sections (they're templates):
- Quick Actions
- System Information
- Quick Reference
- Footer note

### Step 5: Save and Verify

1. Save updated `Dashboard.md`
2. Verify the file is valid markdown
3. Print confirmation message

---

## 📐 Update Template

Use this structure when updating:

```markdown
# 🤖 Personal AI Employee - Dashboard

**Last Updated**: 2026-02-16 14:35:22
**Status**: 🟢 All Clear

---

## 📊 System Status

| Metric | Count | Status |
|--------|-------|--------|
| 📥 Files in Inbox | 0 | ✅ Clear |
| ⏳ Tasks Pending | 0 | ✅ Clear |
| ✅ Tasks Completed Today | 3 | - |
| 📁 Total Files Processed | 12 | - |

---

## 🔄 Active Watchers

- **File System Watcher**: 🟢 Running
  - Monitors: `Inbox/` folder
  - Check Interval: 30 seconds
  - Last Check: 2026-02-16 14:35:00

---

## 📝 Today's Activity Summary

**Date**: 2026-02-16

### Recent Tasks
1. ✅ 14:30 - Processed `budget_2026.xlsx`
   - Type: Excel Spreadsheet | Priority: HIGH | Result: Success
2. ✅ 14:25 - Processed `meeting_notes.txt`
   - Type: Text Document | Priority: MEDIUM | Result: Success
3. ✅ 14:20 - Processed `screenshot.png`
   - Type: PNG Image | Priority: LOW | Result: Success

---

[Keep all remaining static sections unchanged]
```

---

## 🔍 Data Collection Commands

To gather the statistics:

### Count files in Inbox
- List files in `Inbox/` folder
- Count: exclude subdirectories, only files

### Count pending tasks
- List `.md` files in `Needs_Action/` folder
- Count: total task files

### Count completed today
- Option 1: Read today's log and count "PROCESSED" entries
- Option 2: Check Dashboard's previous count and add new completions

### Count total processed
- List all files in `Done/` folder recursively
- Count: total files in all subdirectories

### Get recent activity
- Read `Logs/[YYYY-MM-DD].log` (today's file)
- Parse log entries
- Extract last 5-10 PROCESSED actions
- Format with timestamps and details

---

## 🎯 Success Checklist

After updating Dashboard, verify:

- [ ] "Last Updated" shows current timestamp
- [ ] All counts are accurate (match actual files)
- [ ] Status emojis are correct
- [ ] Recent activity list is populated
- [ ] Watcher status reflects reality
- [ ] No formatting errors in markdown
- [ ] File saved successfully

---

## 📊 Example Update

**Before**:
```
**Last Updated**: System Initializing...
**Status**: 🟡 Setting Up
```

**After**:
```
**Last Updated**: 2026-02-16 14:35:22
**Status**: 🟢 All Clear

[Updated tables with real counts]
[Updated activity log]
```

---

## 🆘 Error Handling

If you can't access a file or folder:
1. Note the error in the activity log
2. Use "?" or "N/A" for that metric
3. Update what you can
4. Log the issue
5. Continue with update

---

## ⚡ Quick Update Mode

For rapid updates (used after each task processing):

1. Read Dashboard
2. Update ONLY:
   - Last Updated timestamp
   - File counts in table
   - Add latest task to Recent Tasks (top of list)
3. Save and exit

Full update mode (this skill):
- Recalculate everything
- Reformat recent activity
- Check watcher status
- Comprehensive refresh

---

*This skill keeps the Dashboard current and provides real-time visibility into AI Employee operations.*
