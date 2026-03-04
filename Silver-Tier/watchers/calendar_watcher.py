"""
Calendar Watcher - Silver Tier
Monitors Google Calendar for upcoming events and creates tasks.
"""

import os
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

_SILVER_ROOT = Path(__file__).parent.parent
load_dotenv(_SILVER_ROOT / '.env')

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_SILVER_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
TOKEN_PATH = _SILVER_ROOT / '.calendar_token.json'
CREDENTIALS_PATH = _SILVER_ROOT / 'credentials.json'
LOOKAHEAD_HOURS = int(os.getenv('CALENDAR_LOOKAHEAD_HOURS', 24))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('calendar_watcher')


def get_calendar_service():
    """Authenticate and return Calendar API service."""
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=8081)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(service, hours_ahead=24):
    """Fetch events in the next N hours."""
    now = datetime.now(timezone.utc)
    end = now + timedelta(hours=hours_ahead)

    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat(),
            timeMax=end.isoformat(),
            maxResults=20,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return []


def create_task_for_event(event):
    """Create a task file for a calendar event."""
    needs_action = VAULT_PATH / 'Needs_Action'
    needs_action.mkdir(exist_ok=True)

    start = event.get('start', {})
    start_time = start.get('dateTime', start.get('date', 'Unknown'))
    summary = event.get('summary', 'Untitled Event')
    location = event.get('location', 'Not specified')
    description = event.get('description', '')[:300]
    attendees = [a.get('email', '') for a in event.get('attendees', [])]

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_summary = ''.join(c for c in summary[:30] if c.isalnum() or c in ' -_').strip()
    filename = f"EVENT_{safe_summary}_{timestamp}.md"

    attendees_str = ', '.join(attendees) if attendees else 'None listed'
    desc_str = description or 'No description provided'
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    content = (
        f"# Calendar Event: {summary}\n"
        f"Created: {now_str}\n"
        "Priority: HIGH\n"
        "Status: PENDING\n"
        "Source: Google Calendar\n"
        "\n"
        "## Event Details\n"
        f"**Title:** {summary}\n"
        f"**Start:** {start_time}\n"
        f"**Location:** {location}\n"
        f"**Attendees:** {attendees_str}\n"
        "\n"
        "## Description\n"
        f"{desc_str}\n"
        "\n"
        "## Prep Tasks\n"
        "- [ ] Review event agenda\n"
        "- [ ] Prepare materials if needed\n"
        "- [ ] Send confirmation if required\n"
        "- [ ] Set reminder\n"
        "\n"
        "## Notes\n"
        "_Add prep notes here_\n"
    )

    filepath = needs_action / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    logger.info(f"Event task created: {filename}")
    return filename


def log_activity(message):
    log_dir = VAULT_PATH / 'Logs'
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = log_dir / f"{today}.log"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] [CALENDAR_WATCHER] {message}\n")


def check_calendar():
    """Check for upcoming events."""
    logger.info("Checking Google Calendar...")
    try:
        service = get_calendar_service()
        events = get_upcoming_events(service, LOOKAHEAD_HOURS)

        if not events:
            logger.info("No upcoming events.")
            return 0

        created = 0
        for event in events:
            filename = create_task_for_event(event)
            ev_summary = event.get('summary', 'Untitled')
            log_activity(f"Event task: {ev_summary} -> {filename}")
            created += 1

        logger.info(f"Created {created} event tasks.")
        return created

    except Exception as e:
        logger.error(f"Calendar check failed: {e}")
        log_activity(f"ERROR: Calendar check failed: {e}")
        return 0


def run(interval_minutes=60):
    import time
    logger.info(f"Starting Calendar Watcher (interval: {interval_minutes} min)")
    log_activity("Calendar Watcher started")

    while True:
        check_calendar()
        time.sleep(interval_minutes * 60)


if __name__ == '__main__':
    run()
