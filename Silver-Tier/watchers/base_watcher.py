"""
Silver-Tier Base Watcher
Abstract base class for all Silver-Tier watchers.
Provides common logging, path setup, and monitoring loop.
"""

import os
import time
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from dotenv import load_dotenv

_SILVER_ROOT = Path(__file__).parent.parent
load_dotenv(_SILVER_ROOT / '.env')


class BaseWatcher(ABC):
    """
    Abstract base class for all Silver-Tier watchers.
    Subclasses must implement check_for_updates() and create_action_file().
    """

    def __init__(self, vault_path, check_interval=30):
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.running = False

        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")

        self.needs_action = self.vault_path / "Needs_Action"
        self.done = self.vault_path / "Done"
        self.logs = self.vault_path / "Logs"
        self.plans = self.vault_path / "Plans"

        self._ensure_directories()

    def _ensure_directories(self):
        """Create required directories if they don't exist."""
        for directory in [self.needs_action, self.done, self.logs, self.plans]:
            directory.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items to process.
        Returns a list of items found (format depends on watcher type).
        """
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create a task .md file in Needs_Action/ for the given item.
        Returns the path to the created file.
        """
        pass

    def log_activity(self, message: str, level: str = "INFO"):
        """Append a log entry to today's log file and print to console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] [{self.__class__.__name__}] {message}\n"

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.logs / f"{today}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        print(log_entry.strip())

    def run(self):
        """Main monitoring loop — runs until KeyboardInterrupt."""
        self.running = True
        self.log_activity(f"Started with {self.check_interval}s check interval")

        print(f"\n{'='*60}")
        print(f"[SILVER] {self.__class__.__name__} Active")
        print(f"{'='*60}")
        print(f"Vault:    {self.vault_path}")
        print(f"Interval: {self.check_interval}s")
        print(f"{'='*60}\n")

        try:
            while self.running:
                try:
                    items = self.check_for_updates()
                    if items:
                        self.log_activity(f"Found {len(items)} new item(s)")
                        for item in items:
                            self.create_action_file(item)
                    time.sleep(self.check_interval)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    self.log_activity(f"Error in check loop: {e}", level="ERROR")
                    time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the watcher gracefully."""
        self.running = False
        self.log_activity("Stopped")
        print(f"\n[STOP] {self.__class__.__name__} stopped.\n")
