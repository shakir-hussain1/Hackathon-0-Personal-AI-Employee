# 🤖 Personal AI Employee - Bronze Tier

**Version**: 1.0 (Foundation)
**Status**: Ready for Testing
**Tier**: Bronze (8-12 hour implementation)

---

## 📖 Overview

This project implements a **local-first autonomous AI employee** that:
- ✅ Monitors a file drop folder (Inbox) 24/7
- ✅ Automatically analyzes incoming files
- ✅ Organizes and categorizes content
- ✅ Maintains a knowledge base in VS Code
- ✅ Logs all activities for audit trail
- ✅ Works within 8GB RAM constraints

**Why This Matters**: Transforms Claude Code from a "tool you prompt" into a "digital employee that acts autonomously."

---

## 🏗️ Architecture

```
[Drop File in Inbox]
    ↓
[Python Watcher] detects new file every 30s
    ↓
[Creates Task] in Needs_Action folder
    ↓
[Claude Code] processes via Agent Skill
    ↓
[Analyzes + Organizes + Logs] automatically
    ↓
[Updates Dashboard] with statistics
```

### Key Components

1. **VS Code Vault** (`AI_Employee_Vault/`): The AI's "brain"
   - Markdown-based knowledge base
   - Human-readable, version-controllable
   - Viewable with VS Code's built-in markdown preview

2. **Python Watcher** (`watchers/`): The AI's "eyes"
   - Monitors Inbox folder continuously
   - Detects new files
   - Creates structured task files

3. **Agent Skills** (`skills/`): The AI's "instructions"
   - Reusable behavior templates
   - Process inbox tasks
   - Update dashboard statistics

4. **Dashboard** (`Dashboard.md`): The AI's "status board"
   - Real-time system statistics
   - Activity log
   - Task queue visibility

---

## 📁 Project Structure

```
E:\Hackathon-0-Personal-AI-Employee\
├── AI_Employee_Vault\          # VS Code workspace (the brain)
│   ├── Dashboard.md            # ⭐ Main control panel
│   ├── Company_Handbook.md     # AI behavior rules
│   ├── Inbox\                  # 📥 Drop files here!
│   ├── Needs_Action\           # ⏳ Auto-generated tasks
│   ├── Done\                   # ✅ Processed files
│   │   ├── Documents\
│   │   ├── Data\
│   │   ├── Media\
│   │   ├── Communications\
│   │   ├── Code\
│   │   └── Uncategorized\
│   ├── Plans\                  # Future: planning documents
│   └── Logs\                   # Daily activity logs
│
├── watchers\                   # Python monitoring scripts
│   ├── __init__.py
│   ├── base_watcher.py         # Template class
│   └── filesystem_watcher.py   # Bronze tier watcher
│
├── skills\                     # Claude Code Agent Skills
│   ├── process_inbox.md        # Main processing skill
│   └── update_dashboard.md     # Dashboard refresh skill
│
├── orchestrator\               # Future: automation coordinator
│
├── venv\                       # Python virtual environment
├── requirements.txt            # Python dependencies
├── .gitignore                  # Excludes logs, venv, etc.
└── README.md                   # This file
```

---

## 🚀 Quick Start Guide

### Prerequisites

- ✅ Windows 10/11 (8GB RAM minimum)
- ✅ Python 3.13+ installed
- ✅ VS Code installed
- ✅ Claude Code CLI installed
- ✅ Node.js v24+ (for Claude Code)

### Installation (5 minutes)

#### Step 1: Setup Python Environment

Open terminal in project directory:

```bash
cd E:\Hackathon-0-Personal-AI-Employee

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output**: Successfully installed watchdog and python-dotenv

#### Step 2: Open VS Code Workspace

1. Open VS Code
2. File → Open Folder
3. Select: `E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault`
4. Open `Dashboard.md`
5. Press `Ctrl+Shift+V` to open markdown preview

**Result**: You should see the Dashboard with initial statistics!

#### Step 3: Verify Folder Structure

Check that these folders exist in `AI_Employee_Vault/`:
- Inbox
- Needs_Action
- Done
- Logs

All should be empty initially.

---

## 🎮 How to Use

### Daily Workflow

#### 1. Start the Watcher (Terminal 1)

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Start file system watcher
python watchers\filesystem_watcher.py
```

