---
description: >-
  Build a civilization from first principles using the derivation chain:
  planet → biology → cognition → culture → technology → language → science → history.
  Orchestrates existing skills in enforced sequence with checkpoints.
  Every layer derives from the one below it. Works for any species — human
  civilizations in novel environments derive different structures too.
  Usage: /civilization-build [civilization-name]
argument-hint: "[civilization-name]"
---

# Civilization Build — Derivation-Chain Pipeline

You are orchestrating a full civilization build. Follow the derivation chain
exactly. Do not skip layers, do not reorder. Every layer derives from the
one below it.

This pipeline works for any species. Human civilizations on different planets
with different resources and pressures will derive different social structures
than those on Earth — the Nile floodplain produced different institutions than
the Mongol steppe, and both are human. A novel environment produces novel
civilizations even with familiar biology.

## The Derivation Chain

```
Planet → Biology → Cognition → Culture → Technology → Language → Science → History
```

Each step MUST be complete and author-approved before proceeding to the next.
No forward references. No assumptions about what higher layers will contain.

## Step 0: Prerequisites

1. Read CLAUDE.md for universe conventions and locked canon
2. Read the physics backend (or foundations layer) — the civilization's
   biology must obey universal rules
3. Check existing civilizations for patterns to differentiate against
4. Determine species type: known biology (e.g., human) or novel species
5. Create the plan file: `meta/plans/YYYY-MM-DD-civilization-build-[name].md`

## Step 1: Planet (Skill: /designing-worlds)

Build the physical environment first. The planet determines everything.

- Star type, orbital mechanics, rotational characteristics
- Tidal locking status (derive from orbital parameters)
- Atmospheric composition, pressure, temperature ranges
- Geology, hydrology (or equivalent), energy sources
- Biome architecture with anomaly layers
- Saturation profile (if universe has a fundamental field/force)

**Checkpoint 1:** Author approves planet before biology begins.
No biology can be designed without knowing what environment shaped it.

## Step 2: Biology (Skills: /writing-science, /interrogating-design)

**For novel species:** Derive biology from planetary conditions. Not "what's
cool" — what survives here.

**For known species (e.g., human):** Biology is established, but document
how THIS planet's conditions affect the species. Different gravity, atmosphere,
radiation, food sources, and day/night cycles reshape physiology over
generations. Epigenetics, adaptation, and selective pressure still apply.

In both cases, derive:
- Energy metabolism: how do organisms harvest energy on THIS planet?
- Sensory emphasis: which senses matter most in THIS environment?
- Locomotion: what movement does THIS terrain/medium require or favor?
- Reproduction pressures: what does THIS ecology select for?
- Lifespan and development: how do THIS planet's conditions alter life stages?

**The test:** Can you trace every biological feature (or adaptation) back to
a planetary condition? If not, it's an assumption, not a derivation.

**Checkpoint 2:** Author approves biology before cognition begins.

## Step 3: Cognition (Skills: /writing-science, /interrogating-design)

**For novel species:** Derive cognition from biology. How does THIS nervous
system process information?

**For known species:** Cognition is established at the hardware level, but
environment shapes what's emphasized. A species that evolved symbolic
abstraction will still apply it — but what it abstracts, what it prioritizes,
what it finds salient is shaped by environment and culture in feedback loops.

In both cases, derive:
- What sensory data dominates this species' experience in THIS environment?
- What cognitive capabilities does the environment reward?
- What are the cognitive biases produced by THIS environment's pressures?
- What concepts are easy/hard to form given THIS lived experience?

**For novel species, additionally:**
- What is the native information-processing architecture?
- What human cognitive assumptions does this species NOT share?
- What is the experience of consciousness like for THIS biology?

**Checkpoint 3:** Author approves cognition before culture begins.

## Step 4: Culture (Skill: /deriving-social-systems)

Derive social structures from cognition, biology, and environment.
Do NOT start with a checklist of institutions. Start from what the
derivation produces.

