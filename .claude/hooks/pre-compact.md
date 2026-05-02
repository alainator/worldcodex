⚠  CONTEXT COMPACTION IMMINENT

Write current session state to `.claude/CURRENT_TASK.md` BEFORE doing anything else.
After compaction, most conversation history will be lost. The session-start hook
injects this file so the next session can resume without re-reading every file.

If CURRENT_TASK.md already exists, update it in place.

```markdown
# Current Worldbuilding Session State

## What I was working on
[Which world, region, character, system, civilization, or storyline — one line]

## Phase
[Which stage — e.g., "Designing elven governance, biology section complete"]

## Canon documents modified this session
[Every file created or edited, with one-line description of the change]

## Canon decisions made
[Names established, relationships defined, physics rules formalized, events set,
any locked canon added — be specific enough that a fresh session can act on these]

## Open questions
[Unresolved decisions that need answers before continuing]

## Next concrete step
[The literal next action — not "continue X" but the specific task]

## Context that must not be lost
[Anything specific to this session not captured in the lore files — author preferences
expressed, approaches rejected, constraints discussed, rationale for decisions]
```

Write this file NOW.
