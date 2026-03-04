#!/usr/bin/env python3
"""
Ralph Wiggum Stop Hook
Called by Claude Code when the session is about to end.

Register in .claude/settings.json:
  {
    "hooks": {
      "Stop": [
        {
          "matcher": "",
          "hooks": [
            {
              "type": "command",
              "command": "python E:\\Hackathon-0-Personal-AI-Employee\\.claude\\hooks\\ralph_wiggum_stop.py"
            }
          ]
        }
      ]
    }
  }

Behavior:
  - If no active Ralph loop: exit 0 (allow Claude to stop)
  - If task not in Done/ yet: print continuation prompt, exit 1 (keep Claude running)
  - If max iterations exceeded: exit 0 (safety release)
"""

import sys
from pathlib import Path

# Find project root
_HOOK_DIR = Path(__file__).parent
_PROJECT_ROOT = _HOOK_DIR.parent.parent

# Try to import ralph_wiggum from Gold-Tier
_GOLD = _PROJECT_ROOT / 'Gold-Tier'
sys.path.insert(0, str(_GOLD))

try:
    from orchestrator.ralph_wiggum import RalphWiggumLoop

    ralph = RalphWiggumLoop()
    should_continue, prompt = ralph.check_and_continue()

    if should_continue:
        # Print the continuation prompt — Claude Code will inject it as a user message
        print(prompt)
        sys.exit(1)  # Signal: do not stop
    else:
        sys.exit(0)  # Allow Claude to stop

except Exception as e:
    # If anything goes wrong with the hook, allow Claude to stop
    # (fail safe — never block Claude indefinitely due to hook error)
    import traceback
    print(f"[RALPH HOOK ERROR] {e}", file=sys.stderr)
    sys.exit(0)
