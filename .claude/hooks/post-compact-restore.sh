#!/bin/bash
# Post-Compact Restore — reads saved session state on session start
if [ -f .claude/CURRENT_TASK.md ]; then
    echo ""
    echo "## Resumed Task State (from previous session)"
    echo ""
    cat .claude/CURRENT_TASK.md
    echo ""
    echo "Continue from the 'Next concrete step' above."
fi
