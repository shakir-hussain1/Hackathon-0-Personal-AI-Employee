"""
Gold-Tier Weekly Business Audit & CEO Briefing Generator
Runs every Sunday evening → generates Monday Morning CEO Briefing.

Reads:
  - Business_Goals.md (targets + metrics)
  - Done/ task files (completed work this week)
  - Accounting/ transactions (income, expenses)
  - Social_Media/ summaries (Facebook, Instagram, Twitter)
  - Logs/ JSON audit logs (system health)

Writes:
  - Briefings/YYYY-MM-DD_Monday_Briefing.md
  - Logs/weekly_audit_YYYY-MM-DD.json
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

_GOLD_ROOT = Path(__file__).parent.parent
load_dotenv(_GOLD_ROOT / '.env')
sys.path.insert(0, str(_GOLD_ROOT))
from orchestrator.audit_logger import audit_log

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_GOLD_ROOT.parent / 'Common' / 'AI_Employee_Vault')))

SUBSCRIPTION_PATTERNS = {
    'netflix': 'Netflix',
    'spotify': 'Spotify',
    'adobe': 'Adobe Creative Cloud',
    'notion': 'Notion',
    'slack': 'Slack',
    'github': 'GitHub',
    'digitalocean': 'DigitalOcean',
    'aws': 'AWS',
    'google cloud': 'Google Cloud',
    'openai': 'OpenAI',
    'anthropic': 'Anthropic API',
}


def _read_business_goals() -> dict:
    """Parse Business_Goals.md for targets and metrics."""
    goals_file = VAULT_PATH / 'Business_Goals.md'
    if not goals_file.exists():
        return {'monthly_revenue_target': 0, 'projects': [], 'metrics': {}}
    content = goals_file.read_text(encoding='utf-8')
    goals = {'raw': content, 'monthly_revenue_target': 0, 'projects': []}
    for line in content.split('\n'):
        if 'monthly goal' in line.lower() or 'monthly target' in line.lower():
            import re
            nums = re.findall(r'[\$Rs,]+\s*[\d,]+', line)
            if nums:
                num_str = ''.join(c for c in nums[0] if c.isdigit())
                if num_str:
                    goals['monthly_revenue_target'] = int(num_str)
        if line.strip().startswith(('1.', '2.', '3.', '-')) and 'project' in line.lower():
            goals['projects'].append(line.strip())
    return goals


def _get_week_transactions() -> dict:
    """Sum income/expenses from Accounting/ for the past 7 days."""
    accounting_dir = VAULT_PATH / 'Accounting'
    since = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    totals = {'income': 0.0, 'expense': 0.0, 'payment': 0.0, 'records': []}

    if not accounting_dir.exists():
        return totals

    for f in accounting_dir.glob('transactions_*.json'):
        try:
            for line in f.read_text(encoding='utf-8').strip().split('\n'):
                if not line.strip():
                    continue
                rec = json.loads(line)
                if rec.get('date', '') >= since:
                    t = rec.get('type', 'unknown')
                    if t in totals:
                        totals[t] += float(rec.get('amount', 0))
                    totals['records'].append(rec)
        except Exception:
            pass
    return totals


def _get_done_tasks_this_week() -> list:
    """List tasks completed (moved to Done/) in the last 7 days."""
    done_dir = VAULT_PATH / 'Done'
    since = datetime.now() - timedelta(days=7)
    tasks = []
    if not done_dir.exists():
        return tasks
    for f in done_dir.rglob('*.md'):
        try:
            if datetime.fromtimestamp(f.stat().st_mtime) >= since:
                tasks.append({
                    'name': f.name,
                    'modified': datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M'),
                    'path': str(f.relative_to(VAULT_PATH)),
                })
        except Exception:
            pass
    return sorted(tasks, key=lambda x: x['modified'], reverse=True)


def _get_social_media_summary() -> str:
    """Read latest social media report files."""
    social_dir = VAULT_PATH / 'Social_Media'
    if not social_dir.exists():
        return "_No social media reports available._"

    summaries = []
    for report in sorted(social_dir.glob('*.md'), key=lambda f: f.stat().st_mtime, reverse=True)[:3]:
        try:
            content = report.read_text(encoding='utf-8')
            lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#')][:5]
            summaries.append(f"**{report.stem}**\n" + '\n'.join(lines))
        except Exception:
            pass
    return '\n\n'.join(summaries) if summaries else "_No social reports this week._"


def _detect_subscription_expenses(transactions: list) -> list:
    """Flag recurring subscription charges for review."""
    flagged = []
    for rec in transactions:
        desc = rec.get('description', '').lower()
        for pattern, name in SUBSCRIPTION_PATTERNS.items():
            if pattern in desc and rec.get('type') == 'expense':
                flagged.append({
                    'name': name,
                    'amount': rec.get('amount', 0),
                    'date': rec.get('date', ''),
                    'description': rec.get('description', ''),
                })
    return flagged


def _get_system_health() -> dict:
    """Summarize errors from JSON audit logs this week."""
    logger_instance = type('L', (), {'get_period_log': lambda self, days: []})()
    try:
        from orchestrator.audit_logger import get_audit_logger
        records = get_audit_logger().get_period_log(days=7)
    except Exception:
        records = []

    total = len(records)
    errors = [r for r in records if r.get('result') == 'error']
    actions = {}
    for r in records:
        at = r.get('action_type', 'unknown')
        actions[at] = actions.get(at, 0) + 1

    return {
        'total_actions': total,
        'errors': len(errors),
        'error_rate': f"{(len(errors) / max(total, 1)) * 100:.1f}%",
        'top_actions': sorted(actions.items(), key=lambda x: x[1], reverse=True)[:5],
    }


def generate_ceo_briefing() -> Path:
    """Generate the Monday Morning CEO Briefing and write to Briefings/."""
    now = datetime.now()
    period_start = (now - timedelta(days=7)).strftime('%Y-%m-%d')
    period_end = now.strftime('%Y-%m-%d')
    briefing_date = now.strftime('%Y-%m-%d')

    goals = _read_business_goals()
    transactions = _get_week_transactions()
    done_tasks = _get_done_tasks_this_week()
    social = _get_social_media_summary()
    health = _get_system_health()
    subs = _detect_subscription_expenses(transactions.get('records', []))

    income = transactions.get('income', 0)
    expenses = transactions.get('expense', 0)
    net = income - expenses
    target = goals.get('monthly_revenue_target', 0)
    mtd_pct = f"{(income / target * 100):.0f}%" if target > 0 else "N/A"

    trend = "On track" if target == 0 or income >= (target * 7 / 30) else "Behind target"

    # Build briefing markdown
    briefing = f"""# Monday Morning CEO Briefing
