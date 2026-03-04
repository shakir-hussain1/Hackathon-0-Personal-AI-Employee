# 📁 Project Structure - Personal AI Employee

**Last Updated**: 2026-02-16
**Organization**: Multi-Tier Architecture

---

## 🎯 Design Philosophy

This project is organized by **implementation tiers** to:

1. **Separate Concerns**: Each tier has its own code, dependencies, and configs
2. **Enable Progression**: Easy to upgrade from Bronze → Silver → Gold → Platinum
3. **Share Common**: Vault and docs are shared across all tiers
4. **Maintain Clarity**: Clear what belongs to which tier
5. **Support Parallel Development**: Multiple people can work on different tiers

---

## 📂 Directory Structure

```
E:\Hackathon-0-Personal-AI-Employee\
│
├── 📁 Common/                                   # Shared across all tiers
│   └── AI_Employee_Vault/                      # The AI's knowledge base
│       ├── Dashboard.md                         # Real-time status board
│       ├── Company_Handbook.md                  # AI behavior rules
│       ├── Inbox/                               # File drop zone
│       │   └── .gitkeep
│       ├── Needs_Action/                        # Task queue
│       │   └── .gitkeep
│       ├── Done/                                # Processed files
│       │   ├── Documents/                       # Text, PDF, Word
│       │   ├── Data/                            # CSV, Excel, JSON
│       │   ├── Media/                           # Images, videos
│       │   ├── Communications/                  # Emails
│       │   ├── Code/                            # Scripts, programs
│       │   ├── Uncategorized/                   # Unknown types
│       │   ├── Errors/                          # Failed processing
│       │   └── .gitkeep
│       ├── Plans/                               # Planning documents
│       │   └── .gitkeep
│       └── Logs/                                # Daily activity logs
│           └── .gitkeep
│
├── 📁 Bronze-Tier/                              # 🥉 Foundation (COMPLETE)
│   ├── watchers/                                # File system monitoring
│   │   ├── __init__.py
│   │   ├── base_watcher.py                      # Abstract base class
│   │   └── filesystem_watcher.py                # File monitor
│   ├── skills/                                  # Agent Skills
│   │   ├── process_inbox.md                     # Main processing
│   │   └── update_dashboard.md                  # Dashboard refresh
│   ├── orchestrator/                            # Coordination (placeholder)
│   │   └── __init__.py
│   ├── venv/                                    # Python virtual env
│   ├── requirements.txt                         # Bronze dependencies
│   ├── start_watcher.bat                        # Launcher
│   └── README-Bronze.md                         # Bronze docs
│
├── 📁 Silver-Tier/                              # 🥈 Enhanced (FUTURE)
│   ├── watchers/                                # Gmail, Calendar
│   │   ├── gmail_watcher.py                     # Email monitoring
│   │   └── calendar_watcher.py                  # Event monitoring
│   ├── skills/                                  # Email processing
│   │   ├── process_email.md
│   │   └── draft_reply.md
│   ├── mcp-servers/                             # Model Context Protocol
│   │   └── email_sender/                        # Send emails
│   ├── venv/                                    # Silver virtual env
│   ├── requirements.txt                         # Silver dependencies
│   └── README-Silver.md                         # Silver docs
│
├── 📁 Gold-Tier/                                # 🥇 Advanced (FUTURE)
│   ├── watchers/                                # Social media
│   │   ├── twitter_watcher.py
│   │   ├── facebook_watcher.py
│   │   └── linkedin_watcher.py
│   ├── integrations/                            # Business systems
│   │   ├── odoo/                                # Accounting
│   │   └── crm/                                 # Customer management
│   ├── skills/                                  # Advanced AI
│   │   ├── social_media_post.md
│   │   └── generate_report.md
│   ├── venv/                                    # Gold virtual env
│   ├── requirements.txt                         # Gold dependencies
│   └── README-Gold.md                           # Gold docs
│
├── 📁 Platinum-Tier/                            # 💎 Production (FUTURE)
│   ├── cloud-deployment/                        # Oracle Cloud
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   ├── monitoring/                              # System monitoring
│   │   ├── prometheus/
│   │   └── grafana/
│   ├── ci-cd/                                   # Automation
│   │   └── github-actions/
│   ├── requirements.txt                         # Platinum dependencies
│   └── README-Platinum.md                       # Platinum docs
│
├── 📁 docs/                                     # 📚 All documentation
│   ├── README.md                                # Main comprehensive guide
│   ├── QUICK_START.md                          # 5-minute setup
│   ├── TESTING_GUIDE.md                        # Test procedures
│   ├── DEMO_SCRIPT.md                          # Demo walkthrough
│   └── IMPLEMENTATION_SUMMARY.md               # Technical report
│
├── 📄 README.md                                 # Project overview (root)
├── 📄 PROJECT_STRUCTURE.md                      # This file
├── 📄 .gitignore                                # Git ignore rules
└── 📄 Personal AI Employee Hackathon 0...pdf   # Original hackathon doc
```

---

## 🎨 Color Coding & Symbols

