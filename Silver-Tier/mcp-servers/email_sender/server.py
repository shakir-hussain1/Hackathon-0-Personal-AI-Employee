"""
Email Sender MCP Server - Silver Tier
Proper MCP server using mcp.server.Server with stdio transport.
Claude calls tools to draft and send emails with human approval.
"""

import os
import base64
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

_SILVER_ROOT = Path(__file__).parent.parent.parent
load_dotenv(_SILVER_ROOT / '.env')

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_SILVER_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
TOKEN_PATH = _SILVER_ROOT / '.gmail_send_token.json'
CREDENTIALS_PATH = _SILVER_ROOT / 'credentials.json'
APPROVED_DIR = VAULT_PATH / 'Approved'
DRAFTS_DIR = VAULT_PATH / 'Plans' / 'email_drafts'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('email_mcp_server')

server = Server("email-sender")


# ── Helpers ──────────────────────────────────────────────────────────────────

def _get_gmail_send_service():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                raise FileNotFoundError(f"credentials.json not found at {CREDENTIALS_PATH}")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=8082)
        with open(TOKEN_PATH, 'w') as f:
            f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def _log_activity(message: str):
    log_dir = VAULT_PATH / 'Logs'
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_dir / f"{today}.log", 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] [EMAIL_MCP] {message}\n")


# ── Tool definitions ──────────────────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="create_email_draft",
            description=(
                "Create an email draft saved to Plans/email_drafts/ awaiting human approval. "
                "The human must move the draft file to the Approved/ folder before it is sent. "
                "Returns the draft ID and file path."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "to":      {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject line"},
                    "body":    {"type": "string", "description": "Full email body text"},
                },
                "required": ["to", "subject", "body"],
            },
        ),
        types.Tool(
            name="list_pending_drafts",
            description="List all email drafts currently awaiting human approval in Plans/email_drafts/.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="check_and_send_approved",
            description=(
                "Check the Approved/ folder for approved email drafts and send them via Gmail. "
                "Returns a summary of emails sent."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


# ── Tool implementations ──────────────────────────────────────────────────────

def _create_email_draft(to: str, subject: str, body: str) -> str:
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    APPROVED_DIR.mkdir(exist_ok=True)

    draft_id = f"DRAFT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    draft_file = DRAFTS_DIR / f"{draft_id}.md"
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    content = (
        f"# Email Draft: {draft_id}\n"
        f"Created: {now_str}\n"
        "Status: AWAITING_APPROVAL\n"
        "\n"
        "## Envelope\n"
        f"**To:** {to}\n"
        f"**Subject:** {subject}\n"
        "\n"
        "## Body\n"
        f"{body}\n"
        "\n"
        "---\n"
        "## Approval Instructions\n"
        "To SEND this email:\n"
        f"  Move this file to: {APPROVED_DIR}/\n"
        "\n"
        "To DISCARD this email:\n"
        "  Delete this file or move to Done/\n"
        "\n"
        "The AI Employee checks the Approved folder every 5 minutes.\n"
    )

    draft_file.write_text(content, encoding='utf-8')
    _log_activity(f"Draft created: {draft_id} | To: {to} | Subject: {subject}")
    logger.info(f"Draft saved: {draft_file}")
    return f"Draft created: {draft_id}\nFile: {draft_file}\nMove to Approved/ folder to send."


def _list_pending_drafts() -> str:
    if not DRAFTS_DIR.exists():
        return "No drafts directory found. No pending drafts."
    drafts = sorted(DRAFTS_DIR.glob("DRAFT_*.md"))
    if not drafts:
        return "No pending drafts."
    lines = [f"Found {len(drafts)} pending draft(s):\n"]
    for draft_file in drafts:
        try:
            text = draft_file.read_text(encoding='utf-8').split('\n')
            to = next((l.replace('**To:**', '').strip() for l in text if '**To:**' in l), 'Unknown')
            subject = next((l.replace('**Subject:**', '').strip() for l in text if '**Subject:**' in l), 'Unknown')
            lines.append(f"  - {draft_file.name}: To={to} | Subject={subject}")
        except Exception as e:
            lines.append(f"  - {draft_file.name}: (error reading: {e})")
    return '\n'.join(lines)


def _check_and_send_approved() -> str:
    if not APPROVED_DIR.exists():
        return "Approved directory not found."
    drafts = list(APPROVED_DIR.glob("DRAFT_*.md"))
    if not drafts:
        return "No approved drafts to send."

    sent, errors = [], []
    for draft_file in drafts:
        try:
            lines = draft_file.read_text(encoding='utf-8').split('\n')
            to = next((l.replace('**To:**', '').strip() for l in lines if '**To:**' in l), None)
            subject = next((l.replace('**Subject:**', '').strip() for l in lines if '**Subject:**' in l), None)
            body_start = next((i for i, l in enumerate(lines) if l == '## Body'), None)
            sep = next((i for i, l in enumerate(lines) if l.startswith('---')), len(lines))
            body = '\n'.join(lines[body_start + 1:sep]).strip() if body_start is not None else ''

            if not (to and subject and body):
                errors.append(f"{draft_file.name}: missing To/Subject/Body")
                continue

            service = _get_gmail_send_service()
            msg = MIMEText(body)
            msg['to'] = to
            msg['subject'] = subject
            raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            result = service.users().messages().send(userId='me', body={'raw': raw}).execute()

            done_dir = VAULT_PATH / 'Done' / 'Communications'
            done_dir.mkdir(parents=True, exist_ok=True)
            draft_file.rename(done_dir / draft_file.name)

            _log_activity(f"Email sent: To={to} | Subject={subject} | Gmail ID={result['id']}")
            sent.append(f"Sent to {to}: {subject}")

        except Exception as e:
            errors.append(f"{draft_file.name}: {e}")
            logger.error(f"Failed to send {draft_file.name}: {e}")

    out = []
    if sent:
        out.append(f"Sent {len(sent)} email(s):")
        out.extend(f"  ✓ {s}" for s in sent)
    if errors:
        out.append(f"\n{len(errors)} error(s):")
        out.extend(f"  ✗ {e}" for e in errors)
    return '\n'.join(out) if out else "No emails processed."


# ── Dispatch ──────────────────────────────────────────────────────────────────

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "create_email_draft":
        result = _create_email_draft(
            to=arguments["to"],
            subject=arguments["subject"],
            body=arguments["body"],
        )
    elif name == "list_pending_drafts":
        result = _list_pending_drafts()
    elif name == "check_and_send_approved":
        result = _check_and_send_approved()
    else:
        result = f"Unknown tool: {name}"
    return [types.TextContent(type="text", text=result)]


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    logger.info("Email Sender MCP Server starting (stdio transport)...")
    logger.info(f"Vault: {VAULT_PATH}")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == '__main__':
    asyncio.run(main())