**Expected output**:
```
============================================================
🤖 FileSystemWatcher Active
============================================================
📁 Vault: E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault
⏱️  Check Interval: 30 seconds
🔄 Monitoring started...
============================================================
```

**Keep this terminal running!**

#### 2. Drop Files in Inbox

Navigate to `AI_Employee_Vault\Inbox\` and drop any file:
- Documents (.txt, .md, .pdf, .docx)
- Spreadsheets (.xlsx, .csv)
- Images (.jpg, .png)
- Code files (.py, .js, .html)
- Emails (.eml, .msg)

**What happens**:
- Watcher detects file within 30 seconds
- Creates task file in `Needs_Action/`
- Logs detection
- Prints: "Detected new file: [filename]"

#### 3. Process with Claude Code (Terminal 2)

Open new terminal:

```bash
# Navigate to vault
claude code --cwd E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault

# Once Claude Code starts, run:
/skill process_inbox
```

**Alternative** (manual command if skills don't work):
```
Read all task files in Needs_Action, process them according to Company_Handbook.md,
and update Dashboard.md
```

**What happens**:
- Claude reads task files
- Analyzes original files
- Creates summaries
- Moves files to Done/
- Updates Dashboard
- Logs all activity

#### 4. View Results

In VS Code:
1. Refresh `Dashboard.md` (or it auto-updates)
2. Check `Done/` folder - files organized by category
3. Check `Logs/` folder - see today's activity log

---

## 📊 Viewing the Dashboard

### Method 1: VS Code Markdown Preview (Recommended)

1. Open `AI_Employee_Vault` folder in VS Code
2. Click `Dashboard.md` in Explorer
3. Press `Ctrl+Shift+V` (or click preview icon)
4. See live statistics and recent activity!

### Method 2: Direct File View

Simply open `Dashboard.md` in any text editor to see the raw markdown with all information.

### Method 3: Browser

Right-click `Dashboard.md` → Open With → Browser (if you have a markdown viewer extension)

---

## 🔍 Testing the System

### Basic Test (5 minutes)

#### Test 1: Text File

1. Create `test_document.txt` with content:
   ```
   This is a test document for the AI Employee.
   Task: Review quarterly budget.
   Deadline: End of week.
   ```

2. Drop in `Inbox/`

3. Wait 30 seconds - watcher should detect it

4. Run Claude Code:
   ```bash
   claude code --cwd E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault
   ```

5. Execute: `/skill process_inbox`

6. Verify:
   - ✅ Task file created in `Needs_Action/`
   - ✅ File analyzed and summarized
   - ✅ Moved to `Done/Documents/`
   - ✅ Dashboard shows: 1 task completed
   - ✅ Log entry created

#### Test 2: Multiple Files

Drop 3 different files:
- `budget.csv`
- `screenshot.png`
- `notes.md`

Wait for detection, then process all at once.

**Expected**: All 3 processed, categorized correctly, Dashboard shows 3 completions.

---

## 🛠️ Troubleshooting

### Issue: Watcher doesn't detect files

**Solution**:
```bash
# Verify path
python
>>> from pathlib import Path
>>> Path(r"E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault\Inbox").exists()
True

# Check watcher is running
# Should see "🤖 FileSystemWatcher Active"

# Try dropping file while watching terminal
```

### Issue: Claude Code can't read files

**Solution**:
```bash
# Use absolute path with --cwd flag
claude code --cwd E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault

