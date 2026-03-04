# Agent Skill: Draft Email Reply

## Purpose
Generate a draft email reply for human review and approval before sending.

## When to Use
After process_email determines a reply is needed.

## Steps

1. **Read the original email** task file in Needs_Action/
2. **Understand context:**
   - What did they ask?
   - What is the appropriate tone? (formal/professional/casual)
   - What information do I have to answer?
3. **Draft the reply:**
   - Use templates from mcp-servers/email_sender/templates/
   - Keep it concise and professional
   - Answer all questions asked
   - State any next steps clearly
4. **Save draft** to AI_Employee_Vault/Plans/email_drafts/DRAFT_{timestamp}.md
   - Format: To, Subject, Body
5. **Add note** to original task: "Reply drafted: DRAFT_{timestamp}.md"
6. **Notify human** by updating Dashboard:
   - Add entry: "Email reply ready for approval: DRAFT_{timestamp}.md"
7. **Log activity**

## Approval Process
Human reviews draft in Plans/email_drafts/
To approve: Move file to AI_Employee_Vault/Approved/
To reject: Delete or edit the file

Email Sender checks Approved/ every 5 minutes and sends automatically.

## Output
- Draft file in Plans/email_drafts/
- Updated task file
- Dashboard notification
- Log entry
