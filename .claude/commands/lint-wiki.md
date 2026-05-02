---
description: >-
  Health-check the worldbuilding wiki. Finds contradictions between pages,
  stale claims superseded by newer sources, orphan pages with no inbound
  links, and missing entity pages for concepts mentioned but not documented.
  Usage: /lint-wiki [scope: all | directory | entity-name]
argument-hint: "[all | directory path | entity name]"
---

# Lint Wiki — Wiki Health Check

You are running a systematic health check on the worldbuilding wiki.
This is NOT a physics audit (use /auditing-physics) or a canon audit
(use /auditing-canon). This checks the wiki's structural integrity.

## The Four Lint Checks

### Check 1: Contradiction Detection

For the specified scope, find pages that make conflicting claims
about the same entity, event, or rule.

Process:
1. Build a claim map: entity → [file, claim] for each factual statement
2. Flag pairs where two files disagree on the same fact
3. Note: cross-civilization differences are NOT contradictions

Output: `| Entity | File A | Claim A | File B | Claim B | Verdict |`

### Check 2: Stale Claims

Find claims that were superseded by newer canon decisions.

Process:
1. Check MASTER-TIMELINE.md and GLOSSARY.md for current definitions
2. grep for older terminology (check naming convention files)
3. Find pages that use superseded terms, names, or rules

Output: `| File | Stale Claim | Current Canon | Action |`

### Check 3: Orphan Pages

Find pages with no inbound links from any other page.

Process:
```bash
# For each .md file, check if it's linked from anywhere
find . -name "*.md" -not -path "./.claude/*" | while read f; do
  name=$(basename "$f" .md)
  links=$(grep -rl "$name" --include="*.md" | grep -v "^$f$" | wc -l)
  [ "$links" -eq 0 ] && echo "ORPHAN: $f"
done
```

Orphans are candidates for deletion, merger, or linking.

### Check 4: Missing Pages (Ghost Entities)

Find entities mentioned across multiple files that have no dedicated page.

Process:
1. Grep for proper nouns (capitalized words) appearing 3+ times in the repo
2. Cross-reference against existing page titles
3. Flag entities with no page as ghost entities

Output: `| Entity | Mentions | Files | Action |`

## Scope Options

- `all` — full repo scan (slow, use periodically)
- `[directory]` — e.g., `civilizations/example/` (targeted)
- `[entity-name]` — find everything about one entity and check it

## Output Format

For each check, produce a prioritized table:

- **CRITICAL** — direct contradiction between two canon files
- **WARNING** — stale claim or orphan with inbound mentions elsewhere
- **INFO** — orphan with no mentions (candidate for cleanup)
- **GHOST** — entity mentioned 3+ times with no page

## After the Report

Do NOT fix anything automatically. Present the report for author review.
Author approves fixes → run /ingest or targeted edits.

After any fixes are applied, append to `meta/LOG.md`:
```
[YYYY-MM-DD] LINT: Fixed CONTRADICTION in physics/mechanics/example-file.md
[YYYY-MM-DD] LINT: Resolved GHOST entity "Elder" → created characters/elder.md
```

## Recommended Cadence

- After every `/ingest` session (new content creates new ghosts)
- Before promoting a section from draft to canon
- Monthly for full-repo structural health
