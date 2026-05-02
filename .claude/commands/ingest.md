---
description: >-
  Ingest new source material into the worldbuilding wiki. Extracts entities,
  writes or updates wiki pages, and updates all cross-linked indexes.
  Usage: /ingest [source file or directory]
argument-hint: "[source file path or directory]"
---

# Ingest — Wiki Ingestion Workflow

You are processing new source material into the worldbuilding wiki.
A single source may touch 10-20 wiki pages. Follow this sequence exactly.

## Step 1: Read the Source Fully

Read the ENTIRE source document — no skimming, no 200-line cutoff.
If it's a .docx or .pdf, use extract-text first.
Note the source path for frontmatter tagging.

## Step 2: Entity Extraction

List every distinct entity in the source that should have its own wiki page:

| Entity | Type | Exists? | Action |
|--------|------|---------|--------|
| [name] | character/location/species/technology/event/concept | yes/no/partial | create/update/skip |

Pause here. Present the extraction plan before writing anything.

## Step 3: Write/Update Pages (after approval)

For each NEW entity:
1. Determine target directory from type (see CLAUDE.md)
2. Write full page with YAML frontmatter (title, tags, status: draft, source)
3. Add cross-references to related entities

For each INCOMPLETE entity (page exists but missing this content):
1. Read the existing page fully
2. Add the new content without overwriting existing content
3. Update cross-references

## Step 4: Update Indexes

For every page created or updated:
- Add entry to the relevant `_index.md`
- Add new terms to `GLOSSARY.md`
- Add new dated events to `MASTER-TIMELINE.md`
- Update any existing pages that cross-reference this entity

## Step 5: Cross-Link Pass

Grep for the new entity names across the full repo.
For every existing page that mentions a new entity but doesn't link to it:
add the link.

## Step 6: Verification

Run /verifying-completion on all created/modified files before declaring done.

## Step 7: Update LOG.md

Append an entry to `meta/LOG.md` for every file created or modified:

```
[YYYY-MM-DD] INGEST: Created characters/elder-council.md from _source/chromat-notes.docx
[YYYY-MM-DD] INGEST: Updated GLOSSARY.md — added "Elder Council"
[YYYY-MM-DD] INGEST: Updated civilizations/chromat/_index.md — added elder-council link
```

LOG.md is append-only. Never edit or delete existing entries. This allows
incoming sessions and subagents to instantly understand the recent evolution
of the lore base without reading every file.

## Rules

- Do NOT summarize source content — preserve faithfully
- Do NOT merge two entities into one page
- Flag contradictions with `<!-- REVIEW: conflicts with [file] -->`
- Present entity extraction plan before writing anything
- Status: draft on all new pages — author promotes to canon

## What This Replaces

Manual extraction sessions where new source material sits unprocessed.
Every source that enters the project should go through /ingest.
