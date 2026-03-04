"""
Platinum Tier Setup
Run once to prepare the vault with Platinum-specific folders and git init.

Usage: python setup/setup_platinum.py
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

_SETUP_ROOT = Path(__file__).parent
_PLATINUM_ROOT = _SETUP_ROOT.parent
sys.path.insert(0, str(_PLATINUM_ROOT))

VAULT_PATH = Path(
    os.getenv("VAULT_PATH",
    str(_PLATINUM_ROOT.parent / "Common" / "AI_Employee_Vault"))
)

# New folders required by Platinum (in addition to Bronze/Silver/Gold folders)
PLATINUM_FOLDERS = [
    "Needs_Action/email",
    "Needs_Action/social",
    "Needs_Action/file",
    "Plans/email",
    "Plans/social",
    "Pending_Approval/email",
    "Pending_Approval/social",
    "In_Progress/cloud",
    "In_Progress/local",
    "Updates",
    "Updates/health",
    "Updates/processed",
    "Signals",
    "Done",
    "Rejected",
    "Logs",
    "Briefings",
    "Accounting",
]


def create_folders():
    print(f"\nVault: {VAULT_PATH}")
    print("Creating Platinum folder structure...\n")
    for folder in PLATINUM_FOLDERS:
        path = VAULT_PATH / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {folder}/")
    print("\nFolders ready.")


def create_gitignore():
    gi = VAULT_PATH / ".gitignore"
    rules = [
        "# Platinum Tier — secrets never sync",
        ".env", "*.env", "credentials.json",
        ".gmail_token.json", "*.session",
        "*.pid", "__pycache__/", "*.pyc",
        "venv/", "*.json",
    ]
    existing = gi.read_text(encoding="utf-8") if gi.exists() else ""
    with open(gi, "a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        for rule in rules:
            if rule not in existing:
                f.write(rule + "\n")
    print("\n✓ .gitignore updated (secrets excluded from sync)")


def init_git():
    import subprocess
    result = subprocess.run(["git", "-C", str(VAULT_PATH), "rev-parse", "--git-dir"],
                            capture_output=True)
    if result.returncode == 0:
        print("✓ Git repo already initialized")
    else:
        subprocess.run(["git", "-C", str(VAULT_PATH), "init"], check=True)
        print("✓ Git repo initialized in vault")


def create_env_example():
    env_file = _PLATINUM_ROOT / ".env.example"
    content = """# Platinum Tier - Local Agent
# Copy to .env and fill in your values

# Vault path (absolute)
VAULT_PATH=E:/Hackathon-0-Personal-AI-Employee/Common/AI_Employee_Vault

# Git remote for cloud-local vault sync (e.g., private GitHub repo)
VAULT_GIT_REMOTE=

# Dry run mode (true = no real actions taken)
DRY_RUN=true

# Enable actual email sending after approval
ENABLE_GMAIL_SEND=false

# Poll interval for local orchestrator (seconds)
CHECK_INTERVAL_SEC=30
"""
    env_file.write_text(content, encoding="utf-8")

    env_cloud = _PLATINUM_ROOT / "cloud" / ".env.cloud.example"
    cloud_content = """# Platinum Tier - Cloud Agent
# Copy to cloud/.env on your cloud VM

# Vault path on cloud VM (git clone of vault repo)
VAULT_PATH=/home/ubuntu/AI_Employee_Vault

# Git remote for vault sync
VAULT_GIT_REMOTE=git@github.com:youruser/ai-employee-vault.git

# Gmail credentials path (NEVER sync this file)
GMAIL_CREDENTIALS=/home/ubuntu/secrets/credentials.json

# Poll interval (minutes)
CHECK_INTERVAL_MIN=15

# Dry run (set false only after testing)
DRY_RUN=true

# Enable Gmail monitoring
ENABLE_GMAIL=false

# Health monitor settings
HEALTH_CHECK_INTERVAL_SEC=60
MAX_RESTARTS_PER_HOUR=5
"""
    env_cloud.write_text(cloud_content, encoding="utf-8")
    print("✓ .env.example files created (fill in and rename to .env)")


def write_setup_signal():
    sig = VAULT_PATH / "Signals" / "PLATINUM_SETUP.md"
    sig.write_text(
        f"# Platinum Tier Activated\n"
        f"Setup completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"Cloud agent: configure cloud/.env and deploy\n"
        f"Local agent: start_platinum_local.bat\n",
        encoding="utf-8",
    )
    print("✓ Setup signal written to vault")


if __name__ == "__main__":
    print("=" * 55)
    print("  Platinum Tier Setup")
    print("=" * 55)
    create_folders()
    create_gitignore()
    init_git()
    create_env_example()
    write_setup_signal()
    print("\n" + "=" * 55)
    print("  Setup complete!")
    print("  Next steps:")
    print("  1. Copy .env.example → .env and fill values")
    print("  2. Set VAULT_GIT_REMOTE to a private GitHub repo")
    print("  3. Run: start_platinum_local.bat")
    print("  4. Deploy cloud/ folder to Oracle/AWS VM")
    print("=" * 55)
