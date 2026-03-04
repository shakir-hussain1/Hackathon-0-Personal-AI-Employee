"""
Gold-Tier Twitter/X MCP Server
Posts tweets and generates engagement summaries using Twitter API v2.

Setup:
  1. Create Twitter Developer App: https://developer.twitter.com/
  2. Generate Bearer Token, API Key/Secret, Access Token/Secret
  3. Set TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_API_SECRET,
     TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET in .env
  4. pip install tweepy

Docs: https://docs.tweepy.org/en/stable/
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

_GOLD_ROOT = Path(__file__).parent.parent.parent
load_dotenv(_GOLD_ROOT / '.env')
sys.path.insert(0, str(_GOLD_ROOT))
from orchestrator.audit_logger import audit_log
from orchestrator.error_handler import with_retry, twitter_breaker, TransientError

TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', '')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET', '')
DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'
VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_GOLD_ROOT.parent / 'Common' / 'AI_Employee_Vault')))

server = Server("twitter-x")


def _get_client():
    """Return authenticated Tweepy client (API v2)."""
    try:
        import tweepy
        return tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET,
        )
    except ImportError:
        raise RuntimeError("tweepy not installed — run: pip install tweepy")


def _missing_config() -> str | None:
    missing = [k for k in ['TWITTER_API_KEY', 'TWITTER_ACCESS_TOKEN', 'TWITTER_BEARER_TOKEN']
               if not os.getenv(k)]
    if missing:
        return f"Missing in .env: {', '.join(missing)}. See Gold-Tier/config/social_media_setup.md"
    return None


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="post_tweet",
            description=(
                "Post a tweet to Twitter/X. Max 280 characters. "
                "Creates approval request first (HITL). "
                "Set DRY_RUN=false in .env to send real tweets."
            ),
            inputSchema={
                "type": "object",
                "required": ["text"],
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Tweet text (max 280 chars)",
                        "maxLength": 280,
                    },
                    "reply_to_tweet_id": {
                        "type": "string",
                        "description": "Tweet ID to reply to (optional)",
                    },
                },
            },
        ),
        types.Tool(
            name="get_twitter_summary",
            description="Get Twitter/X account summary: follower count, recent tweet stats.",
            inputSchema={
                "type": "object",
                "properties": {
                    "period_days": {
                        "type": "integer",
                        "description": "Days to summarize (default: 7)",
                    },
                    "max_tweets": {
                        "type": "integer",
                        "description": "Max tweets to include (default: 10)",
                    },
                },
            },
        ),
        types.Tool(
            name="search_twitter",
            description="Search recent tweets for a keyword or hashtag.",
            inputSchema={
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., '#AI' or 'from:username')",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Max results (10-100, default: 10)",
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    audit_log(f'twitter_{name}', actor='twitter-x', parameters=arguments)

    if name == "post_tweet":
        return await _post_tweet(arguments)
    elif name == "get_twitter_summary":
        return await _get_twitter_summary(arguments)
    elif name == "search_twitter":
        return await _search_twitter(arguments)
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def _post_tweet(args: dict) -> list[types.TextContent]:
    text = args.get('text', '')
    if len(text) > 280:
        return [types.TextContent(type="text", text=
            f"Tweet too long ({len(text)} chars). Max 280 chars.")]

    err = _missing_config()
    if err:
        return [types.TextContent(type="text", text=err)]

    if DRY_RUN:
        audit_log('tweet_post', result='dry_run', parameters=args)
        return [types.TextContent(type="text", text=
            f"[DRY RUN] Would tweet:\n\n{text}\n\n"
            "Set DRY_RUN=false in .env to post real tweets.")]

    # Create approval file (HITL for social posts)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    approval_file = VAULT_PATH / 'Pending_Approval' / f'TWEET_{ts}.md'
    approval_file.write_text(f"""# Approval Required: Tweet
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: PENDING
Characters: {len(text)}/280

## Tweet Text
{text}

## To Approve
Move this file to `Approved/`.

