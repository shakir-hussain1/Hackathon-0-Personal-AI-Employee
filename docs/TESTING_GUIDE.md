# 🧪 Testing Guide - Personal AI Employee

This guide walks you through testing the Bronze Tier implementation step-by-step.

---

## 🎯 Pre-Test Checklist

Before testing, verify:

- [ ] Python virtual environment created (`venv/` folder exists)
- [ ] Dependencies installed (watchdog, python-dotenv)
- [ ] All folders exist in `AI_Employee_Vault/`
- [ ] Dashboard.md and Company_Handbook.md exist
- [ ] VS Code can open the vault folder
- [ ] Claude Code CLI is installed

---

## 🧪 Test 1: Basic Infrastructure

### Verify Folder Structure

```bash
cd E:\Hackathon-0-Personal-AI-Employee
dir AI_Employee_Vault
```

**Expected folders**:
- Inbox
- Needs_Action
- Done
- Plans
- Logs

### Verify Dashboard

1. Open VS Code
2. Open Folder: `E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault`
3. Click `Dashboard.md`
4. Press `Ctrl+Shift+V` for preview

**Expected**: Dashboard displays with initial statistics (all zeros)

### Verify Python Setup

```bash
.\venv\Scripts\activate
python --version
pip list
```

**Expected**:
- Python 3.13+
- watchdog==4.0.0
- python-dotenv==1.0.0

---

## 🧪 Test 2: File System Watcher

### Start the Watcher

**Option 1** (Batch file):
```bash
start_watcher.bat
```

**Option 2** (Manual):
```bash
.\venv\Scripts\activate
python watchers\filesystem_watcher.py
```

**Expected Output**:
```
============================================================
🤖 FileSystemWatcher Active
============================================================
📁 Vault: E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault
⏱️  Check Interval: 30 seconds
🔄 Monitoring started...
============================================================

[TIMESTAMP] [INFO] FileSystemWatcher started with 30s interval
```

### Create Test File

While watcher is running, create a test file:

1. Open Notepad
2. Type:
   ```
   This is a test document.
   Task: Review project status.
   Deadline: Tomorrow
   ```
3. Save as: `AI_Employee_Vault\Inbox\test_document.txt`

### Verify Detection (within 30 seconds)

**Expected in watcher terminal**:
```
[TIMESTAMP] [INFO] Detected new file: test_document.txt
[TIMESTAMP] [INFO] Created task: FILE_test_document_YYYYMMDD_HHMMSS.md [Priority: MEDIUM]
```

### Verify Task Creation

