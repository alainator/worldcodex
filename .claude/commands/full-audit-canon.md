---
description: >-
  Run a full canon audit cycle — scope → scan → triage → fix → verify.
  Orchestrates the worldbuilder-physicist and worldbuilder-editor agents
  through physics consistency and prose standards checks.
  Usage: /full-audit-canon [scope: physics | canon | full]
argument-hint: "[physics | canon | full]"
---

# Full Audit Canon — Complete Audit Cycle

You are orchestrating a full canon audit. Follow this sequence exactly.
Do not skip steps or combine phases.

## Step 1: Scope Selection

If the user specified a scope, use it. Otherwise ask:
- `physics` — physics/ through applied/ (cross-layer consistency)
- `canon` — naming, frontmatter, writing standards, cross-references
- `full` — both passes (split into two sessions, physics first)

For scope prioritisation, identify recently modified files first:
```bash
git log --since="30 days ago" --name-only --pretty=format: \
  | grep "\.md$" | sort | uniq -c | sort -rn | head -20
```
Start with the highest-churn files in the chosen scope.

## Step 2: Load Audit References

Before scanning, load the appropriate reference files:
- **physics scope:** Load `auditing-physics/references/` (all 5 files)
- **canon scope:** Load `auditing-canon/references/` (all 4 files)
- **Chain of Draft mode:** Compress each reasoning step to ≤5 words.
  Mark conclusions with ####. Example:
  ```
  Name check. Human term found. Science file. #### VIOLATION: use in-universe name.
  ```

## Step 3: Scan (Present scope for approval first)

List the files to be scanned. Wait for author approval before starting.

Invoke @worldbuilder-physicist for physics scope.
Invoke @worldbuilder-editor for canon/prose scope.

Each agent:
- Reads only the reference files it needs (not the full physics backend)
- Reports findings in pinned format with exact file and line
- Applies metascience diagnostic filters (see /canon-rules)
- Does NOT fix anything during the scan

## Step 4: Triage

Present findings grouped by severity:

- **CONTRADICTION** — two files disagree on a physics rule or fact
- **VIOLATION** — signal name, spelling, or writing standard broken
- **BROKEN-REF** — link to nonexistent file
- **DRIFT** — terminology inconsistency
- **META** — meta-commentary in science file
- **GAP** — missing section downstream files depend on

Author decides: which to fix now, which to defer, which to reject.

## Step 5: Fix (one severity batch at a time)

For approved findings, invoke the appropriate agent:
- Physics contradictions → @worldbuilder-physicist
- Naming/prose violations → @worldbuilder-editor

Each fix:
1. Targets only the approved finding
2. Makes minimal changes
3. Runs /verifying-completion after
4. Presents diff for review before committing

Maximum 2 fix attempts per finding. If still broken after 2 → defer and flag.

## Step 6: Verify and Close

After all approved findings are fixed:
- Run /cross-checking on any terms that were renamed or corrected
- Update GLOSSARY.md if definitions changed
- Append to `meta/LOG.md`:
  ```
  [YYYY-MM-DD] AUDIT: Fixed VIOLATION in [file] — [one-line description]
  ```
- Report: N findings scanned, N fixed, N deferred, N rejected

## Rules

- Never skip scope approval (Step 3) or verification (Step 6)
- Findings without an exact file + line reference are rejected
- Cross-civilization differences are NOT contradictions
- Demand the mechanism: "File A contradicts File B because [specific rule]"
- One severity batch at a time — never mix criticals and moderates