- 📁 **Folder** - Directory
- 📄 **File** - Regular file
- 🥉 **Bronze** - Foundation tier
- 🥈 **Silver** - Enhanced tier
- 🥇 **Gold** - Advanced tier
- 💎 **Platinum** - Production tier
- 🌐 **Common** - Shared components
- 📚 **Docs** - Documentation

---

## 🔑 Key Principles

### 1. Common is Shared
The `Common/` folder contains components used by **all tiers**:
- **Vault**: The AI's knowledge base (markdown files)
- **Folder structure**: Inbox, Needs_Action, Done, Logs
- **Dashboard & Handbook**: Core AI interface

**Why**: All tiers need the same vault. No duplication.

### 2. Tiers are Independent
Each tier folder (`Bronze-Tier/`, `Silver-Tier/`, etc.) contains:
- Tier-specific code
- Tier-specific dependencies (requirements.txt)
- Tier-specific virtual environment (venv/)
- Tier-specific documentation

**Why**: Easy to upgrade without breaking existing tier.

### 3. Docs are Centralized
All comprehensive documentation in `docs/`:
- Main guide (README.md)
- Quick start guide
- Testing procedures
- Demo scripts
- Implementation reports

**Why**: One place for all documentation, accessible to all tiers.

### 4. Progressive Enhancement
```
Bronze → Silver → Gold → Platinum
  ↓         ↓        ↓         ↓
 10h      +20h     +30h      +20h
Basic   Email   Social   Production
```

Each tier **builds on** the previous but doesn't **modify** it.

---

## 📍 Path References

### Absolute Paths (Use These)

**Vault**:
```
E:\Hackathon-0-Personal-AI-Employee\Common\AI_Employee_Vault
```

**Bronze Tier**:
```
E:\Hackathon-0-Personal-AI-Employee\Bronze-Tier
```

**Documentation**:
```
E:\Hackathon-0-Personal-AI-Employee\docs
```

### Relative Paths (From Different Locations)

**From Bronze-Tier to Vault**:
```
..\Common\AI_Employee_Vault
```

**From Vault to Bronze-Tier**:
```
..\..\Bronze-Tier
```

**From Root to Vault**:
```
Common\AI_Employee_Vault
```

---

## 🔧 Configuration Files

