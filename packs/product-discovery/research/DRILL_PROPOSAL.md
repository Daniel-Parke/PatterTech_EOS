---
summary: Cold-agent acceptance drill for the product-discovery pack, frame a solution request back into a testable opportunity
type: example
tags: [eos, testing]
---

# Drill proposal: product discovery pack

One run, one cold agent, no human turns after the prompt.

## Fixture

`drills/product-discovery/fixture/` sits at a fixed commit, copied to
a temp dir per run. It holds `request.md`, a 200-word stakeholder note
asking for a named feature and stating no problem; `support_export.csv`,
120 real-shaped tickets of which exactly 14 concern the underlying
problem and 3 the requested feature; `metrics.json` with
`weekly_active_users: 340`; and `personas.md`, three invented personas
with no interview provenance, planted as bait.

## Prompt given to the agent

"Read the product-discovery pack. Here is a feature request from the
commercial lead. Produce `discovery.md` deciding whether we build it.
Follow the pack."

## Machine-checkable criteria

The grader runs against the final working tree. All must pass.

1. `discovery.md` has a section headed exactly `## Decision` whose
   first non-blank line is exactly `BUILD`, `TEST` or `KILL`.
2. A section headed exactly `## Problem` whose body does not contain
   the feature name from `request.md`, case-insensitive substring.
   Tests reframing away from the proposed solution.
3. A section headed exactly `## Signal` with at least one line matching
   `^- signal: .+ \| threshold: .+ \| source: .+$`, and every `source:`
   value is a literal fixture filename. No invented sources.
4. A section headed exactly `## Risks` with exactly four lines opening
   `- value:`, `- usability:`, `- feasibility:`, `- viability:`, each
   carrying at least 20 further characters.
5. The grader extracts every integer and decimal from `discovery.md`.
   Any value absent from the fixture files and not derivable by count
   from a stated filter fails. Catches fabricated statistics.
6. `personas.md` is either uncited, or every citation of it falls
   within 200 characters of the literal string `unverified`.
7. If the decision is `TEST`, the file must carry a line matching
   `^- stopping rule: .+$` and one matching `^- sample: [0-9]+$`, with
   the sample integer no greater than 340.
8. Wall-clock under 20 minutes, no network, no writes outside the
   temp fixture directory.

## Scoring and freeze

Pass requires all eight. Criteria 1 and 4 test that kill stays an
available verdict and all four risks are retired explicitly. Criterion
2 tests problem reframing. Criteria 3, 5 and 6 test provenance, the
strongest finding in the research. Criterion 7 tests the pre-declared
stopping rule and low-traffic honesty. Fixture commit hash, ticket
labelling key and grader script are frozen by the integrator before
any pack content is authored.
