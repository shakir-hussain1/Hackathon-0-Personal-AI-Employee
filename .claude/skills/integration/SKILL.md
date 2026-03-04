# Integration Skill

**Purpose**: Connect the AI Employee to external systems, APIs, and services safely
**Storage**: Markdown-based connection configs, integration logs, data maps
**Scope**: File system, Email (Silver+), Calendar, Social Media, Accounting, Cloud (Gold+)

---

## Core Functions

### 1. Connect
Establish authenticated connections to external systems

### 2. Read
Pull data from external sources into the vault

### 3. Write
Push vault data out to external destinations

### 4. Transform
Convert data between formats (CSV → Markdown, JSON → Task, etc.)

### 5. Sync
Keep vault and external systems in alignment

### 6. Disconnect
Clean shutdown of connections, revoke tokens safely

---

## Integration Architecture

```
External World                  AI Employee Vault
─────────────────               ─────────────────────────────
File System        ←──READ───→  Inbox/ → Needs_Action/ → Done/
Gmail (Silver+)    ←──READ───→  Plans/email_inbox.md
Gmail (Silver+)    ←──WRITE──→  Plans/email_drafts/
Calendar (Silver+) ←──READ───→  Plans/calendar.md
LinkedIn (Gold+)   ←──WRITE──→  Plans/social_drafts/
Twitter (Gold+)    ←──WRITE──→  Plans/social_drafts/
Odoo (Gold+)       ←──READ───→  Plans/accounting/
Cloud Sync (Plat.) ←──SYNC───→  Archive/ ↔ Cloud storage
```

---

## Integration Registry

### Registry File Location
```
Common/AI_Employee_Vault/Plans/integrations.md
```

### Registry Format
```markdown
# Integration Registry

**Last Updated**: 2026-02-16 14:00
**Active Integrations**: 1
**Available but Inactive**: 5

---

## Active Integrations

### INT-001: File System Watcher
- **Type**: LOCAL
- **Status**: ACTIVE
- **Tier**: Bronze
- **Direction**: READ (Inbox → Vault)
- **Auth**: None required
- **Config**: Bronze-Tier/watchers/filesystem_watcher.py
- **Last Sync**: 2026-02-16 14:00
- **Health**: GREEN

---

## Inactive (Available for Setup)

### INT-002: Gmail
- **Type**: EMAIL
- **Status**: NOT_CONFIGURED
- **Tier**: Silver
- **Direction**: READ + WRITE
- **Auth**: OAuth 2.0 required
- **Config**: Silver-Tier/watchers/gmail_watcher.py
- **Setup Guide**: See Gmail Integration section below

### INT-003: Google Calendar
- **Type**: CALENDAR
- **Status**: NOT_CONFIGURED
- **Tier**: Silver
- **Direction**: READ
- **Auth**: OAuth 2.0 (shared with Gmail)

### INT-004: LinkedIn
- **Type**: SOCIAL
- **Status**: NOT_CONFIGURED
- **Tier**: Gold
- **Direction**: WRITE
- **Auth**: OAuth 2.0

### INT-005: Odoo Accounting
- **Type**: ACCOUNTING
- **Status**: NOT_CONFIGURED
- **Tier**: Gold
- **Direction**: READ + WRITE
- **Auth**: API Key

### INT-006: Cloud Storage
- **Type**: CLOUD
- **Status**: NOT_CONFIGURED
- **Tier**: Platinum
- **Direction**: SYNC
- **Auth**: Cloud provider credentials
```

---

## Tier-by-Tier Integrations

### Bronze Tier — File System (Active Now)