### Bronze Tier
- **requirements.txt**: Python dependencies (watchdog, python-dotenv)
- **start_watcher.bat**: Launcher script
- **venv/**: Isolated Python environment

### Silver Tier (Future)
- **requirements.txt**: Adds Gmail API, OAuth libraries
- **.env**: Environment variables (API keys)
- **mcp-config.json**: MCP server configuration

### Gold Tier (Future)
- **requirements.txt**: Adds social media APIs, Odoo libraries
- **odoo-config.yml**: Odoo connection settings

### Platinum Tier (Future)
- **docker-compose.yml**: Container orchestration
- **Dockerfile**: Container image definition
- **.env.production**: Production environment variables

---

## 🚀 Usage Patterns

### Bronze Tier (Current)
```bash
# From Bronze-Tier folder
.\venv\Scripts\activate
python watchers\filesystem_watcher.py

# Claude Code (from vault)
cd ..\Common\AI_Employee_Vault
claude code
```

### Silver Tier (Future)
```bash
# From Silver-Tier folder
.\venv\Scripts\activate
python orchestrator.py --enable gmail calendar

# Runs on schedule (Task Scheduler)
```

### Gold Tier (Future)
```bash
# From Gold-Tier folder
.\venv\Scripts\activate
python orchestrator.py --enable all

# Full automation
```

### Platinum Tier (Future)
```bash
# Deploy to cloud
cd Platinum-Tier
docker-compose up -d

# Access web dashboard
open https://your-ai-employee.com
```

---

## 📦 Dependencies Management

### Strategy
Each tier has its own `requirements.txt`:

**Bronze** (`Bronze-Tier/requirements.txt`):
```txt
watchdog==4.0.0
python-dotenv==1.0.0
```

**Silver** (`Silver-Tier/requirements.txt`):
```txt
# Include Bronze deps
watchdog==4.0.0
python-dotenv==1.0.0

# Add Silver deps
google-auth==2.16.0
google-api-python-client==2.80.0
mcp==0.1.0
```

**Gold** (`Gold-Tier/requirements.txt`):
```txt
# Include Silver deps
...

# Add Gold deps
tweepy==4.12.0
facebook-sdk==3.1.0
odoo-client==0.1.0
```

### Why Separate?
- No dependency conflicts
- Clear what each tier needs
- Easy to upgrade independently
- Smaller venv for simpler tiers

---

## 🗂️ Data Flow

### Bronze Tier
```
Files → Inbox → Watcher → Task → Claude → Done → Dashboard
                   ↓                           ↓
                 Logs ←─────────────────────── Logs
```

### Silver Tier (Future)
```
Gmail → Email Watcher → Task → Claude → Email MCP → Reply
Files → File Watcher  → Task → Claude → Done
Calendar → Cal Watcher → Task → Claude → Dashboard
                ↓                   ↓
              Logs ←─────────────── Logs
```

### Gold Tier (Future)
```
                ┌─ Gmail
                ├─ Files
Multiple        ├─ Twitter
Sources    →    ├─ Facebook    → Orchestrator → Claude → Multiple
                ├─ LinkedIn                               Actions
                ├─ Odoo
                └─ Calendar
                        ↓                           ↓
                      Logs ←─────────────────────── Logs
```

---

## 🔒 Security Considerations

### Bronze Tier
- ✅ Local-only, no cloud
- ✅ No API keys needed
- ✅ No network access (except Claude API)
- ✅ Human-readable files

### Silver Tier (Future)
- 🔐 Gmail OAuth tokens (secure storage)
- 🔐 API keys in `.env` (not committed)
- 🔐 Email content (local processing)

### Gold Tier (Future)
- 🔐 Multiple API keys
- 🔐 Social media tokens
- 🔐 Database credentials
- 🔐 Odoo access tokens

### Platinum Tier (Future)
- 🔐 Cloud secrets management
- 🔐 SSL certificates
- 🔐 Encrypted connections
- 🔐 Access control lists

---

## 📊 Storage Estimates

### Bronze Tier
- Code: ~50MB
- Venv: ~200MB
- Logs: ~10MB/month
- **Total**: ~260MB + logs

### Silver Tier (Future)
- Code: ~100MB (adds Gmail libs)
- Venv: ~350MB
- Logs: ~50MB/month (more activity)
- **Total**: ~450MB + logs

### Gold Tier (Future)
- Code: ~200MB (adds social media libs)
- Venv: ~500MB
- Logs: ~100MB/month
- **Total**: ~700MB + logs

### Platinum Tier (Future)
- Docker images: ~1GB
- Database: ~500MB
- Logs: ~200MB/month (production)
- **Total**: ~1.7GB + logs

---

## 🎯 Navigation Guide

### I want to...

**...start using Bronze tier**:
→ Go to `Bronze-Tier/` and run `start_watcher.bat`

**...read documentation**:
→ Go to `docs/` and start with `README.md`

**...view the Dashboard**:
→ Go to `Common/AI_Employee_Vault/` and open `Dashboard.md` in VS Code

**...check logs**:
→ Go to `Common/AI_Employee_Vault/Logs/` and open today's `.log` file

**...modify AI behavior**:
→ Go to `Common/AI_Employee_Vault/` and edit `Company_Handbook.md`

**...change watcher settings**:
→ Go to `Bronze-Tier/watchers/` and edit `filesystem_watcher.py`

**...plan Silver tier**:
→ Create `Silver-Tier/` folder and start building

**...understand architecture**:
→ Read `docs/IMPLEMENTATION_SUMMARY.md`

---

## 🔄 Migration Path

### From Old Structure to New

**What Changed**:
```
Old:
├── AI_Employee_Vault/         → Common/AI_Employee_Vault/
├── watchers/                  → Bronze-Tier/watchers/
├── skills/                    → Bronze-Tier/skills/
├── orchestrator/              → Bronze-Tier/orchestrator/
├── venv/                      → Bronze-Tier/venv/
├── requirements.txt           → Bronze-Tier/requirements.txt
├── start_watcher.bat          → Bronze-Tier/start_watcher.bat
└── docs/*.md                  → docs/

New Root README.md created
Bronze-Tier/README-Bronze.md created
PROJECT_STRUCTURE.md created (this file)
```

**Path Updates Needed**:
- `start_watcher.bat`: Update vault path to `..\Common\AI_Employee_Vault`
- `filesystem_watcher.py`: Default path updated in main()
- Documentation: Paths updated in all guides

**Git Status**:
- All files tracked via git mv (preserves history)
- `.gitignore` updated for new structure

---

## ✅ Verification Checklist

After restructuring, verify:

- [ ] Bronze-Tier folder contains all Bronze files
- [ ] Common/AI_Employee_Vault accessible
- [ ] docs/ contains all documentation
- [ ] start_watcher.bat works from Bronze-Tier
- [ ] Claude Code can access vault with new path
- [ ] VS Code can open vault
- [ ] Dashboard displays correctly
- [ ] Logs are being written
- [ ] File processing works end-to-end
- [ ] All paths in docs updated

---

## 📝 Maintenance

### Adding New Tiers
1. Create tier folder (e.g., `Silver-Tier/`)
2. Add tier-specific code
3. Create `requirements.txt`
4. Create `README-Silver.md`
5. Update root `README.md`
6. Update this `PROJECT_STRUCTURE.md`

### Modifying Existing Tiers
- Edit files within tier folder
- Update tier's README
- Test independently
- Don't break other tiers

### Updating Common Components
- Edit `Common/AI_Employee_Vault/` carefully
- Changes affect **all tiers**
- Test with all active tiers
- Document changes

---

**Structure Version**: 2.0 (Multi-Tier)
**Last Updated**: 2026-02-16
**Status**: Production Ready

Clean, organized, and ready to scale! 🚀
