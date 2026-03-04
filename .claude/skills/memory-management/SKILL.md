# 🧠 Memory Management Skill

**Purpose**: Use Markdown as efficient long-term memory
**Storage**: Optimized for low footprint
**Format**: Human-readable, version-controllable

---

## 🎯 Core Functions

### 1. 📇 Index Files
Maintain searchable index of all vault content

### 2. 📦 Archive Old Tasks
Move completed tasks to archive, compress history

### 3. 📜 Maintain History
Track changes, preserve context, enable search

### 4. 🔍 Avoid Duplication
Detect similar content, link related items

### 5. 💾 Optimize Storage
Compress archives, remove redundancy, efficient formats

---

## 📊 Memory Architecture

```
AI_Employee_Vault/
├── Active/              # Current working memory
│   ├── Inbox/          # New items (process quickly)
│   ├── Needs_Action/   # Pending tasks (< 7 days)
│   └── In_Progress/    # Active work (< 30 days)
│
├── Done/               # Short-term memory (90 days)
│   ├── 2026-02/       # Monthly folders
│   └── 2026-01/
│
├── Archive/            # Long-term memory (compressed)
│   ├── 2025/          # Yearly archives
│   │   ├── Q4/        # Quarterly
│   │   └── summary.md # Quick reference
│   └── index.md       # Searchable index
│
└── Knowledge/          # Permanent memory
    ├── patterns.md    # Learned patterns
    ├── contacts.md    # People & relationships
    └── reference.md   # Important info
```

---

## 🗂️ Indexing System

### Master Index Format

**File**: `Archive/index.md`

```markdown
# 📇 Master Index

**Last Updated**: 2026-02-16
**Total Items**: 1,250
**Storage**: 15.3 MB

## Quick Stats
- Active Tasks: 12
- Archived Tasks: 1,238
- Unique Topics: 47
- Time Range: 2024-06 to 2026-02

---

## By Topic

### Budget & Finance (89 items)
- [2026-02] Q1 Budget Review → Archive/2026/Q1/budget_review.md
- [2026-01] Expense Report → Archive/2026/Q1/expense_jan.md
- [2025-12] Year End Financial → Archive/2025/Q4/year_end.md

### Team Meetings (156 items)
- [2026-02] Planning Session → Archive/2026/Q1/planning_feb.md
- [2026-02] Weekly Sync → Archive/2026/Q1/weekly_sync_02.md

### Projects (234 items)
...

## By Person

### Alice (Project Manager)
- Mentioned in: 45 files
- Last interaction: 2026-02-15
- Topics: Planning, Budget, Hiring

### Bob (Developer)
- Mentioned in: 67 files
- Last interaction: 2026-02-14
- Topics: Code review, Deployment, Bugs

## By Priority

### HIGH (12 active)
- Payment processing issue → Needs_Action/payment_issue.md
- Contract renewal → Needs_Action/contract_renewal.md

## By Date

### 2026-02 (45 items)
### 2026-01 (67 items)
### 2025-Q4 (234 items)

---

## Search Tags

#urgent #financial #legal #meeting #action-item #follow-up
```

### Auto-Index Generation

**Trigger**: Daily at midnight or after batch processing

**Process**:
1. Scan all folders
2. Extract metadata (date, topic, people, tags)
3. Group by categories
4. Update index.md
5. Compress to index.json (optional for search)

---

## 📦 Archive Strategy

### Archive Rules

**Age-Based**:
- Completed > 90 days → Archive
- In Archive > 1 year → Compress
- In Compress > 2 years → Summary only

**Priority-Based**:
- LOW priority → Archive after 30 days
- MEDIUM priority → Archive after 60 days
- HIGH priority → Archive after 90 days
- CRITICAL → Never auto-archive (manual review)

**Size-Based**:
- Large files (>1MB) → Compress immediately
- Attachments → Move to separate storage
- Images → Thumbnail + compress

### Archive Process

