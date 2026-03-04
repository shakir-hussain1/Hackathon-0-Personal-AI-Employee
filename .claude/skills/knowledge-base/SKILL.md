# Knowledge Base Skill

**Purpose**: Build, maintain, and query a structured repository of everything the AI Employee has learned, observed, and been taught
**Storage**: Markdown-based knowledge files, organized by topic, entity, and type
**Scope**: Facts, procedures, decisions, lessons, contacts, templates, rules, domain knowledge

---

## Core Functions

### 1. Store Knowledge
Save useful information in structured, retrievable format

### 2. Retrieve Knowledge
Find relevant knowledge quickly before any task begins

### 3. Update Knowledge
Keep entries current as facts change over time

### 4. Connect Knowledge
Link related entries — people to projects, topics to procedures

### 5. Validate Knowledge
Check if stored knowledge is still accurate and not outdated

### 6. Summarize Knowledge
Compress and distill knowledge for efficient context injection

---

## Knowledge Architecture

```
Common/AI_Employee_Vault/Knowledge/
│
├── facts/                     # Stable factual knowledge
│   ├── company.md            # Company info, structure, key facts
│   ├── products.md           # Products/services the business offers
│   ├── policies.md           # Internal rules and policies
│   └── glossary.md           # Terms, acronyms, domain vocabulary
│
├── people/                    # Person-specific knowledge
│   ├── contacts.md           # Master contact directory
│   ├── alice_johnson.md      # Individual profile (example)
│   ├── bob_chen.md           # Individual profile (example)
│   └── vendors.md            # External vendor profiles
│
├── procedures/                # How-to knowledge
│   ├── file_processing.md    # How files are handled by type
│   ├── escalation_paths.md   # Who to involve for what situation
│   ├── approval_workflows.md # What needs approval and from whom
│   └── onboarding.md        # How new entities are onboarded
│
├── decisions/                 # Past decisions and their rationale
│   ├── 2026-02.md            # Monthly decision log
│   ├── 2026-01.md
│   └── index.md              # Searchable decision index
│
├── lessons/                   # Learned lessons (from Learning Skill)
│   ├── active_rules.md       # Rules currently applied
│   ├── patterns.md           # Detected behavioral patterns
│   └── feedback_history.md   # Human feedback over time
│
├── templates/                 # Reusable content templates
│   ├── email_templates.md    # Email drafts by situation
│   ├── report_templates.md   # Report structures
│   └── task_templates.md     # Task file formats
│
├── domain/                    # Industry-specific knowledge
│   ├── finance.md            # Financial terms, processes
│   ├── legal.md              # Legal terms, risk signals
│   └── technical.md          # Technical concepts
│
└── index.md                   # Master searchable index (auto-generated)
```

---

## Knowledge Entry Format

### Standard Entry

```markdown
# Knowledge Entry: {title}

**ID**: KB-{category}-{id}
**Created**: 2026-02-16
**Updated**: 2026-02-16
**Type**: fact | procedure | person | decision | lesson | template
**Topic**: {primary topic}
**Tags**: #finance #alice #invoices
**Confidence**: HIGH | MEDIUM | LOW
**Source**: human_taught | observed | inferred | document
**Expires**: never | {date} | review_after_90_days
**Related**: [KB-PEOPLE-001], [KB-PROC-003]

---

## Content

{The actual knowledge, written in clear plain language}

---

## When to Use This

{Specific situations where this knowledge is relevant}

---

## History

| Date       | Change                          | By         |
|------------|---------------------------------|------------|
| 2026-02-16 | Created                         | AI         |
| 2026-02-20 | Updated email address           | Human      |
```

---

## Knowledge Types

### Type 1: Facts
```
Definition: Stable truths about the world, company, or people

Examples:
  - "Alice Johnson is the Project Manager at Acme Corp"
  - "Invoices from Acme Corp are always due within 30 days"
  - "The company fiscal year ends December 31"
  - "Bob's code reviews always use Python 3.11+"

Properties:
  Confidence: starts MEDIUM, becomes HIGH after 3+ confirmations
  Expiry:     set review dates for facts that could change
  Source:     human_taught or observed from multiple interactions

Storage: Knowledge/facts/ or Knowledge/people/
```

