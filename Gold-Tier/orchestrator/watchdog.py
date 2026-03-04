"""
Gold-Tier Watchdog
Monitors critical processes and auto-restarts them on crash (Section 7.4).
Monitors: Gold orchestrator, Silver orchestrator, Bronze watcher.
Writes alerts to Dashboard.md and Logs/.

Run as a separate process: python Gold-Tier/orchestrator/watchdog.py
Or managed by Windows Task Scheduler for auto-start on boot.
"""

import json
import os
import subprocess
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

_GOLD_ROOT = Path(__file__).parent.parent
load_dotenv(_GOLD_ROOT / '.env')
sys.path.insert(0, str(_GOLD_ROOT))
from orchestrator.audit_logger import audit_log

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(_GOLD_ROOT / f"watchdog_{datetime.now().strftime('%Y%m%d')}.log")),
    ]
)
logger = logging.getLogger('gold_watchdog')

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_GOLD_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
WATCHDOG_INTERVAL = int(os.getenv('WATCHDOG_INTERVAL_SECONDS', '60'))

# Processes to monitor (name → command to restart)
GOLD_VENV = str(_GOLD_ROOT / 'venv' / 'Scripts' / 'python.exe')
SILVER_VENV = str(_GOLD_ROOT.parent / 'Silver-Tier' / 'venv' / 'Scripts' / 'python.exe')
BRONZE_VENV = str(_GOLD_ROOT.parent / 'Bronze-Tier' / 'venv' / 'Scripts' / 'python.exe')

MONITORED_PROCESSES = {
    'gold_orchestrator': {
        'command': [GOLD_VENV, str(_GOLD_ROOT / 'orchestrator' / 'orchestrator.py')],
        'pid_file': _GOLD_ROOT / '.gold_orchestrator.pid',
        'enabled': os.getenv('WATCHDOG_GOLD', 'true').lower() == 'true',
    },
    'silver_orchestrator': {
        'command': [SILVER_VENV, str(_GOLD_ROOT.parent / 'Silver-Tier' / 'orchestrator' / 'orchestrator.py')],
        'pid_file': _GOLD_ROOT / '.silver_orchestrator.pid',
        'enabled': os.getenv('WATCHDOG_SILVER', 'true').lower() == 'true',
    },
}


def _read_pid(pid_file: Path) -> int | None:
    """Read PID from file."""
    try:
        if pid_file.exists():
            return int(pid_file.read_text().strip())
    except (ValueError, OSError):
        pass
    return None


def _is_process_running(pid: int) -> bool:
    """Check if process with given PID is running on Windows."""
    if pid is None:
        return False
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x0400, False, pid)  # PROCESS_QUERY_INFORMATION
        if handle:
            import ctypes.wintypes
            exit_code = ctypes.wintypes.DWORD()
            kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
            kernel32.CloseHandle(handle)
            return exit_code.value == 259  # STILL_ACTIVE
        return False
    except Exception:
        # Fallback: try tasklist
        try:
            result = subprocess.run(
                ['tasklist', '/FI', f'PID eq {pid}', '/NH'],
                capture_output=True, text=True,
            )
            return str(pid) in result.stdout
        except Exception:
            return False


def _start_process(name: str, config: dict) -> int | None:
    """Start a process and write its PID to file."""
    try:
        proc = subprocess.Popen(
            config['command'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
        )
        config['pid_file'].write_text(str(proc.pid))
        logger.info(f"Started {name} (PID: {proc.pid})")
        audit_log('watchdog_start_process', actor='watchdog', target=name,
                  parameters={'pid': proc.pid}, result='success')
        _notify_dashboard(f"[WATCHDOG] {name} restarted (PID: {proc.pid})")
        return proc.pid
    except Exception as e:
        logger.error(f"Failed to start {name}: {e}")
        audit_log('watchdog_start_process', actor='watchdog', target=name,
                  result='error', error=str(e))
        return None


def _notify_dashboard(message: str):
    """Write watchdog alert to Dashboard.md."""
    try:
        dashboard = VAULT_PATH / 'Dashboard.md'
        if not dashboard.exists():
            return
        content = dashboard.read_text(encoding='utf-8')
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alert = f"\n> **[WATCHDOG]** {ts} — {message}\n"
        # Append after ## Watchdog section or at end
        if '## Watchdog' in content:
            import re
            content = re.sub(
                r'(## Watchdog\n)',
                f'\\1{alert}',
                content,
            )
        else:
            content += f"\n## Watchdog\n{alert}"
        dashboard.write_text(content, encoding='utf-8')
    except Exception:
        pass


def _log_to_vault(message: str, level: str = "INFO"):
    """Write to daily Logs/ file."""
    try:
        log_dir = VAULT_PATH / 'Logs'
        log_dir.mkdir(exist_ok=True)
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = log_dir / f"{today}.log"
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{ts}] [{level}] [WATCHDOG] {message}\n")
    except Exception:
        pass


def check_and_restart():
    """Check all monitored processes and restart any that are down."""
    restarts = 0
    for name, config in MONITORED_PROCESSES.items():
        if not config.get('enabled', True):
            continue
        pid = _read_pid(config['pid_file'])
        if not _is_process_running(pid):
            logger.warning(f"{name} not running (last PID: {pid}). Restarting...")
            _log_to_vault(f"{name} not running — restarting", level="WARNING")
            new_pid = _start_process(name, config)
            if new_pid:
                restarts += 1
    return restarts


def run():
    """Main watchdog loop."""
    logger.info("="*50)
    logger.info("Gold Tier Watchdog Starting")
    logger.info(f"Monitoring: {list(MONITORED_PROCESSES.keys())}")
    logger.info(f"Check interval: {WATCHDOG_INTERVAL}s")
    logger.info("="*50)
    audit_log('watchdog_start', actor='watchdog')

    try:
        while True:
            try:
                restarts = check_and_restart()
                if restarts:
                    logger.info(f"Restarted {restarts} process(es)")
            except Exception as e:
                logger.error(f"Watchdog check error: {e}")
            time.sleep(WATCHDOG_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Watchdog stopped.")
        audit_log('watchdog_stop', actor='watchdog')


if __name__ == '__main__':
    run()
