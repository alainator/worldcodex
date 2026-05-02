# Metascience Diagnostic Filters — Worldbuilding Audit

Apply these six filters during triage to separate real canon violations
from noise. See /canon-rules skill for the full epistemological framework.

## Filter 1: Sample Size
Was the full repo checked, or just the primary source?
A rule consistent in physics/ may conflict in civilizations/.
Reject: findings cleared without cross-repo verification.

## Filter 2: Effect Size
Is the fix complexity proportional to the finding severity?
A critical contradiction justifies extensive edits.
A low-priority drift finding does not justify 20-file cascades.

## Filter 3: Confirmation Bias
Was the new content designed to fit the constraints, or were the
constraints quietly reinterpreted to fit the content?
Check whether any foundational rule was loosened to accommodate
the new idea. If yes, flag — don't clear.

## Filter 4: Flexible Analysis
Did any rule definition change in the same session as the new lore?
Reinterpreting a stable foundational rule to permit new content =
flexible analysis. Reject without explicit author approval.

## Filter 5: Replication
Does the rule hold across ALL civilizations subject to it?
"Works for one civilization" is not sufficient for a universal physics rule.
Verify cross-civilization unless the rule is explicitly local.

## Filter 6: Survivorship Bias
What files reference this concept that WEREN'T checked?
Use grep to find every mention before declaring any rule consistent.
What's absent from the check is the danger zone.

## How to Apply

For every finding, before approving a fix:
1. Filter 1: full-repo grep done?
2. Filter 2: fix complexity proportional?
3. Filter 4: any rule definition changed this session?
4. Filter 5: cross-civilization check done (if universal rule)?
5. Filter 6: every mentioning file checked?

Findings failing these filters: downgrade severity or reject.
Findings passing: approve with exact file+line in the report.
