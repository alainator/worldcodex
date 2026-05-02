You have a worldbuilding skill suite loaded.

COMMANDS (orchestrated multi-step workflows — user types /command):
  /ingest — extract entities, write wiki pages, update indexes from new source material
  /query — answer complex questions, file high-value syntheses back as wiki pages
  /lint-wiki — health-check the wiki: contradictions, orphans, stale claims, missing pages
  /full-audit-canon — full canon audit cycle: scope → scan → triage → fix → verify
  /civilization-build — full derivation-chain civilization pipeline with enforced checkpoints

SKILLS (progressive disclosure — loaded on demand):
  RESEARCH: /researching-papers (find/download papers), /integrating-research (map to canon formalism)
  READING: /deep-reading (content-map a file; structure, entities, claims)
  AUDITING: /auditing-physics (cross-layer science contradictions), /auditing-canon (names, frontmatter, prose), /cross-checking (one term everywhere), /auditing-human-assumptions (imported assumptions in any civ)
  WRITING: /writing-science (academic prose science files), /writing-worldbuilding (civilizations, characters, locations)
  DESIGN: /designing-worlds (biomes, planets, climate), /designing-lore (myths, legends, eras, relics), /deriving-social-systems (derive coordination from biology/environment)
  EXTRACTION: /extracting-entities (pull entities from source docs), /compiling-entities (everything about one entity)
  PLANNING: /interrogating-design (stress-test a decision), /planning-worldbuilding (decompose large tasks)
  VERIFICATION: /verifying-completion (mandatory completion checklist before declaring done)
  REFERENCE: /canon-rules (epistemology, metascience filters, anti-patterns), /writing-style (WRITING.md generation)

AGENTS: @worldbuilder-physicist (physics consistency, real science grounding), @worldbuilder-researcher (read-only lookup), @worldbuilder-editor (writing quality, prose standards). All agents have persistent memory at .claude/agent-memory/ — they learn across sessions.

KEY TOOLS: tools/research-tool.py (paper search/download across arXiv, Crossref, PMC, Semantic Scholar, Open Library, SEP)

REASONING PRINCIPLES (apply to every task):
  Mechanism over association — state the causal chain or it's not proven.
  First-principles over tropes — derive from established physics/biology, not genre convention.
  Evidence hierarchy — canon source > derived lore page > cross-referenced inference > "it feels right."
  Anti-reductionism — trace implications through every connected system before accepting a change.
  Adversarial self-validation — "what existing canon contradicts this? what edge case breaks it?"

Read CLAUDE.md before every task. Canon consistency is the #1 priority.
Use /commands for multi-step workflows. Use skills for single-phase work.

LONG SESSIONS: Keep .claude/CURRENT_TASK.md updated with current focus, canon decisions, and next concrete step. Pre-compact hook saves state. Post-compact hook restores it.

PROTECTED FILES (cannot be written): CLAUDE.md, settings.json, agents/*, skills/*, hooks/*. Edit outside Claude Code.