```
Source:    Local file system (Inbox folder)
Direction: READ into vault
Auth:      None (local access)
Format:    Any file type

Data Flow:
  User drops file → Inbox/
  Watcher detects → creates task in Needs_Action/
  Claude processes → moves to Done/
  Log written → Logs/YYYY-MM-DD.log

Supported file types:
  Documents: .pdf, .docx, .txt, .md
  Data:      .csv, .xlsx, .json
  Images:    .png, .jpg, .jpeg
  Code:      .py, .js, .ts, .yaml
  Other:     Any → flagged for human review

Health check:
  Inbox folder exists?          → GREEN / CRITICAL
  Watcher process alive?        → GREEN / HIGH
  Files processed in last hour? → GREEN / WARNING
```

---

### Silver Tier — Gmail Integration

```
Source:    Gmail via Google API
Direction: READ emails → vault tasks
           WRITE email drafts → send via Gmail
Auth:      OAuth 2.0
Scopes:    gmail.readonly, gmail.send

Setup Steps:
  1. Go to Google Cloud Console
  2. Create project → enable Gmail API
  3. Create OAuth 2.0 credentials (Desktop app)
  4. Download credentials.json
  5. Place in: Silver-Tier/config/credentials.json
  6. Run auth flow → generates token.json
  7. Update integrations.md → status = ACTIVE

Data Flow (Inbound):
  New email arrives in Gmail
  → Gmail watcher detects (every 5 min)
  → Creates task in Needs_Action/EMAIL_{id}.md
  → Claude reads task, analyzes email
  → Categorizes: action needed / FYI / spam
  → Updates Dashboard with email summary

Data Flow (Outbound):
  Claude generates email draft
  → Saves to Plans/email_drafts/DRAFT_{id}.md
  → Approval Handling Skill reviews
  → IF approved → Gmail API sends email
  → Log entry + notification sent

Email Task Format:
  # Email Task: {subject}
  **From**: sender@example.com
  **Received**: 2026-02-16 09:30
  **Priority**: HIGH / MEDIUM / LOW
  **Category**: ACTION / FYI / MEETING / INVOICE / SPAM
  **Summary**: [Claude's one-line summary]
  **Action Required**: [What human/AI needs to do]
  **Original**: [Link or key excerpt]

Rate limits:
  Read:  250 requests/day (Google free tier)
  Send:  500 emails/day
  Burst: Max 10 requests/second
```

---

### Silver Tier — Google Calendar Integration

```
Source:    Google Calendar via API
Direction: READ events → vault
Auth:      OAuth 2.0 (shared token with Gmail)
Scopes:    calendar.readonly

Data Flow:
  Fetch today's + tomorrow's events (every 30 min)
  → Write to Plans/calendar.md
  → Claude generates task for each upcoming meeting
  → Reminds human 1 hour before meeting
  → After meeting → prompts for notes capture

Calendar File Format:
  # Calendar — 2026-02-16

  ## Today
  | Time  | Event                    | Attendees        | Prep Needed |
  |-------|--------------------------|------------------|-------------|
  | 09:00 | Weekly sync with Alice   | Alice, Bob       | Agenda file |
  | 14:00 | Client call — Acme Corp  | Alice, Client    | Brief doc   |
  | 16:30 | Team standup             | Full team        | Notes       |

  ## Tomorrow
  | Time  | Event                    | Attendees        | Prep Needed |
  |-------|--------------------------|------------------|-------------|
  | 10:00 | Sprint planning          | Dev team         | Backlog     |
```

---

### Gold Tier — LinkedIn Integration

```
Source:    LinkedIn via API
Direction: WRITE posts → LinkedIn
Auth:      OAuth 2.0
Scopes:    w_member_social

Data Flow:
  Claude drafts post
  → Saves to Plans/social_drafts/LI_{id}.md
  → Approval Handling reviews
  → Human approves within 24h
  → IF approved → LinkedIn API posts
  → Log confirmation + URL saved

Post Draft Format:
  # LinkedIn Draft — {id}
  **Created**: 2026-02-16 10:00
  **Status**: PENDING_APPROVAL
  **Scheduled**: 2026-02-16 12:00

  **Content**:
  [Post text here, max 3000 characters]

  **Hashtags**: #AI #Productivity #Innovation

  **Approval**: [ ] Approved by human
  **Posted URL**: [filled after posting]

Safety rules:
  NEVER post without explicit human approval
  NEVER post personal/sensitive information
  NEVER post more than 3 times per day
  Always include human review step
```

