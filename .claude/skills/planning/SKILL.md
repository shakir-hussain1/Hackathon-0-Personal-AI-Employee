# 📋 Planning Skill

**Purpose**: Break complex tasks into clear, executable plans
**Output**: Step-by-step execution plans with dependencies
**Format**: Markdown checklists, dependency graphs, timelines

---

## 🎯 Core Capabilities

### 1. Break Tasks into Steps
Transform vague requests into concrete action items

### 2. Create Checklists
Generate trackable, sequential task lists

### 3. Detect Dependencies
Identify what must happen before what

### 4. Output Execution Plans
Clear, actionable plans ready to execute

---

## 📝 Planning Process

```
Input: Complex Task
    ↓
1. Understand Goal
    ↓
2. Break into Phases
    ↓
3. Identify Steps
    ↓
4. Detect Dependencies
    ↓
5. Order Sequentially
    ↓
6. Add Checkpoints
    ↓
Output: Execution Plan
```

---

## 🔨 Task Breakdown Strategy

### Step 1: Goal Analysis

**Questions to ask:**
```markdown
- What is the desired outcome?
- Who is involved?
- What resources are needed?
- What are the constraints?
- What defines success?
```

**Example:**
```markdown
Task: "Launch new website"

Goal Analysis:
- Outcome: Live website accessible to users
- Involved: Designer, Developer, Content writer
- Resources: Domain, hosting, content, design files
- Constraints: 2-week timeline, $5k budget
- Success: Site live, fast, mobile-friendly
```

---

### Step 2: Phase Identification

**Break into major phases:**

```markdown
Phase 1: Planning & Design (Days 1-3)
Phase 2: Development (Days 4-8)
Phase 3: Content & Assets (Days 9-11)
Phase 4: Testing & QA (Days 12-13)
Phase 5: Launch (Day 14)
```

**Phase criteria:**
- Each phase has clear deliverable
- Phases can be parallelized where possible
- Each phase 20-40% of total time
- 3-7 phases (not too many, not too few)

---

### Step 3: Step Decomposition

**For each phase, list concrete steps:**

```markdown
Phase 1: Planning & Design
├── 1.1 Define requirements
├── 1.2 Create wireframes
├── 1.3 Design mockups
├── 1.4 Get approval
└── 1.5 Finalize design

Phase 2: Development
├── 2.1 Setup development environment
├── 2.2 Create site structure
├── 2.3 Implement responsive layout
├── 2.4 Add navigation
├── 2.5 Integrate CMS
└── 2.6 Code review
```

**Good step characteristics:**
- ✅ Specific and concrete
- ✅ Measurable (done or not done)
- ✅ Assigned to person/role
- ✅ Time-bounded (hours/days)
- ✅ Produces deliverable

**Bad step characteristics:**
- ❌ Vague ("work on design")
- ❌ Too large (weeks of work)
- ❌ Ambiguous completion criteria
- ❌ Multiple people unclear

---

## ✅ Checklist Generation

### Basic Checklist Format

```markdown
## Execution Checklist

### Pre-flight Checks
- [ ] All resources available
- [ ] Team members notified
- [ ] Tools/access configured
- [ ] Deadline confirmed

### Phase 1: Planning & Design
- [ ] Requirements documented
- [ ] Wireframes created (Designer)
- [ ] Mockups designed (Designer)
- [ ] Design approved (Client)
- [ ] Design files delivered

### Phase 2: Development
- [ ] Dev environment ready (Developer)
- [ ] Site structure created (Developer)
- [ ] Responsive layout implemented (Developer)
- [ ] Navigation working (Developer)
- [ ] CMS integrated (Developer)
- [ ] Code reviewed (Tech Lead)

### Phase 3: Content & Assets
- [ ] Copy written (Content Writer)
- [ ] Images optimized (Designer)
- [ ] Content uploaded (Content Writer)
- [ ] SEO metadata added (Content Writer)

### Phase 4: Testing & QA
- [ ] Browser testing (QA)
- [ ] Mobile testing (QA)
- [ ] Performance testing (QA)
- [ ] Bug fixes complete (Developer)
- [ ] Final review (Client)

### Phase 5: Launch
- [ ] Domain configured (DevOps)
- [ ] SSL certificate installed (DevOps)
- [ ] Site deployed (DevOps)
- [ ] DNS propagated (DevOps)
- [ ] Launch verified (Team)

### Post-Launch
- [ ] Monitor uptime
- [ ] Check analytics
- [ ] Gather feedback
```

---

### Advanced Checklist Features

