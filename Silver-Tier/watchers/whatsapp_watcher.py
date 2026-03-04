"""
Silver-Tier WhatsApp Watcher
Monitors WhatsApp Web for unread messages containing business-critical keywords.
Uses Playwright persistent browser context so you only scan QR code once.

Setup:
  1. pip install playwright && playwright install chromium
  2. First run: set WHATSAPP_HEADLESS=false in .env, scan QR code in browser
  3. After scan: session saved to WHATSAPP_SESSION_PATH — subsequent runs are headless
"""

import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

_SILVER_ROOT = Path(__file__).parent.parent
load_dotenv(_SILVER_ROOT / '.env')

# Must import BaseWatcher after path setup
sys.path.insert(0, str(_SILVER_ROOT))
from watchers.base_watcher import BaseWatcher

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_SILVER_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
SESSION_PATH = Path(os.getenv('WHATSAPP_SESSION_PATH', str(_SILVER_ROOT / '.whatsapp_session')))
HEADLESS = os.getenv('WHATSAPP_HEADLESS', 'true').lower() == 'true'
CHECK_INTERVAL = int(os.getenv('WHATSAPP_INTERVAL_SECONDS', '60'))

# Keywords that trigger a Needs_Action task
URGENT_KEYWORDS = [
    'urgent', 'asap', 'emergency', 'critical',
    'invoice', 'payment', 'overdue', 'deadline',
    'help', 'problem', 'issue', 'fix', 'broken',
    'meeting', 'call me', 'call us',
]


class WhatsAppWatcher(BaseWatcher):
    """
    Watches WhatsApp Web for unread messages matching urgent keywords.
    Uses Playwright persistent context so session survives restarts.
    """

    def __init__(self, vault_path: str, session_path: str, headless: bool = True):
        super().__init__(vault_path, check_interval=CHECK_INTERVAL)
        self.session_path = Path(session_path)
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.headless = headless
        self.keywords = URGENT_KEYWORDS

    def check_for_updates(self) -> list:
        """
        Open WhatsApp Web in a persistent browser context, scrape unread messages
        with matching keywords, and return them as a list of dicts.
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.log_activity(
                "playwright not installed — run: pip install playwright && playwright install chromium",
                level="ERROR"
            )
            return []

        messages = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=self.headless,
                    args=['--no-sandbox'],
                )
                page = browser.pages[0] if browser.pages else browser.new_page()

                self.log_activity("Navigating to WhatsApp Web...")
                page.goto('https://web.whatsapp.com')

                # Wait for chat list — if not logged in this will timeout
                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30_000)
                except Exception:
                    self.log_activity(
                        "WhatsApp not logged in — set WHATSAPP_HEADLESS=false and scan QR code",
                        level="WARNING"
                    )
                    browser.close()
                    return []

                # Find chats with unread badge
                unread_chats = page.query_selector_all('[data-testid="icon-unread-count"]')
                self.log_activity(f"Found {len(unread_chats)} unread chat(s)")

                for badge in unread_chats:
                    try:
                        # Click the chat to open it
                        chat_item = badge.evaluate_handle(
                            'el => el.closest("[data-testid=\'list-item-\']") || el.closest("li")'
                        )
                        chat_text = page.evaluate('el => el ? el.innerText : ""', chat_item)
                        chat_text_lower = chat_text.lower()

                        matched_keywords = [kw for kw in self.keywords if kw in chat_text_lower]
                        if matched_keywords:
                            # Get sender name (first line of innerText usually)
                            lines = [l.strip() for l in chat_text.split('\n') if l.strip()]
                            sender = lines[0] if lines else 'Unknown'
                            preview = ' | '.join(lines[1:3]) if len(lines) > 1 else chat_text[:200]

                            messages.append({
                                'sender': sender,
                                'preview': preview,
                                'keywords': matched_keywords,
                                'raw_text': chat_text[:500],
                            })
                    except Exception as e:
                        self.log_activity(f"Error parsing chat item: {e}", level="WARNING")
                        continue

                browser.close()

        except Exception as e:
            self.log_activity(f"Playwright error: {e}", level="ERROR")

        return messages

    def create_action_file(self, item: dict) -> Path:
        """Create a Needs_Action task file for an urgent WhatsApp message."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sender_slug = item['sender'].replace(' ', '_').replace('/', '_')[:30]
        filename = f"WHATSAPP_{sender_slug}_{timestamp}.md"
        task_file = self.needs_action / filename

        keywords_str = ', '.join(item['keywords'])
        content = f"""# WhatsApp Task: {item['sender']}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Priority: HIGH
Status: PENDING
Source: WhatsApp Watcher

## Message Preview
**From:** {item['sender']}
**Keywords Detected:** {keywords_str}

```
{item['preview']}
```

## What To Do
1. Review the WhatsApp message from {item['sender']}
2. Determine if an action or reply is required
3. If reply needed: use `draft_reply` skill or respond directly on WhatsApp
4. Update status to COMPLETED when handled
5. Move this file to Done/

## Notes
_Add your response / action taken here_
"""
        task_file.write_text(content, encoding='utf-8')
        self.log_activity(f"Task created: {filename} (keywords: {keywords_str})")
        return task_file


def check_whatsapp(vault_path: str = None, session_path: str = None) -> int:
    """
    One-shot check — used by orchestrator.
    Returns number of new tasks created.
    """
    vp = vault_path or str(VAULT_PATH)
    sp = session_path or str(SESSION_PATH)
    watcher = WhatsAppWatcher(vault_path=vp, session_path=sp, headless=HEADLESS)
    items = watcher.check_for_updates()
    for item in items:
        watcher.create_action_file(item)
    return len(items)


if __name__ == '__main__':
    # Standalone mode — runs continuously
    watcher = WhatsAppWatcher(
        vault_path=str(VAULT_PATH),
        session_path=str(SESSION_PATH),
        headless=HEADLESS,
    )
    watcher.run()