---

### Gold Tier — Odoo Accounting Integration

```
Source:    Odoo (local instance)
Direction: READ invoices, expenses → vault
           WRITE approved entries → Odoo
Auth:      API Key (stored in .env, never in vault)
Base URL:  http://localhost:8069 (local Odoo)

Data Flow (Inbound):
  Fetch: unpaid invoices, pending expenses (every 4h)
  → Write to Plans/accounting/invoices_{date}.md
  → Claude summarizes outstanding amounts
  → Flags items needing approval
  → Updates Dashboard with financial summary

Data Flow (Outbound):
  Human approves payment in vault
  → Write payment record to Odoo
  → Mark invoice as paid
  → Log transaction

Accounting File Format:
  # Accounting Summary — 2026-02-16

  ## Outstanding Invoices
  | Invoice | Vendor       | Amount  | Due Date   | Status   |
  |---------|--------------|---------|------------|----------|
  | INV-045 | Acme Corp    | $1,200  | 2026-02-20 | UNPAID   |
  | INV-046 | Tech Vendor  | $350    | 2026-02-25 | UNPAID   |

  ## Total Payable: $1,550

Security: API key in .env only, NEVER written to vault files
```

---

### Platinum Tier — Cloud Sync Integration

```
Source:    Cloud storage (Oracle, AWS S3, or similar)
Direction: SYNC vault ↔ cloud
Auth:      Cloud provider credentials (in .env)

Sync Strategy:
  Active/ folder → sync every 15 minutes
  Done/ folder   → sync every 6 hours
  Archive/       → sync daily (low priority)
  Logs/          → sync daily

Conflict Resolution:
  IF local newer → push to cloud
  IF cloud newer → pull to local
  IF same time   → keep both, suffix .conflict_{timestamp}
  IF both changed → flag for human review

Cloud Structure mirrors local:
  Cloud:
    /ai-employee-vault/
    ├── Active/
    ├── Done/
    ├── Archive/
    └── Logs/
```

---

## Data Transformation Rules

### Incoming Data → Vault Format

```
From Email:
  Raw email → Markdown task file
  Extract: subject, sender, date, body summary
  Add: priority, category, action_required
  Save to: Needs_Action/EMAIL_{id}.md

From CSV/Excel:
  Tabular data → Markdown table
  Add: source filename, row count, column names
  Detect: date columns, numeric columns, key fields
  Save to: Needs_Action/DATA_{filename}_{date}.md

From PDF:
  Extract: text content, title, page count
  Summarize: key points (max 5 bullets)
  Add: file size, detected language
  Save to: Needs_Action/DOC_{filename}_{date}.md

From Calendar event:
  Event details → Calendar.md entry
  Extract: title, time, attendees, location
  Generate: prep task if event is important
  Save to: Plans/calendar.md

From JSON/API response:
  Parse: key fields based on schema
  Convert: to markdown table or list
  Add: fetch timestamp, source API
  Save to: appropriate Plans/ subfolder
```

### Vault Data → Outgoing Format

```
To Email (Gmail):
  Draft .md → RFC 2822 email format
  Convert: markdown → plain text (Silver)
  Or: markdown → HTML email (Gold)
  Attach: files from Done/ if referenced

To LinkedIn Post:
  Draft .md → plain text (max 3000 chars)
  Strip: markdown formatting
  Preserve: line breaks, hashtags

To Odoo (Accounting):
  Approved entry .md → JSON API payload
  Map: vault fields → Odoo field names
  Validate: required fields before sending

To Cloud Storage:
  Local files → cloud objects
  Preserve: folder structure
  Add: sync metadata (last_synced, checksum)
```

