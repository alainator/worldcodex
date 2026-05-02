# Epistemological Framework — Named Sources & Concepts

Sources: Ioannidis (metascience), Gelman (statistical crisis), Taleb (fat tails,
anti-fragility), Hossenfelder (aesthetic fallacy), Briggs (predictive power),
Glassman/BSI (Broken Science Initiative), Pearl (Ladder of Causation), Boyd
(OODA Loop), Kay (mechanistic reasoning), Turchin (cliodynamics), Alexander
(pattern language), Epstein (simple rules). Adapted for worldbuilding canon
enforcement.

---

## 1. Mechanism Over Association

"This feels consistent" is association. "This is consistent because the metabolic
pathway governs substrate competition" is mechanism. (Kay)

In worldbuilding: a lore element without an unbroken causal chain back to
the foundational axiom is a coincidence that will contradict something later. Every claim
must trace to a specific foundational physics rule.

**Ladder of Causation (Pearl):** Three rungs of causal reasoning:
1. Association — "X correlates with Y" (curve fitting, pattern matching)
2. Intervention — "What happens if we change X?" (active manipulation)
3. Counterfactual — "What would have happened if X hadn't occurred?"

Most worldbuilding operates at Rung 1. Auditing must reach Rung 2-3:
"If we remove this mechanism, what downstream content breaks?"

---

## 2. The Ioannidis Corollaries (Six Conditions for False Results)

Ioannidis mathematically proved that most published research findings are false
when specific structural conditions are present. These conditions map directly
to worldbuilding:

| Corollary | Scientific Failure | Worldbuilding Equivalent |
|-----------|-------------------|--------------------------|
| 1. Small sample | Low statistical power → noise as signal | Checking one file → missing contradictions in the other 76 |
| 2. Small effect | Chasing marginal gains → false positives | Micro-inconsistencies elevated to "violations" when they're perspectival |
| 3. Data dredging | Testing many relationships without pre-selection | Searching for contradictions without a specific hypothesis → finding "issues" by chance |
| 4. Analytical flexibility | Shifting methods until desired result achieved | Reinterpreting a rule until new lore doesn't violate it (the #1 danger) |
| 5. Prejudicial interest | Bias toward desired outcome | Writing lore that confirms what you want, ignoring constraints that prohibit it |
| 6. Competition/heat | Race to publish → abandoning rigor | Rushing to write content without cross-checking → shipping contradictions |

When a worldbuilding task triggers 3+ of these corollaries, the output is
structurally unreliable. Slow down, narrow scope, pre-register constraints.

---

## 3. The Garden of Forking Paths (Gelman)

A researcher believes they're testing a pre-chosen hypothesis, but the
specific analysis they chose was contingent on the data itself. Had the
data been different, they would have taken a different analytical path to
find a different "significant" result.

In worldbuilding: if you would have written the rule differently had the
lore turned out differently — if you adjusted the rule to fit the content
rather than testing the content against the rule — you're in the Garden.

**Detection:** Did any constraint definition change in the same session as
the new lore was written? If yes, that's the Garden of Forking Paths.

---

## 4. The Aesthetic Fallacy (Hossenfelder)

Theoretical physics has made no concrete progress in 50 years because it
substituted empirical predictive power with subjective aesthetic criteria:
"simplicity," "naturalness," "elegance." When the LHC failed to find
predicted particles, physicists moved the goalposts instead of discarding
the theories.

In worldbuilding: "This mechanism is elegant" or "This fits the narrative
beautifully" is the aesthetic fallacy. If it contradicts established physics,
elegance is irrelevant. Mathematical beauty and narrative elegance do not
override mechanistic consistency.

**Test:** Would you accept this mechanism if it were ugly but consistent?
If you'd reject it despite consistency because it "doesn't feel right,"
you're applying aesthetics, not physics.

---

## 5. The Humpty Dumpty Problem (Taleb)

