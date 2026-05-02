# WRITING.md Template

Fill YAML tokens with your universe's conventions.

````markdown
---
name: "[Your Universe] Writing System"
description: "[One-line description of your prose standards]"

document-types:
  science:
    dirs: ["physics", "chemistry", "biology"]
    voice: third-person academic
    tense-laws: present
    tense-observations: past
  worldbuilding:
    dirs: ["civilizations", "locations", "characters", "events"]
    voice: engaged analytical
    tense: "past (historical), present (descriptions)"
  narrative:
    dirs: ["narrative", "stories"]
    voice: authorial

citations:
  format: "inline parenthetical"
  style: "(Author, Year)"
  section: "## References"
  annotation: "one-sentence per entry"

equations:
  notation: LaTeX
  display: "blank line above and below $$ blocks"

forbidden-words:
  - "obviously"
  - "clearly"
  - "simply"
  - "basically"
  - "interestingly"
  - "it should be noted"

forbidden-phrases:
  - "This section establishes"
  - "This document addresses"
  - "The following section"
  - "As we can see"

locked-spellings:
  # Add your universe's proper nouns here
  # example: "Kha'zul (never Khazul or Kha-zul)"

structure:
  frontmatter: required
  frontmatter-fields: [title, tags, status]
  status-values: [canon, draft, needs-review, superseded]
  cross-references: relative markdown paths
  contradiction-flag: "<!-- REVIEW: potential conflict with [file] -->"
---

## Science Files

Academic prose. Every subsection explains WHY, not just WHAT. No bullet-list
science. No meta-commentary. In-universe terminology mandatory.

## Worldbuilding Files

Engaged analytical voice for civilizations and locations. Human-readable
names appropriate here.

## Anti-Patterns (Avoid Everywhere)

- Replace polished generality with concrete anchors
- Guard against fake specificity — numbers need support or get cut
- Break templated patterns: repeated cadence, hidden lists, generic signposts
- Self-audit workflow: draft → audit against rules → rewrite
````
