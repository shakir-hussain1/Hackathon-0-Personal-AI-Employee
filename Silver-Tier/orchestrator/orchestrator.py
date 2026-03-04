"""
Silver Tier Orchestrator
Coordinates Gmail Watcher, Calendar Watcher, Email Sender,
Claude Reasoning Loop (Plan.md), and LinkedIn Watcher/Poster.
Runs on Windows Task Scheduler or manual start.
"""

import os
import sys
import time
import logging
import schedule
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

_SILVER_ROOT = Path(__file__).parent.parent
load_dotenv(_SILVER_ROOT / '.env')

# Add watchers to path
sys.path.insert(0, str(_SILVER_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(_SILVER_ROOT / f"orchestrator_{datetime.now().strftime('%Y%m%d')}.log"))
    ]
)
logger = logging.getLogger('silver_orchestrator')

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_SILVER_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
GMAIL_INTERVAL = int(os.getenv('CHECK_INTERVAL_MINUTES', 15))
CALENDAR_INTERVAL = int(os.getenv('CALENDAR_INTERVAL_MINUTES', 60))
LINKEDIN_INTERVAL = int(os.getenv('LINKEDIN_CHECK_INTERVAL_MINUTES', 60))
ENABLE_GMAIL = os.getenv('ENABLE_GMAIL', 'true').lower() == 'true'
ENABLE_CALENDAR = os.getenv('ENABLE_CALENDAR', 'true').lower() == 'true'
ENABLE_EMAIL_SENDER = os.getenv('ENABLE_EMAIL_SENDER', 'true').lower() == 'true'
ENABLE_LINKEDIN = os.getenv('ENABLE_LINKEDIN', 'true').lower() == 'true'
ENABLE_WHATSAPP = os.getenv('ENABLE_WHATSAPP', 'false').lower() == 'true'
WHATSAPP_INTERVAL = int(os.getenv('WHATSAPP_INTERVAL_SECONDS', '60'))
ENABLE_REASONING = bool(os.getenv('ANTHROPIC_API_KEY', ''))


def run_gmail_check():
    """Run Gmail watcher check."""
    if not ENABLE_GMAIL:
        return
    try:
        from watchers.gmail_watcher import check_inbox
        count = check_inbox()
        logger.info(f"Gmail check complete: {count} new emails processed")
    except ImportError:
        logger.warning("Gmail watcher not available (missing credentials?)")
    except Exception as e:
        logger.error(f"Gmail check failed: {e}")


def run_calendar_check():
    """Run Calendar watcher check."""
    if not ENABLE_CALENDAR:
        return
    try:
        from watchers.calendar_watcher import check_calendar
        count = check_calendar()
        logger.info(f"Calendar check complete: {count} events processed")
    except ImportError:
        logger.warning("Calendar watcher not available")
    except Exception as e:
        logger.error(f"Calendar check failed: {e}")


def run_email_sender():
    """Check for approved email drafts and send them (direct call, bypasses MCP transport)."""
    if not ENABLE_EMAIL_SENDER:
        return
    try:
        sys.path.insert(0, str(_SILVER_ROOT / 'mcp-servers' / 'email_sender'))
        import importlib, server as _email_server
        importlib.reload(_email_server)
        _email_server._check_and_send_approved()
    except Exception as e:
        logger.error(f"Email sender check failed: {e}")


def run_reasoning_loop():
    """Run Claude reasoning loop — create Plan.md for each unplanned task."""
    if not ENABLE_REASONING:
        return
    try:
        import importlib.util as _ilu
        _spec = _ilu.spec_from_file_location(
            "silver_reasoning_loop",
            str(_SILVER_ROOT / "orchestrator" / "reasoning_loop.py")
        )
        _mod = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        count = _mod.run_reasoning_loop()
        if count:
            logger.info(f"Reasoning loop: {count} Plan(s) created")
    except Exception as e:
        logger.error(f"Reasoning loop failed: {e}")


def run_linkedin_check():
    """Check Done/ for new business content and queue LinkedIn post suggestions."""
    if not ENABLE_LINKEDIN:
        return
    try:
        from watchers.linkedin_watcher import check_for_linkedin_content
        count = check_for_linkedin_content()
        if count:
            logger.info(f"LinkedIn watcher: {count} post suggestion(s) queued")
    except Exception as e:
        logger.error(f"LinkedIn check failed: {e}")


