"""
Health Monitor - Platinum Tier (Cloud Side)
Monitors critical processes and auto-restarts them if they crash.
Writes health reports to /Updates/health/ in the vault.

Processes monitored:
  - cloud_orchestrator.py
  - (extensible: add more to PROCESSES dict)

Usage: python health_monitor.py
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime

import psutil
from dotenv import load_dotenv

_CLOUD_ROOT = Path(__file__).parent
_PLATINUM_ROOT = _CLOUD_ROOT.parent
load_dotenv(_CLOUD_ROOT / ".env")
load_dotenv(_PLATINUM_ROOT / ".env")

VAULT_PATH = Path(os.getenv("VAULT_PATH", str(_PLATINUM_ROOT.parent / "Common" / "AI_Employee_Vault")))
CHECK_INTERVAL = int(os.getenv("HEALTH_CHECK_INTERVAL_SEC", "60"))
MAX_RESTARTS = int(os.getenv("MAX_RESTARTS_PER_HOUR", "5"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [HEALTH] %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(_CLOUD_ROOT / f"health_{datetime.now().strftime('%Y%m%d')}.log")),
    ],
)
logger = logging.getLogger("health_monitor")

# Processes to monitor: name → command
PROCESSES = {
    "cloud_orchestrator": [sys.executable, str(_CLOUD_ROOT / "cloud_orchestrator.py")],
}

# PID tracking
_pids: dict[str, int] = {}
_restart_counts: dict[str, int] = {}
_last_reset = datetime.now()


def _reset_counters_if_new_hour():
    global _last_reset
    now = datetime.now()
    if (now - _last_reset).seconds > 3600:
        _restart_counts.clear()
        _last_reset = now


def is_running(pid: int) -> bool:
    try:
        proc = psutil.Process(pid)
        return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def start_process(name: str) -> int | None:
    cmd = PROCESSES[name]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info(f"Started {name} (pid={proc.pid})")
        return proc.pid
    except Exception as e:
        logger.error(f"Failed to start {name}: {e}")
        return None


def write_health_report(status: dict):
    health_dir = VAULT_PATH / "Updates" / "health"
    health_dir.mkdir(parents=True, exist_ok=True)
    report = health_dir / "HEALTH_LATEST.md"

    lines = [
        "# Cloud Health Report",
        f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Process Status",
    ]
    for name, info in status.items():
        icon = "✅" if info["running"] else "❌"
        lines.append(f"- {icon} **{name}** | pid={info['pid']} | restarts={info['restarts']}")

    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run():
    logger.info("Health Monitor started (Platinum Tier)")

    # Start all monitored processes initially
    for name in PROCESSES:
        _pids[name] = start_process(name) or 0
        _restart_counts[name] = 0

    while True:
        time.sleep(CHECK_INTERVAL)
        _reset_counters_if_new_hour()

        status = {}
        for name in PROCESSES:
            pid = _pids.get(name, 0)
            running = pid > 0 and is_running(pid)

            if not running:
                restarts = _restart_counts.get(name, 0)
                if restarts >= MAX_RESTARTS:
                    logger.error(f"{name} exceeded max restarts ({MAX_RESTARTS}/hr). Not restarting.")
                    _pids[name] = 0
                else:
                    logger.warning(f"{name} is down. Restarting... ({restarts + 1}/{MAX_RESTARTS})")
                    new_pid = start_process(name)
                    _pids[name] = new_pid or 0
                    _restart_counts[name] = restarts + 1

            status[name] = {
                "running": running or (_pids[name] > 0),
                "pid": _pids[name],
                "restarts": _restart_counts.get(name, 0),
            }

        write_health_report(status)
        all_ok = all(s["running"] for s in status.values())
        logger.info(f"Health check: {'ALL OK' if all_ok else 'ISSUES DETECTED'}")


if __name__ == "__main__":
    run()
