"""
Gold-Tier Facebook + Instagram MCP Server
Uses Meta Graph API to post content and generate engagement summaries.

Setup:
  1. Create Facebook Developer App: https://developers.facebook.com/
  2. Get Page Access Token with pages_manage_posts + instagram_basic + instagram_content_publish scopes
  3. Set FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN, IG_ACCOUNT_ID in .env

API Docs:
  Facebook: https://developers.facebook.com/docs/graph-api/reference/page/feed/
  Instagram: https://developers.facebook.com/docs/instagram-api/guides/content-publishing/
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

_GOLD_ROOT = Path(__file__).parent.parent.parent
load_dotenv(_GOLD_ROOT / '.env')
sys.path.insert(0, str(_GOLD_ROOT))
from orchestrator.audit_logger import audit_log
from orchestrator.error_handler import with_retry, meta_breaker, TransientError

FB_PAGE_ID = os.getenv('FB_PAGE_ID', '')
FB_PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN', '')
IG_ACCOUNT_ID = os.getenv('IG_ACCOUNT_ID', '')
GRAPH_API_BASE = 'https://graph.facebook.com/v19.0'
DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'
VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_GOLD_ROOT.parent / 'Common' / 'AI_Employee_Vault')))

server = Server("facebook-instagram")


def _missing_config() -> str | None:
    missing = []
    if not FB_PAGE_ID:
        missing.append('FB_PAGE_ID')
    if not FB_PAGE_ACCESS_TOKEN:
        missing.append('FB_PAGE_ACCESS_TOKEN')
    if missing:
        return f"Missing in .env: {', '.join(missing)}. See Gold-Tier/config/social_media_setup.md"
    return None


@with_retry(max_attempts=3, base_delay=2, retryable=(TransientError,))
@meta_breaker
def _graph_post(endpoint: str, data: dict) -> dict:
    """POST to Meta Graph API."""
    resp = requests.post(
        f"{GRAPH_API_BASE}/{endpoint}",
        params={'access_token': FB_PAGE_ACCESS_TOKEN},
        json=data,
        timeout=20,
    )
    if resp.status_code == 429:
        raise TransientError("Meta API rate limited")
    if not resp.ok:
        raise TransientError(f"Meta API error {resp.status_code}: {resp.text[:200]}")
    return resp.json()


@with_retry(max_attempts=3, base_delay=2, retryable=(TransientError,))
@meta_breaker
def _graph_get(endpoint: str, params: dict = None) -> dict:
    """GET from Meta Graph API."""
    p = {'access_token': FB_PAGE_ACCESS_TOKEN}
    if params:
        p.update(params)
    resp = requests.get(f"{GRAPH_API_BASE}/{endpoint}", params=p, timeout=20)
    if not resp.ok:
        raise TransientError(f"Meta API error {resp.status_code}: {resp.text[:200]}")
    return resp.json()


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="post_to_facebook",
            description="Post a message to your Facebook Page. Requires approval for first post.",
            inputSchema={
                "type": "object",
                "required": ["message"],
                "properties": {
                    "message": {"type": "string", "description": "Post text (max 63,206 chars)"},
                    "link": {"type": "string", "description": "Optional URL to attach"},
                    "scheduled_publish_time": {
                        "type": "string",
                        "description": "Optional ISO datetime to schedule post",
                    },
                },
            },
        ),
        types.Tool(
            name="post_to_instagram",
            description="Post an image or text to Instagram Business account.",
            inputSchema={
                "type": "object",
                "required": ["caption", "image_url"],
                "properties": {
                    "caption": {"type": "string", "description": "Post caption with hashtags"},
                    "image_url": {
                        "type": "string",
                        "description": "Public URL to image (JPEG/PNG, min 500px)",
                    },
                },
            },
        ),
        types.Tool(
            name="get_facebook_summary",
            description="Get Facebook Page performance summary: posts, reactions, reach for a period.",
            inputSchema={
                "type": "object",
                "properties": {
                    "period_days": {"type": "integer", "description": "Days to summarize (default: 7)"},
                },
            },
        ),
        types.Tool(
            name="get_instagram_summary",
            description="Get Instagram account summary: followers, recent posts, engagement.",
            inputSchema={
                "type": "object",
                "properties": {
                    "period_days": {"type": "integer", "description": "Days to summarize (default: 7)"},
                },
            },
        ),
        types.Tool(
            name="save_social_draft",
            description="Save a social media draft to LinkedIn_Queue/ for human review before posting.",
            inputSchema={
                "type": "object",
                "required": ["platform", "content"],
                "properties": {
                    "platform": {
                        "type": "string",
                        "enum": ["facebook", "instagram", "both"],
                    },
                    "content": {"type": "string", "description": "Post text"},
                    "image_url": {"type": "string", "description": "Image URL (Instagram)"},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    audit_log(f'social_{name}', actor='facebook-instagram', parameters=arguments)

    if name == "post_to_facebook":
        return await _post_to_facebook(arguments)
    elif name == "post_to_instagram":
        return await _post_to_instagram(arguments)
    elif name == "get_facebook_summary":
        return await _get_facebook_summary(arguments)
    elif name == "get_instagram_summary":
        return await _get_instagram_summary(arguments)
    elif name == "save_social_draft":
        return await _save_social_draft(arguments)
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def _post_to_facebook(args: dict) -> list[types.TextContent]:
    err = _missing_config()
    if err:
        return [types.TextContent(type="text", text=err)]

    if DRY_RUN:
        audit_log('facebook_post', result='dry_run', parameters=args)
        return [types.TextContent(type="text", text=
            f"[DRY RUN] Would post to Facebook Page {FB_PAGE_ID}:\n\n{args['message']}\n\n"
            "Set DRY_RUN=false in .env to post for real.")]

    # Create approval file first (HITL for social posts)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    approval_file = VAULT_PATH / 'Pending_Approval' / f'FB_POST_{ts}.md'
    approval_file.write_text(f"""# Approval Required: Facebook Post
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: PENDING