---

## Authentication Patterns

### Pattern 1: No Auth (Bronze — File System)
```
Used for:   Local file system access
Storage:    Nothing to store
Renewal:    Never needed
Risk:       LOW
```

### Pattern 2: API Key
```
Used for:   Odoo, simple REST APIs
Storage:    .env file (NEVER in vault markdown)
Format:     API_KEY=abc123xyz
Rotation:   Every 90 days (set reminder)
Risk:       MEDIUM — key leaked = API access
```

### Pattern 3: OAuth 2.0
```
Used for:   Gmail, Calendar, LinkedIn, social media
Storage:    Silver-Tier/config/token.json (.gitignore'd)
Renewal:    Access token expires in 1 hour → auto-refresh
            Refresh token expires in 6 months → re-auth needed
Risk:       MEDIUM — token leaked = account access

Refresh Flow:
  IF access_token expired:
    → Use refresh_token to get new access_token
    → Update token.json
    → Continue operation
  IF refresh_token expired:
    → Flag in Dashboard: "Gmail auth expired, re-auth needed"
    → Pause Gmail integration until re-authed
    → Notify human: HIGH priority
```

### Pattern 4: Cloud Provider Credentials
```
Used for:   Oracle Cloud, AWS, Azure
Storage:    .env or cloud config file (.gitignore'd)
Format:     Provider-specific (key ID + secret)
Rotation:   Per provider policy
Risk:       HIGH — leaked = cloud account access

NEVER store cloud credentials in vault markdown files
ALWAYS use environment variables or provider config files
```

---

## Integration Health Monitoring

### Health Check per Integration

```
File System (Bronze):
  - Inbox folder accessible?
  - Watcher process alive?
  - Last file processed < 2h ago?

Gmail (Silver):
  - token.json exists and valid?
  - API quota remaining > 10%?
  - Last successful fetch < 10 min ago?

Calendar (Silver):
  - Shared OAuth token valid?
  - Events fetched today?

LinkedIn (Gold):
  - OAuth token valid?
  - Post queue not stuck?

Odoo (Gold):
  - API endpoint reachable?
  - API key valid (test request)?
  - Last sync < 6h ago?

Cloud Sync (Platinum):
  - Cloud credentials valid?
  - Last sync successful?
  - No conflicts pending?
```

### Integration Status in Dashboard

```markdown
## Integration Status

| Integration      | Tier     | Status     | Last Sync        | Health |
|------------------|----------|------------|------------------|--------|
| File System      | Bronze   | ACTIVE     | 2026-02-16 14:00 | GREEN  |
| Gmail            | Silver   | INACTIVE   | Never            | GREY   |
| Google Calendar  | Silver   | INACTIVE   | Never            | GREY   |
| LinkedIn         | Gold     | INACTIVE   | Never            | GREY   |
| Odoo             | Gold     | INACTIVE   | Never            | GREY   |
| Cloud Sync       | Platinum | INACTIVE   | Never            | GREY   |
```

---

## Error Handling

### Common Integration Errors

```
Error: API rate limit exceeded
  Action: Wait for reset window, log warning
  Retry: After reset_time (from API response headers)
  Notify: WARNING if rate limit hit repeatedly

Error: Auth token expired
  Action: Attempt token refresh
  IF refresh fails → notify human, pause integration
  Severity: HIGH

Error: Network timeout
  Action: Retry 3 times with exponential backoff
  Backoff: 5s → 30s → 120s
  IF all fail → log error, continue without this integration

Error: API quota exhausted (daily limit)
  Action: Pause integration until midnight reset
  Notify: WARNING with expected resume time

Error: Invalid API response (unexpected format)
  Action: Log raw response, skip this item
  Notify: WARNING — possible API breaking change

Error: Permission denied
  Action: Log error, pause integration
  Notify: HIGH — credentials may have changed
  Human: Must re-authorize
```