### Type 2: Procedures
```
Definition: Step-by-step knowledge about how to do something

Examples:
  - "How to process an invoice from a new vendor"
  - "Steps for escalating a legal document"
  - "Process for handling after-hours urgent files"
  - "How to set up a new integration"

Properties:
  Confidence: HIGH (procedures are explicit, not inferred)
  Expiry:     review when related skills or rules change
  Source:     human_taught or Company_Handbook

Storage: Knowledge/procedures/
```

### Type 3: Person Knowledge
```
Definition: What the AI knows about specific people

Examples:
  - Communication preferences (formal vs casual)
  - Typical file types they send
  - Priority patterns for their work
  - Best time to expect their files
  - Topics they own or are responsible for

Properties:
  Confidence: grows over time with more interactions
  Expiry:     flag for review if no interaction in 90 days
  Source:     observed over multiple interactions

Storage: Knowledge/people/{name}.md
```

### Type 4: Decision Records
```
Definition: Log of significant decisions made with rationale

Examples:
  - "Decided to prioritize Alice's files as HIGH on 2026-02-10"
  - "Chose to quarantine .exe files from all senders"
  - "Agreed with human to archive Done/ tasks after 60 days"

Properties:
  Confidence: HIGH (decisions are deliberate)
  Expiry:     keep permanently (decision log is an audit record)
  Source:     human_approved or AI_decided_and_confirmed

Storage: Knowledge/decisions/YYYY-MM.md
```

### Type 5: Lessons
```
Definition: Extracted knowledge from Learning Skill observations

Examples:
  - "Files from alice@company.com = HIGH priority (95% confidence)"
  - "Finance team Excel files need encoding pre-process"
  - "Human prefers 3-bullet summaries over 5"

Properties:
  Confidence: as calculated by Learning Skill
  Expiry:     retire if confidence drops below 60%
  Source:     learning_observed

Storage: Knowledge/lessons/active_rules.md
```

### Type 6: Templates
```
Definition: Reusable patterns for common outputs

Examples:
  - Standard email for invoice follow-up
  - Weekly report structure
  - Task file template for new document types
  - LinkedIn post format for company updates

Properties:
  Confidence: HIGH (templates are deliberate designs)
  Expiry:     review when communication style changes
  Source:     human_taught or refined_from_feedback

Storage: Knowledge/templates/
```

---

## Knowledge Retrieval

### Retrieval Methods

#### Method 1: Direct Lookup
```
Use when: You know exactly what you are looking for

Process:
  1. Check knowledge index (Knowledge/index.md)
  2. Look up by ID or title
  3. Return full entry

Speed: Instant
Use case: "What do I know about Alice Johnson?"
```

#### Method 2: Tag Search
```
Use when: Looking for all knowledge on a topic

Process:
  1. Extract tags from query
  2. Scan index for matching tags
  3. Return all matching entries ranked by relevance

Speed: Fast (index lookup)
Use case: "What do I know about invoices?"
Returns: All entries tagged #invoices
```

#### Method 3: Entity Search
```
Use when: Processing a file or task, need context about who sent it

Process:
  1. Extract entity identifier (name, email, company)
  2. Check Knowledge/people/ for profile
  3. Check decisions and lessons mentioning this entity
  4. Compile entity knowledge package

Speed: Fast
Use case: "File from alice@company.com — what do I know?"
```

#### Method 4: Situational Search
```
Use when: Facing an unfamiliar situation, need guidance

Process:
  1. Describe the situation in keywords
  2. Search procedures for matching scenarios
  3. Search lessons for similar past situations
  4. Search decisions for precedents

Speed: Medium
Use case: "New vendor, first contact, sent a contract"
```

#### Method 5: Full Text Search
```
Use when: Looking for something specific across all knowledge

Process:
  1. Scan all knowledge files for keyword
  2. Rank by relevance (exact match > partial)
  3. Return top 5 results with context

Speed: Slow (scans all files)
Use case: Last resort when index doesn't have the answer
```

---