def run_whatsapp_check():
    """Check WhatsApp Web for urgent unread messages."""
    if not ENABLE_WHATSAPP:
        return
    try:
        from watchers.whatsapp_watcher import check_whatsapp
        count = check_whatsapp()
        if count:
            logger.info(f"WhatsApp watcher: {count} urgent message task(s) created")
    except ImportError:
        logger.warning("WhatsApp watcher unavailable (playwright not installed?)")
    except Exception as e:
        logger.error(f"WhatsApp check failed: {e}")


def update_dashboard():
    """Update Dashboard.md with Silver-tier status."""
    try:
        dashboard = VAULT_PATH / 'Dashboard.md'
        if not dashboard.exists():
            return

        content = dashboard.read_text(encoding='utf-8')
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        status_line = f"**Silver Tier Last Run:** {ts}"
        if 'Silver Tier Last Run' in content:
            import re
            content = re.sub(r'\*\*Silver Tier Last Run:\*\*.*', status_line, content)
        else:
            content += f"\n\n## Silver Tier\n{status_line}\n"

        dashboard.write_text(content, encoding='utf-8')
    except Exception as e:
        logger.error(f"Dashboard update failed: {e}")


def log_activity(message):
    log_dir = VAULT_PATH / 'Logs'
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = log_dir / f"{today}.log"
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] [SILVER_ORCHESTRATOR] {message}\n")


def setup_schedules():
    """Configure all scheduled tasks."""
    schedule.every(GMAIL_INTERVAL).minutes.do(run_gmail_check)
    schedule.every(CALENDAR_INTERVAL).minutes.do(run_calendar_check)
    schedule.every(5).minutes.do(run_email_sender)
    schedule.every(30).minutes.do(run_reasoning_loop)
    schedule.every(LINKEDIN_INTERVAL).minutes.do(run_linkedin_check)
    schedule.every(WHATSAPP_INTERVAL).seconds.do(run_whatsapp_check)
    schedule.every(30).minutes.do(update_dashboard)

    daily_report_time = os.getenv('DAILY_REPORT_TIME', '18:00')
    schedule.every().day.at(daily_report_time).do(
        lambda: log_activity("Daily report trigger")
    )

    logger.info("Schedules configured:")
    logger.info(f"  Gmail check:      every {GMAIL_INTERVAL} minutes")
    logger.info(f"  Calendar check:   every {CALENDAR_INTERVAL} minutes")
    logger.info(f"  Email sender:     every 5 minutes")
    logger.info(f"  Reasoning loop:   every 30 minutes ({'ENABLED' if ENABLE_REASONING else 'DISABLED — set ANTHROPIC_API_KEY'})")
    logger.info(f"  LinkedIn watcher: every {LINKEDIN_INTERVAL} minutes ({'ENABLED' if ENABLE_LINKEDIN else 'DISABLED'})")
    logger.info(f"  WhatsApp watcher: every {WHATSAPP_INTERVAL}s ({'ENABLED' if ENABLE_WHATSAPP else 'DISABLED (set ENABLE_WHATSAPP=true)'})")
    logger.info(f"  Dashboard update: every 30 minutes")
    logger.info(f"  Daily report:     at {daily_report_time}")


def run():
    """Main orchestrator loop."""
    logger.info("=" * 50)
    logger.info("Silver Tier Orchestrator Starting")
    logger.info(f"Vault: {VAULT_PATH.resolve()}")
    logger.info(f"Gmail:          {'ENABLED' if ENABLE_GMAIL else 'DISABLED'}")
    logger.info(f"Calendar:       {'ENABLED' if ENABLE_CALENDAR else 'DISABLED'}")
    logger.info(f"Email Sender:   {'ENABLED' if ENABLE_EMAIL_SENDER else 'DISABLED'}")
    logger.info(f"Reasoning Loop: {'ENABLED' if ENABLE_REASONING else 'DISABLED (set ANTHROPIC_API_KEY)'}")
    logger.info(f"LinkedIn:       {'ENABLED' if ENABLE_LINKEDIN else 'DISABLED'}")
    logger.info(f"WhatsApp:       {'ENABLED' if ENABLE_WHATSAPP else 'DISABLED (set ENABLE_WHATSAPP=true in .env)'}")
    logger.info("=" * 50)

    log_activity("Silver Orchestrator started")

    # Initial run
    run_gmail_check()
    run_calendar_check()
    run_email_sender()
    run_reasoning_loop()
    run_linkedin_check()
    run_whatsapp_check()
    update_dashboard()

    # Setup recurring schedules
    setup_schedules()

    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Orchestrator stopped by user.")
        log_activity("Silver Orchestrator stopped")


if __name__ == '__main__':
    run()
