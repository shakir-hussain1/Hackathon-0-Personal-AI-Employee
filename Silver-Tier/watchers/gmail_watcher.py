"""
Gmail Watcher - Silver Tier
Monitors Gmail inbox for new emails and creates tasks in Needs_Action/
"""

import os
import json
import base64
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

_SILVER_ROOT = Path(__file__).parent.parent
load_dotenv(_SILVER_ROOT / '.env')

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_SILVER_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
TOKEN_PATH = _SILVER_ROOT / '.gmail_token.json'
CREDENTIALS_PATH = _SILVER_ROOT / 'credentials.json'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('gmail_watcher')


def get_gmail_service():
    """Authenticate and return Gmail API service."""
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                logger.error("credentials.json not found. Download from Google Cloud Console.")
                raise FileNotFoundError("credentials.json required for Gmail OAuth")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=8080)

        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
        logger.info("Gmail token saved.")

    return build('gmail', 'v1', credentials=creds)


def get_unread_emails(service, max_results=10):
    """Fetch unread emails from inbox."""
    try:
        results = service.users().messages().list(
            userId='me',
            q='is:unread in:inbox',
            maxResults=max_results
        ).execute()
        return results.get('messages', [])
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        return []


def get_email_details(service, msg_id):
    """Get full email details."""
    try:
        msg = service.users().messages().get(
            userId='me', id=msg_id, format='full'
        ).execute()

        headers = {h['name']: h['value'] for h in msg['payload']['headers']}
        subject = headers.get('Subject', '(no subject)')
        sender = headers.get('From', 'unknown')
        date = headers.get('Date', '')

        body = ''
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
                        break
        elif 'body' in msg['payload']:
            data = msg['payload']['body'].get('data', '')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')

        attachments = []
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part.get('filename'):
                    attachments.append(part['filename'])

        return {
            'id': msg_id,
            'subject': subject,
            'sender': sender,
            'date': date,
            'body': body[:500],
            'attachments': attachments,
            'snippet': msg.get('snippet', '')
        }
    except Exception as e:
        logger.error(f"Error getting email {msg_id}: {e}")
        return None


def determine_priority(email):
    """Determine email priority based on content."""
    subject_lower = email['subject'].lower()
    body_lower = email['body'].lower()

    urgent_keywords = ['urgent', 'asap', 'immediately', 'critical', 'emergency']
    high_keywords = ['invoice', 'payment', 'contract', 'deadline', 'important']

    for kw in urgent_keywords:
        if kw in subject_lower or kw in body_lower:
            return 'CRITICAL'

    for kw in high_keywords:
        if kw in subject_lower or kw in body_lower:
            return 'HIGH'

    if email['attachments']:
        return 'HIGH'

    return 'MEDIUM'


def create_task_file(email):
    """Create a task markdown file in Needs_Action/."""
    needs_action = VAULT_PATH / 'Needs_Action'
    needs_action.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_subject = ''.join(c for c in email['subject'][:30] if c.isalnum() or c in ' -_').strip()
    filename = f"EMAIL_{safe_subject}_{timestamp}.md"
    filepath = needs_action / filename

    priority = determine_priority(email)
    attachments_list = chr(10).join(f'- {a}' for a in email['attachments']) if email['attachments'] else 'None'

    subj = email['subject']
    sndr = email['sender']
    dt   = email['date']
    eid  = email['id']
    snip = email['snippet']
    bod  = email['body']
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    content = (
        f"# Email Task: {subj}\n"
        f"Created: {now_str}\n"
        f"Priority: {priority}\n"
        "Status: PENDING\n"
        "Source: Gmail\n"
        "\n"
        "## Email Details\n"
        f"**From:** {sndr}\n"
        f"**Subject:** {subj}\n"
        f"**Date:** {dt}\n"
        f"**Gmail ID:** {eid}\n"
        "\n"
        "## Preview\n"
        f"{snip}\n"
        "\n"
        "## Body (First 500 chars)\n"
        f"{bod}\n"
        "\n"
        "## Attachments\n"
        f"{attachments_list}\n"
        "\n"
        "## Suggested Actions\n"
        "- [ ] Review email content\n"
        "- [ ] Draft reply if needed (use draft_reply skill)\n"
        "- [ ] Extract any action items\n"
        "- [ ] File in appropriate category\n"
        "\n"
        "## Notes\n"
        "_Add your notes here_\n"
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    logger.info(f"Task created: {filename} (Priority: {priority})")
    return filename


def mark_as_read(service, msg_id):
    """Mark email as read in Gmail."""
    try:
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
    except Exception as e:
        logger.error(f"Error marking email as read: {e}")


def log_activity(message):
    """Write to daily log."""
    log_dir = VAULT_PATH / 'Logs'
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = log_dir / f"{today}.log"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] [GMAIL_WATCHER] {message}\n")


def check_inbox():
    """Main check: scan Gmail and create tasks."""
    logger.info("Checking Gmail inbox...")

    try:
        service = get_gmail_service()
        emails = get_unread_emails(service)

        if not emails:
            logger.info("No new emails.")
            return 0

        created = 0
        for msg in emails:
            email = get_email_details(service, msg['id'])
            if email:
                filename = create_task_file(email)
                mark_as_read(service, msg['id'])
                subj = email['subject']
                log_activity(f"Task created from email: {subj} -> {filename}")
                created += 1

        logger.info(f"Processed {created} emails.")
        return created

    except Exception as e:
        logger.error(f"Gmail check failed: {e}")
        log_activity(f"ERROR: Gmail check failed: {e}")
        return 0


def run(interval_minutes=15):
    """Run watcher on a schedule."""
    import time
    logger.info(f"Starting Gmail Watcher (interval: {interval_minutes} min)")
    log_activity("Gmail Watcher started")

    while True:
        check_inbox()
        logger.info(f"Next check in {interval_minutes} minutes...")
        time.sleep(interval_minutes * 60)


if __name__ == '__main__':
    interval = int(os.getenv('CHECK_INTERVAL_MINUTES', 15))
    run(interval)