## Knowledge Retrieval Package

### What Gets Assembled Per Task

```
When a new task arrives, assemble knowledge package:

1. Entity knowledge (if sender known):
   → Person profile from Knowledge/people/
   → Recent decisions about this person
   → Active lessons applying to this sender

2. Procedural knowledge (by task/file type):
   → Processing procedure for this file type
   → Escalation path if needed
   → Approval requirements

3. Domain knowledge (by content topic):
   → Finance knowledge if invoice/budget
   → Legal knowledge if contract/agreement
   → Technical knowledge if code/config

4. Template knowledge (for output):
   → Task file template for this category
   → Summary template for this type
   → Communication template if response needed

5. Relevant decisions (precedents):
   → Last 3 decisions about similar situations
   → Any overrides or corrections for this entity

Package size target: Under 500 words (focused, not overwhelming)
```

---

## Knowledge Validation

### Freshness Checks

```
Run validation weekly:

For each knowledge entry:
  IF type = fact AND last_updated > 90 days → FLAG for review
  IF type = person AND no_interaction > 90 days → FLAG as possibly stale
  IF type = lesson AND confidence < 60% → FLAG for retirement
  IF type = template AND last_used > 180 days → FLAG for review
  IF expires != never AND expires < today → FLAG as EXPIRED

Flag format in index.md:
  ⚠️ KB-PEOPLE-001 Alice Johnson — no interaction 93 days (possibly stale)
  ❌ KB-FACT-007 Office address — EXPIRED (set expiry was 2026-01-01)
  📉 KB-LESSON-012 Bob priority rule — confidence dropped to 55% (retire?)
```

### Validation Process

```
Step 1: Weekly scan → generate flagged entries list
Step 2: For each flagged entry:
  IF AI can verify from recent interactions → update automatically
  IF needs human input → add to Dashboard "Knowledge Review" section
Step 3: Human reviews flagged items (weekly, low urgency)
Step 4: Human confirms, corrects, or deletes outdated entries
Step 5: Update entry, remove flag, log change
```

---

## Knowledge Capture Triggers

### When to Capture New Knowledge

```
Always capture:
  ✓ First contact with a new entity (create person profile)
  ✓ Human teaches AI something explicitly
  ✓ Human corrects AI (capture the correction)
  ✓ Significant decision made (log with rationale)
  ✓ New procedure established
  ✓ Learning Skill proposes and approves a new rule

Capture if pattern seen 3+ times:
  ✓ Entity consistently sends same file type
  ✓ Topic always handled the same way
  ✓ Specific error always needs specific fix

Do NOT capture:
  ✗ One-time anomalies (don't over-generalize)
  ✗ Speculative information (only verified facts)
  ✗ PII beyond what is necessary (respect privacy)
  ✗ Credentials or secrets (never in knowledge base)
  ✗ Outdated information without updating the entry
```

### Auto-Capture from Human Feedback

```
When human says "always do X for Y":
  → Create procedure entry immediately
  → Set confidence = HIGH (explicit instruction)
  → Apply immediately

When human corrects a decision:
  → Update relevant person profile
  → Create decision record noting the correction
  → Feed to Learning Skill

When human approves an AI action:
  → Reinforce relevant knowledge (bump confidence)
  → Log approval in decision history

When human rejects an AI action:
  → Flag related knowledge for review
  → Add correction note
  → Feed to Learning Skill as negative signal
```

---

## Person Profile Format