## To Reject
Move this file to `Rejected/`.
""", encoding='utf-8')
    audit_log('tweet_post', approval_status='pending_human', target='twitter/x')
    return [types.TextContent(type="text", text=
        f"Tweet queued for approval: `Pending_Approval/{approval_file.name}`")]


async def _get_twitter_summary(args: dict) -> list[types.TextContent]:
    days = args.get('period_days', 7)
    max_tweets = min(args.get('max_tweets', 10), 100)

    err = _missing_config()
    if err:
        return [types.TextContent(type="text", text=err)]

    try:
        import tweepy
        client = _get_client()

        # Get authenticated user info
        me = client.get_me(user_fields=['public_metrics'])
        if not me.data:
            return [types.TextContent(type="text", text="Could not fetch Twitter user info.")]

        user = me.data
        metrics = user.public_metrics or {}

        # Get recent tweets
        tweets_resp = client.get_users_tweets(
            user.id,
            max_results=max_tweets,
            tweet_fields=['public_metrics', 'created_at'],
        )
        tweets = tweets_resp.data or []

        total_likes = sum(t.public_metrics.get('like_count', 0) for t in tweets if t.public_metrics)
        total_rt = sum(t.public_metrics.get('retweet_count', 0) for t in tweets if t.public_metrics)
        total_replies = sum(t.public_metrics.get('reply_count', 0) for t in tweets if t.public_metrics)

        summary = (
            f"**Twitter/X Summary — Last {days} days**\n\n"
            f"**Account:** @{user.username}\n\n"
            f"| Metric | Value |\n|--------|-------|\n"
            f"| Followers | {metrics.get('followers_count', 'N/A'):,} |\n"
            f"| Following | {metrics.get('following_count', 'N/A'):,} |\n"
            f"| Total Tweets | {metrics.get('tweet_count', 'N/A'):,} |\n"
            f"| Recent Tweets | {len(tweets)} |\n"
            f"| Recent Likes | {total_likes:,} |\n"
            f"| Recent Retweets | {total_rt:,} |\n"
            f"| Recent Replies | {total_replies:,} |\n"
        )

        if tweets:
            best = max(tweets, key=lambda t: (t.public_metrics or {}).get('like_count', 0))
            best_text = best.text[:80] + '...' if len(best.text) > 80 else best.text
            summary += f"\n**Best Tweet:** {best_text} ({(best.public_metrics or {}).get('like_count', 0)} likes)\n"

        # Save to vault
        social_dir = VAULT_PATH / 'Social_Media'
        social_dir.mkdir(exist_ok=True)
        report_file = social_dir / f"twitter_summary_{datetime.now().strftime('%Y-%m-%d')}.md"
        report_file.write_text(f"# Twitter Summary\nGenerated: {datetime.now().isoformat()}\n\n{summary}",
                                encoding='utf-8')

        audit_log('twitter_summary', result='success', parameters={'tweets': len(tweets)})
        return [types.TextContent(type="text", text=summary)]

    except ImportError:
        return [types.TextContent(type="text", text=
            "tweepy not installed. Run: `pip install tweepy` in Gold-Tier/venv")]
    except Exception as e:
        audit_log('twitter_summary', result='error', error=str(e))
        return [types.TextContent(type="text", text=f"Twitter API error: {e}")]


async def _search_twitter(args: dict) -> list[types.TextContent]:
    query = args.get('query', '')
    max_results = min(args.get('max_results', 10), 100)

    err = _missing_config()
    if err:
        return [types.TextContent(type="text", text=err)]

    try:
        import tweepy
        client = _get_client()
        resp = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=['public_metrics', 'author_id', 'created_at'],
        )
        tweets = resp.data or []
        if not tweets:
            return [types.TextContent(type="text", text=f"No tweets found for: {query}")]

        lines = [f"**Twitter Search: `{query}`** ({len(tweets)} results)\n"]
        for t in tweets:
            metrics = t.public_metrics or {}
            text = (t.text[:80] + '...') if len(t.text) > 80 else t.text
            lines.append(
                f"- {text} | "
                f"Likes: {metrics.get('like_count', 0)} | "
                f"RT: {metrics.get('retweet_count', 0)}"
            )
        return [types.TextContent(type="text", text='\n'.join(lines))]

    except ImportError:
        return [types.TextContent(type="text", text="tweepy not installed.")]
    except Exception as e:
        audit_log('twitter_search', result='error', error=str(e))
        return [types.TextContent(type="text", text=f"Twitter search error: {e}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == '__main__':
    asyncio.run(main())