Complex systems cannot be understood by disassembling them, studying isolated
parts, and adding the knowledge back together. When you disassemble a complex
system, the non-linear relationships between the pieces are permanently
destroyed.

In worldbuilding: evaluating a new particle type in isolation, without
tracing its interactions through the full science stack —
is Humpty Dumpty reductionism. The
element might "work" alone but shatter the system when connected.

**Test:** Have you traced this element through every system that connects
to it? If you've only checked the immediate layer, you've broken Humpty
Dumpty.

---

## 6. Predictive Power as Ultimate Metric (Glassman/BSI)

The Broken Science Initiative distills the demarcation between true science
and pseudoscience to a single metric: predictive power. A model is an
inductive argument mapping known facts to unrealized facts. Its validity is
measured solely by how accurately it predicts future, unseen data.

In worldbuilding: a physics rule that can't predict how a new civilization
would interact with the universe's core systems is a decoration, not a rule. Canon rules must
be predictive — given the established physics, you should be able to DERIVE
what a new species' saturation profile would look like, not invent it freely.

**Test:** Can someone unfamiliar with your universe derive the correct
answer from the established rules alone? If the rules don't constrain the
answer, they lack predictive power.

---

## 7. The OODA Loop (Boyd)

Observe → Orient → Decide → Act. Not a linear process — a continuous,
iterative cycle where the Orient phase (synthesis of all mental models)
is the critical step.

In worldbuilding audit:
- **Observe:** Read the files, grep the repo, gather data
- **Orient:** Synthesize against foundational constraints, destroy outdated
  mental models, update priors with new canon decisions
- **Decide:** Formulate a specific hypothesis about what's wrong
- **Act:** Test the hypothesis (don't just assert it)

The key insight: Orient requires actively destroying your current mental
model when new data contradicts it. Don't defend an old interpretation —
update it.

---

## 8. Cliodynamics Pattern (Turchin)

History is not random narrative — it follows quantifiable structural and
demographic cycles. Elite overproduction (too many ambitious actors
competing for limited high-status positions) reliably fragments societies.

In worldbuilding: civilizational rise and fall should follow measurable
patterns (the 5 measurement axes, the 8 archetypes). "The empire fell
because the emperor was weak" is narrative. "The empire fell because
SEP reached 4+ and NSS collapsed to Inversion Spiral" is cliodynamics.

---

## 9. Pattern Language (Alexander)

The most beautiful, functional structures are not built by top-down design
from credentialed architects. They emerge from bottom-up application of
archetypal patterns by people who understand the local context.

In worldbuilding: the repo's structure should follow recurring patterns
(one entity per file, YAML frontmatter, cross-reference links, dependency
order) that anyone can apply. The patterns ARE the architecture. Don't
deviate from them for "creative" reasons.

---

## 10. Simple Rules for Complex Worlds (Epstein)

Complex systems function optimally with simple, foundational axioms rather
than complex regulatory micromanagement. Establish clear "rules of the road"
rather than attempting to control the "composition of the traffic."

In worldbuilding: your foundational axiom is a simple rule. Your CLAUDE.md rules are
simple rules. Don't add complex exception-handling to rules — if a rule
needs exceptions, the rule is wrong. Fix the rule, don't patch around it.

---

## 11. The Irony of the New Orthodoxy (Weinstein Critique)

When a system wholesale rejects institutional consensus, it destroys the
traditional mechanisms for quality control. In the absence of peer review,
a new locus of authority emerges — often the system itself. The crusader
against gatekeeping becomes a gatekeeper.

In worldbuilding: this .claude system must remain self-aware. If the
foundational constraints become so rigid that genuinely good new ideas are
rejected because "the rules say no," the system has become its own orthodoxy.
Intentional ambiguities in your universe are deliberate escape valves — never resolve them.

**Test:** Would a senior Anthropic employee reviewing this system say the
rules have become dogmatic rather than diagnostic?