## Post Content
{args['message']}

## To Approve
Move this file to `Approved/` — post will be published automatically.

## To Reject
Move this file to `Rejected/`.
""", encoding='utf-8')
    audit_log('facebook_post', approval_status='pending_human', target=f"Page:{FB_PAGE_ID}")
    return [types.TextContent(type="text", text=
        f"Facebook post queued for approval: `Pending_Approval/{approval_file.name}`")]


async def _post_to_instagram(args: dict) -> list[types.TextContent]:
    err = _missing_config()
    if err:
        return [types.TextContent(type="text", text=err)]
    if not IG_ACCOUNT_ID:
        return [types.TextContent(type="text", text="IG_ACCOUNT_ID not set in .env")]

    if DRY_RUN:
        audit_log('instagram_post', result='dry_run', parameters=args)
        return [types.TextContent(type="text", text=
            f"[DRY RUN] Would post to Instagram @{IG_ACCOUNT_ID}:\n"
            f"Caption: {args['caption']}\nImage: {args.get('image_url', 'N/A')}\n\n"
            "Set DRY_RUN=false in .env to post for real.")]

    # Two-step Instagram publish: create container → publish
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    approval_file = VAULT_PATH / 'Pending_Approval' / f'IG_POST_{ts}.md'
    approval_file.write_text(f"""# Approval Required: Instagram Post
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: PENDING

## Caption
{args['caption']}

## Image URL
{args.get('image_url', 'N/A')}