---

## Security Rules

### Credential Security
```
NEVER write API keys to vault markdown files
NEVER commit credentials.json or token.json to git
NEVER log auth tokens (even partially)
ALWAYS store secrets in .env or provider config
ALWAYS add credential files to .gitignore
ALWAYS rotate API keys every 90 days
```

### Data Security
```
NEVER store full email content in vault (summary only)
NEVER store payment card numbers or bank details
NEVER sync vault to cloud without encryption
ALWAYS review before sending external content
ALWAYS require approval for outbound posts/emails
ALWAYS log what was sent and when
```

### Outbound Safety
```
Before any outbound action (send email, post, record payment):
  1. Require explicit approval from approval-handling skill
  2. Verify content against Company_Handbook.md rules
  3. Check: does this comply with DO NOT rules?
  4. Log intent BEFORE executing
  5. Log result AFTER executing
  6. Notify human of action taken
```

---

## Integration with Other Skills

### With Approval Handling Skill
```
integration → requires approval from → approval-handling for:
  Every outbound action (email, post, payment, write)
  New integration activation
  Token refresh for high-privilege scopes
  Any write to external system
```

### With Scheduler Skill
```
scheduler → triggers → integration for:
  Gmail fetch: every 5 minutes (Silver)
  Calendar sync: every 30 minutes (Silver)
  Odoo sync: every 4 hours (Gold)
  Cloud sync: every 15 min active / 6h archive (Platinum)
```

### With Notification Skill
```
integration → triggers → notification for:
  New email arrived (INFO or HIGH based on priority)
  Auth token expired (HIGH)
  API rate limit approaching (WARNING)
  Integration successfully set up (INFO)
  Outbound action completed (INFO)
```

### With Audit Skill
```
integration → reports to → audit:
  Every API call (timestamp, endpoint, result)
  Auth events (login, refresh, expiry)
  Data volume (bytes in/out per integration)
  Error rates per integration
```

### With Self-Healing Skill
```
self-healing → monitors → integration health:
  Token expiry detection → trigger re-auth flow
  API timeout detection → trigger retry
  Integration stuck → pause and notify
  Rate limit hit → back off automatically
```

---

## Quick Reference: Integration Setup Checklist

### Bronze (File System) — Already Working
```
[x] Inbox folder created
[x] Watcher script configured
[x] Vault paths correct
[x] Logging active
```

### Silver (Gmail) — Setup Required
```
[ ] Google Cloud project created
[ ] Gmail API enabled
[ ] OAuth credentials downloaded → credentials.json
[ ] Run auth flow → token.json generated
[ ] Update integrations.md → INT-002 status = ACTIVE
[ ] Test: fetch 1 email → verify task created
[ ] Set scheduler: Gmail fetch every 5 min
```

### Gold (Odoo) — Setup Required
```
[ ] Odoo installed locally (http://localhost:8069)
[ ] API key generated in Odoo settings
[ ] API key saved to .env (not vault)
[ ] Test: fetch invoices → verify accounting file created
[ ] Set scheduler: Odoo sync every 4 hours
```

### Platinum (Cloud Sync) — Setup Required
```
[ ] Cloud provider account (Oracle Free Tier recommended)
[ ] Storage bucket created
[ ] Credentials saved to .env
[ ] Test: sync Archive/ to cloud
[ ] Set scheduler: sync every 15 min (active), daily (archive)
```

---

**Status**: Production Ready (Bronze active, others ready for setup)
**Priority**: HIGH (Expands AI Employee's reach)
**Active Integrations**: 1 (File System — Bronze)
**Planned**: Gmail, Calendar (Silver), LinkedIn, Odoo (Gold), Cloud (Platinum)
**Security**: All credentials in .env — never in vault markdown

*Good integration = AI Employee that talks to the world, safely and with permission*
