---
description: >-
  Answer a complex question by searching the wiki, synthesizing across files,
  and filing the answer back as a new wiki page if it's worth keeping.
  Usage: /query [question]
argument-hint: "[your question about the worldbuilding universe]"
---

# Query — Wiki Query with Compounding

You are answering a question by searching the worldbuilding wiki and
filing the answer back if it produces a high-value synthesis.

This is the third LLM Wiki operation (alongside /ingest and /lint-wiki).
The key insight: if an answer required synthesizing 5+ files, that synthesis
should become a permanent wiki page so it compounds — never re-derived
from scratch.

## Step 1: Search the Wiki

1. Check GLOSSARY.md for the key terms in the question
2. Check relevant `_index.md` files for file paths
3. `grep -r` for specific terms across the repo
4. Read the full content of every relevant file (not just headers)
5. Check `_source/` for unconverted material that might be relevant

## Step 2: Synthesize the Answer

Answer the question with direct citations to specific files and sections.
Format: "According to [filename], [claim]."

If files disagree: report the disagreement explicitly with both sources.
If the answer isn't in the wiki: say so — don't invent.

## Step 3: Evaluate for Filing

After answering, evaluate whether this answer should become a wiki page:

**File it if:**
- The answer synthesized 3+ source files
- The answer resolved an ambiguity or connected concepts not previously linked
- The answer would be useful to someone asking a similar question later
- The answer revealed a gap, contradiction, or missing cross-reference

**Don't file if:**
- The answer was a simple lookup from one file
- The answer is purely about session logistics or process
- The content already exists as a single page

## Step 4: File the Answer (if warranted)

Create a new synthesis page at the appropriate location:

```markdown
---
title: "[Synthesis Topic]"
tags: [synthesis, relevant-tags]
status: draft
source: "Synthesized from [list of source files]"
query: "[The original question that prompted this synthesis]"
---

# [Synthesis Topic]

[The synthesized answer, with cross-references to source files]

## Sources Consulted
[List of every file read to produce this answer]
```

After filing:
- Add the new page to the relevant `_index.md`
- Add new terms to GLOSSARY.md if the synthesis introduced any
- Append to `meta/LOG.md`:
  ```
  [YYYY-MM-DD] QUERY: Created [path] — synthesized from [N] sources
  ```

## Step 5: Report Back

Tell the user:
1. The answer
2. Whether it was filed (and where)
3. Any gaps or contradictions discovered during the search

## Rules

- Never invent content that isn't in the wiki
- Cite specific files, not vague references
- Filing is optional — only file genuinely useful syntheses
- Filed pages get status: draft — author promotes to canon
