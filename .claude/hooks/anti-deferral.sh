#!/bin/bash
# anti-deferral.sh — PreToolUse hook (Write, Edit, MultiEdit)
# Scans content being written for deferral language and warns Claude.
# Worldbuilding deferrals ("will flesh out later") create permanent canon gaps.

input=$(cat)

content=$(echo "$input" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    tool = data.get('tool_name', '')
    params = data.get('tool_input', {})
    if tool == 'Write':
        print(params.get('content', params.get('file_text', '')))
    elif tool == 'Edit':
        print(params.get('new_string', params.get('new_str', '')))
    elif tool == 'MultiEdit':
        edits = params.get('edits', [])
        print('\n'.join(e.get('new_string', e.get('new_str', '')) for e in edits))
except Exception:
    pass
" 2>/dev/null)

[ -z "$content" ] && exit 0

patterns=(
    "TODO"
    "FIXME"
    "XXX"
    "will flesh out"
    "will detail"
    "will expand"
    "will add"
    "will write"
    "will describe"
    "flesh out later"
    "add later"
    "expand later"
    "detail later"
    "placeholder"
    "stub"
    "needs more work"
    "for now"
    "later"
    "next session"
    "to be determined"
    "TBD"
    "filler"
    "draft only"
    "coming soon"
)

found=()
for pattern in "${patterns[@]}"; do
    if echo "$content" | grep -qi "$pattern"; then
        found+=("$pattern")
    fi
done

if [ ${#found[@]} -gt 0 ]; then
    cat << WARN

⚠  ANTI-DEFERRAL WARNING: ${found[*]}

Deferred worldbuilding creates permanent canon gaps. Before continuing:
1. Can this be written now? If yes, write it.
2. If deferral is genuinely correct, get explicit user approval.
3. Do not declare the task done while deferral language remains.

WARN
fi

exit 0
