# Agent Skill: Process Email Tasks

## Purpose
Process email tasks created by Gmail Watcher in Needs_Action/ folder.

## When to Use
When you see task files starting with EMAIL_ in Needs_Action/

## Steps

1. **Scan Needs_Action** for EMAIL_*.md files
2. **Read each email task** file
3. **Analyze the email:**
   - What is the sender asking?
   - What action is required?
   - Is this time-sensitive?
   - Are there attachments to handle?
4. **Categorize** (invoice/meeting/request/information/other)
5. **Update priority** if analysis changes initial assessment
6. **Add analysis** to task file under "## Analysis" section
7. **Determine next action:**
   - Needs reply -> use draft_reply skill
   - Just archive -> move to Done/Communications/
   - Has attachment -> process attachment separately
8. **Log activity** to today's log file
9. **Update Dashboard** task counts

## Output
- Updated task file with analysis
- Draft reply file (if reply needed)
- Activity log entry