---
generated: {now.isoformat()}
period: {period_start} to {period_end}
tier: Gold
---

## Executive Summary
Week {now.isocalendar()[1]} of {now.year}. {'Revenue ahead of weekly target.' if trend == 'On track' else 'Revenue behind weekly target — action recommended.'} {len(done_tasks)} tasks completed. System health: {health['error_rate']} error rate.

---

## Revenue & Financials

| Metric | This Week |
|--------|-----------|
| Income | {income:,.2f} |
| Expenses | {expenses:,.2f} |
| Net | {net:,.2f} |
| MTD vs Target | {mtd_pct} |
| Trend | {trend} |

---

## Completed Tasks This Week ({len(done_tasks)} total)

"""
    for task in done_tasks[:10]:
        briefing += f"- [x] `{task['name']}` — {task['modified']}\n"
    if len(done_tasks) > 10:
        briefing += f"\n_...and {len(done_tasks) - 10} more in Done/_\n"

    briefing += f"""
---

## Social Media Performance

{social}

---

## System Health

| Metric | Value |
|--------|-------|
| Total Actions | {health['total_actions']} |
| Errors | {health['errors']} |
| Error Rate | {health['error_rate']} |

**Top Actions This Week:**
"""
    for action, count in health['top_actions']:
        briefing += f"- `{action}`: {count} times\n"

    if subs:
        briefing += f"""
---

## Subscription Audit

The following subscriptions were detected this week:

| Service | Amount | Date |
|---------|--------|------|
"""
        for sub in subs:
            briefing += f"| {sub['name']} | {sub['amount']:,.2f} | {sub['date']} |\n"
        briefing += "\n> **Review:** Are all subscriptions actively used?\n"

    briefing += f"""
---

## Active Projects

"""
    for project in goals.get('projects', [])[:5]:
        briefing += f"- {project}\n"
    if not goals.get('projects'):
        briefing += "_No projects found in Business_Goals.md_\n"

    briefing += f"""
---

## Upcoming Actions Required

"""
    # Check Pending_Approval for anything waiting
    pending_dir = VAULT_PATH / 'Pending_Approval'
    pending = list(pending_dir.glob('*.md')) if pending_dir.exists() else []
    if pending:
        briefing += f"**{len(pending)} items awaiting your approval:**\n"
        for p in pending[:5]:
            briefing += f"- `Pending_Approval/{p.name}`\n"
    else:
        briefing += "_Nothing pending your approval. All clear._\n"

    briefing += f"\n---\n_Generated by AI Employee Gold Tier — {now.strftime('%Y-%m-%d %H:%M')} | Weekly Audit_\n"

    # Write to Briefings/
    briefings_dir = VAULT_PATH / 'Briefings'
    briefings_dir.mkdir(exist_ok=True)
    briefing_file = briefings_dir / f"{briefing_date}_Monday_Briefing.md"
    briefing_file.write_text(briefing, encoding='utf-8')

    # Log JSON audit record
    audit_log(
        'weekly_audit_complete',
        actor='weekly_audit',
        target=str(briefing_file),
        parameters={
            'income': income,
            'expenses': expenses,
            'tasks_completed': len(done_tasks),
            'errors': health['errors'],
        },
        result='success',
    )

    return briefing_file


def run_weekly_audit() -> Path:
    """Called by orchestrator every Sunday at configured time."""
    try:
        path = generate_ceo_briefing()
        return path
    except Exception as e:
        audit_log('weekly_audit', result='error', error=str(e))
        raise


if __name__ == '__main__':
    path = generate_ceo_briefing()
    print(f"CEO Briefing written to: {path}")
