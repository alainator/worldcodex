# CLAUDE.md — Worldbuilding Repository

<!-- Replace this line with: one sentence describing your universe -->

## Rules (priority: canon > mechanistic coherence > voice/tone > minimal changes > style)

Evidence hierarchy: canon source > derived lore page > cross-referenced inference > "it feels right."
Mechanism over association: if you can't state the causal chain back to foundational physics/biology, it's not proven.

1. Your foundational axiom governs everything — every mechanism must reduce to it
2. Use in-universe terminology in science files, human-readable names only in narrative/applied content
3. One entity per file, kebab-case filenames, YAML frontmatter (title, tags, status)
4. Science prose: academic third-person, present tense for laws, past tense for observations, no bullet-list physics, no meta-commentary
5. Cross-link with relative markdown paths; flag contradictions with `<!-- REVIEW: -->`
6. Dependency order: foundations → physics → chemistry → biology → applied → civilizations
7. In-universe cited science is canon science — no disclaimers, no "inspired by"
8. Do NOT commit, push, or overwrite canon files without explicit author approval
9. Cross-civilization differences are NOT contradictions — different species interpret differently
10. After writing: update _index.md, GLOSSARY.md, MASTER-TIMELINE.md
11. NEVER write "TODO", "placeholder", "will flesh out", or deferral language without explicit user approval — deferred worldbuilding tends to never get done
12. During long sessions, keep `.claude/CURRENT_TASK.md` updated with current focus, canon decisions made, and next concrete step

## Locked Spellings

<!-- Add your universe's proper nouns here, one per line -->

## Key Files

<!-- Suggested structure — create these files for your universe: -->
- `reference/core-canon-locked.md` — Locked canon decisions (READ ONLY)
- `GLOSSARY.md` — Term definitions
- `MASTER-TIMELINE.md` — Chronological event log
<!-- Add your universe's key reference files here -->

## Change Control

Only the author pushes changes. Claude Code proposes via clearly
marked suggestions. Never commit, push, or overwrite canon-status
files without explicit author approval.