```markdown
# Person Profile: Alice Johnson

**KB ID**: KB-PEOPLE-001
**Created**: 2026-01-10
**Updated**: 2026-02-16
**Confidence**: HIGH (34 interactions)

---

## Identity
- **Full Name**: Alice Johnson
- **Role**: Project Manager
- **Company**: Acme Corp (client)
- **Email**: alice@company.com
- **Timezone**: EST (UTC-5)

---

## Communication Style
- **Preferred tone**: Professional, concise
- **Response expectation**: Same day for HIGH, next day for MEDIUM
- **Format preference**: Bullet points, not paragraphs
- **Summary length**: 3 bullets maximum

---

## Work Patterns
- **Sends files**: Monday mornings 08:00-10:00 (very consistent)
- **File types**: PDF (reports), DOCX (briefs), XLSX (budgets)
- **Typical volume**: 3-5 files per week
- **Priority**: Always HIGH (confirmed by 7 human corrections)

---

## Topics
- Sprint planning (owner)
- Q1/Q2/Q3/Q4 budget reviews (owner)
- Hiring and team growth (contributor)
- Client presentations (contributor)

---

## Active Projects
- Project Alpha: Q1 2026 (IN_PROGRESS, deadline March 31)
- Project Beta: Planning phase (PLANNING)

---

## Interaction History (last 5)
| Date     | File                  | Category | Result          |
|----------|-----------------------|----------|-----------------|
| Feb 15   | plan_sprint_7.pdf     | Planning | Summarized, HIGH|
| Feb 12   | budget_q1.xlsx        | Finance  | Flagged 3 items |
| Feb 10   | brief_project_alpha.docx | Planning| Summarized     |
| Feb 05   | report_jan.pdf        | Report   | Summarized, HIGH|
| Feb 03   | team_update.pdf       | HR/Team  | Summarized      |

---

## Applied Rules
- RULE-001: priority = HIGH (always)
- RULE-004: summary = 3 bullets max

---

## Notes
- Alice is time-sensitive — flag delays immediately
- She cc's Bob Chen on technical files
- Budget files always need a summary of key numbers
```

---

## Knowledge Index Format

```markdown
# Knowledge Base Index

**Generated**: 2026-02-16 14:00
**Total Entries**: 47
**Flagged for Review**: 3
**Expired**: 0

---

## By Type

| Type       | Count | Recent Addition        |
|------------|-------|------------------------|
| Facts      | 8     | Office closure policy  |
| People     | 12    | Acme Corp vendor       |
| Procedures | 9     | Invoice handling       |
| Decisions  | 6     | Priority escalation    |
| Lessons    | 7     | Alice HIGH priority    |
| Templates  | 5     | Email follow-up        |

---

## By Topic Tag

| Tag          | Entries | Top Entry               |
|--------------|---------|-------------------------|
| #finance     | 11      | Invoice 30-day terms    |
| #alice       | 8       | Alice Johnson profile   |
| #invoices    | 6       | Acme invoice procedure  |
| #priority    | 5       | HIGH priority triggers  |
| #security    | 4       | Quarantine procedure    |
| #email       | 4       | Email follow-up template|

---

## Recently Added (last 7 days)

| Date     | ID            | Title                          | Type      |
|----------|---------------|--------------------------------|-----------|
| Feb 16   | KB-LESSON-018 | Bob sends code on Fridays      | Lesson    |
| Feb 15   | KB-PEOPLE-012 | Acme Corp vendor profile       | Person    |
| Feb 14   | KB-PROC-009   | Large PDF chunked processing   | Procedure |

---

## Flagged for Review

| ID            | Entry                    | Flag Reason               | Priority |
|---------------|--------------------------|---------------------------|----------|
| KB-FACT-003   | Office address           | Not verified in 90 days   | LOW      |
| KB-PEOPLE-007 | John from TechVendor     | No interaction 95 days    | LOW      |
| KB-LESSON-012 | Bob priority rule        | Confidence dropped to 55% | MEDIUM   |
```

---

## Knowledge Governance

### Who Can Add Knowledge
```
AI Employee can add:
  - Observed patterns (after 3+ occurrences)
  - Inferred facts (with LOW confidence until confirmed)
  - Auto-captured corrections from human feedback
  - New entity stubs on first contact

Human must confirm before HIGH confidence:
  - Any fact that drives behavior
  - New procedures
  - Changes to existing entries
  - Sensitive personal information

Human exclusively can add:
  - Company policies and rules
  - Explicit personal preferences
  - Legal or financial facts
  - Entries marked as AUTHORITATIVE
```