**Monthly Archive** (1st of month):
```markdown
1. Identify candidates:
   - Tasks in Done/ older than 90 days
   - Status = COMPLETED
   - No recent references

2. Create monthly archive:
   Archive/YYYY/MM/
   ├── tasks.md (concatenated tasks)
   ├── summary.md (quick overview)
   └── metadata.json (searchable data)

3. Update index:
   - Add entries to master index
   - Update statistics
   - Generate summary

4. Clean up:
   - Remove archived tasks from Done/
   - Update cross-references
   - Verify no broken links
```

**Yearly Compression** (Jan 1st):
```markdown
1. Previous year's archives:
   Archive/YYYY/
   ├── Q1/ → Compress to Q1.md
   ├── Q2/ → Compress to Q2.md
   ├── Q3/ → Compress to Q3.md
   ├── Q4/ → Compress to Q4.md
   └── year_summary.md (generated)

2. Compression format:
   - Keep: Title, date, summary, outcome
   - Remove: Full details, attachments
   - Preserve: Links to critical items

3. Space savings: ~80% reduction
```

---

## 📜 History Tracking

### Task Lifecycle History

**Format**: Track state changes
```markdown
# Task History: Update Website

**Created**: 2026-01-15 10:00
**Status Changes**:
- 2026-01-15 10:00: PENDING → Created by watcher
- 2026-01-15 14:30: IN_PROGRESS → Assigned to Bob
- 2026-01-18 09:15: COMPLETED → Finished, deployed
- 2026-04-20 00:01: ARCHIVED → Moved to Archive/2026/Q1/

**Mentions**: 3 related tasks
- Design mockups (referenced in this task)
- Deploy to production (follow-up)
- User feedback collection (follow-up)

**Outcome**: Successfully updated website, +15% traffic
```

### Change Log Format

**File**: `Knowledge/changelog.md`
```markdown
# System Change Log

## 2026-02-16
- Archived 67 tasks from January
- Updated contact info for Alice
- Added new pattern: Sprint Planning
- Storage: 15.3 MB (↓ 2.1 MB from compression)

## 2026-02-15
- Processed 5 high-priority tasks
- Created budget summary for Q1
- Updated index with 45 new entries

## 2026-02-14
- Archived Q4 2025 to compressed format
- Storage saved: 8.7 MB
- Total items: 1,250
```

---

## 🔍 Duplication Detection

### Similarity Check

**Method**: Content fingerprinting

**Algorithm**:
```markdown
1. Extract key features:
   - Title (normalized)
   - Main keywords (top 10)
   - Participants (people mentioned)
   - Date (within ±7 days)

2. Calculate similarity:
   - Title match: 40%
   - Keyword overlap: 30%
   - Participants overlap: 20%
   - Date proximity: 10%

3. Threshold:
   - >90% = Duplicate (flag)
   - 70-90% = Similar (link)
   - <70% = Unique
```

**Action on Duplicate**:
```markdown
Option 1: Merge
- Combine content
- Keep newer metadata
- Update all references
- Archive old version

Option 2: Link
- Keep both
- Add "See also:" links
- Note relationship
- Update index

Option 3: Deduplicate
- Remove exact copy
- Update references
- Log deletion
```

### Deduplication Utilities

**Find duplicates**:
```markdown
scan_for_duplicates(folder_path):
  Input: Folder to scan
  Output: List of duplicate groups

  For each file:
    - Calculate fingerprint
    - Compare with existing
    - Group similar items
    - Report matches >70%
```

**Merge duplicates**:
```markdown
merge_tasks(task1, task2):
  Input: Two similar tasks
  Output: Merged task

  Process:
    1. Compare timestamps (keep newer)
    2. Merge content (union)
    3. Combine metadata
    4. Update references
    5. Archive old task
    6. Update index
```

---

## 💾 Storage Optimization

### Compression Strategies

**1. Remove Redundancy**
```markdown
Before:
  Task 1: "Meeting with Alice about Q1 budget"
  Task 2: "Meeting with Alice about Q1 budget planning"
  Task 3: "Q1 budget meeting notes with Alice"

After (merged):
  "Q1 Budget Meeting with Alice"
  - Sub-tasks: Planning, Review, Approval
  - Space saved: 2 files, ~4KB
```

**2. Summarize Details**
```markdown
Before (120 lines):
  Full meeting transcript
  All discussion points
  Detailed notes

After (15 lines):
  Summary: Key decisions made
  Action items: 3 tasks
  Outcome: Budget approved

Space saved: ~87.5%
```

