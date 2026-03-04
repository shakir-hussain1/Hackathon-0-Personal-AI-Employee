"""
Gold-Tier JSON Audit Logger
Logs every AI action to /Vault/Logs/YYYY-MM-DD.json (Section 6.3 of spec).
Format: {"timestamp", "action_type", "actor", "target", "parameters", "approval_status", "result"}
Retains logs for 90+ days.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

_GOLD_ROOT = Path(__file__).parent.parent
load_dotenv(_GOLD_ROOT / '.env')

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_GOLD_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
LOG_RETENTION_DAYS = int(os.getenv('LOG_RETENTION_DAYS', 90))


class AuditLogger:
    """JSON audit logger — every Gold-Tier action writes here."""

    def __init__(self, vault_path: Path = None):
        self.vault_path = vault_path or VAULT_PATH
        self.log_dir = self.vault_path / 'Logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _log_file(self, date: datetime = None) -> Path:
        d = date or datetime.now()
        return self.log_dir / f"{d.strftime('%Y-%m-%d')}.json"

    def log(
        self,
        action_type: str,
        actor: str = 'gold_orchestrator',
        target: str = '',
        parameters: dict = None,
        approval_status: str = 'auto',
        approved_by: str = 'system',
        result: str = 'success',
        error: str = None,
    ) -> dict:
        """Write a JSON audit record and return it."""
        record = {
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "action_type": action_type,
            "actor": actor,
            "target": target,
            "parameters": parameters or {},
            "approval_status": approval_status,
            "approved_by": approved_by,
            "result": result,
        }
        if error:
            record["error"] = error

        log_file = self._log_file()
        # Append JSON record (one per line for easy parsing)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + '\n')

        return record

    def log_action(self, action_type: str, **kwargs) -> dict:
        """Convenience wrapper — log(action_type, **kwargs)."""
        return self.log(action_type, **kwargs)

    def log_error(self, action_type: str, error: str, **kwargs) -> dict:
        """Log a failed action."""
        return self.log(action_type, result='error', error=error, **kwargs)

    def get_today_log(self) -> list:
        """Return list of all records logged today."""
        log_file = self._log_file()
        if not log_file.exists():
            return []
        records = []
        for line in log_file.read_text(encoding='utf-8').strip().split('\n'):
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return records

    def get_period_log(self, days: int = 7) -> list:
        """Return records from the last N days."""
        records = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            log_file = self._log_file(date)
            if log_file.exists():
                for line in log_file.read_text(encoding='utf-8').strip().split('\n'):
                    line = line.strip()
                    if line:
                        try:
                            records.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        return records

    def purge_old_logs(self):
        """Delete JSON logs older than LOG_RETENTION_DAYS."""
        cutoff = datetime.now() - timedelta(days=LOG_RETENTION_DAYS)
        purged = 0
        for log_file in self.log_dir.glob('*.json'):
            try:
                file_date = datetime.strptime(log_file.stem, '%Y-%m-%d')
                if file_date < cutoff:
                    log_file.unlink()
                    purged += 1
            except ValueError:
                pass
        return purged


# Module-level singleton
_logger = None


def get_audit_logger() -> AuditLogger:
    global _logger
    if _logger is None:
        _logger = AuditLogger()
    return _logger


def audit_log(action_type: str, **kwargs) -> dict:
    """Quick module-level log call."""
    return get_audit_logger().log(action_type, **kwargs)
