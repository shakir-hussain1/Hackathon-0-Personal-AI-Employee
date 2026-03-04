"""
Vault Sync - Platinum Tier
Git-based bidirectional sync between Cloud and Local agents.

Security rule: Only markdown/state files sync. Secrets (.env, tokens,
WhatsApp sessions, credentials.json) are NEVER committed or synced.

Usage:
    sync = VaultSync(vault_path, git_remote)
    sync.push("cloud: processed 3 emails")   # Cloud pushes
    sync.pull()                               # Local pulls latest
"""

import subprocess
import logging
import os
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("vault_sync")

# Files/patterns that must NEVER be synced
GITIGNORE_RULES = [
    ".env",
    "*.env",
    "*.json",        # credentials.json, tokens
    "*.session",     # WhatsApp sessions
    "*.pid",
    "__pycache__/",
    "*.pyc",
    "venv/",
    ".gmail_token.json",
    "credentials.json",
]


class VaultSync:
    def __init__(self, vault_path: str, remote: str = None):
        self.vault = Path(vault_path)
        self.remote = remote or os.getenv("VAULT_GIT_REMOTE", "")
        self._ensure_gitignore()

    def _ensure_gitignore(self):
        """Make sure .gitignore exists with security rules."""
        gi = self.vault / ".gitignore"
        existing = gi.read_text(encoding="utf-8") if gi.exists() else ""
        missing = [r for r in GITIGNORE_RULES if r not in existing]
        if missing:
            with open(gi, "a", encoding="utf-8") as f:
                if existing and not existing.endswith("\n"):
                    f.write("\n")
                f.write("# Platinum Tier - secrets never sync\n")
                for rule in missing:
                    f.write(f"{rule}\n")
            logger.info(".gitignore updated with security rules")

    def _git(self, *args, check=True):
        """Run a git command in vault directory."""
        cmd = ["git", "-C", str(self.vault)] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if check and result.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return result

    def is_git_repo(self) -> bool:
        result = self._git("rev-parse", "--git-dir", check=False)
        return result.returncode == 0

    def init(self):
        """Initialize git repo in vault if not already done."""
        if not self.is_git_repo():
            self._git("init")
            logger.info("Initialized git repo in vault")
        if self.remote:
            # Add remote if not present
            remotes = self._git("remote", check=False).stdout
            if "origin" not in remotes:
                self._git("remote", "add", "origin", self.remote)
                logger.info(f"Git remote set: {self.remote}")

    def push(self, message: str = None) -> bool:
        """Stage all markdown/state changes and push to remote."""
        try:
            # Stage only safe file types (never secrets)
            self._git("add", "*.md", check=False)
            self._git("add", "Logs/*.log", check=False)
            self._git("add", "Updates/", check=False)
            self._git("add", "Signals/", check=False)

            msg = message or f"vault sync {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            result = self._git("commit", "-m", msg, check=False)

            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                logger.debug("Nothing to push — vault is clean")
                return True

            if self.remote:
                self._git("push", "origin", "main", "--force-with-lease", check=False)
                logger.info(f"Vault pushed: {msg}")
            return True
        except Exception as e:
            logger.error(f"Push failed: {e}")
            return False

    def pull(self) -> bool:
        """Pull latest changes from remote."""
        try:
            if not self.remote:
                logger.debug("No remote configured — skipping pull")
                return True
            self._git("pull", "origin", "main", "--rebase")
            logger.info("Vault pulled from remote")
            return True
        except Exception as e:
            logger.error(f"Pull failed: {e}")
            return False

    def sync(self, message: str = None) -> bool:
        """Pull then push (full sync cycle)."""
        pulled = self.pull()
        pushed = self.push(message)
        return pulled and pushed
