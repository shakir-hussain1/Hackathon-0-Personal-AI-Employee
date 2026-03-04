"""
Gold-Tier Orchestrator
Coordinates all Gold-Tier systems: Odoo, Social Media (FB/IG/Twitter),
Weekly CEO Briefing, Ralph Wiggum autonomous loop, and cross-tier integration.

Inherits all Silver-Tier functionality (runs Silver orchestrator as subprocess
or integrates Silver functions directly).

Startup: start_gold.bat
"""

import os
import sys
import time
import logging
import schedule
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

_GOLD_ROOT = Path(__file__).parent.parent
load_dotenv(_GOLD_ROOT / '.env')
sys.path.insert(0, str(_GOLD_ROOT))

from orchestrator.audit_logger import audit_log, get_audit_logger
from orchestrator.error_handler import safe_run

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(_GOLD_ROOT / f"orchestrator_{datetime.now().strftime('%Y%m%d')}.log")),
    ]
)
logger = logging.getLogger('gold_orchestrator')

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_GOLD_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'

# Feature flags
ENABLE_ODOO = os.getenv('ENABLE_ODOO', 'false').lower() == 'true'
ENABLE_FACEBOOK = os.getenv('ENABLE_FACEBOOK', 'false').lower() == 'true'
ENABLE_INSTAGRAM = os.getenv('ENABLE_INSTAGRAM', 'false').lower() == 'true'
ENABLE_TWITTER = os.getenv('ENABLE_TWITTER', 'false').lower() == 'true'
ENABLE_WEEKLY_AUDIT = os.getenv('ENABLE_WEEKLY_AUDIT', 'true').lower() == 'true'
ENABLE_RALPH_LOOP = os.getenv('ENABLE_RALPH_LOOP', 'true').lower() == 'true'
ENABLE_SILVER_INTEGRATION = os.getenv('ENABLE_SILVER_INTEGRATION', 'true').lower() == 'true'

# Intervals
SOCIAL_SUMMARY_INTERVAL = int(os.getenv('SOCIAL_SUMMARY_INTERVAL_HOURS', '6'))
AUDIT_LOG_PURGE_DAYS = int(os.getenv('AUDIT_LOG_PURGE_DAYS', '90'))
WEEKLY_AUDIT_DAY = os.getenv('WEEKLY_AUDIT_DAY', 'sunday')
WEEKLY_AUDIT_TIME = os.getenv('WEEKLY_AUDIT_TIME', '20:00')


def run_silver_checks():
    """Run Silver-Tier checks (Gmail, Calendar, LinkedIn, Reasoning)."""
    if not ENABLE_SILVER_INTEGRATION:
        return
    try:
        silver_root = _GOLD_ROOT.parent / 'Silver-Tier'
        silver_python = silver_root / 'venv' / 'Scripts' / 'python.exe'
        silver_orch = silver_root / 'orchestrator' / 'orchestrator.py'
        if not silver_python.exists() or not silver_orch.exists():
            logger.warning("Silver-Tier not found — skipping Silver integration")
            return
        # Import Silver orchestrator functions directly
        sys.path.insert(0, str(silver_root))
        import importlib, importlib.util
        spec = importlib.util.spec_from_file_location("silver_orch", str(silver_orch))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        safe_run(mod.run_gmail_check)
        safe_run(mod.run_calendar_check)
        safe_run(mod.run_linkedin_check)
        safe_run(mod.run_reasoning_loop)
        safe_run(mod.update_dashboard)
        logger.info("Silver-Tier checks complete")
    except Exception as e:
        logger.warning(f"Silver integration check failed: {e}")


def run_odoo_health_check():
    """Verify Odoo is reachable and log status."""
    if not ENABLE_ODOO:
        return
    try:
        import requests
        odoo_url = os.getenv('ODOO_URL', 'http://localhost:8069')
        resp = requests.get(f"{odoo_url}/web/health", timeout=5)
        if resp.ok:
            logger.info("Odoo: healthy")
            audit_log('odoo_health_check', result='success')
        else:
            logger.warning(f"Odoo health check returned {resp.status_code}")
            audit_log('odoo_health_check', result='warning',
                      error=f"HTTP {resp.status_code}")
    except Exception as e:
        logger.warning(f"Odoo not reachable: {e} — Start with docker-compose up")
        audit_log('odoo_health_check', result='error', error=str(e))


