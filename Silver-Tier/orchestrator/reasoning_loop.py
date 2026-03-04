"""
Claude Reasoning Loop - Silver Tier
Reads pending tasks from Needs_Action/ and uses the Anthropic API to create Plan.md files.
Runs on a schedule via the orchestrator.
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

_SILVER_ROOT = Path(__file__).parent.parent
load_dotenv(_SILVER_ROOT / '.env')

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_SILVER_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
MODEL = os.getenv('REASONING_MODEL', 'claude-opus-4-6')

logger = logging.getLogger('reasoning_loop')

SYSTEM_PROMPT = """You are a Silver-Tier AI Employee. You analyze incoming tasks and create detailed, actionable plans.

For every task, reason through:
1. What exactly happened or is being requested?
2. What are the key facts, priorities, and constraints?
3. What ordered actions should be taken?
4. Who needs to be involved or notified?
5. What is the single most important next step right now?

Output a structured Plan in markdown with these sections:
## Summary
## Key Facts
## Action Plan
(numbered, ordered steps)
## Immediate Next Step
## Estimated Effort
(Low / Medium / High — with one sentence justification)

Be specific. Refer to actual names, numbers, and dates from the task. Do not give generic advice."""


def _get_pending_tasks() -> list[Path]:
    needs_action = VAULT_PATH / 'Needs_Action'
    if not needs_action.exists():
        return []
    return [f for f in needs_action.glob('*.md') if not f.name.startswith('.')]


def _plan_already_exists(task_file: Path) -> bool:
    plans_dir = VAULT_PATH / 'Plans'
    if not plans_dir.exists():
        return False
    safe_name = task_file.stem[:40]
    return any(plans_dir.glob(f"Plan_{safe_name}_*.md"))


def _create_plan(task_file: Path) -> Path:
    """Call Claude API to reason about a task and write Plan_{name}_{ts}.md."""
    try:
        import anthropic
    except ImportError:
        raise ImportError("anthropic package not installed. Run: pip install anthropic")

    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set in .env — reasoning loop disabled")

    task_content = task_file.read_text(encoding='utf-8')

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Analyze this task and create an action plan:\n\n{task_content}"
        }],
    )
    plan_body = message.content[0].text

    plans_dir = VAULT_PATH / 'Plans'
    plans_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_name = task_file.stem[:40]
    plan_file = plans_dir / f"Plan_{safe_name}_{timestamp}.md"

    header = (
        f"# Plan: {task_file.stem}\n"
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Source Task: {task_file.name}\n"
        f"Model: {MODEL}\n"
        "\n---\n\n"
    )
    plan_file.write_text(header + plan_body, encoding='utf-8')
    return plan_file


def _log(message: str):
    log_dir = VAULT_PATH / 'Logs'
    log_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_dir / f"{today}.log", 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] [REASONING_LOOP] {message}\n")


def run_reasoning_loop() -> int:
    """
    Process all unplanned pending tasks. Returns count of Plan.md files created.
    Safe to call repeatedly — skips tasks that already have a Plan.
    """
    tasks = _get_pending_tasks()
    if not tasks:
        logger.info("Reasoning loop: no pending tasks.")
        return 0

    created = 0
    for task_file in tasks:
        if _plan_already_exists(task_file):
            logger.info(f"Plan already exists for: {task_file.name} — skipping")
            continue
        try:
            plan_file = _create_plan(task_file)
            logger.info(f"Plan created: {plan_file.name}")
            _log(f"Plan created: {plan_file.name} ← {task_file.name}")
            created += 1
        except ValueError as e:
            # API key not set — log once and stop trying
            logger.warning(str(e))
            _log(f"WARNING: {e}")
            break
        except Exception as e:
            logger.error(f"Failed to plan {task_file.name}: {e}")
            _log(f"ERROR planning {task_file.name}: {e}")

    return created