## To Approve
Move this file to `Approved/`.
""", encoding='utf-8')
    audit_log('instagram_post', approval_status='pending_human')
    return [types.TextContent(type="text", text=
        f"Instagram post queued for approval: `Pending_Approval/{approval_file.name}`")]


async def _get_facebook_summary(args: dict) -> list[types.TextContent]:
    days = args.get('period_days', 7)
    err = _missing_config()
    if err:
        return [types.TextContent(type="text", text=err)]

    # Save summary to vault Social_Media/ for weekly audit
    social_dir = VAULT_PATH / 'Social_Media'
    social_dir.mkdir(exist_ok=True)

    try:
        # Get page posts
        since = int((datetime.now() - timedelta(days=days)).timestamp())
        data = _graph_get(f"{FB_PAGE_ID}/posts", {
            'fields': 'message,created_time,likes.summary(true),comments.summary(true)',
            'since': since,
            'limit': 20,
        })
        posts = data.get('data', [])

        total_likes = sum(p.get('likes', {}).get('summary', {}).get('total_count', 0) for p in posts)
        total_comments = sum(p.get('comments', {}).get('summary', {}).get('total_count', 0) for p in posts)

        summary = (
            f"**Facebook Page Summary — Last {days} days**\n\n"
            f"| Metric | Count |\n|--------|-------|\n"
            f"| Posts | {len(posts)} |\n"
            f"| Total Likes | {total_likes} |\n"
            f"| Total Comments | {total_comments} |\n"
            f"| Avg Engagement | {(total_likes + total_comments) / max(len(posts), 1):.1f} |\n\n"
            f"**Recent Posts:**\n"
        )
        for p in posts[:5]:
            msg = (p.get('message', '')[:80] + '...') if len(p.get('message', '')) > 80 else p.get('message', '')
            likes = p.get('likes', {}).get('summary', {}).get('total_count', 0)
            summary += f"- {p.get('created_time', '')[:10]}: {msg} ({likes} likes)\n"

        # Write to vault
        report_file = social_dir / f"facebook_summary_{datetime.now().strftime('%Y-%m-%d')}.md"
        report_file.write_text(f"# Facebook Summary\nGenerated: {datetime.now().isoformat()}\n\n{summary}",
                                encoding='utf-8')
        audit_log('facebook_summary', result='success', parameters={'days': days, 'posts': len(posts)})
        return [types.TextContent(type="text", text=summary)]
    except Exception as e:
        audit_log('facebook_summary', result='error', error=str(e))
        return [types.TextContent(type="text", text=f"Facebook API error: {e}")]


async def _get_instagram_summary(args: dict) -> list[types.TextContent]:
    days = args.get('period_days', 7)
    err = _missing_config()
    if err:
        return [types.TextContent(type="text", text=err)]
    if not IG_ACCOUNT_ID:
        return [types.TextContent(type="text", text="IG_ACCOUNT_ID not set in .env")]

    try:
        data = _graph_get(f"{IG_ACCOUNT_ID}", {
            'fields': 'followers_count,media_count,biography',
        })
        media = _graph_get(f"{IG_ACCOUNT_ID}/media", {
            'fields': 'timestamp,like_count,comments_count,caption',
            'limit': 10,
        })
        posts = media.get('data', [])
        total_likes = sum(p.get('like_count', 0) for p in posts)

        summary = (
            f"**Instagram Account Summary — Last {days} days**\n\n"
            f"| Metric | Value |\n|--------|-------|\n"
            f"| Followers | {data.get('followers_count', 'N/A')} |\n"
            f"| Total Posts | {data.get('media_count', 'N/A')} |\n"
            f"| Recent Posts | {len(posts)} |\n"
            f"| Recent Likes | {total_likes} |\n\n"
            f"**Recent Posts:**\n"
        )
        for p in posts[:5]:
            cap = (p.get('caption', '')[:60] + '...') if len(p.get('caption', '')) > 60 else p.get('caption', '')
            summary += f"- {p.get('timestamp', '')[:10]}: {cap} ({p.get('like_count', 0)} likes)\n"

        audit_log('instagram_summary', result='success')
        return [types.TextContent(type="text", text=summary)]
    except Exception as e:
        audit_log('instagram_summary', result='error', error=str(e))
        return [types.TextContent(type="text", text=f"Instagram API error: {e}")]


async def _save_social_draft(args: dict) -> list[types.TextContent]:
    """Save draft to LinkedIn_Queue (used for all social)."""
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    platform = args.get('platform', 'facebook')
    queue_dir = VAULT_PATH / 'LinkedIn_Queue'
    queue_dir.mkdir(exist_ok=True)
    draft_file = queue_dir / f"{platform.upper()}_DRAFT_{ts}.md"
    draft_file.write_text(f"""# Social Draft: {platform.upper()}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Platform: {platform}
Status: PENDING_APPROVAL

## Content
{args['content']}

{f"## Image URL{chr(10)}{args['image_url']}" if args.get('image_url') else ''}

## To Post
Move to `LinkedIn_Approved/` (or approve via Gold orchestrator).
""", encoding='utf-8')
    audit_log(f'{platform}_draft_saved', approval_status='pending_human')
    return [types.TextContent(type="text", text=
        f"Draft saved: `LinkedIn_Queue/{draft_file.name}`")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == '__main__':
    asyncio.run(main())