**3. External Storage**
```markdown
Large files → External storage:
  - Attachments: Cloud/local storage
  - Images: Thumbnail in vault, full in storage
  - Videos: Link only
  - Audio: Transcription in vault

Vault keeps:
  - Metadata
  - Summary
  - Link to external storage
```

### Storage Targets

```markdown
Bronze Tier:
- Active memory: < 50 MB
- Archive: < 200 MB
- Total: < 250 MB

Silver Tier:
- Active memory: < 100 MB
- Archive: < 500 MB
- Total: < 600 MB

Gold Tier:
- Active memory: < 200 MB
- Archive: < 1 GB
- Total: < 1.2 GB
```

---

## 🛠️ Memory Utilities

### 1. `index_vault()`
**Purpose**: Generate master index

**Process**:
- Scan all markdown files
- Extract metadata
- Group by categories
- Generate index.md
- Update statistics

**Output**: `Archive/index.md`

---

### 2. `archive_old_tasks(days=90)`
**Purpose**: Move old completed tasks to archive

**Process**:
- Find tasks in Done/ older than `days`
- Create monthly archive folders
- Move tasks to archive
- Update index
- Update references

**Output**: Archived tasks, updated index

---

### 3. `compress_archive(year)`
**Purpose**: Compress yearly archives

**Process**:
- Find year's archives
- Concatenate by quarter
- Summarize content
- Remove full details
- Preserve key info

**Output**: Compressed archives, space saved

---

### 4. `find_duplicates(threshold=0.7)`
**Purpose**: Detect duplicate/similar tasks

**Process**:
- Calculate fingerprints
- Compare all pairs
- Group by similarity
- Report matches above threshold

**Output**: List of duplicate groups

---

### 5. `cleanup_vault()`
**Purpose**: Remove cruft, optimize storage

**Process**:
- Find empty files
- Remove temp files
- Clean broken links
- Compress images
- Update index

**Output**: Space saved, cleanup log

---

### 6. `search_memory(query)`
**Purpose**: Search across all memory

**Process**:
- Check index first (fast)
- Search active memory
- Search archives (slower)
- Rank results
- Return matches

**Output**: Ranked search results

---

### 7. `generate_summary(period)`
**Purpose**: Create period summary

**Process**:
- Extract tasks from period
- Group by topic
- Identify key events
- Generate markdown summary

**Output**: Summary markdown file

---

### 8. `maintain_history(task_id)`
**Purpose**: Track task lifecycle

**Process**:
- Record status changes
- Track timestamps
- Note references
- Update changelog

**Output**: Updated history

---

### 9. `link_related(task_id)`
**Purpose**: Find and link related tasks

**Process**:
- Find similar content
- Identify common topics
- Detect shared participants
- Create cross-references

**Output**: Updated task with links

---

### 10. `optimize_storage()`
**Purpose**: Comprehensive optimization

**Process**:
- Run all optimization utilities
- Measure space saved
- Update statistics
- Generate report

**Output**: Optimization report

---

## 📋 Memory Maintenance Schedule

### Daily (00:00)
- [ ] Update index with new tasks
- [ ] Check for duplicates
- [ ] Update changelog
- [ ] Backup active memory

### Weekly (Sunday 00:00)
- [ ] Archive tasks completed >7 days ago
- [ ] Cleanup temp files
- [ ] Verify index accuracy
- [ ] Generate weekly summary

### Monthly (1st, 00:00)
- [ ] Archive tasks completed >90 days ago
- [ ] Compress previous month
- [ ] Update master index
- [ ] Generate monthly summary
- [ ] Storage optimization

### Quarterly (1st of Q)
- [ ] Compress previous quarter
- [ ] Generate quarter summary
- [ ] Deep cleanup
- [ ] Verify no data loss
- [ ] Backup full vault

### Yearly (Jan 1st, 00:00)
- [ ] Compress previous year
- [ ] Generate year summary
- [ ] Major optimization
- [ ] Archive statistics
- [ ] Plan next year storage

---

## 🔍 Search Optimization

### Index Structure

