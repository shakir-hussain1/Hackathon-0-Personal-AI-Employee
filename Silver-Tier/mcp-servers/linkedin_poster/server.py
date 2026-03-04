"""
LinkedIn Poster MCP Server - Silver Tier
Claude calls tools to draft and publish LinkedIn posts for business promotion.
Human approval required before any post goes live.
"""

import os
import json
import asyncio
import logging
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

_SILVER_ROOT = Path(__file__).parent.parent.parent
load_dotenv(_SILVER_ROOT / '.env')

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_SILVER_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
LINKEDIN_AUTHOR_URN = os.getenv('LINKEDIN_AUTHOR_URN', '')   # e.g. "urn:li:person:XXXXXXXX"
QUEUE_DIR = VAULT_PATH / 'LinkedIn_Queue'
APPROVED_DIR = VAULT_PATH / 'LinkedIn_Approved'

LINKEDIN_API_BASE = 'https://api.linkedin.com/v2'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('linkedin_mcp_server')

server = Server("linkedin-poster")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _log(message: str):
    log_dir = VAULT_PATH / 'Logs'
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_dir / f"{today}.log", 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] [LINKEDIN_MCP] {message}\n")


def _post_to_linkedin_api(text: str, visibility: str = 'PUBLIC') -> dict:
    """Post to LinkedIn via UGC Posts API."""
    if not LINKEDIN_ACCESS_TOKEN:
        raise ValueError("LINKEDIN_ACCESS_TOKEN not set in .env")
    if not LINKEDIN_AUTHOR_URN:
        raise ValueError("LINKEDIN_AUTHOR_URN not set in .env (e.g. urn:li:person:XXXXXXXX)")

    headers = {
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0',
    }
    payload = {
        "author": LINKEDIN_AUTHOR_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": visibility
        },
    }
    response = requests.post(
        f"{LINKEDIN_API_BASE}/ugcPosts",
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json() if response.text else {"status": "posted", "id": response.headers.get('x-restli-id', 'unknown')}


# ── Tool definitions ──────────────────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="create_linkedin_draft",
            description=(
                "Save a LinkedIn post draft to LinkedIn_Queue/ for human review. "
                "The human moves the file to LinkedIn_Approved/ to authorize posting. "
                "Use this for all LinkedIn posts — never post directly without approval."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The full text of the LinkedIn post (max 1300 chars recommended)",
                    },
                    "post_type": {
                        "type": "string",
                        "enum": ["announcement", "insight", "milestone", "thought_leadership", "promotion"],
                        "description": "Category of post for reference",
                    },
                    "visibility": {
                        "type": "string",
                        "enum": ["PUBLIC", "CONNECTIONS"],
                        "description": "Who can see the post (default PUBLIC)",
                    },
                },
                "required": ["content", "post_type"],
            },
        ),
        types.Tool(
            name="post_approved_linkedin_drafts",
            description=(
                "Check LinkedIn_Approved/ folder and publish any approved LinkedIn post drafts. "
                "Only call this after the human has moved drafts to LinkedIn_Approved/."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="list_linkedin_queue",
            description="List all LinkedIn post drafts currently awaiting approval.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


# ── Tool implementations ──────────────────────────────────────────────────────

def _create_linkedin_draft(content: str, post_type: str, visibility: str = 'PUBLIC') -> str:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    APPROVED_DIR.mkdir(exist_ok=True)

    char_count = len(content)
    if char_count > 3000:
        return f"Error: Post is {char_count} characters. LinkedIn limit is 3000; aim for under 1300."

    draft_id = f"LIPOST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    draft_file = QUEUE_DIR / f"{draft_id}.md"
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    file_content = (
        f"# LinkedIn Post Draft: {draft_id}\n"
        f"Created: {now_str}\n"
        f"Type: {post_type}\n"
        f"Visibility: {visibility}\n"
        f"Characters: {char_count}/3000\n"
        "Status: AWAITING_APPROVAL\n"
        "\n"
        "## Post Content\n"
        f"{content}\n"
        "\n"
        "---\n"
        "## Approval Instructions\n"
        "To PUBLISH this post:\n"
        f"  Move this file to: {APPROVED_DIR}/\n"
        "\n"
        "To DISCARD this post:\n"
        "  Delete this file.\n"
        "\n"
        "The AI Employee checks LinkedIn_Approved/ on its next scheduled run.\n"
    )

    draft_file.write_text(file_content, encoding='utf-8')
    _log(f"LinkedIn draft created: {draft_id} | Type: {post_type} | {char_count} chars")
    return (
        f"LinkedIn draft saved: {draft_id}\n"
        f"File: {draft_file}\n"
        f"Characters: {char_count}/3000\n"
        f"Move to LinkedIn_Approved/ to publish."
    )


def _post_approved_drafts() -> str:
    if not APPROVED_DIR.exists():
        return "LinkedIn_Approved/ directory not found."
    drafts = list(APPROVED_DIR.glob("LIPOST_*.md"))
    if not drafts:
        return "No approved LinkedIn drafts to post."

    posted, errors = [], []
    for draft_file in drafts:
        try:
            lines = draft_file.read_text(encoding='utf-8').split('\n')
            visibility = next((l.replace('Visibility:', '').strip() for l in lines if l.startswith('Visibility:')), 'PUBLIC')

            content_start = next((i for i, l in enumerate(lines) if l == '## Post Content'), None)
            sep = next((i for i, l in enumerate(lines) if l.startswith('---')), len(lines))
            content = '\n'.join(lines[content_start + 1:sep]).strip() if content_start is not None else ''

            if not content:
                errors.append(f"{draft_file.name}: empty content")
                continue

            result = _post_to_linkedin_api(content, visibility)
            post_id = result.get('id', 'unknown')

            done_dir = VAULT_PATH / 'Done' / 'Communications'
            done_dir.mkdir(parents=True, exist_ok=True)
            draft_file.rename(done_dir / draft_file.name)

            _log(f"LinkedIn post published: {draft_file.name} | Post ID: {post_id}")
            posted.append(f"Published {draft_file.name} (LinkedIn ID: {post_id})")

        except Exception as e:
            errors.append(f"{draft_file.name}: {e}")
            logger.error(f"Failed to post {draft_file.name}: {e}")

    out = []
    if posted:
        out.append(f"Published {len(posted)} post(s):")
        out.extend(f"  ✓ {p}" for p in posted)
    if errors:
        out.append(f"\n{len(errors)} error(s):")
        out.extend(f"  ✗ {e}" for e in errors)
    return '\n'.join(out)


def _list_linkedin_queue() -> str:
    if not QUEUE_DIR.exists():
        return "No LinkedIn_Queue/ directory. No pending drafts."
    drafts = sorted(QUEUE_DIR.glob("LIPOST_*.md"))
    if not drafts:
        return "No LinkedIn drafts pending approval."
    lines = [f"Found {len(drafts)} LinkedIn draft(s) awaiting approval:\n"]
    for f in drafts:
        try:
            text = f.read_text(encoding='utf-8').split('\n')
            post_type = next((l.replace('Type:', '').strip() for l in text if l.startswith('Type:')), 'Unknown')
            chars = next((l.replace('Characters:', '').strip() for l in text if l.startswith('Characters:')), '?')
            lines.append(f"  - {f.name}: Type={post_type} | {chars} chars")
        except Exception as e:
            lines.append(f"  - {f.name}: (error: {e})")
    return '\n'.join(lines)


# ── Dispatch ──────────────────────────────────────────────────────────────────

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "create_linkedin_draft":
        result = _create_linkedin_draft(
            content=arguments["content"],
            post_type=arguments["post_type"],
            visibility=arguments.get("visibility", "PUBLIC"),
        )
    elif name == "post_approved_linkedin_drafts":
        result = _post_approved_drafts()
    elif name == "list_linkedin_queue":
        result = _list_linkedin_queue()
    else:
        result = f"Unknown tool: {name}"
    return [types.TextContent(type="text", text=result)]


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    logger.info("LinkedIn Poster MCP Server starting (stdio transport)...")
    logger.info(f"Vault: {VAULT_PATH}")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == '__main__':
    asyncio.run(main())