# Inside Claude, test:
Read Dashboard.md
```

### Issue: Files don't move to Done

**Solution**:
- Verify `Done/` folder exists
- Check file isn't open in another program
- Look for error in Claude's output
- Check today's log file for details

### Issue: Skills not found

**Solution**:
- Skills are in `E:\Hackathon-0-Personal-AI-Employee\skills\`
- Claude runs from vault, so skills are outside working directory
- Use manual commands instead:
  ```
  Read Needs_Action folder, process tasks per Company_Handbook.md
  ```

### Issue: Permission errors

**Solution**:
```bash
# Run terminal as administrator
# Or check file permissions in Windows Explorer
```

---

## 📈 System Requirements

### Hardware

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8GB | 16GB |
| Storage | 10GB free | 20GB free |
| CPU | Dual-core | Quad-core |

### Memory Usage (8GB RAM)

- Windows OS: ~2.5GB
- Python Watcher: ~50MB
- Claude Code: ~300MB
- VS Code: ~150MB
- **Total**: ~3GB
- **Available**: ~5GB ✅

### Storage Usage

- Project files: ~50MB
- Python venv: ~200MB
- Logs (30 days): ~10MB
- **Total**: ~260MB

---

## 🎯 Bronze Tier Features

### ✅ Implemented

- [x] File system monitoring (Inbox folder)
- [x] Automatic task creation
- [x] File analysis and summarization
- [x] Intelligent categorization
- [x] Activity logging
- [x] Dashboard with real-time stats
- [x] VS Code markdown preview
- [x] Company Handbook (AI rules)
- [x] Agent Skills for reusable behaviors
- [x] Priority determination (HIGH/MEDIUM/LOW)
- [x] Error handling and logging
- [x] Resource optimization for 8GB RAM

### 🚫 Not Yet Implemented (Future Tiers)

- [ ] Gmail monitoring (Silver tier)
- [ ] Email sending via MCP (Silver tier)
- [ ] Social media automation (Silver/Gold tier)
- [ ] Accounting integration (Gold tier)
- [ ] Cloud deployment (Platinum tier)
- [ ] Scheduled automation (Silver tier)
- [ ] Human approval workflow (Silver tier)

---

## 🔐 Security & Privacy

### Local-First Architecture

- ✅ All data stays on your machine
- ✅ No cloud dependencies (except Claude API)
- ✅ Human-readable files (markdown)
- ✅ Version-controllable with Git
- ✅ No external API calls (except Claude Code)

### Best Practices

1. **Don't commit sensitive files**:
   - `.gitignore` excludes `Logs/` and `Done/`
   - Review files before committing

2. **Backup your vault**:
   - Regular backups of `AI_Employee_Vault/`
   - Consider Git for version control

3. **Review AI actions**:
   - Check daily logs in `Logs/`
   - Verify file movements in `Done/`

---

## 📚 How It Works (Technical Details)

### File Detection Flow

1. **FileSystemWatcher** runs in infinite loop
2. Every 30 seconds, scans `Inbox/` for files
3. Compares to `processed_files` set (avoids duplicates)
4. For each new file:
   - Determines priority based on extension and filename
   - Creates task markdown file in `Needs_Action/`
   - Logs detection event
   - Adds to `processed_files` set

### Task Processing Flow

1. **Claude Code** invoked with `/skill process_inbox`
2. Lists all `.md` files in `Needs_Action/`
3. For each task:
   - Reads task metadata
   - Reads original file from `Inbox/`
   - Analyzes content based on file type
   - Updates task with summary
   - Moves original to `Done/[category]/`
   - Moves task to `Done/`
   - Logs action to `Logs/[date].log`
4. Updates `Dashboard.md` with new statistics

### Dashboard Update Flow

1. Counts files in each folder
2. Reads today's log for recent activity
3. Formats statistics into markdown table
4. Updates "Last Updated" timestamp
5. Saves updated `Dashboard.md`

---

## 🎓 Learning Resources

### Understanding the Architecture

- **Watchers**: Autonomous monitoring scripts that detect events
- **Agent Skills**: Reusable instruction templates for Claude Code
- **Vault**: Centralized knowledge base (markdown files)
- **Task Files**: Structured communication between watcher and AI

### Key Concepts

- **Local-First**: Data stored locally, privacy-centric
- **Autonomous**: Minimal human intervention required
- **Transparent**: All actions logged and visible
- **Composable**: Skills can be combined and reused

---

## 🚀 Next Steps (Upgrading to Silver Tier)

Once Bronze is working, you can add:

### Silver Tier (20-30 hours)

1. **Gmail Watcher**:
   - OAuth setup for Gmail API
   - Monitor inbox for new emails
   - Create tasks from emails
   - Extract attachments

2. **Email Sending (MCP)**:
   - Implement Model Context Protocol server
   - Send drafted emails
   - Human-in-the-loop approval

3. **Task Scheduling**:
   - Windows Task Scheduler integration
   - Automated processing (hourly/daily)
   - No manual triggering needed

4. **Enhanced Analysis**:
   - Sentiment analysis
   - Entity extraction
   - Link relationships between documents

---

## 📝 File Formats

### Task File Format (in Needs_Action/)

```markdown
# 📋 Task: Process File

