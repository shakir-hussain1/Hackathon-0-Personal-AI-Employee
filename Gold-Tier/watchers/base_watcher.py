"""
Gold-Tier Base Watcher
Extends the BaseWatcher ABC pattern with JSON audit logging and error recovery.
"""

import os
import sys
import time
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from dotenv import load_dotenv

_GOLD_ROOT = Path(__file__).parent.parent
load_dotenv(_GOLD_ROOT / '.env')

sys.path.insert(0, str(_GOLD_ROOT))
from orchestrator.audit_logger import audit_log
from orchestrator.error_handler import safe_run


class BaseWatcher(ABC):
    """Abstract base for all Gold-Tier watchers — with audit logging and graceful degradation."""

    def __init__(self, vault_path, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.running = False

        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")

        self.needs_action = self.vault_path / "Needs_Action"
        self.done = self.vault_path / "Done"
        self.logs = self.vault_path / "Logs"
        self.plans = self.vault_path / "Plans"
        self.pending_approval = self.vault_path / "Pending_Approval"

        for d in [self.needs_action, self.done, self.logs, self.plans, self.pending_approval]:
            d.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process."""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md task file in Needs_Action/ and return path."""
        pass

    def log_activity(self, message: str, level: str = "INFO"):
        """Write to daily .log file and print to console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] [{self.__class__.__name__}] {message}\n"
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.logs / f"{today}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(entry.strip())

    def run(self):
        """Main monitoring loop — runs until KeyboardInterrupt."""
        self.running = True
        self.log_activity(f"Started — check interval {self.check_interval}s")
        audit_log('watcher_start', actor=self.__class__.__name__, target=str(self.vault_path))

        print(f"\n{'='*60}")
        print(f"[GOLD] {self.__class__.__name__} Active")
        print(f"Vault: {self.vault_path} | Interval: {self.check_interval}s")
        print(f"{'='*60}\n")

        try:
            while self.running:
                try:
                    items = self.check_for_updates()
                    if items:
                        self.log_activity(f"Found {len(items)} new item(s)")
                        for item in items:
                            safe_run(self.create_action_file, item, log_errors=True)
                    time.sleep(self.check_interval)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    self.log_activity(f"Check loop error: {e}", level="ERROR")
                    audit_log('watcher_error', actor=self.__class__.__name__,
                              result='error', error=str(e))
                    time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        self.log_activity("Stopped")
        audit_log('watcher_stop', actor=self.__class__.__name__)
