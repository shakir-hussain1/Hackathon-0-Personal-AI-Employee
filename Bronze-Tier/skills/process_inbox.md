# 🤖 Agent Skill: Process Inbox

**Purpose**: Main task processing skill for the AI Employee
**Trigger**: Manual execution or scheduled automation
**Vault**: AI_Employee_Vault

---

## 📋 Instructions for AI

When this skill is invoked, you are acting as an autonomous AI Employee. Follow these steps precisely:

### Step 1: Scan for Pending Tasks

1. List all `.md` files in the `Needs_Action/` folder
2. If no tasks found:
   - Print: "✅ No pending tasks. Inbox is clear!"
   - Update Dashboard with current status
   - Exit gracefully
3. If tasks found:
   - Print: "📋 Found X task(s) to process"
   - Proceed to Step 2

### Step 2: Process Each Task

For each task file in `Needs_Action/`:

#### A. Read Task File
- Open the task `.md` file
- Extract metadata:
  - Original filename
  - Priority level
  - File location in Inbox
  - Task creation timestamp

#### B. Read Original File
- Locate original file in `Inbox/` folder
- Read the file content
- Handle different file types appropriately:
  - **Text files** (.txt, .md): Read full content
  - **Documents** (.doc, .docx): Note file type, extract what's readable
  - **Spreadsheets** (.csv, .xlsx): Note structure, sample data if possible
  - **Images** (.jpg, .png): Note image properties (can't view content in Bronze tier)
  - **PDFs**: Note page count and properties
  - **Code files** (.py, .js, etc.): Read and analyze code
  - **Unknown types**: Note file type and size only

#### C. Analyze Content
Based on the Company Handbook rules (`Company_Handbook.md`), determine:

1. **What is this file?**
   - Brief description
   - Purpose/context if identifiable

2. **Key information**
   - Main points, data, or content summary
   - Important details

3. **Action items** (if any)
   - Tasks to do
   - Deadlines mentioned
   - Follow-ups needed

4. **Categorization**
   - Appropriate subdirectory in `Done/`:
     - `Done/Documents/`
     - `Done/Data/`
     - `Done/Media/`
     - `Done/Communications/`
     - `Done/Code/`
     - `Done/Uncategorized/`

#### D. Update Task File
- Fill in the "Analysis Results" section with your findings
- Add processing timestamp
- Change status from "⏳ PENDING" to "✅ COMPLETED"
- Save updated task file

#### E. Move Files
1. Create destination subdirectory in `Done/` if needed
2. Move original file from `Inbox/` to `Done/[category]/`
3. Move task file from `Needs_Action/` to `Done/`

#### F. Log Activity
- Append to today's log file in `Logs/`
- Format: `[TIMESTAMP] PROCESSED | [filename] | SUCCESS | Moved to Done/[category]/`
- Include any errors or warnings

### Step 3: Update Dashboard

After processing all tasks:
1. Read current `Dashboard.md`
2. Update statistics:
   - Count files in Inbox (should be 0)
   - Count tasks in Needs_Action (should be 0)
   - Count files in Done
   - Increment "Tasks Completed Today"
3. Update "Recent Tasks" section with summary of what was processed
4. Update "Last Updated" timestamp
5. Update watcher status if you can determine it
6. Save updated Dashboard

### Step 4: Report Results

Print a summary:
```
✅ Processing Complete!

Tasks Processed: X
Files Moved: X
Categories: [list of categories used]
Errors: [any errors or 0]

Dashboard updated: [timestamp]
```

---

## 🛡️ Safety Rules

**CRITICAL - Always follow these:**

- ✅ ALWAYS read files before moving them
- ✅ ALWAYS move files (never delete)
- ✅ ALWAYS log actions
- ✅ ALWAYS update Dashboard when done
- ❌ NEVER delete original files
- ❌ NEVER modify file contents (just move/organize)
- ❌ NEVER skip logging
- ❌ NEVER process files outside the vault

---

## 🔍 Example Task Processing

**Example task file found**: `FILE_budget_20260216_143022.md`

**Processing steps**:
1. ✅ Read task file → Extract: original filename = `budget_2026.xlsx`, priority = HIGH
2. ✅ Read original file from `Inbox/budget_2026.xlsx`
3. ✅ Analyze: Spreadsheet with budget data, Q1-Q4 columns, expense categories
4. ✅ Update task file with analysis
5. ✅ Move `budget_2026.xlsx` → `Done/Data/budget_2026.xlsx`
6. ✅ Move `FILE_budget_20260216_143022.md` → `Done/FILE_budget_20260216_143022.md`
7. ✅ Log: `[2026-02-16 14:30:45] PROCESSED | budget_2026.xlsx | SUCCESS | Moved to Done/Data/`
8. ✅ Update Dashboard counters

---

## 📊 Expected Behavior

**Input**: Task files in `Needs_Action/` + Files in `Inbox/`
**Output**:
- All files moved to `Done/` with proper categorization
- All task files completed and moved
- Dashboard updated with current statistics
- Activity logged

**Success Metrics**:
- Zero files remain in `Inbox/`
- Zero task files remain in `Needs_Action/`
- Dashboard shows accurate counts
- Log file contains all processing entries

---

## 🆘 Error Handling

If you encounter an error:

1. **Log the error** with details
2. **Skip that file** and continue with others
3. **Report errors** in final summary
4. **Don't stop processing** - handle each file independently
5. **Mark failed tasks** with "❌ ERROR" status

Error scenarios:
- File not found → Log and skip
- File can't be read → Move to `Done/Errors/` and log
- Task file corrupted → Log and skip
- Permission error → Log and alert in Dashboard

---

## 🎯 Success Checklist

After execution, verify:

- [ ] All tasks in `Needs_Action/` processed
- [ ] All files from `Inbox/` moved to `Done/`
- [ ] Task files updated with analysis
- [ ] Task files moved to `Done/`
- [ ] Log entries created
- [ ] Dashboard updated with new statistics
- [ ] "Last Updated" timestamp current
- [ ] No errors (or errors properly logged)

---

*This skill embodies the core autonomous behavior of the AI Employee. Execute it thoroughly and carefully, following the Company Handbook at all times.*
