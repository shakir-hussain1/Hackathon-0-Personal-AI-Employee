# 🎬 Demo Script - Personal AI Employee

Use this script for a 5-10 minute live demonstration of the Bronze tier implementation.

---

## 🎯 Demo Objectives

Show that the AI Employee can:
1. Automatically detect files
2. Create structured tasks
3. Analyze content intelligently
4. Organize files by category
5. Update dashboard in real-time
6. Maintain complete audit logs

---

## 🎬 Demo Script (10 minutes)

### Introduction (1 minute)

**Say**:
> "I'm going to demonstrate a local-first autonomous AI Employee that monitors folders, processes files automatically, and maintains a knowledge base in VS Code. This is the Bronze tier - the foundation layer that proves the concept."

**Show**:
- Project folder structure in Windows Explorer
- Open VS Code with AI_Employee_Vault folder

---

### Part 1: The Vault (2 minutes)

**Say**:
> "The 'vault' is the AI's brain - all markdown files that Claude Code can read and write to. Let me show you the key files."

**Show**:

1. **Open `Dashboard.md`** in VS Code
   - Press `Ctrl+Shift+V` for preview
   - Point out: System Status table, Watcher status, Activity log
   - **Say**: "This updates in real-time as files are processed"

2. **Open `Company_Handbook.md`**
   - Scroll through sections
   - Point out: Core principles, File processing rules, Priority levels
   - **Say**: "This defines how the AI behaves - it's the employee handbook"

3. **Show folder structure** in VS Code Explorer
   - Inbox (file drop)
   - Needs_Action (task queue)
   - Done (organized results)
   - Logs (audit trail)

---

### Part 2: Starting the Watcher (1 minute)

**Say**:
> "The watcher is Python script that monitors the Inbox folder every 30 seconds and creates tasks when it detects new files."

**Do**:
1. Open Command Prompt
2. Navigate to project folder:
   ```bash
   cd E:\Hackathon-0-Personal-AI-Employee
   ```
3. Run the watcher:
   ```bash
   start_watcher.bat
   ```

**Show**:
- Terminal output showing watcher active
- Point out: Vault path, Check interval, "Monitoring started"
- **Say**: "This will run continuously, 24/7 if needed"

**Keep this terminal visible!**

---

### Part 3: Creating Test Files (1 minute)

**Say**:
> "Let me create a few test files to show how it handles different types. In real usage, you'd just drag and drop files from email, downloads, etc."

**Do**:
1. Open Notepad, create `meeting_notes.txt`:
   ```
   Team Meeting - Q1 Planning
   Date: 2026-02-16
   Attendees: Alice, Bob, Charlie

   Key Points:
   - Budget approved for Q1
   - New project launches March 1st
   - Hiring 2 new engineers

   Action Items:
   - Alice: Send project timeline
   - Bob: Update website
   - Charlie: Schedule follow-ups
   ```
   Save to: `AI_Employee_Vault\Inbox\meeting_notes.txt`

2. Create simple CSV `team_data.csv`:
   ```
   Name,Role,Email
   Alice,Manager,alice@company.com
   Bob,Designer,bob@company.com
   Charlie,Developer,charlie@company.com
   ```
   Save to: `AI_Employee_Vault\Inbox\team_data.csv`

3. Save any screenshot/image as `diagram.png` to Inbox

**Say**:
> "I've dropped three files: a text document, a CSV file, and an image. Let's watch the watcher detect them."

---

### Part 4: Automatic Detection (1 minute)

**Watch the watcher terminal** (may need to wait up to 30 seconds)

**Point out when logs appear**:
```
[INFO] Detected new file: meeting_notes.txt
[INFO] Created task: FILE_meeting_notes_[timestamp].md [Priority: MEDIUM]
[INFO] Detected new file: team_data.csv
[INFO] Created task: FILE_team_data_[timestamp].md [Priority: HIGH]
[INFO] Detected new file: diagram.png
[INFO] Created task: FILE_diagram_[timestamp].md [Priority: LOW]
```

