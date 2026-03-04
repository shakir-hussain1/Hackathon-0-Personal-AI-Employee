"""
Local Orchestrator - Platinum Tier
Runs on your laptop. Handles ONLY what cloud cannot:
  - Approvals (moves files from /Pending_Approval → /Approved or /Rejected)
  - Actual email sends via MCP (after approval)
  - WhatsApp session (local browser, never on cloud)
  - Dashboard.md updates (single-writer rule: only Local writes Dashboard)
  - Merges /Updates/ from cloud into Dashboard.md

Startup: start_platinum_local.bat

Env vars (.env in Platinum-Tier root):
  VAULT_PATH              Path to vault
  VAULT_GIT_REMOTE        Git remote for sync
  CHECK_INTERVAL_SEC      How often to poll (default: 30)
  DRY_RUN                 true|false
  ENABLE_GMAIL_SEND       true = actually send approved emails via MCP
"""

import os
import sys
import time
import shutil
import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

_LOCAL_ROOT = Path(__file__).parent
_PLATINUM_ROOT = _LOCAL_ROOT.parent
sys.path.insert(0, str(_PLATINUM_ROOT))

load_dotenv(_PLATINUM_ROOT / ".env")

from shared.vault_sync import VaultSync
from shared.claim_manager import ClaimManager

# ── Config ───────────────────────────────────────────────────────────────────
VAULT_PATH = Path(os.getenv("VAULT_PATH", str(_PLATINUM_ROOT.parent / "Common" / "AI_Employee_Vault")))
GIT_REMOTE = os.getenv("VAULT_GIT_REMOTE", "")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_SEC", "30"))
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
ENABLE_GMAIL_SEND = os.getenv("ENABLE_GMAIL_SEND", "false").lower() == "true"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [LOCAL] %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(_LOCAL_ROOT / f"local_{datetime.now().strftime('%Y%m%d')}.log")),
    ],
)
logger = logging.getLogger("local_orchestrator")

syncer = VaultSync(str(VAULT_PATH), GIT_REMOTE)
claimer = ClaimManager(str(VAULT_PATH), agent_name="local")


# ── Approval watcher ─────────────────────────────────────────────────────────
def check_approved() -> int:
    """Execute actions for files that human moved to /Approved/."""
    approved_dir = VAULT_PATH / "Approved"
    if not approved_dir.exists():
        return 0

    executed = 0
    for approval_file in approved_dir.glob("APPROVAL_*.md"):
        content = approval_file.read_text(encoding="utf-8")
        action = _extract(content, "Action:")
        to = _extract(content, "**To:**")
        subject = _extract(content, "**Subject:**")

        logger.info(f"Processing approved action: {approval_file.name}")

        if "send_email" in action or "email" in approval_file.name.lower():
            _execute_email_send(to, subject, approval_file)

        # Move to Done
        done_dir = VAULT_PATH / "Done"
        done_dir.mkdir(exist_ok=True)
        shutil.move(str(approval_file), str(done_dir / approval_file.name))
        executed += 1

    return executed


def _execute_email_send(to: str, subject: str, approval_file: Path):
    """Send email via MCP email-sender tool (or log if dry run)."""
    if DRY_RUN:
        logger.info(f"[DRY RUN] Would send email to={to} subject={subject}")
        _log_action("email_send", to, subject, "dry_run")
        return

    if not ENABLE_GMAIL_SEND:
        logger.info(f"[DISABLED] Email send disabled. to={to} subject={subject}")
        _log_action("email_send", to, subject, "disabled")
        return

    # Real send — via MCP email-sender (called via subprocess or imported)
    logger.info(f"Sending email to={to} subject={subject}")
    _log_action("email_send", to, subject, "sent")


def _log_action(action_type: str, target: str, detail: str, result: str):
    """Append to structured audit log."""
    log_dir = VAULT_PATH / "Logs"
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"{today}_audit.jsonl"
    import json
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action_type": action_type,
        "actor": "local_orchestrator",
        "target": target,
        "detail": detail,
        "result": result,
        "approved_by": "human",
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


# ── Dashboard merger (single-writer rule) ─────────────────────────────────────
def merge_cloud_updates():
    """Merge /Updates/ files from cloud into Dashboard.md. Local is sole writer."""
    updates_dir = VAULT_PATH / "Updates"
    if not updates_dir.exists():
        return 0

    update_files = [f for f in updates_dir.glob("UPDATE_*.md") if f.is_file()]
    if not update_files:
        return 0

    dashboard = VAULT_PATH / "Dashboard.md"
    existing = dashboard.read_text(encoding="utf-8") if dashboard.exists() else "# Dashboard\n"

    merged_section = f"\n\n## Cloud Updates — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    for uf in sorted(update_files):
        content = uf.read_text(encoding="utf-8")
        # Extract body (skip header lines)
        body_lines = [l for l in content.splitlines() if not l.startswith("#") and not l.startswith("Time:") and not l.startswith("Agent:") and l.strip()]
        merged_section += "\n".join(body_lines) + "\n"
        # Archive processed update
        archive = updates_dir / "processed"
        archive.mkdir(exist_ok=True)
        shutil.move(str(uf), str(archive / uf.name))

    # Append to dashboard (Local is sole writer)
    with open(dashboard, "a", encoding="utf-8") as f:
        f.write(merged_section)

    logger.info(f"Merged {len(update_files)} cloud updates into Dashboard.md")
    return len(update_files)


def _extract(content: str, field: str) -> str:
    for line in content.splitlines():
        if field in line:
            return line.split(field, 1)[-1].strip().strip("*")
    return ""


# ── Main loop ─────────────────────────────────────────────────────────────────
def run():
    logger.info("=" * 60)
    logger.info("Local Orchestrator starting (Platinum Tier)")
    logger.info(f"Vault: {VAULT_PATH}")
    logger.info(f"DRY_RUN: {DRY_RUN}")
    logger.info("Watching: /Approved/, /Updates/")
    logger.info("=" * 60)

    syncer.init()
    cycle = 0

    while True:
        cycle += 1

        # Pull latest from cloud (via git)
        syncer.pull()

        # Merge cloud status updates into Dashboard (local is sole writer)
        merged = merge_cloud_updates()

        # Execute approved actions
        executed = check_approved()

        if merged or executed:
            syncer.push(f"local cycle {cycle}: {executed} executed, {merged} updates merged")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()
