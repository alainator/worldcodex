#!/bin/bash
# post-tool-use.sh — PostToolUse hook (Write, Edit, MultiEdit on *.md files)
# Lints worldbuilding documents after writing for deterministic formatting violations.
# Checks: meta-commentary in science dirs, equation formatting, frontmatter presence.
# Customize the science_dirs and checks below for your universe.

input=$(cat)

filepath=$(echo "$input" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    tool = data.get('tool_name', '')
    params = data.get('tool_input', {})
    if tool in ('Write', 'Edit', 'MultiEdit'):
        print(params.get('file_path', params.get('filePath', params.get('path', ''))))
except Exception:
    pass
" 2>/dev/null)

# Only check markdown files
[[ "$filepath" != *.md ]] && exit 0
[ -z "$filepath" ] || [ ! -f "$filepath" ] && exit 0

issues=()

# Check 1: Meta-commentary in science directories
# Customize this pattern for your universe's science directory names
if echo "$filepath" | grep -qE "^(physics|chemistry|biology|science)"; then
    for phrase in "This section" "This document" "This file" "The following" "As mentioned"; do
        if grep -qi "^$phrase" "$filepath" 2>/dev/null; then
            issues+=("META-COMMENTARY: '$phrase' found — science files state facts, not document structure")
        fi
    done
fi

# Check 2: Equation formatting (bare $$ without blank lines)
if grep -qP '^\$\$' "$filepath" 2>/dev/null; then
    if grep -P '.\$\$|^\$\$.' "$filepath" 2>/dev/null | grep -qv '^\$\$$'; then
        issues+=("EQUATION-FORMAT: \$\$ blocks may lack blank lines above/below")
    fi
fi

# Check 3: Missing YAML frontmatter
if ! head -1 "$filepath" | grep -q "^---$" 2>/dev/null; then
    issues+=("FRONTMATTER: File lacks YAML frontmatter (expected --- on line 1)")
fi

if [ ${#issues[@]} -gt 0 ]; then
    echo ""
    echo "⚠  POST-WRITE LINT: $filepath"
    for issue in "${issues[@]}"; do
        echo "  • $issue"
    done
    echo ""
fi

exit 0