**Say**:
> "Notice it detected all three files and assigned priorities automatically:
> - CSV is HIGH (could be important data)
> - Text is MEDIUM (standard document)
> - Image is LOW (visual content)"

**Show in VS Code**:
- Open `Needs_Action` folder
- Show the three task files created
- Open one task file, point out:
  - Status: PENDING
  - Priority with emoji
  - File information
  - Empty analysis section (AI will fill this)

---

### Part 5: AI Processing (3 minutes)

**Say**:
> "Now Claude Code will act as the AI Employee, reading these tasks and processing them according to the Company Handbook."

**Do**:
1. Open new terminal (keep watcher running!)
2. Start Claude Code:
   ```bash
   claude code --cwd E:\Hackathon-0-Personal-AI-Employee\AI_Employee_Vault
   ```

3. Once Claude starts, run:
   ```
   /skill process_inbox
   ```

   **OR** if skills don't work:
   ```
   Please process all tasks in Needs_Action folder according to Company_Handbook.md.
   Read each task, analyze the original file, update the task with your analysis,
   move files to Done/, log activity, and update Dashboard.md.
   ```

**Watch Claude work**:
- Point out as it reads files
- Point out as it analyzes content
- Point out as it updates tasks
- Point out as it moves files

**Say while processing**:
> "Watch how it:
> 1. Reads each task file
> 2. Reads the original file
> 3. Analyzes the content
> 4. Extracts key information
> 5. Updates the task with its analysis
> 6. Moves files to appropriate categories
> 7. Logs everything"

---

### Part 6: Viewing Results (2 minutes)

**After processing completes:**

**1. Show Dashboard** (in VS Code):
- Refresh or reopen `Dashboard.md`
- Point out updated statistics:
  - Files in Inbox: 0 (cleared!)
  - Tasks Pending: 0 (all processed!)
  - Tasks Completed Today: 3
  - Recent activity shows the 3 files

**Say**:
> "The Dashboard now shows all files processed, inbox cleared, and recent activity logged."

**2. Show Done folder**:
Navigate in VS Code Explorer:
- `Done/Documents/` - contains `meeting_notes.txt`
- `Done/Data/` - contains `team_data.csv`
- `Done/Media/` - contains `diagram.png`
- `Done/` - contains the three completed task files

**Say**:
> "Files automatically organized by category. The AI determined the right place for each based on file type."

**3. Open a completed task file** (e.g., `FILE_meeting_notes_[timestamp].md`):
- Point out: Status changed to COMPLETED
- Point out: Analysis section filled in
- Point out: Key information extracted
- Point out: Action items identified
- Point out: Processing timestamp

**Say**:
> "The AI read the meeting notes, extracted the key points, identified action items, and created this summary automatically."

**4. Show today's log** (`Logs/2026-02-16.log`):
- Scroll through entries
- Point out: Timestamps, file names, results
- Point out: Complete audit trail

**Say**:
> "Every action is logged with timestamps. This provides a complete audit trail of what the AI did."

---

### Conclusion (1 minute)

**Summarize**:
> "So in summary, this Bronze tier implementation:
>
> ✅ Automatically monitors a folder 24/7
> ✅ Detects new files within 30 seconds
> ✅ Creates structured task files
> ✅ Uses Claude Code as the 'AI brain' to analyze content
> ✅ Intelligently categorizes and organizes files
> ✅ Updates a real-time dashboard
> ✅ Maintains complete activity logs
> ✅ All local-first, privacy-respecting, human-readable
>
> This proves the autonomous AI Employee concept works. Future tiers will add:
> - Email monitoring (Silver)
> - Social media posting (Silver/Gold)
> - Accounting integration (Gold)
> - Cloud deployment (Platinum)
>
> But the foundation is here and working!"