### Knowledge Quality Levels
```
AUTHORITATIVE → Explicitly taught by human, cannot be auto-modified
  Example: "Always mark legal documents as CRITICAL priority"

VERIFIED → AI observed, human confirmed
  Example: "Alice sends files Monday mornings" (human said "yes, correct")

OBSERVED → AI detected pattern, not yet confirmed
  Example: "Bob's files seem to arrive Friday afternoons" (3 occurrences)

INFERRED → AI deduced from limited signals
  Example: "New vendor likely from the finance sector" (file type clues)

UNCERTAIN → Single observation or contradictory signals
  Example: "Invoice from unknown vendor — possibly recurring"
```

---

## Integration with Other Skills

### With Context Skill
```
knowledge-base → supplies → context with:
  Entity knowledge packages on demand
  Relevant procedures for current task type
  Domain knowledge for content analysis
  Decision precedents for similar situations
```

### With Learning Skill
```
learning → writes approved lessons to → knowledge-base:
  New active rules
  Updated confidence levels
  Retired rules (moved to history)
  Feedback patterns
```

### With Decision Skill
```
decision → queries → knowledge-base for:
  Precedents (how was similar situation handled before?)
  Entity-specific rules (any rules for this sender?)
  Procedure to follow (is there a defined process?)
  Authority level (who approves this type of action?)
```

### With Memory Management Skill
```
memory-management → maintains → knowledge-base:
  Archive old decision logs (keep index)
  Compress person profiles older than 1 year (keep summary)
  Remove expired entries
  Optimize knowledge/ folder size
```

### With Security Skill
```
security → enforces on → knowledge-base:
  No credentials stored in any knowledge file
  PII limited to necessary fields only
  AUTHORITATIVE entries cannot be modified by AI alone
  Access log for sensitive knowledge entries
```

### With Analytics Skill
```
analytics → reads from → knowledge-base:
  Entity interaction counts for entity analytics
  Lesson accuracy data for quality metrics
  Decision history for outcome tracking
```

### With Collaboration Skill
```
collaboration → shares → knowledge via:
  Knowledge packages in handoff records
  Entity profiles shared with human in escalations
  Procedure references in task instructions
```

---

## Best Practices

### DO
```
- Capture knowledge immediately when observed or taught
- Link related entries (people ↔ projects ↔ procedures)
- Set expiry dates for time-sensitive facts
- Update entries when corrections arrive
- Keep person profiles current after every interaction
- Index everything (unsearchable knowledge is worthless)
- Validate weekly (stale knowledge causes wrong decisions)
- Mark confidence levels honestly
```

### DON'T
```
- Store credentials or secrets in knowledge base
- Over-generalize from single observations (wait for 3+)
- Let knowledge base grow without pruning stale entries
- Store raw log data as knowledge (summarize instead)
- Mark uncertain observations as HIGH confidence
- Duplicate information across multiple entries
- Ignore expired entries (remove or renew them)
- Make knowledge entries too long (use summaries + links)
```

---

## Quick Reference: Knowledge by Use Case

```
Use Case                        | Knowledge Source          | Type
--------------------------------|---------------------------|----------
Processing file from Alice      | Knowledge/people/alice    | Person
Handling an invoice             | Knowledge/procedures/     | Procedure
Deciding priority for new sender| Knowledge/lessons/        | Lesson
Writing email to vendor         | Knowledge/templates/      | Template
Checking finance terms          | Knowledge/domain/finance  | Domain
Reviewing past similar decision | Knowledge/decisions/      | Decision
Understanding acronym in file   | Knowledge/facts/glossary  | Fact
Onboarding new entity           | Knowledge/procedures/     | Procedure
Verifying company policy        | Knowledge/facts/policies  | Fact
Checking if Alice likes bullets | Knowledge/people/alice    | Person
```

---

**Status**: Production Ready
**Priority**: HIGH (Foundation of all intelligent behavior)
**Total Knowledge Types**: 6 (Facts, People, Procedures, Decisions, Lessons, Templates)
**Retrieval Methods**: 5 (Direct, Tag, Entity, Situational, Full Text)
**Validation**: Weekly automated scan + human review queue
**Quality Levels**: 5 (Authoritative → Verified → Observed → Inferred → Uncertain)

*Good knowledge base = AI Employee that remembers everything, applies it correctly, and knows when it doesn't know*