**Fast lookup**:
```markdown
index.json:
{
  "topics": {
    "budget": [file1, file2, file3],
    "meetings": [file4, file5]
  },
  "people": {
    "alice": [file1, file4],
    "bob": [file2, file5]
  },
  "dates": {
    "2026-02": [file1, file2],
    "2026-01": [file3, file4]
  },
  "tags": {
    "#urgent": [file1, file3],
    "#financial": [file2]
  }
}
```

**Search strategy**:
1. Check index.json first (instant)
2. If not found, scan active memory (fast)
3. If still not found, search archives (slow)
4. Cache frequent searches

---

## 📊 Storage Monitoring

### Metrics to Track

```markdown
storage_metrics.md:

## Current Status
- Active: 45 MB / 50 MB (90%)
- Archive: 180 MB / 200 MB (90%)
- Total: 225 MB / 250 MB (90%)

## Warnings
⚠️ Active memory at 90% - Archive old tasks
⚠️ Total storage at 90% - Compress archives

## History
- 2026-02: 225 MB (↓ 10 MB from compression)
- 2026-01: 235 MB (↑ 15 MB from activity)
- 2025-12: 220 MB

## Optimization Opportunities
- 50 tasks ready for archive (save ~8 MB)
- Q3 2025 ready for compression (save ~12 MB)
- 15 duplicate tasks detected (save ~2 MB)
```

---

## 🎯 Best Practices

### DO ✅
- Archive regularly (monthly minimum)
- Maintain index (daily updates)
- Compress old archives (yearly)
- Remove duplicates (as found)
- Monitor storage (weekly check)
- Backup before major changes
- Document important patterns
- Use consistent formatting

### DON'T ❌
- Delete without archiving
- Ignore growing storage
- Skip index updates
- Store large attachments in vault
- Duplicate information
- Keep incomplete tasks forever
- Archive active items
- Lose context in compression

---

## 🔄 Migration Strategy

### When Storage Full

**Option 1: Aggressive Compression**
```markdown
1. Compress all archives >1 year
2. Keep only summaries
3. Move attachments to external storage
4. Expected savings: 60-80%
```

**Option 2: Selective Archive**
```markdown
1. Identify low-value items
2. Remove or ultra-compress
3. Keep high-value items full
4. Expected savings: 40-60%
```

**Option 3: External Archive**
```markdown
1. Move old archives to cloud/external
2. Keep index and summaries local
3. Fetch on-demand if needed
4. Expected savings: 80%+ local
```

---

## 📚 Knowledge Base Format

### patterns.md
```markdown
# Learned Patterns

## Sprint Planning
**When**: Every 2 weeks
**Who**: Alice, Bob, team
**Format**: 2-hour meeting
**Output**: Sprint backlog, assignments
**Notes**: Schedule on Monday mornings

## Budget Reviews
**When**: Monthly (1st Tuesday)
**Who**: Alice (owner), Finance team
**Format**: 1-hour review + presentation
**Output**: Budget report, adjustments
**Notes**: Prepare reports by Friday prior
```

### contacts.md
```markdown
# Contact Directory

## Alice Johnson
- Role: Project Manager
- Email: alice@company.com
- Topics: Planning, Budget, Hiring
- Last contact: 2026-02-15
- Files: 45 references

## Bob Chen
- Role: Lead Developer
- Email: bob@company.com
- Topics: Code, Deployment, Technical
- Last contact: 2026-02-14
- Files: 67 references
```

---

## 🎓 Memory Efficiency Tips

1. **Use references, not copies**
   - Link to source, don't duplicate
   - Single source of truth

2. **Summarize aggressively**
   - 80/20 rule: 20% of info = 80% of value
   - Keep essence, drop details

3. **Archive early, archive often**
   - Don't let active memory overflow
   - Regular maintenance prevents crisis

4. **Index everything**
   - Searchable index > browsing
   - Fast lookup saves time

5. **Clean as you go**
   - Remove duplicates immediately
   - Don't accumulate cruft

---

**Status**: Production Ready
**Priority**: HIGH (Essential for long-term operation)
**Storage Target**: <250 MB for Bronze Tier
**Maintenance**: Automated + monthly review

*Good memory management = Fast AI + Low storage costs*
