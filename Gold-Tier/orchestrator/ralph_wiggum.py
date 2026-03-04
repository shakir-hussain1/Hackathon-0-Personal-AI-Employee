"""
Gold-Tier Ralph Wiggum Loop
Implements the "file movement" completion strategy (Gold-tier, Section 2D).

How it works:
  1. Orchestrator creates a state file with the task prompt
  2. Claude works on the task
  3. When Claude tries to stop, the Stop hook runs this module
  4. Hook checks if the task file has moved to Done/
  5. If YES → allow exit
  6. If NO → re-inject the prompt (Claude continues)
  7. Repeat until done OR max_iterations exceeded

State file location: Common/AI_Employee_Vault/In_Progress/.ralph_state.json
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

_GOLD_ROOT = Path(__file__).parent.parent
load_dotenv(_GOLD_ROOT / '.env')

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_GOLD_ROOT.parent / 'Common' / 'AI_Employee_Vault')))
STATE_FILE = VAULT_PATH / 'In_Progress' / '.ralph_state.json'
MAX_DEFAULT_ITERATIONS = int(os.getenv('RALPH_MAX_ITERATIONS', '10'))


class RalphWiggumLoop:
    """Manages Ralph Wiggum loop state."""

    def __init__(self):
        self.state_file = STATE_FILE
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def start_task(
        self,
        task_file: str,
        prompt: str,
        max_iterations: int = MAX_DEFAULT_ITERATIONS,
    ) -> dict:
        """
        Create a new Ralph loop state.
        Call this before starting a multi-step Claude session.

        Args:
            task_file: Path to the task .md file in Needs_Action/
            prompt: The prompt Claude should work on
            max_iterations: Safety limit (default 10)
        """
        state = {
            "task_file": str(task_file),
            "task_name": Path(task_file).name,
            "prompt": prompt,
            "max_iterations": max_iterations,
            "current_iteration": 0,
            "started_at": datetime.now().isoformat(),
            "status": "running",
        }
        self.state_file.write_text(json.dumps(state, indent=2), encoding='utf-8')
        return state

    def get_state(self) -> dict | None:
        """Return current loop state, or None if no active loop."""
        if not self.state_file.exists():
            return None
        try:
            return json.loads(self.state_file.read_text(encoding='utf-8'))
        except Exception:
            return None

    def clear_state(self):
        """Remove state file — allows Claude to exit."""
        if self.state_file.exists():
            self.state_file.unlink()

    def is_task_done(self, state: dict) -> bool:
        """
        Check if the task file has moved to Done/ (file-movement strategy).
        Also checks for TASK_COMPLETE promise in task file content.
        """
        task_file = Path(state.get('task_file', ''))
        task_name = state.get('task_name', '')
        done_dir = VAULT_PATH / 'Done'

        # Check: file moved to Done/ or any subdirectory of Done/
        if any(done_dir.rglob(task_name)):
            return True

        # Check: original file no longer in Needs_Action
        if task_file.exists():
            content = task_file.read_text(encoding='utf-8')
            if 'TASK_COMPLETE' in content or 'Status: COMPLETED' in content.upper():
                return True
        elif not task_file.exists() and not task_file.parent.name == 'Done':
            # File gone from Needs_Action but not in Done — might be deleted
            return True

        return False

    def check_and_continue(self) -> tuple[bool, str]:
        """
        Called by Stop hook.
        Returns: (should_continue: bool, continuation_prompt: str)

        If should_continue=True: Claude must continue working.
        If should_continue=False: Claude may exit.
        """
        state = self.get_state()

        if not state:
            return False, ""  # No active Ralph loop — allow exit

        current_iter = state.get('current_iteration', 0)
        max_iter = state.get('max_iterations', MAX_DEFAULT_ITERATIONS)

        # Safety: max iterations exceeded
        if current_iter >= max_iter:
            print(f"[RALPH] Max iterations ({max_iter}) reached for task: {state.get('task_name')}")
            self.clear_state()
            return False, ""

        # Check if task is done
        if self.is_task_done(state):
            print(f"[RALPH] Task complete: {state.get('task_name')} (iteration {current_iter})")
            self.clear_state()
            return False, ""  # Allow exit

        # Task not done — increment and continue
        state['current_iteration'] = current_iter + 1
        state['last_checked'] = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(state, indent=2), encoding='utf-8')

        continuation = (
            f"[RALPH WIGGUM — iteration {current_iter + 1}/{max_iter}]\n\n"
            f"The task is not yet complete. Task file: `{state.get('task_name')}`\n\n"
            f"Continue working. When done, make sure the task file is moved to `Done/`.\n\n"
            f"Original task:\n{state.get('prompt', 'Continue processing the current task.')}"
        )

        print(f"[RALPH] Iteration {current_iter + 1}/{max_iter} — continuing task: {state.get('task_name')}")
        return True, continuation


def stop_hook_main():
    """
    Entry point called by .claude/hooks/ralph_wiggum_stop.py
    Outputs continuation prompt if task not done, exits 0 to allow exit.
    """
    ralph = RalphWiggumLoop()
    should_continue, prompt = ralph.check_and_continue()

    if should_continue:
        # Output the continuation prompt — Claude Code will inject it
        print(prompt)
        sys.exit(1)  # Non-zero signals: do not exit Claude
    else:
        sys.exit(0)  # Allow Claude to exit


def start_ralph_loop(task_file: str, prompt: str, max_iterations: int = MAX_DEFAULT_ITERATIONS) -> dict:
    """Convenience function — start a Ralph loop for a task."""
    ralph = RalphWiggumLoop()
    state = ralph.start_task(task_file, prompt, max_iterations)
    print(f"[RALPH] Loop started for: {Path(task_file).name} (max {max_iterations} iterations)")
    return state


if __name__ == '__main__':
    # If called directly — run as stop hook
    stop_hook_main()
