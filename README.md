# Worldbuilding Codex

A complete Claude Code skill suite for building and maintaining fictional universes with scientific rigor. 19 skills, 5 commands, 3 agents with persistent memory, 6 hooks across 5 lifecycle events, and an epistemological framework adapted from metascience research.

## What It Does

Worldbuilding Codex turns Claude Code from a chatbot into a disciplined worldbuilding engine. It enforces canon consistency, prevents deferral, survives context compaction, and treats your fictional universe with the same structural rigor a codebase deserves.

**The core insight:** The tools that make Claude Code useful for code — persistent file systems, hooks, skills, agents, long autonomous sessions — map almost perfectly to the worldbuilding problem. Code has compilation errors → you have physics contradictions. Code has tests → you have canon audits. Code has architecture docs → you have a foundations layer. Code has linting → you have naming enforcement.

## Architecture

Three layers (the [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern):

| Layer | Purpose | Access |
|-------|---------|--------|
| **Raw Sources** | Immutable reference documents, research papers, canonical lock files | Read-only |
| **The Wiki** | Active worldbuilding directories — civilizations, locations, characters, physics | LLM-maintained |
| **The Schema** | CLAUDE.md, skills, agents, hooks — governance and workflow | Author-controlled |

Three operational tiers ([Trinity Architecture](https://github.com/shanraisshan/claude-code-best-practice)):

| Component | Role | Example |
|-----------|------|---------|
| **Commands** | Orchestrate multi-step workflows | `/ingest`, `/query`, `/lint-wiki`, `/full-audit-canon` |
| **Agents** | Autonomous executors with isolated context | `@worldbuilder-physicist`, `@worldbuilder-editor`, `@worldbuilder-researcher` |
| **Skills** | Progressive-disclosure knowledge loaded on demand | 19 skills across research, writing, auditing, design, planning, verification |

## Installation

```bash
# Clone into your worldbuilding project
git clone https://github.com/YOUR-USERNAME/worldbuilding-codex.git /tmp/wbc

# Copy the .claude directory into your project
cp -r /tmp/wbc/.claude /path/to/your/worldbuilding-project/
cp /tmp/wbc/CLAUDE.md /path/to/your/worldbuilding-project/

# Make hooks executable
chmod +x /path/to/your/worldbuilding-project/.claude/hooks/*.sh

# Clean up
rm -rf /tmp/wbc

# Edit CLAUDE.md to describe YOUR universe
```

Then open Claude Code in your project. The bootstrap hook loads automatically.

## What's Inside

### 6 Hooks (5 Lifecycle Events)

| Hook | Event | Purpose |
|------|-------|---------|
| `bootstrap.md` | SessionStart | Lists available skills, commands, reasoning principles |
| `post-compact-restore.sh` | SessionStart | Restores saved session state after compaction |
| `skill-eval.md` | UserPromptSubmit | Forces skill evaluation before every response |
| `anti-deferral.sh` | PreToolUse | Catches "TODO", "placeholder", "will flesh out" before writing |
| `post-tool-use.sh` | PostToolUse | Lints formatting after every write |
| `pre-compact.md` | PreCompact | Saves session state before context compaction |

### 5 Commands

| Command | Purpose |
|---------|---------|
| `/ingest` | Extract entities from source material → write wiki pages → update indexes |
| `/query` | Answer questions from the wiki → file high-value syntheses as new pages |
| `/lint-wiki` | Health-check: contradictions, orphans, stale claims, ghost entities |
| `/full-audit-canon` | Full audit cycle: scope → scan → triage → fix → verify |
| `/civilization-build` | Full derivation-chain civilization pipeline with enforced checkpoints |

### 19 Skills

**Research:** `researching-papers`, `integrating-research`
**Reading:** `deep-reading`
**Auditing:** `auditing-physics`, `auditing-canon`, `cross-checking`, `auditing-human-assumptions`
**Writing:** `writing-science`, `writing-worldbuilding`
**Design:** `designing-worlds`, `designing-lore`, `deriving-social-systems`
**Extraction:** `extracting-entities`, `compiling-entities`
**Planning:** `interrogating-design`, `planning-worldbuilding`
**Verification:** `verifying-completion`
**Reference:** `canon-rules`, `writing-style`

### 3 Agents with Persistent Memory

| Agent | Role | Memory |
|-------|------|--------|
| `@worldbuilder-physicist` | Physics consistency, real science grounding | Paper mappings, recurring patterns |
| `@worldbuilder-editor` | Writing quality, prose standards | Style corrections, voice notes |
| `@worldbuilder-researcher` | Read-only lookup and compilation | Entity locations, search patterns |

Agents use `memory: project` — the first 200 lines of their MEMORY.md are auto-injected at startup. They learn across sessions.

### Epistemological Framework

Adapted from metascience research (Ioannidis, Gelman, Taleb, Hossenfelder, Pearl, Boyd). Located in `canon-rules/references/`:

- **5 Operating Principles:** Mechanism over association, first-principles over tropes, evidence hierarchy, anti-reductionism, adversarial self-validation
- **6 Metascience Filters:** Sample size, effect size, confirmation bias, flexible analysis, replication, survivorship bias
- **7 Adversarial Protocols:** Red Teaming (5-level escalation), Adversarial Collaboration (Kahneman protocol), Russell Conjugation stripping, Self-Correction Loop, Ensemble Thinking, Active Inference, CADS

### Governance

- **Deny list** protects all `.claude/` files from mid-session edits
- **Anti-deferral hook** catches placeholder language before it gets written
- **Post-tool-use hook** lints formatting deterministically after every write
- **CURRENT_TASK.md** survives context compaction

## Customization

1. **CLAUDE.md** — Fill in your universe description, rules, locked spellings, and key files
2. **WRITING.md** — Run `/writing-style` to generate your prose token system
3. **post-tool-use.sh** — Customize the science directory patterns and spelling checks for your universe
4. **Reference files** — Add your own foundational constraints to `auditing-physics/references/`

## How It Compares

| Feature | This | Superpowers | cc-sentinel | Raw CLAUDE.md |
|---------|------|------------|-------------|---------------|
| Skills | 19 worldbuilding-specific | 14 code-specific | 0 | 0 |
| Commands | 5 (wiki lifecycle + civilization) | 3 (code lifecycle) | 0 | 0 |
| Agents | 3 with persistent memory | 0 | 0 | 0 |
| Hooks | 6 across 5 events | 1 | 3 | 0 |
| Epistemological framework | Yes (named sources) | No | No | No |
| LLM Wiki pattern | Yes (ingest/query/lint) | No | No | No |
| Chain of Draft | Yes (auditing skills) | No | No | No |

## Sources & Inspiration

- [obra/superpowers](https://github.com/obra/superpowers) — Verification, planning, subagent patterns
- [turqoisehex/cc-sentinel](https://github.com/turqoisehex/cc-sentinel) — Anti-deferral, pre-compact state save
- [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) — Trinity Architecture, agent memory
- [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — Three-layer wiki pattern
- [Chain of Draft (arXiv)](https://arxiv.org/abs/2502.18600) — Token-efficient reasoning
- [Anbeeld/WRITING.md](https://github.com/Anbeeld/WRITING.md) — Prose anti-patterns
- [google-labs-code/design.md](https://github.com/nichochar/design.md) — YAML token system (adapted as WRITING.md)
- Ioannidis, Gelman, Taleb, Hossenfelder, Pearl, Boyd — Epistemological framework

## License

MIT
