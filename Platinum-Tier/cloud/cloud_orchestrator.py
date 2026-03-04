"""
Cloud Orchestrator - Platinum Tier
Runs 24/7 on a cloud VM (Oracle Free Tier / AWS / etc.)

Responsibilities (DRAFT-ONLY — never sends/posts directly):
  1. Monitor Gmail → create tasks in /Needs_Action/email/
  2. Claim tasks → move to /In_Progress/cloud/
  3. Draft email replies → write to /Plans/email/
  4. Write approval requests → /Pending_Approval/email/
  5. Draft social posts → /Needs_Action/social/ (for local to post after approval)
  6. Write status updates → /Updates/  (Local merges into Dashboard.md)
  7. Sync vault via Git after each cycle

Security: Cloud NEVER stores WhatsApp sessions, banking creds, or payment tokens.
          Secrets are in local .env only — never committed, never synced.

Env vars (cloud .env):
  VAULT_PATH           Path to synced vault clone
  VAULT_GIT_REMOTE     Git remote URL for vault sync
  GMAIL_CREDENTIALS    Path to credentials.json (local to VM, never synced)
  CHECK_INTERVAL_MIN   Poll interval in minutes (default: 15)
  DRY_RUN              true|false (default: true — safe mode)
  ENABLE_GMAIL         true|false
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# ── Path setup ──────────────────────────────────────────────────────────────
_CLOUD_ROOT = Path(__file__).parent
_PLATINUM_ROOT = _CLOUD_ROOT.parent
sys.path.insert(0, str(_PLATINUM_ROOT))

load_dotenv(_CLOUD_ROOT / ".env")
load_dotenv(_PLATINUM_ROOT / ".env")

from shared.vault_sync import VaultSync
from shared.claim_manager import ClaimManager

# ── Config ───────────────────────────────────────────────────────────────────
VAULT_PATH = Path(os.getenv("VAULT_PATH", str(_PLATINUM_ROOT.parent / "Common" / "AI_Employee_Vault")))
GIT_REMOTE = os.getenv("VAULT_GIT_REMOTE", "")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_MIN", "15")) * 60
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
ENABLE_GMAIL = os.getenv("ENABLE_GMAIL", "false").lower() == "true"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [CLOUD] %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(_CLOUD_ROOT / f"cloud_{datetime.now().strftime('%Y%m%d')}.log")),
    ],
)
logger = logging.getLogger("cloud_orchestrator")

# ── Shared utilities ─────────────────────────────────────────────────────────
syncer = VaultSync(str(VAULT_PATH), GIT_REMOTE)
claimer = ClaimManager(str(VAULT_PATH), agent_name="cloud")


# ── Gmail integration ────────────────────────────────────────────────────────
def check_gmail() -> int:
    """Pull unread emails, create task files in /Needs_Action/email/."""
    if not ENABLE_GMAIL:
        return 0
    try:
        # Import Silver gmail_watcher function
        silver_root = _PLATINUM_ROOT.parent / "Silver-Tier"
        sys.path.insert(0, str(silver_root))
        from watchers.gmail_watcher import get_gmail_service, get_unread_emails, get_email_details

        service = get_gmail_service()
        emails = get_unread_emails(service, max_results=10)

        domain_dir = VAULT_PATH / "Needs_Action" / "email"
        domain_dir.mkdir(parents=True, exist_ok=True)

        created = 0
        for msg in emails:
            email = get_email_details(service, msg["id"])
            if not email:
                continue

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe = "".join(c for c in email["subject"][:25] if c.isalnum() or c in " -_").strip()
            fname = f"EMAIL_{safe}_{ts}.md"
            fpath = domain_dir / fname

            if fpath.exists():
                continue

            content = (
                f"# Email Task: {email['subject']}\n"
                f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Agent: cloud\n"
                f"Domain: email\n"
                f"Priority: {_priority(email)}\n"
                "Status: PENDING\n\n"
                "## Email Details\n"
                f"**From:** {email['sender']}\n"
                f"**Subject:** {email['subject']}\n"
                f"**Date:** {email['date']}\n"
                f"**Gmail ID:** {email['id']}\n\n"
                "## Preview\n"
                f"{email['snippet']}\n\n"
                "## Body (first 500 chars)\n"
                f"{email['body']}\n\n"
                "## Suggested Actions\n"
                "- [ ] Draft reply (cloud)\n"
                "- [ ] Human approval (local)\n"
                "- [ ] Send via MCP (local)\n"
            )
            fpath.write_text(content, encoding="utf-8")
            created += 1
            logger.info(f"Task created: {fname}")

        return created
    except Exception as e:
        logger.error(f"Gmail check failed: {e}")
        return 0


def _priority(email: dict) -> str:
    s = email.get("subject", "").lower()
    b = email.get("body", "").lower()
    for kw in ["urgent", "asap", "critical", "emergency"]:
        if kw in s or kw in b:
            return "CRITICAL"
    for kw in ["invoice", "payment", "contract", "deadline"]:
        if kw in s or kw in b:
            return "HIGH"
    return "MEDIUM"


# ── Draft email replies ───────────────────────────────────────────────────────
def draft_replies() -> int:
    """Claim pending email tasks and write draft replies + approval requests."""
    pending = claimer.list_pending("email")
    drafted = 0

    for task_file in pending:
        claimed = claimer.claim(task_file)
        if not claimed:
            continue

        content = claimed.read_text(encoding="utf-8")
        subject = _extract_field(content, "Subject:")
        sender = _extract_field(content, "From:")

        # Write draft reply plan
        plans_dir = VAULT_PATH / "Plans" / "email"
        plans_dir.mkdir(parents=True, exist_ok=True)
        plan_file = plans_dir / f"PLAN_{claimed.stem}.md"

        plan_content = (
            f"# Draft Reply Plan\n"
            f"Task: {claimed.name}\n"
            f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Agent: cloud (draft-only)\n\n"
            f"## Original Email\n"
            f"**From:** {sender}\n"
            f"**Subject:** {subject}\n\n"
            f"## Draft Reply\n"
            f"Thank you for your email regarding '{subject}'.\n"
            f"I have reviewed your message and will respond shortly.\n\n"
            f"_[Cloud drafted this. Local agent must review and approve before sending.]_\n\n"
            f"## Status\n"
            f"- [x] Drafted by cloud\n"
            f"- [ ] Reviewed by human\n"
            f"- [ ] Sent by local agent\n"
        )
        plan_file.write_text(plan_content, encoding="utf-8")

        # Write approval request
        approval_dir = VAULT_PATH / "Pending_Approval" / "email"
        approval_dir.mkdir(parents=True, exist_ok=True)
        approval_file = approval_dir / f"APPROVAL_{claimed.stem}.md"

        approval_content = (
            f"# Approval Required: Email Reply\n"
            f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Action: send_email\n"
            f"Agent: cloud → awaiting local execution\n\n"
            f"## Reply Details\n"
            f"**To:** {sender}\n"
            f"**Subject:** Re: {subject}\n"
            f"**Draft:** See Plans/email/PLAN_{claimed.stem}.md\n\n"
            f"## To Approve\n"
            f"Move this file to `/Approved/` folder.\n\n"
            f"## To Reject\n"
            f"Move this file to `/Rejected/` folder.\n"
        )
        approval_file.write_text(approval_content, encoding="utf-8")

        logger.info(f"Draft + approval created for: {claimed.name}")
        drafted += 1

    return drafted


def _extract_field(content: str, field: str) -> str:
    for line in content.splitlines():
        if field in line:
            return line.split(field, 1)[-1].strip().strip("*")
    return "unknown"


# ── Write status update (cloud → local merge) ─────────────────────────────────
def write_update(message: str):
    """Cloud writes status to /Updates/ — Local merges into Dashboard.md."""
    updates_dir = VAULT_PATH / "Updates"
    updates_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    update_file = updates_dir / f"UPDATE_{ts}.md"
    update_file.write_text(
        f"# Cloud Update\n"
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Agent: cloud\n\n"
        f"{message}\n",
        encoding="utf-8",
    )


# ── Main loop ─────────────────────────────────────────────────────────────────
def run():
    logger.info("=" * 60)
    logger.info("Cloud Orchestrator starting (Platinum Tier)")
    logger.info(f"Vault: {VAULT_PATH}")
    logger.info(f"DRY_RUN: {DRY_RUN}")
    logger.info(f"Gmail: {'enabled' if ENABLE_GMAIL else 'disabled'}")
    logger.info("=" * 60)

    syncer.init()

    cycle = 0
    while True:
        cycle += 1
        logger.info(f"── Cycle {cycle} ──────────────────────────────────")

        # 1. Pull latest vault state from local
        syncer.pull()

        # 2. Check Gmail
        new_emails = check_gmail()

        # 3. Draft replies for pending tasks
        drafted = draft_replies()

        # 4. Write status update
        if new_emails or drafted:
            write_update(
                f"- Emails detected: {new_emails}\n"
                f"- Replies drafted: {drafted}\n"
                f"- Pending approval: check /Pending_Approval/email/"
            )

        # 5. Push vault changes
        syncer.push(f"cloud cycle {cycle}: {new_emails} emails, {drafted} drafts")

        logger.info(f"Cycle {cycle} complete. Sleeping {CHECK_INTERVAL // 60} min...")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()
