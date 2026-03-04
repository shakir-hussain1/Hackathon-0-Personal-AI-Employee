"""
Base Watcher Class
Template for all watcher implementations with standard logging and structure
"""

import os
import time
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path


class BaseWatcher(ABC):
    """
    Abstract base class for all watchers.
    Provides common functionality for logging, file operations, and monitoring loop.
    """

    def __init__(self, vault_path, check_interval=30):
        """
        Initialize the watcher.

        Args:
            vault_path: Path to the AI_Employee_Vault directory
            check_interval: Seconds between checks (default 30)
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.running = False

        # Validate vault path exists
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")

        # Setup key directories
        self.inbox = self.vault_path / "Inbox"
        self.needs_action = self.vault_path / "Needs_Action"
        self.done = self.vault_path / "Done"
        self.logs = self.vault_path / "Logs"

        # Ensure required directories exist
        self._ensure_directories()

    def _ensure_directories(self):
        """Create required directories if they don't exist"""
        for directory in [self.inbox, self.needs_action, self.done, self.logs]:
            directory.mkdir(exist_ok=True)

    @abstractmethod
    def check_for_updates(self):
        """
        Check for new items to process.
        Must be implemented by subclasses.

        Returns:
            List of items found (format depends on watcher type)
        """
        pass

    @abstractmethod
    def create_action_file(self, item):
        """
        Create a task file in Needs_Action folder.
        Must be implemented by subclasses.

        Args:
            item: The item to create a task for
        """
        pass

    def log_activity(self, message, level="INFO"):
        """
        Log activity to daily log file.

        Args:
            message: Log message
            level: Log level (INFO, WARNING, ERROR)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        # Create log file for today
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.logs / f"{today}.log"

        # Append to log file
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        # Also print to console
        print(log_entry.strip())

    def get_priority(self, filename):
        """
        Determine priority based on file characteristics.

        Args:
            filename: Name of the file

        Returns:
            Priority level: HIGH, MEDIUM, LOW, or NEEDS_REVIEW
        """
        filename_lower = filename.lower()
        extension = Path(filename).suffix.lower()

        # HIGH priority
        high_priority_extensions = ['.xlsx', '.xls', '.csv', '.eml', '.msg']
        high_priority_keywords = ['urgent', 'important', 'asap', 'critical', 'invoice', 'payment']

        if extension in high_priority_extensions:
            return "HIGH"
        if any(keyword in filename_lower for keyword in high_priority_keywords):
            return "HIGH"

        # MEDIUM priority
        medium_priority_extensions = ['.txt', '.md', '.doc', '.docx', '.pdf', '.py', '.js', '.html', '.css', '.json']

        if extension in medium_priority_extensions:
            return "MEDIUM"

        # LOW priority
        low_priority_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.avi', '.mp3']

        if extension in low_priority_extensions:
            return "LOW"

        # Unknown - needs review
        return "NEEDS_REVIEW"

    def run(self):
        """
        Main execution loop.
        Continuously checks for updates at specified interval.
        """
        self.running = True
        self.log_activity(f"{self.__class__.__name__} started with {self.check_interval}s interval")

        # Use simple text for Windows console compatibility
        print(f"\n{'='*60}")
        print(f"[AI] {self.__class__.__name__} Active")
        print(f"{'='*60}")
        print(f"Vault: {self.vault_path}")
        print(f"Check Interval: {self.check_interval} seconds")
        print(f"Monitoring started...")
        print(f"{'='*60}\n")

        try:
            while self.running:
                try:
                    # Check for updates
                    items = self.check_for_updates()

                    # Process each item found
                    if items:
                        self.log_activity(f"Found {len(items)} new item(s)")
                        for item in items:
                            self.create_action_file(item)

                    # Wait before next check
                    time.sleep(self.check_interval)

                except KeyboardInterrupt:
                    raise  # Re-raise to be caught by outer try-except
                except Exception as e:
                    self.log_activity(f"Error in check loop: {str(e)}", level="ERROR")
                    time.sleep(self.check_interval)  # Continue running despite error

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the watcher gracefully"""
        self.running = False
        self.log_activity(f"{self.__class__.__name__} stopped")
        print(f"\n{'='*60}")
        print(f"[STOP] {self.__class__.__name__} Stopped")
        print(f"{'='*60}\n")