def run_social_summaries():
    """Pull Facebook, Instagram, Twitter summaries and save to vault."""
    if not any([ENABLE_FACEBOOK, ENABLE_INSTAGRAM, ENABLE_TWITTER]):
        return
    logger.info("Running social media summary collection...")

    if ENABLE_FACEBOOK or ENABLE_INSTAGRAM:
        safe_run(_run_meta_summary)
    if ENABLE_TWITTER:
        safe_run(_run_twitter_summary)


def _run_meta_summary():
    """Run Facebook + Instagram summary via direct import."""
    try:
        sys.path.insert(0, str(_GOLD_ROOT / 'mcp-servers' / 'facebook_instagram'))
        import asyncio
        import facebook_instagram_server as fb
        # Direct function call (bypass MCP transport)
        fb_result = asyncio.run(fb._get_facebook_summary({'period_days': 7}))
        ig_result = asyncio.run(fb._get_instagram_summary({'period_days': 7}))
        logger.info("Meta summary collected")
    except Exception as e:
        logger.warning(f"Meta summary failed: {e}")


def _run_twitter_summary():
    """Run Twitter summary via direct import."""
    try:
        sys.path.insert(0, str(_GOLD_ROOT / 'mcp-servers' / 'twitter_x'))
        import asyncio
        import twitter_x_server as tw
        asyncio.run(tw._get_twitter_summary({'period_days': 7}))
        logger.info("Twitter summary collected")
    except Exception as e:
        logger.warning(f"Twitter summary failed: {e}")


def run_weekly_audit():
    """Generate Monday Morning CEO Briefing."""
    if not ENABLE_WEEKLY_AUDIT:
        return
    try:
        from orchestrator.weekly_audit import run_weekly_audit as _audit
        briefing_path = _audit()
        logger.info(f"CEO Briefing generated: {briefing_path}")
        _notify_dashboard(f"CEO Briefing ready: `{briefing_path.name}`")
    except Exception as e:
        logger.error(f"Weekly audit failed: {e}")
        audit_log('weekly_audit', result='error', error=str(e))


def process_approved_actions():
    """
    Check Pending_Approval/ for files moved to Approved/.
    Execute the corresponding action and move to Done/.
    """
    approved_dir = VAULT_PATH / 'Approved'
    done_dir = VAULT_PATH / 'Done'
    if not approved_dir.exists():
        return

    for approved_file in approved_dir.glob('*.md'):
        try:
            content = approved_file.read_text(encoding='utf-8')
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')

            if 'FB_POST' in approved_file.name and (ENABLE_FACEBOOK or DRY_RUN):
                _execute_facebook_post(content, approved_file)
            elif 'IG_POST' in approved_file.name and (ENABLE_INSTAGRAM or DRY_RUN):
                _execute_instagram_post(content, approved_file)
            elif 'TWEET' in approved_file.name and (ENABLE_TWITTER or DRY_RUN):
                _execute_tweet(content, approved_file)
            elif 'INVOICE' in approved_file.name and (ENABLE_ODOO or DRY_RUN):
                _execute_create_invoice(content, approved_file)
            else:
                # Generic approval — log and move to Done
                logger.info(f"Generic approval: {approved_file.name}")
                audit_log('generic_approval', target=approved_file.name,
                          approval_status='approved', approved_by='human')

            # Move to Done/
            import shutil
            done_comms = done_dir / 'Communications'
            done_comms.mkdir(parents=True, exist_ok=True)
            shutil.move(str(approved_file), str(done_comms / approved_file.name))
            logger.info(f"Processed approved action: {approved_file.name}")

        except Exception as e:
            logger.error(f"Failed to process approved action {approved_file.name}: {e}")
            audit_log('approved_action_error', target=approved_file.name,
                      result='error', error=str(e))