1. Check `AI_Employee_Vault\Needs_Action\`
2. You should see: `FILE_test_document_[timestamp].md`
3. Open the file - should contain:
   - File information
   - Priority: MEDIUM
   - Task instructions
   - Empty analysis section

### Verify Logging

1. Check `AI_Employee_Vault\Logs\`
2. Open today's log file: `YYYY-MM-DD.log`
3. Should contain entries about detection and task creation

**✅ Test 2 Success Criteria**:
- Watcher started without errors
- File detected within 30 seconds
- Task file created in Needs_Action
- Log entries created

---

## 🧪 Test 3: Claude Code Integration

### Start Claude Code

Open a new terminal:

```bash
claude code --cwd E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault
```

### Test File Reading

In Claude session, type:
```
Read Dashboard.md
```

**Expected**: Claude displays Dashboard content

### Test Company Handbook Access

```
Read Company_Handbook.md and summarize the core principles
```

**Expected**: Claude reads and summarizes the AI behavior rules

### Test Task Access

```
List all files in Needs_Action folder
```

**Expected**: Claude lists the task file(s) created by watcher

**✅ Test 3 Success Criteria**:
- Claude Code starts successfully
- Can read all markdown files
- Can access all folders

---

## 🧪 Test 4: Process Inbox Skill (Core Test)

This is the main test of the autonomous workflow.

### Prepare Test Files

With watcher running, create these test files in `Inbox/`:

1. **test_notes.txt**:
   ```
   Meeting notes from project discussion.
   Attendees: John, Sarah, Mike
   Topic: Q1 Planning
   Action items:
   - Complete budget review
   - Schedule follow-up meeting
   ```

2. **test_data.csv**:
   ```
   Name,Department,Salary
   Alice,Engineering,75000
   Bob,Marketing,65000
   Charlie,Sales,70000
   ```

3. **test_image.png** (any screenshot or image)

Wait 30-60 seconds for watcher to detect all three files.

### Execute Processing Skill

In Claude Code session:
```
/skill process_inbox
```

**Alternative** (if skill doesn't work):
```
Please process all tasks in the Needs_Action folder according to the Company_Handbook.md guidelines. For each task:
1. Read the task file
2. Read the original file from Inbox
3. Analyze the content
4. Update the task file with your analysis
5. Move both files to appropriate subdirectories in Done/
6. Log all activity
7. Update Dashboard.md
```

### Monitor Processing

Watch Claude:
1. List tasks in Needs_Action
2. Read each task file
3. Read each original file
4. Analyze content
5. Update task files
6. Move files
7. Update Dashboard

### Verify Results

#### Check Inbox (should be empty)
```bash
dir AI_Employee_Vault\Inbox
```
**Expected**: Only .gitkeep file

#### Check Needs_Action (should be empty)
```bash
dir AI_Employee_Vault\Needs_Action
```
**Expected**: Only .gitkeep file

#### Check Done (should have files)
```bash
dir AI_Employee_Vault\Done /s
```
**Expected**:
- `Done\Documents\test_notes.txt`
- `Done\Data\test_data.csv`
- `Done\Media\test_image.png`
- `Done\FILE_test_notes_[timestamp].md`
- `Done\FILE_test_data_[timestamp].md`
- `Done\FILE_test_image_[timestamp].md`

#### Check Task Files (should have analysis)

Open any task file in `Done/`, should contain:
- ✅ Completed status
- 📊 Analysis results filled in
- 📝 Processing timestamp
- Summary of content
- Categorization info

#### Check Dashboard (should be updated)

Open `Dashboard.md` in VS Code preview:
- **Files in Inbox**: 0
- **Tasks Pending**: 0
- **Tasks Completed Today**: 3
- **Recent Tasks**: Should list the 3 files processed
- **Last Updated**: Recent timestamp

#### Check Logs (should have entries)

Open today's log in `Logs/`:
```
[TIMESTAMP] [INFO] PROCESSED | test_notes.txt | SUCCESS | Moved to Done/Documents/
[TIMESTAMP] [INFO] PROCESSED | test_data.csv | SUCCESS | Moved to Done/Data/
[TIMESTAMP] [INFO] PROCESSED | test_image.png | SUCCESS | Moved to Done/Media/
```

**✅ Test 4 Success Criteria**:
- All 3 files processed successfully
- Files moved to correct categories
- Task files completed with analysis
- Dashboard shows 3 completions
- Logs capture all actions
- No errors

---

## 🧪 Test 5: Priority Detection

Test that the watcher correctly assigns priorities.

### High Priority Files

Drop these in Inbox:
- `urgent_report.xlsx` (Excel = HIGH)
- `IMPORTANT_memo.txt` (keyword = HIGH)
- `invoice_Q1.csv` (CSV = HIGH)

**Expected**: Task files show Priority: 🔴 HIGH

### Medium Priority Files

Drop these:
- `notes.md` (Markdown = MEDIUM)
- `script.py` (Code = MEDIUM)
- `document.pdf` (Document = MEDIUM)

**Expected**: Task files show Priority: 🟡 MEDIUM

### Low Priority Files

Drop these:
- `photo.jpg` (Image = LOW)
- `screenshot.png` (Image = LOW)

**Expected**: Task files show Priority: 🟢 LOW

### Unknown Files

Drop:
- `data.xyz` (Unknown extension)

**Expected**: Task files show Priority: 🟣 NEEDS_REVIEW

**✅ Test 5 Success Criteria**:
- Priorities assigned correctly based on file type
- Keywords detected (urgent, important)
- Unknown types flagged for review

---

## 🧪 Test 6: Error Handling

Test how the system handles errors gracefully.

### Test: Non-existent File

1. Manually create a task file in Needs_Action with a fake filename
2. Try to process it with Claude

**Expected**: Error logged, processing continues with other files

### Test: Locked File

1. Drop file in Inbox
2. Open file in Notepad (locks it on Windows)
3. Try to process

**Expected**: Error logged, file skipped or handled gracefully

### Test: Invalid Characters

Drop file with special characters:
- `test@file#2024.txt`

**Expected**: Watcher handles filename, creates safe task name

**✅ Test 6 Success Criteria**:
- Errors logged appropriately
- System doesn't crash
- Other files still process
- Dashboard shows error count if applicable

---

## 🧪 Test 7: Multiple File Types

Test comprehensive file type handling.

### Create Test Files

1. **Text**: `notes.txt`, `readme.md`
2. **Data**: `data.csv`, `config.json`, `data.xml`
3. **Code**: `script.py`, `app.js`, `style.css`, `index.html`
4. **Images**: `photo.jpg`, `diagram.png`, `icon.gif`
5. **Documents**: `report.pdf`, `letter.docx`

Drop all in Inbox folder.

### Process All Files

Run `/skill process_inbox`

### Verify Categorization

Check Done folder structure:
```
Done\
├── Documents\    (text, md, pdf, docx)
├── Data\         (csv, json, xml)
├── Code\         (py, js, css, html)
└── Media\        (jpg, png, gif)
```

**✅ Test 7 Success Criteria**:
- All file types categorized correctly
- Analysis appropriate for each type
- No files in wrong category

---

## 🧪 Test 8: Continuous Operation

Test that the system runs continuously without intervention.

### Setup Continuous Test

1. Start watcher in one terminal
2. Start Claude Code in another terminal
3. Drop 1-2 files in Inbox
4. Wait 30 seconds
5. In Claude, run `/skill process_inbox`
6. Verify processing
7. Drop 2-3 more files
8. Wait 30 seconds
9. Run skill again
10. Verify processing

