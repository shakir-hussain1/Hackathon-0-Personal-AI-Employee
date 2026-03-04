# ⚡ Quick Start Guide - Personal AI Employee

Get your AI Employee running in 5 minutes!

---

## 🎯 Prerequisites Check

Before starting, verify you have:
- ✅ Windows 10/11
- ✅ Python 3.13+ installed (`python --version`)
- ✅ VS Code installed
- ✅ Claude Code CLI installed (`claude --version`)

---

## 🚀 Setup (3 minutes)

### Step 1: Install Python Dependencies

Open Command Prompt or PowerShell in the project directory:

```bash
cd E:\Hackathon-0-Personal-AI-Employee

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Expected**: "Successfully installed watchdog-4.0.0 python-dotenv-1.0.0"

### Step 2: Open VS Code Workspace

1. Open VS Code
2. File → Open Folder
3. Navigate to: `E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault`
4. Click "Select Folder"

### Step 3: View Dashboard

In VS Code:
1. Click on `Dashboard.md` in the Explorer
2. Press `Ctrl+Shift+V` to open markdown preview
3. You should see the dashboard with initial stats!

---

## 🎮 Usage (2 minutes)

### Start the Watcher

**Option 1 - Batch File** (Easiest):
```bash
start_watcher.bat
```

**Option 2 - Manual**:
```bash
.\venv\Scripts\activate
python watchers\filesystem_watcher.py
```

**Expected Output**:
```
============================================================
[AI] FileSystemWatcher Active
============================================================
Vault: E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault
Check Interval: 30 seconds
Monitoring started...
============================================================
```

**Keep this terminal running!**

---

## 📝 Test the System

### Test 1: Drop a File

1. Create a text file with any content
2. Save it in: `AI_Employee_Vault\Inbox\test.txt`
3. Wait 30 seconds
4. Watch the watcher terminal - you should see:
   ```
   [INFO] Detected new file: test.txt
   [INFO] Created task: FILE_test_[timestamp].md [Priority: MEDIUM]
   ```

### Test 2: Process with Claude Code

Open a NEW terminal (keep watcher running):

```bash
cd E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault
claude code
```

In Claude Code session, type:
```
/skill process_inbox
```

**OR** if skills don't work, use manual command:
```
Please process all tasks in Needs_Action folder according to Company_Handbook.md.
For each task: read the original file, analyze it, update the task file,
move files to Done/, log activity, and update Dashboard.md
```

### Test 3: View Results

1. In VS Code, refresh Dashboard.md (or it auto-updates)
2. Check `Done/` folder - your file should be there, categorized!
3. Check `Logs/` folder - see activity log with timestamps
4. Open completed task file in `Done/` - see the AI's analysis

---

## ✅ Verification Checklist

Your system is working if:

- [x] Watcher starts without errors
- [x] Detects files within 30 seconds
- [x] Creates task files in `Needs_Action/`
- [x] Claude Code can read vault files
- [x] Processing moves files to `Done/`
- [x] Dashboard shows updated statistics
- [x] Logs capture all activity

---

## 🎬 Daily Workflow

### Morning Routine:
1. Start watcher: `start_watcher.bat`
2. Drop files in Inbox throughout the day
3. Watcher automatically detects them

### Processing Routine (run as needed):
1. Open Claude Code: `claude code --cwd [vault_path]`
2. Run: `/skill process_inbox`
3. Check Dashboard for results
4. Review organized files in `Done/`

### Evening Review:
1. Check Dashboard for day's activity
2. Review `Done/` folder organization
3. Check logs for any errors
4. Stop watcher (Ctrl+C)

---

## 🐛 Quick Troubleshooting

### Watcher won't start
```bash
# Check Python
python --version

# Check venv
.\venv\Scripts\activate

# Check dependencies
pip list | findstr watchdog
```

### Files not detected
- Wait full 30 seconds
- Check watcher terminal for errors
- Verify file is in correct Inbox folder
- Ensure file isn't locked/open

### Claude Code can't read files
```bash
# Use absolute path with --cwd
claude code --cwd E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault

# Test file access
Read Dashboard.md
```

### Skills not working
- Use manual commands instead (see Test 2 above)
- Skills folder may not be in Claude's path
- Manual commands work just as well!

---

## 📊 What Each Component Does

### 1. Watcher (Python Script)
- Monitors `Inbox/` folder every 30 seconds
- Detects new files automatically
- Creates structured task files in `Needs_Action/`
- Logs all detections

### 2. Claude Code (AI Processing)
- Reads task files from `Needs_Action/`
- Analyzes original files from `Inbox/`
- Creates summaries and extracts key info
- Organizes files into `Done/` categories
- Updates Dashboard with statistics
- Logs all processing

### 3. Dashboard (VS Code)
- Shows real-time system status
- Displays task queue and completion count
- Lists recent activity
- Human-readable markdown format

### 4. Logs (Audit Trail)
- Daily log files in `Logs/` folder
- Timestamps for all activities
- Complete audit trail
- Useful for debugging

---

## 🎯 Next Steps

Once comfortable with basic operation:

1. **Test Different File Types**:
   - Documents (.txt, .pdf, .docx)
   - Spreadsheets (.csv, .xlsx)
   - Images (.jpg, .png)
   - Code files (.py, .js)

2. **Review AI Analysis**:
   - Check completed task files in `Done/`
   - See how AI categorizes different types
   - Notice priority assignment

3. **Monitor Dashboard**:
   - Watch statistics update in real-time
   - Track daily productivity
   - Review recent activity log

4. **Customize Behavior**:
   - Edit `Company_Handbook.md` to change rules
   - Adjust watcher interval in `filesystem_watcher.py`
   - Add new file type classifications

---

## 📚 More Information

- **Full Documentation**: See `README.md`
- **Detailed Testing**: See `TESTING_GUIDE.md`
- **Architecture**: See plan document or README
- **Troubleshooting**: See README troubleshooting section

---

## 🎉 Success!

If you can:
1. ✅ Start the watcher
2. ✅ Drop a file
3. ✅ See it detected
4. ✅ Process with Claude
5. ✅ View results in Dashboard

**Congratulations! Your AI Employee is working!** 🚀

Now you can:
- Use it for organizing documents
- Let it run continuously
- Process files throughout the day
- Review organized results anytime

---

## 🆘 Need Help?

1. Check the watcher terminal for error messages
2. Check today's log file in `Logs/`
3. Review `TESTING_GUIDE.md` for detailed tests
4. Check `README.md` for comprehensive documentation

---

*Get started now by running `start_watcher.bat`!*
