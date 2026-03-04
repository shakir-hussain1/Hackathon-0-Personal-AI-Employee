"""
File System Watcher
Monitors the Inbox folder for new files and creates tasks for processing
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Handle both relative and absolute imports
try:
    from .base_watcher import BaseWatcher
except ImportError:
    # Add parent directory to path for direct script execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from watchers.base_watcher import BaseWatcher


class FileSystemWatcher(BaseWatcher):
    """
    Watches the Inbox folder for new files.
    Creates task files in Needs_Action when new files are detected.
    """

    def __init__(self, vault_path, check_interval=30):
        """
        Initialize the File System Watcher.

        Args:
            vault_path: Path to the AI_Employee_Vault directory
            check_interval: Seconds between checks (default 30)
        """
        super().__init__(vault_path, check_interval)
        self.processed_files = set()  # Track files we've already seen
        self._load_existing_files()

    def _load_existing_files(self):
        """
        Load existing files in Inbox to avoid processing them as "new"
        on first run.
        """
        try:
            if self.inbox.exists():
                for file_path in self.inbox.iterdir():
                    if file_path.is_file():
                        self.processed_files.add(file_path.name)
                if self.processed_files:
                    self.log_activity(f"Loaded {len(self.processed_files)} existing files from Inbox")
        except Exception as e:
            self.log_activity(f"Error loading existing files: {str(e)}", level="ERROR")

    def check_for_updates(self):
        """
        Check Inbox folder for new files.

        Returns:
            List of new file paths found
        """
        new_files = []

        try:
            # List all files in Inbox
            if not self.inbox.exists():
                return new_files

            for file_path in self.inbox.iterdir():
                if file_path.is_file():
                    filename = file_path.name

                    # Check if this is a new file we haven't seen
                    if filename not in self.processed_files:
                        new_files.append(file_path)
                        self.processed_files.add(filename)
                        self.log_activity(f"Detected new file: {filename}")

        except Exception as e:
            self.log_activity(f"Error checking for updates: {str(e)}", level="ERROR")

        return new_files

    def create_action_file(self, file_path):
        """
        Create a task file in Needs_Action folder for the new file.

        Args:
            file_path: Path object of the new file
        """
        try:
            filename = file_path.name
            file_size = file_path.stat().st_size
            priority = self.get_priority(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Create task filename
            # Format: FILE_[originalname]_[timestamp].md
            safe_name = "".join(c for c in file_path.stem if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name[:50]  # Limit length
            task_filename = f"FILE_{safe_name}_{timestamp}.md"
            task_path = self.needs_action / task_filename

            # Create task file content
            task_content = self._generate_task_content(
                filename=filename,
                file_size=file_size,
                priority=priority,
                timestamp=timestamp
            )

            # Write task file
            with open(task_path, 'w', encoding='utf-8') as f:
                f.write(task_content)

            self.log_activity(f"Created task: {task_filename} [Priority: {priority}]")

        except Exception as e:
            self.log_activity(f"Error creating task for {file_path.name}: {str(e)}", level="ERROR")

    def _generate_task_content(self, filename, file_size, priority, timestamp):
        """
        Generate the markdown content for a task file.

        Args:
            filename: Original filename
            file_size: File size in bytes
            priority: Priority level
            timestamp: Creation timestamp

        Returns:
            Formatted markdown string
        """
        # Convert file size to human readable
        size_str = self._human_readable_size(file_size)

        # Get file extension for type hint
        file_ext = Path(filename).suffix.lower()
        file_type = self._get_file_type_description(file_ext)

        # Priority emoji
        priority_emoji = {
            "HIGH": "🔴",
            "MEDIUM": "🟡",
            "LOW": "🟢",
            "NEEDS_REVIEW": "🟣"
        }.get(priority, "⚪")

        content = f"""# 📋 Task: Process File

**Status**: ⏳ PENDING
**Priority**: {priority_emoji} {priority}
**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📁 File Information

- **Filename**: `{filename}`
- **Size**: {size_str}
- **Type**: {file_type}
- **Location**: `Inbox/{filename}`

---

## 🎯 Task Instructions

**AI Employee**: Please process this file according to the Company Handbook guidelines.

### Required Actions:
1. ✅ Read the file from `Inbox/{filename}`
2. ✅ Analyze the content based on file type
3. ✅ Extract key information
4. ✅ Create summary below
5. ✅ Move original file to appropriate subdirectory in `Done/`
6. ✅ Move this task file to `Done/`
7. ✅ Log the activity
8. ✅ Update Dashboard

---

## 📊 Analysis Results

*AI will complete this section during processing*

### File Summary:


### Key Information Extracted:


### Action Items Identified:


### Categorization:
**Moved to**: Done/[category]/

---

## 📝 Processing Log

**Processed**: [Timestamp will be added by AI]
**Processed By**: AI Employee
**Status**: ⏳ PENDING → [AI will update to ✅ COMPLETED]

---

## 🔧 Metadata

```
Task ID: {timestamp}
Original Filename: {filename}
File Size Bytes: {file_size}
Priority Level: {priority}
Watcher: FileSystemWatcher
```

---

*Task auto-generated by File System Watcher*
"""
        return content

    def _human_readable_size(self, size_bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def _get_file_type_description(self, extension):
        """Get a human-readable description of the file type"""
        type_map = {
            '.txt': 'Text Document',
            '.md': 'Markdown Document',
            '.doc': 'Word Document',
            '.docx': 'Word Document',
            '.pdf': 'PDF Document',
            '.xlsx': 'Excel Spreadsheet',
            '.xls': 'Excel Spreadsheet',
            '.csv': 'CSV Data File',
            '.json': 'JSON Data File',
            '.xml': 'XML Data File',
            '.py': 'Python Script',
            '.js': 'JavaScript File',
            '.html': 'HTML File',
            '.css': 'CSS Stylesheet',
            '.jpg': 'JPEG Image',
            '.jpeg': 'JPEG Image',
            '.png': 'PNG Image',
            '.gif': 'GIF Image',
            '.bmp': 'Bitmap Image',
            '.mp4': 'Video File',
            '.avi': 'Video File',
            '.mp3': 'Audio File',
            '.zip': 'Compressed Archive',
            '.rar': 'Compressed Archive',
            '.eml': 'Email Message',
            '.msg': 'Outlook Message',
        }
        return type_map.get(extension, f'Unknown ({extension})')


def main():
    """
    Main entry point for running the File System Watcher.
    """
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        # Default path (updated for multi-tier structure)
        vault_path = r"E:\Hackathon-0-Personal-AI-Employee\Common\AI_Employee_Vault"

    print("Starting File System Watcher...")
    print(f"Vault Path: {vault_path}")

    try:
        watcher = FileSystemWatcher(vault_path=vault_path, check_interval=30)
        watcher.run()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nUsage: python filesystem_watcher.py [vault_path]")
        print(f"Default vault path: {vault_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