### Monitor Resources

While running:
- Check Task Manager
- Python process should use ~50-100MB RAM
- Claude Code should use ~300-500MB RAM
- No memory leaks over time

**✅ Test 8 Success Criteria**:
- Watcher runs indefinitely without crashing
- Can process multiple batches
- Memory usage stable
- No performance degradation

---

## 🧪 Test 9: Dashboard Refresh

Test the update_dashboard skill.

### Manually Update Dashboard

In Claude Code:
```
/skill update_dashboard
```

**Expected**:
- File counts refreshed
- Recent activity updated
- Timestamp updated
- All statistics accurate

### Verify Accuracy

Manually count:
- Files in each folder
- Entries in today's log

Compare to Dashboard numbers.

**✅ Test 9 Success Criteria**:
- Dashboard reflects actual state
- Counts are accurate
- Recent activity matches log
- No stale data

---

## 🧪 Test 10: End-to-End Workflow

Complete workflow from file drop to completion.

### Workflow Steps

1. **Start System**:
   ```bash
   # Terminal 1
   start_watcher.bat

   # Terminal 2
   claude code --cwd E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault
   ```

2. **Drop File**: `project_plan.txt` in Inbox

3. **Observe**:
   - Watcher detects (within 30s)
   - Task created in Needs_Action
   - Log entry created

4. **Process**:
   ```
   /skill process_inbox
   ```

5. **Verify**:
   - File moved to Done/Documents/
   - Task completed
   - Dashboard updated
   - Log entry added

6. **View Results**:
   - Open Dashboard in VS Code
   - See updated statistics
   - Read completed task file
   - Check log file

**✅ Test 10 Success Criteria**:
- Complete workflow works without manual intervention
- All components work together
- Results visible in Dashboard
- Full audit trail in logs

---

## 📊 Final Verification Checklist

After all tests, verify:

### Functionality
- [x] Watcher detects files automatically
- [x] Task files created correctly
- [x] Priority assigned appropriately
- [x] Claude can read all files
- [x] Processing skill works
- [x] Files categorized correctly
- [x] Dashboard updates accurately
- [x] Logs capture all activity
- [x] Error handling works

### Performance
- [x] Watcher uses <100MB RAM
- [x] No memory leaks during continuous operation
- [x] Processing completes in reasonable time
- [x] System responsive

### Reliability
- [x] No crashes during testing
- [x] Handles errors gracefully
- [x] Works with various file types
- [x] Continuous operation stable

### Usability
- [x] Dashboard readable in VS Code
- [x] Easy to start watcher (batch file)
- [x] Clear log messages
- [x] Instructions in README work

---

## 🐛 Troubleshooting Common Issues

### Watcher doesn't start
```bash
# Check Python installation
python --version

# Check venv activation
.\venv\Scripts\activate

# Check dependencies
pip list
```

### Files not detected
- Verify Inbox path is correct
- Check watcher terminal for errors
- Ensure file isn't hidden or locked
- Wait full 30 seconds

### Claude can't read files
- Use --cwd flag with absolute path
- Verify file permissions
- Check file isn't corrupted

### Skills don't work
- Skills folder might not be accessible
- Use manual commands instead
- Check skill file syntax

### Files won't move
- Check file isn't open in another program
- Verify destination folder exists
- Check permissions

---

## ✅ Bronze Tier Passing Criteria

Your implementation passes Bronze tier if:

1. ✅ **Core Workflow Works**:
   - Watcher detects files
   - Tasks created automatically
   - Claude processes tasks
   - Files organized in Done/
   - Dashboard updates

2. ✅ **All Components Present**:
   - Folder structure complete
   - Dashboard.md and Company_Handbook.md
   - Watcher scripts functional
   - Agent Skills exist (even if used manually)
   - Logging works

3. ✅ **Documentation Complete**:
   - README with setup instructions
   - Testing guide (this file)
   - Code comments
   - Architecture explained

4. ✅ **Demo-able**:
   - Can show complete workflow
   - Results visible in Dashboard
   - Logs prove activity
   - Reproducible by others

---

## 📹 Demo Recording Checklist

Record a video showing:

1. **Introduction** (1 min):
   - Project overview
   - Architecture diagram
   - Goals of Bronze tier

2. **Setup** (2 min):
   - Folder structure in Explorer
   - Dashboard in VS Code preview
   - Python environment

3. **Live Demo** (5 min):
   - Start watcher
   - Drop test files
   - Show detection
   - Start Claude Code
   - Run processing skill
   - Show results in Done/
   - Show updated Dashboard
   - Show log entries

4. **Conclusion** (1 min):
   - Success criteria met
   - Next steps (Silver tier)
   - Lessons learned

---

## 🎉 Success!

If all tests pass, congratulations! You have a working Bronze tier AI Employee.

**Next steps**:
1. Use it daily for a week
2. Note improvement opportunities
3. Plan Silver tier upgrades
4. Share your implementation

---

*Happy testing! 🚀*