**With Time Estimates:**
```markdown
- [ ] Requirements documented (2h)
- [ ] Wireframes created (4h)
- [ ] Mockups designed (8h)
- [ ] Design approved (1h meeting)
```

**With Assignees:**
```markdown
- [ ] @designer Create wireframes
- [ ] @developer Setup environment
- [ ] @writer Draft homepage copy
```

**With Priorities:**
```markdown
- [ ] 🔴 HIGH: SSL certificate (blocking)
- [ ] 🟡 MEDIUM: Image optimization
- [ ] 🟢 LOW: Add favicon
```

**With Dependencies:**
```markdown
- [ ] Design mockups ⟵ Requires: Wireframes
- [ ] Code layout ⟵ Requires: Design mockups
- [ ] Content upload ⟵ Requires: CMS integration
```

---

## 🔗 Dependency Detection

### Types of Dependencies

**1. Sequential (Must happen in order)**
```markdown
A → B → C

Example:
Design → Code → Test
Can't code before design
Can't test before code
```

**2. Blocking (B can't start until A done)**
```markdown
A blocks B

Example:
Domain purchase blocks DNS setup
API key blocks API integration
```

**3. Parallel (Can happen simultaneously)**
```markdown
A ‖ B ‖ C

Example:
Design ‖ Write copy ‖ Setup hosting
All independent, can do together
```

**4. Convergent (Multiple inputs to one output)**
```markdown
A ↘
    C
B ↗

Example:
Design + Content → Combine into pages
```

---

### Dependency Notation

**Standard format:**
```markdown
Task: [ID] Description
Depends on: [ID, ID, ID]
Blocks: [ID, ID]
```

**Example:**
```markdown
[1.1] Define requirements
Depends on: None (starting task)
Blocks: [1.2], [1.3]

[1.2] Create wireframes
Depends on: [1.1]
Blocks: [1.3]

[1.3] Design mockups
Depends on: [1.2]
Blocks: [1.4], [2.3]

[2.3] Code layout
Depends on: [1.3], [2.1]
Blocks: [2.4]
```

---

### Dependency Graph

**Visual representation:**

```markdown
                    [1.1] Requirements
                          ↓
                    [1.2] Wireframes
                          ↓
                    [1.3] Mockups
                          ↓
         ┌────────────────┼────────────────┐
         ↓                ↓                ↓
   [2.3] Layout    [3.1] Content    [2.5] CMS
         ↓                ↓                ↓
         └────────────────┼────────────────┘
                          ↓
                    [3.2] Upload
                          ↓
                    [4.1] Testing
                          ↓
                    [5.1] Launch
```

---

### Critical Path

**Definition**: Longest sequence of dependent tasks

**Why it matters**: Determines minimum project duration

**How to find:**
```markdown
1. List all task sequences end-to-end
2. Calculate total time for each
3. Longest sequence = critical path
4. These tasks cannot be delayed

Example:
Path 1: Req → Wire → Mock → Code → Test → Launch = 14 days
Path 2: Content → Upload → Test → Launch = 8 days
Path 3: Setup → CMS → Upload → Test → Launch = 10 days

Critical path: Path 1 (14 days) ← Determines project timeline
```

**Critical tasks** (on critical path):
- Must be monitored closely
- Delays here delay entire project
- Should have buffer time
- Highest priority

---

## 📊 Execution Plan Template

### Complete Plan Format

```markdown
# Execution Plan: [Project Name]

**Goal**: [Clear objective]
**Timeline**: [Start date] to [End date]
**Owner**: [Primary responsible person]
**Status**: 🟡 Planning / 🔵 In Progress / 🟢 Complete

---

## 📋 Quick Summary

- **Total Tasks**: 25
- **Estimated Time**: 14 days
- **Team Size**: 4 people
- **Critical Path**: 14 days (Design → Code → Test → Launch)
- **Parallel Work**: Design + Content (saves 3 days)

---

## 🎯 Success Criteria

- [ ] Website live and accessible
- [ ] Page load < 2 seconds
- [ ] Mobile responsive
- [ ] All content published
- [ ] Analytics tracking active

---

## 👥 Team & Roles

| Role | Person | Responsibilities |
|------|--------|-----------------|
| Designer | Alice | Wireframes, mockups, assets |
| Developer | Bob | Code, integration, deployment |
| Writer | Carol | Copy, content, SEO |
| QA | Dave | Testing, bug reports |

---

## 📅 Timeline

```
Week 1:
├── Mon-Wed: Phase 1 (Design)
└── Thu-Fri: Phase 2 start (Development)

Week 2:
├── Mon-Wed: Phase 2 cont + Phase 3 (Content)
├── Thu: Phase 4 (Testing)
└── Fri: Phase 5 (Launch)
```

---

## 🔄 Phases

### Phase 1: Planning & Design (3 days)
**Goal**: Approved design ready for development
**Owner**: Alice (Designer)
**Deliverable**: Design files + approval

#### Tasks:
- [ ] [1.1] Define requirements (2h) - Alice + Client
  - Depends on: None
  - Blocks: [1.2]

- [ ] [1.2] Create wireframes (4h) - Alice
  - Depends on: [1.1]
  - Blocks: [1.3]

- [ ] [1.3] Design mockups (8h) - Alice
  - Depends on: [1.2]
  - Blocks: [1.4], [2.3]

- [ ] [1.4] Get approval (1h) - Client
  - Depends on: [1.3]
  - Blocks: [2.3]

**Checkpoint**: ✅ Design approved, files delivered

---

### Phase 2: Development (5 days)
**Goal**: Functional website coded
**Owner**: Bob (Developer)
**Deliverable**: Working site on staging

#### Tasks:
- [ ] [2.1] Setup dev environment (2h) - Bob
  - Depends on: None (parallel with design)
  - Blocks: [2.2]

- [ ] [2.2] Create site structure (4h) - Bob
  - Depends on: [2.1]
  - Blocks: [2.3]

- [ ] [2.3] Code responsive layout (12h) - Bob
  - Depends on: [2.2], [1.3] ← Design mockups
  - Blocks: [2.4]
  - 🔴 CRITICAL PATH

- [ ] [2.4] Add navigation (4h) - Bob
  - Depends on: [2.3]
  - Blocks: [2.5]

- [ ] [2.5] Integrate CMS (8h) - Bob
  - Depends on: [2.4]
  - Blocks: [3.2]

- [ ] [2.6] Code review (2h) - Tech Lead
  - Depends on: [2.5]
  - Blocks: [3.2]

**Checkpoint**: ✅ Code reviewed, staging site ready

---

### Phase 3: Content & Assets (3 days, parallel)
**Goal**: All content ready and uploaded
**Owner**: Carol (Writer)
**Deliverable**: Published content

#### Tasks:
- [ ] [3.1] Write all copy (12h) - Carol
  - Depends on: [1.3] (design context)
  - Blocks: [3.2]
  - Can work parallel with Phase 2

- [ ] [3.2] Upload content (4h) - Carol
  - Depends on: [3.1], [2.5] ← CMS ready
  - Blocks: [4.1]

**Checkpoint**: ✅ All content live on staging

---

### Phase 4: Testing & QA (2 days)
**Goal**: All bugs fixed, site polished
**Owner**: Dave (QA)
**Deliverable**: Bug-free site approved for launch

#### Tasks:
- [ ] [4.1] Browser testing (4h) - Dave
  - Depends on: [3.2]
  - Blocks: [4.4]

- [ ] [4.2] Mobile testing (4h) - Dave
  - Depends on: [3.2]
  - Blocks: [4.4]

- [ ] [4.3] Performance testing (2h) - Dave
  - Depends on: [3.2]
  - Blocks: [4.4]

- [ ] [4.4] Bug fixes (8h) - Bob
  - Depends on: [4.1], [4.2], [4.3]
  - Blocks: [4.5]
  - 🔴 CRITICAL PATH

- [ ] [4.5] Final approval (1h) - Client
  - Depends on: [4.4]
  - Blocks: [5.1]

**Checkpoint**: ✅ Client approved for production

---

### Phase 5: Launch (1 day)
**Goal**: Site live and accessible to public
**Owner**: DevOps
**Deliverable**: Live production website

#### Tasks:
- [ ] [5.1] Configure domain (1h) - DevOps
  - Depends on: [4.5]
  - Blocks: [5.3]

- [ ] [5.2] Install SSL (1h) - DevOps
  - Depends on: [4.5]
  - Blocks: [5.3]

- [ ] [5.3] Deploy to production (2h) - DevOps
  - Depends on: [5.1], [5.2]
  - Blocks: [5.4]
  - 🔴 CRITICAL PATH

- [ ] [5.4] Verify launch (1h) - Team
  - Depends on: [5.3]
  - Blocks: None (end task)

**Checkpoint**: ✅ Site live and verified

---

## 🚨 Risk Management

### Identified Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Design approval delayed | 🔴 High | Daily check-ins with client |
| Browser bugs found late | 🟡 Medium | Early cross-browser testing |
| Content delivery late | 🟡 Medium | Parallel writing with dev |
| DNS propagation slow | 🟢 Low | Configure DNS early |

---

## 📊 Progress Tracking

**Daily standup questions:**
- What did you complete yesterday?
- What will you complete today?
- Any blockers?

**Weekly review:**
- Tasks completed vs planned
- On track for deadline?
- Any risks materialized?
- Need to adjust plan?

---

## 🔄 Plan Adjustments

**If behind schedule:**
1. Identify critical path delays
2. Add resources to critical tasks
3. Reduce scope of non-critical features
4. Parallelize more work if possible

**If ahead of schedule:**
1. Use buffer time for polish
2. Add nice-to-have features
3. Extra testing rounds
4. Early launch

---

## 📝 Meeting Notes Template

### Planning Meeting
**Date**: [Date]
**Attendees**: [Names]

#### Decisions Made:
- Decision 1
- Decision 2

#### Action Items:
- [ ] @person Do task by [date]
- [ ] @person Do task by [date]

#### Next Meeting:
**Date**: [Date]
**Agenda**: [Topics]
```

---

## 🎯 Planning Best Practices

### DO ✅

**1. Start with the end**
- Define success criteria first
- Work backwards to steps
- Clear goal = clear plan

**2. Right-size tasks**
- Each task: 1-8 hours
- Too large → break down
- Too small → combine

**3. Identify dependencies early**
- What blocks what?
- What can parallelize?
- Critical path analysis

**4. Add checkpoints**
- End of each phase
- Verify deliverables
- Catch issues early

**5. Buffer for unknowns**
- Add 20% time buffer
- Expect the unexpected
- Don't plan to 100% capacity

**6. Assign ownership**
- Every task has owner
- One person accountable
- Clear responsibilities

**7. Make it visual**
- Gantt charts, diagrams
- Easy to understand
- Track progress visually

---

### DON'T ❌

**1. Don't skip planning**
- "Just start coding" = chaos
- Time planning saves time executing

**2. Don't plan too detailed**
- 50-page plans nobody reads
- Balance detail with flexibility

**3. Don't ignore dependencies**
- Missed dependencies = delays
- Map them explicitly

**4. Don't forget resources**
- Plans assume unlimited resources
- Check availability first

**5. Don't make it static**
- Plans change, that's okay
- Update as you learn

**6. Don't plan alone**
- Get team input
- Those doing work know best

**7. Don't hide risks**
- Surface issues early
- Better to know now than later

---

## 🔍 Quick Planning Guide

### 1-Hour Task
```markdown
✅ Single checklist item
✅ One person
✅ Clear output
Example: "Write homepage copy"
```

### 1-Day Task
```markdown
✅ 3-5 checklist items
✅ One person
✅ Mini-phases
Example: "Design homepage mockup"
  - Sketch concepts
  - Create digital mockup
  - Get feedback
  - Iterate
```

### 1-Week Project
```markdown
✅ 2-3 phases
✅ 10-20 tasks
✅ 2-3 people
✅ Daily checkpoints
Example: "Build landing page"
```

### 1-Month Project
```markdown
✅ 4-5 phases
✅ 30-50 tasks
✅ 3-5 people
✅ Weekly checkpoints
Example: "Launch new website"
```

### 3-Month Project
```markdown
✅ 6-8 phases
✅ 100+ tasks
✅ 5-10 people
✅ Bi-weekly checkpoints
Example: "Build mobile app"
```

---

## 📊 Planning Metrics

**Good plan characteristics:**
- ✅ Every task < 8 hours
- ✅ Dependencies mapped
- ✅ Owners assigned
- ✅ Checkpoints every 3-5 days
- ✅ Total time = sum + 20% buffer
- ✅ Critical path identified
- ✅ Risks documented

**Plan health indicators:**
- 🟢 Green: On track, no blockers
- 🟡 Yellow: Minor delays, manageable
- 🔴 Red: Blocked, needs intervention

---

## 🚀 From Plan to Execution

**1. Kickoff meeting**
- Present plan to team
- Confirm understanding
- Address questions
- Get commitment

**2. Setup tracking**
- Create task board (Kanban/Trello)
- Assign initial tasks
- Setup daily standup
- Configure notifications

**3. Execute with discipline**
- Follow the plan
- Update task status daily
- Communicate blockers immediately
- Hold regular check-ins

**4. Adapt as needed**
- Learn from reality
- Adjust timeline if needed
- Re-prioritize if needed
- Update plan document

**5. Celebrate milestones**
- Mark phase completions
- Acknowledge wins
- Maintain momentum

---

**Status**: Production Ready
**Use Case**: All complex tasks requiring structured execution
**Output Format**: Markdown checklist + dependency graph + timeline

*Good planning makes execution look easy.*