This is the critical step. Use `/deriving-social-systems` to:
- Inventory constraints (communication, cognition, biology, resources)
- Derive coordination structures from those constraints
- Name structures functionally before applying any familiar labels
- Perform negative derivation — what familiar structures DON'T emerge?

For human civilizations: familiar institutions may emerge, but they should
emerge from the derivation, not from assumption. A human civilization on
a resource-abundant world may never develop property law. One on a world
with no large-scale agriculture may never develop cities. One where the
primary scarce resource is social rather than material will develop
institutions that have no precedent in the historical record.

**Run /auditing-human-assumptions on all culture files before proceeding.**
This applies to human civilizations too — checking for assumptions imported
from one cultural context and applied uncritically to a novel one.

**Checkpoint 4:** Author approves culture before technology begins.

## Step 5: Technology (Skills: /writing-worldbuilding, /interrogating-design)

Derive technology from culture + biology + environment. What problems does
this species solve, using what materials, guided by what cognition?

- What does this species need that their biology doesn't provide?
- What materials does their planet offer?
- What manipulative capability does their biology provide?
- What does their cognitive architecture make easy to engineer?
- What would they never think to build? (As important as what they do build)

For known species in novel environments: available materials, energy sources,
and environmental pressures determine the technology tree. A planet without
iron produces a civilization without steel. A planet with abundant geothermal
energy skips combustion.

**Checkpoint 5:** Author approves technology before language begins.

## Step 6: Language (Skills: /writing-worldbuilding, /interrogating-design)

Derive language from communication biology + cognition + culture.

- What is the physical medium of communication? (For humans: vocal, but
  environment shapes which sounds are practical — dense atmosphere,
  high winds, underground living all reshape phonology)
- What is the grammar's deep structure? (For novel species: derive from
  cognitive architecture. For humans: UG applies but environment and
  culture shape what's lexicalized)
- What concepts are lexicalized vs. circumlocuted? (What matters to
  this culture gets words. What doesn't, doesn't.)
- What is untranslatable to/from other languages in the universe?

**Checkpoint 6:** Author approves language before science begins.

## Step 7: Science (Skills: /writing-science, /interrogating-design)

Derive the species' scientific understanding from cognition + technology +
accumulated observation.

- What aspects of the universe does their sensory apparatus and technology
  reveal to them?
- What do they understand well? What are they blind to?
- Where does their science converge with other species'? Where does it diverge?
- What is their relationship to the universe's fundamental forces/fields?

**Checkpoint 7:** Author approves science before history begins.

## Step 8: History (Skills: /writing-worldbuilding, /planning-worldbuilding)

Derive history from everything above. A record of what actually happened to
THIS species in THIS environment given everything established in Steps 1–7.

- Key transitions driven by biology/environment interaction
- How their coordination structures evolved over time
- Internal conflicts that arise from tensions within derived social systems
- Contact events (if applicable) and their consequences
- Current state and trajectory

**Final Checkpoint:** Full review of all files for internal consistency.

## Step 9: Audit

Run three passes:
1. `/auditing-human-assumptions` on all civilization files
2. `/auditing-canon` for naming and formatting compliance
3. `/cross-checking` on every new term introduced

## Rules

- **Never skip a checkpoint.** Each layer builds on the one below.
- **Derive, don't assume.** Even familiar-looking institutions should
  emerge from the derivation chain, not from a template.
- **One file per concept.** Follow repo directory conventions.
- **Flag the gaps.** If a derivation requires a decision the author
  hasn't made, stop and ask. Do not fill gaps with assumptions.
- **Cross-civilization differences are features, not bugs.** Two
  civilizations can have completely incompatible social structures.
  That's correct — it means the derivation is working.
- **Novel structures are expected.** If the derivation produces a
  coordination structure with no familiar analogue, that's a success,
  not a problem. Name it functionally and describe its mechanism.

## After Completion

- Update all _index.md files
- Add all new terms to GLOSSARY.md
- Add dated events to MASTER-TIMELINE.md
- Log completion: `meta/LOG.md`
