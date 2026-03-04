"""
LinkedIn Watcher - Silver Tier
Monitors Done/ for newly processed business content and queues LinkedIn post suggestions.
Also monitors LinkedIn_Queue/ for content ready to post (after human approval).
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

_SILVER_ROOT = Path(__file__).parent.parent
load_dotenv(_SILVER_ROOT / '.env')

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_SILVER_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
LINKEDIN_QUEUE_DIR = VAULT_PATH / 'LinkedIn_Queue'
LINKEDIN_APPROVED_DIR = VAULT_PATH / 'LinkedIn_Approved'
PROCESSED_LOG = _SILVER_ROOT / '.linkedin_processed.json'

logger = logging.getLogger('linkedin_watcher')


def _load_processed() -> set:
    if PROCESSED_LOG.exists():
        try:
            return set(json.loads(PROCESSED_LOG.read_text()))
        except Exception:
            return set()
    return set()


def _save_processed(processed: set):
    PROCESSED_LOG.write_text(json.dumps(list(processed)))


def _log(message: str):
    log_dir = VAULT_PATH / 'Logs'
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_dir / f"{today}.log", 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] [LINKEDIN_WATCHER] {message}\n")


def _is_business_content(filepath: Path) -> bool:
    """Return True if the file looks like valuable business content worth posting about."""
    business_keywords = [
        'invoice', 'contract', 'proposal', 'meeting', 'report',
        'milestone', 'launch', 'announcement', 'partnership', 'deal',
        'client', 'project', 'update', 'summary', 'completed',
    ]
    name_lower = filepath.stem.lower()
    return any(kw in name_lower for kw in business_keywords)


def _create_post_suggestion(source_file: Path) -> Path:
    """Create a LinkedIn post suggestion task in Needs_Action/."""
    LINKEDIN_QUEUE_DIR.mkdir(exist_ok=True)
    needs_action = VAULT_PATH / 'Needs_Action'
    needs_action.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_name = ''.join(c for c in source_file.stem[:30] if c.isalnum() or c in ' -_').strip()
    filename = f"LINKEDIN_POST_{safe_name}_{timestamp}.md"
    filepath = needs_action / filename
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Try to read source content for context
    try:
        source_content = source_file.read_text(encoding='utf-8')[:600]
    except Exception:
        source_content = f"(Could not read {source_file.name})"

    content = (
        f"# LinkedIn Post Task: {source_file.stem}\n"
        f"Created: {now_str}\n"
        "Priority: MEDIUM\n"
        "Status: PENDING\n"
        "Source: LinkedIn Watcher\n"
        "\n"
        "## What To Do\n"
        "Use the `linkedin_post` skill to draft a professional LinkedIn post based on this business content.\n"
        "Post it via the `linkedin-poster` MCP tool (requires approval first).\n"
        "\n"
        "## Source Document\n"
        f"**File:** {source_file}\n"
        "\n"
        "## Source Content Preview\n"
        f"```\n{source_content}\n```\n"
        "\n"
        "## Post Guidelines\n"
        "- Focus on business value and outcomes\n"
        "- Keep it under 1300 characters (LinkedIn limit)\n"
        "- Add 3-5 relevant hashtags\n"
        "- Professional tone, genuine insight\n"
        "- Avoid sharing confidential figures or client names without permission\n"
        "\n"
        "## Suggested Post Types\n"
        "- [ ] Project milestone / completion announcement\n"
        "- [ ] Business insight derived from the work\n"
        "- [ ] Thought leadership from findings\n"
        "- [ ] Team / client success story\n"
    )

    filepath.write_text(content, encoding='utf-8')
    logger.info(f"LinkedIn post suggestion created: {filename}")
    return filepath


def check_for_linkedin_content() -> int:
    """
    Scan Done/ for new business content files and create LinkedIn post suggestion tasks.
    Returns count of new suggestions created.
    """
    done_dir = VAULT_PATH / 'Done'
    if not done_dir.exists():
        return 0

    processed = _load_processed()
    created = 0

    for filepath in done_dir.rglob('*.md'):
        file_key = str(filepath)
        if file_key in processed:
            continue
        if _is_business_content(filepath):
            try:
                _create_post_suggestion(filepath)
                _log(f"Post suggestion queued for: {filepath.name}")
                created += 1
            except Exception as e:
                logger.error(f"Error creating post suggestion for {filepath.name}: {e}")
        processed.add(file_key)

    _save_processed(processed)

    if created:
        logger.info(f"LinkedIn watcher: {created} new post suggestion(s) queued")
    return created


def run(interval_minutes: int = 60):
    import time
    logger.info(f"Starting LinkedIn Watcher (interval: {interval_minutes} min)")
    _log("LinkedIn Watcher started")
    while True:
        check_for_linkedin_content()
        time.sleep(interval_minutes * 60)


if __name__ == '__main__':
    interval = int(os.getenv('LINKEDIN_CHECK_INTERVAL_MINUTES', 60))
    run(interval)