**Status**: ⏳ PENDING
**Priority**: 🟡 MEDIUM
**Created**: 2026-02-16 14:30:22

## 📁 File Information
- **Filename**: `example.txt`
- **Size**: 1.23 KB
- **Type**: Text Document
- **Location**: `Inbox/example.txt`

## 🎯 Task Instructions
[Standard instructions for AI]

## 📊 Analysis Results
[AI fills this in during processing]

## 📝 Processing Log
**Processed**: [timestamp]
**Status**: ⏳ PENDING → ✅ COMPLETED
```

### Log File Format (in Logs/)

```
[2026-02-16 14:30:22] [INFO] FileSystemWatcher started with 30s interval
[2026-02-16 14:30:55] [INFO] Detected new file: example.txt
[2026-02-16 14:31:10] [INFO] Created task: FILE_example_20260216_143110.md [Priority: MEDIUM]
[2026-02-16 14:32:00] [INFO] PROCESSED | example.txt | SUCCESS | Moved to Done/Documents/
```

---

## 🤝 Contributing

This is a hackathon project, but improvements welcome!

### Ideas for Enhancement

- Add more file type handlers
- Improve priority detection logic
- Add web interface for Dashboard
- Implement search functionality
- Add file tagging system
- Create mobile app view

---

## 📄 License

This project is for educational and personal use.

---

## 🙏 Acknowledgments

- Built with **Claude Code** (Anthropic)
- Uses **watchdog** for file monitoring
- Inspired by the concept of autonomous AI employees
- Part of Hackathon-0: Building Autonomous FTEs

---

## 📞 Support

### Getting Help

1. Check troubleshooting section above
2. Review logs in `Logs/` folder
3. Check `Company_Handbook.md` for AI behavior rules
4. Verify all steps in Quick Start Guide

### Common Questions

**Q: Can I use this with Obsidian instead of VS Code?**
A: Yes! The vault is just markdown files. Open `AI_Employee_Vault` as an Obsidian vault.

**Q: Does this work on Mac/Linux?**
A: The Python code should work cross-platform. Adjust paths in commands.

**Q: How much does Claude API cost?**
A: Depends on usage. Bronze tier processes files locally with minimal API calls.

**Q: Can I process PDFs?**
A: Bronze tier notes PDF properties. Full PDF analysis comes in Silver tier.

**Q: Is my data private?**
A: Yes! Everything is local except Claude API calls for analysis.

---

## ✅ Bronze Tier Success Checklist

Use this to verify your implementation:

- [ ] Folder structure created correctly
- [ ] Dashboard.md displays in VS Code preview
- [ ] Company_Handbook.md exists with rules
- [ ] Python virtual environment works
- [ ] File System Watcher starts without errors
- [ ] Watcher detects files dropped in Inbox
- [ ] Task files created in Needs_Action
- [ ] Claude Code can read vault files
- [ ] `/skill process_inbox` executes successfully
- [ ] Files move from Inbox to Done
- [ ] Files categorized correctly
- [ ] Dashboard updates with statistics
- [ ] Logs capture all activity
- [ ] No hardcoded secrets in code
- [ ] README documentation complete

---

## 🎉 Demo Video Checklist

Record a 5-10 minute video showing:

1. **Project structure** in VS Code
2. **Dashboard** in markdown preview
3. **Start watcher** in terminal
4. **Drop test file** in Inbox
5. **Watcher detection** message
6. **Start Claude Code** with --cwd flag
7. **Execute** /skill process_inbox
8. **Show results**: files in Done, updated Dashboard, log entries
9. **Explain** the autonomous workflow

---

**🚀 Ready to build your AI Employee! Start with the Quick Start Guide above.**

**⭐ Star this repo if you found it useful!**
