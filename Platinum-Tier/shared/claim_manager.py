"""
Claim Manager - Platinum Tier
Implements the claim-by-move rule to prevent double-work between Cloud and Local agents.

Rule: First agent to move a file from /Needs_Action/<domain>/ to
      /In_Progress/<agent>/ owns it. Other agents MUST ignore claimed tasks.

Usage:
    cm = ClaimManager(vault_path, agent_name="cloud")
    task = cm.claim("Needs_Action/email/EMAIL_task.md")
    if task:
        # Process it — you own it now
        cm.release(task, destination="Done")
"""

import shutil
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("claim_manager")


class ClaimManager:
    def __init__(self, vault_path: str, agent_name: str):
        self.vault = Path(vault_path)
        self.agent = agent_name  # "cloud" or "local"
        self.in_progress = self.vault / "In_Progress" / agent_name
        self.in_progress.mkdir(parents=True, exist_ok=True)

    def claim(self, task_file: Path) -> Path | None:
        """
        Atomically claim a task by moving it to In_Progress/<agent>/.
        Returns the new path if claim succeeded, None if already claimed.
        """
        task_file = Path(task_file)
        if not task_file.exists():
            return None  # Already claimed by another agent

        dest = self.in_progress / task_file.name
        try:
            shutil.move(str(task_file), str(dest))
            logger.info(f"[{self.agent}] Claimed: {task_file.name}")
            return dest
        except (FileNotFoundError, PermissionError):
            # Another agent claimed it first — race condition handled gracefully
            logger.debug(f"[{self.agent}] Lost race for: {task_file.name}")
            return None

    def release(self, claimed_file: Path, destination: str = "Done"):
        """
        Move completed task from In_Progress to Done (or Rejected).
        destination: "Done", "Rejected", or absolute path string
        """
        claimed_file = Path(claimed_file)
        if destination in ("Done", "Rejected"):
            dest_dir = self.vault / destination
        else:
            dest_dir = Path(destination)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / claimed_file.name
        try:
            shutil.move(str(claimed_file), str(dest))
            logger.info(f"[{self.agent}] Released to {destination}: {claimed_file.name}")
        except Exception as e:
            logger.error(f"Release failed: {e}")

    def list_pending(self, domain: str) -> list[Path]:
        """List unclaimed tasks for a domain (e.g. 'email', 'social')."""
        domain_dir = self.vault / "Needs_Action" / domain
        if not domain_dir.exists():
            return []
        return sorted(domain_dir.glob("*.md"))

    def list_mine(self) -> list[Path]:
        """List tasks currently claimed by this agent."""
        return sorted(self.in_progress.glob("*.md"))