**Show**:
- Final Dashboard with statistics
- Organized Done folder
- Complete log file

---

## 🎥 Recording Tips

### Before Recording:

1. **Clean slate**:
   - Clear Inbox folder
   - Clear Needs_Action folder
   - Clear Done folder (or move to archive)
   - Delete today's log (for fresh start)

2. **Prepare test files**:
   - Have them ready on desktop
   - Easy to drag-drop during demo

3. **Test run**:
   - Do a practice run to verify everything works
   - Note any timing issues (30-second detection wait)

4. **Window arrangement**:
   - VS Code on left half
   - Terminals on right half
   - Easy to show both

### During Recording:

1. **Speak clearly**:
   - Explain what you're doing
   - Explain what's happening
   - Point out key features

2. **Be patient**:
   - Wait for 30-second detection
   - Don't rush through Claude's processing
   - Let the system work

3. **Show, don't just tell**:
   - Open files to show content
   - Show the actual code briefly
   - Show the folder structure

4. **Handle errors gracefully**:
   - If something doesn't work, explain it
   - Show logs to debug
   - Demonstrate error handling

### After Recording:

1. **Edit**:
   - Cut dead time (waiting for detection)
   - Speed up long processing (optional)
   - Add titles/annotations

2. **Length**:
   - Aim for 5-10 minutes
   - Can be longer if comprehensive
   - Don't rush through key points

---

## 🎬 Quick Demo (5 minutes, abbreviated)

For a faster demo:

1. **Introduction** (30 seconds): Show Dashboard and handbook
2. **Start watcher** (30 seconds): Run start_watcher.bat
3. **Drop file** (30 seconds): One test file in Inbox
4. **Show detection** (30 seconds): Watch watcher log
5. **Process with Claude** (2 minutes): Run /skill process_inbox
6. **Show results** (1 minute): Dashboard, Done folder, logs
7. **Conclusion** (30 seconds): Summarize capabilities

---

## 📝 Demo Talking Points

### Key Messages:

1. **Autonomous**: "Runs 24/7, no human intervention needed for detection"
2. **Intelligent**: "Uses Claude's AI to understand and analyze content"
3. **Organized**: "Automatically categorizes by file type"
4. **Transparent**: "Complete logs, real-time dashboard, human-readable"
5. **Local-First**: "All data stays on your machine, privacy-respecting"
6. **Extensible**: "Foundation for Silver, Gold, Platinum tiers"

### Common Questions:

**Q: How fast does it detect files?**
A: Within 30 seconds. Configurable in the code.

**Q: What file types can it handle?**
A: Documents, spreadsheets, images, code files, emails - 20+ types.

**Q: Does it delete files?**
A: No, it only moves them. Originals are preserved.

**Q: Can I customize the behavior?**
A: Yes, edit Company_Handbook.md to change rules.

**Q: How much RAM does it use?**
A: About 600MB total (watcher + Claude Code).

**Q: Can it run on a server?**
A: Bronze tier is local. Platinum tier will add cloud deployment.

---

## ✅ Demo Checklist

Before starting demo:

- [ ] Watcher script tested and working
- [ ] Claude Code installed and working
- [ ] VS Code can open vault
- [ ] Test files prepared
- [ ] Dashboard displays correctly
- [ ] Logs folder empty (or archived)
- [ ] Inbox empty
- [ ] Done folder empty (or archived)
- [ ] Terminal windows arranged
- [ ] Screen recording software ready
- [ ] Microphone tested

---

## 🎉 Demo Success!

After demo, you should have shown:
- ✅ Complete autonomous workflow
- ✅ File detection and task creation
- ✅ AI processing and analysis
- ✅ Automatic organization
- ✅ Real-time dashboard updates
- ✅ Complete audit logs

**Audience should understand**:
- How the system works
- Why it's useful
- How they could use it
- What future tiers will add

---

*Good luck with your demo! 🚀*