def _execute_facebook_post(content: str, approval_file: Path):
    """Post to Facebook after human approval."""
    import re
    msg_match = re.search(r'## Post Content\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
    message = msg_match.group(1).strip() if msg_match else ''
    if not message:
        return
    if DRY_RUN:
        logger.info(f"[DRY RUN] Facebook post approved: {message[:50]}...")
        audit_log('facebook_post_executed', result='dry_run', approved_by='human')
        return
    try:
        import requests
        fb_page_id = os.getenv('FB_PAGE_ID')
        token = os.getenv('FB_PAGE_ACCESS_TOKEN')
        if fb_page_id and token:
            resp = requests.post(
                f"https://graph.facebook.com/v19.0/{fb_page_id}/feed",
                params={'access_token': token},
                json={'message': message},
                timeout=15,
            )
            if resp.ok:
                post_id = resp.json().get('id', 'unknown')
                audit_log('facebook_post_executed', target=post_id,
                          approval_status='approved', approved_by='human', result='success')
                logger.info(f"Facebook post published: {post_id}")
    except Exception as e:
        logger.error(f"Facebook post failed: {e}")
        audit_log('facebook_post_executed', result='error', error=str(e))


def _execute_tweet(content: str, approval_file: Path):
    """Tweet after human approval."""
    import re
    text_match = re.search(r'## Tweet Text\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
    text = text_match.group(1).strip() if text_match else ''
    if not text:
        return
    if DRY_RUN:
        logger.info(f"[DRY RUN] Tweet approved: {text[:50]}...")
        audit_log('tweet_executed', result='dry_run', approved_by='human')
        return
    try:
        import tweepy
        client = tweepy.Client(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_SECRET'),
        )
        resp = client.create_tweet(text=text)
        tweet_id = resp.data.get('id', 'unknown')
        audit_log('tweet_executed', target=str(tweet_id),
                  approval_status='approved', approved_by='human', result='success')
        logger.info(f"Tweet published: {tweet_id}")
    except ImportError:
        logger.error("tweepy not installed")
    except Exception as e:
        logger.error(f"Tweet failed: {e}")
        audit_log('tweet_executed', result='error', error=str(e))


def _execute_instagram_post(content: str, approval_file: Path):
    """Instagram post after human approval (queued — requires image)."""
    audit_log('instagram_post_executed', approval_status='approved', approved_by='human',
              result='queued' if DRY_RUN else 'pending_image')
    logger.info(f"Instagram post {'[DRY RUN] queued' if DRY_RUN else 'noted'}: {approval_file.name}")


def _execute_create_invoice(content: str, approval_file: Path):
    """Create Odoo invoice after human approval."""
    import re
    client_match = re.search(r'\*\*Client:\*\* (.+)', content)
    amount_match = re.search(r'\*\*Amount:\*\* (.+)', content)
    desc_match = re.search(r'\*\*Description:\*\* (.+)', content)
    client = client_match.group(1).strip() if client_match else 'Unknown'
    amount = float(amount_match.group(1).strip()) if amount_match else 0
    desc = desc_match.group(1).strip() if desc_match else 'Services'
    if DRY_RUN:
        logger.info(f"[DRY RUN] Invoice approved: {client} {amount}")
        audit_log('odoo_invoice_created', result='dry_run', approved_by='human')
        return
    try:
        sys.path.insert(0, str(_GOLD_ROOT / 'mcp-servers' / 'odoo_connector'))
        from odoo_connector_server import get_odoo
        odoo = get_odoo()
        # Find or create partner
        partners = odoo.search_read('res.partner', [['name', 'ilike', client]], ['id', 'name'], limit=1)
        partner_id = partners[0]['id'] if partners else odoo.create('res.partner', {'name': client})
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': partner_id,
            'invoice_line_ids': [(0, 0, {'name': desc, 'quantity': 1, 'price_unit': amount})],
        }
        inv_id = odoo.create('account.move', invoice_vals)
        audit_log('odoo_invoice_created', target=client,
                  approval_status='approved', approved_by='human',
                  parameters={'invoice_id': inv_id, 'amount': amount}, result='success')
        logger.info(f"Odoo invoice created: ID {inv_id} for {client} ({amount})")
    except Exception as e:
        logger.error(f"Odoo invoice creation failed: {e}")
        audit_log('odoo_invoice_created', result='error', error=str(e))


def _notify_dashboard(message: str):
    """Append a status line to Dashboard.md."""
    try:
        dashboard = VAULT_PATH / 'Dashboard.md'
        if not dashboard.exists():
            return
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(dashboard, 'a', encoding='utf-8') as f:
            f.write(f"\n> **[GOLD]** {ts} — {message}\n")
    except Exception:
        pass


def update_dashboard():
    """Update Dashboard.md with Gold-Tier status."""
    try:
        dashboard = VAULT_PATH / 'Dashboard.md'
        if not dashboard.exists():
            return
        import re
        content = dashboard.read_text(encoding='utf-8')
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status_line = f"**Gold Tier Last Run:** {ts}"
        if 'Gold Tier Last Run' in content:
            content = re.sub(r'\*\*Gold Tier Last Run:\*\*.*', status_line, content)
        else:
            content += f"\n\n## Gold Tier\n{status_line}\n"
        dashboard.write_text(content, encoding='utf-8')
    except Exception as e:
        logger.error(f"Dashboard update failed: {e}")


def purge_old_logs():
    """Remove JSON audit logs older than AUDIT_LOG_PURGE_DAYS."""
    try:
        purged = get_audit_logger().purge_old_logs()
        if purged:
            logger.info(f"Purged {purged} old audit log(s)")
    except Exception as e:
        logger.error(f"Log purge failed: {e}")


def setup_schedules():
    """Configure all Gold-Tier scheduled tasks."""
    # Social media summaries every N hours
    schedule.every(SOCIAL_SUMMARY_INTERVAL).hours.do(run_social_summaries)

    # Silver integration every 15 minutes
    schedule.every(15).minutes.do(run_silver_checks)

    # Odoo health check every 30 minutes
    schedule.every(30).minutes.do(run_odoo_health_check)

    # Approved action processing every 5 minutes
    schedule.every(5).minutes.do(process_approved_actions)

    # Dashboard update every 30 minutes
    schedule.every(30).minutes.do(update_dashboard)

    # Weekly CEO Briefing (Sunday 8pm by default)
    getattr(schedule.every(), WEEKLY_AUDIT_DAY).at(WEEKLY_AUDIT_TIME).do(run_weekly_audit)

    # Monthly log purge (daily at midnight)
    schedule.every().day.at("00:00").do(purge_old_logs)

    logger.info("Gold-Tier schedules configured:")
    logger.info(f"  Silver integration:  every 15 minutes ({'ENABLED' if ENABLE_SILVER_INTEGRATION else 'DISABLED'})")
    logger.info(f"  Social summaries:    every {SOCIAL_SUMMARY_INTERVAL} hours")
    logger.info(f"  Odoo health check:   every 30 minutes ({'ENABLED' if ENABLE_ODOO else 'DISABLED'})")
    logger.info(f"  Approved actions:    every 5 minutes")
    logger.info(f"  Weekly CEO briefing: {WEEKLY_AUDIT_DAY.capitalize()} at {WEEKLY_AUDIT_TIME} ({'ENABLED' if ENABLE_WEEKLY_AUDIT else 'DISABLED'})")
    logger.info(f"  DRY RUN MODE:        {'ON (no real external actions)' if DRY_RUN else 'OFF — LIVE MODE'}")


def run():
    """Main Gold-Tier orchestrator loop."""
    logger.info("=" * 60)
    logger.info("Gold Tier Orchestrator Starting")
    logger.info(f"Vault:       {VAULT_PATH.resolve()}")
    logger.info(f"DRY RUN:     {'YES — safe mode' if DRY_RUN else 'NO — LIVE'}")
    logger.info(f"Odoo:        {'ENABLED' if ENABLE_ODOO else 'DISABLED (set ENABLE_ODOO=true)'}")
    logger.info(f"Facebook:    {'ENABLED' if ENABLE_FACEBOOK else 'DISABLED'}")
    logger.info(f"Instagram:   {'ENABLED' if ENABLE_INSTAGRAM else 'DISABLED'}")
    logger.info(f"Twitter:     {'ENABLED' if ENABLE_TWITTER else 'DISABLED'}")
    logger.info(f"Ralph Loop:  {'ENABLED' if ENABLE_RALPH_LOOP else 'DISABLED'}")
    logger.info("=" * 60)

    audit_log('gold_orchestrator_start', actor='gold_orchestrator',
              parameters={'dry_run': DRY_RUN, 'vault': str(VAULT_PATH)})

    # Initial run
    safe_run(run_silver_checks)
    safe_run(run_odoo_health_check)
    safe_run(process_approved_actions)
    safe_run(update_dashboard)

    # Setup recurring schedules
    setup_schedules()

    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Gold Tier Orchestrator stopped.")
        audit_log('gold_orchestrator_stop', actor='gold_orchestrator')


if __name__ == '__main__':
    run()
