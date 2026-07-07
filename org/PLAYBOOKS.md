---
summary: The EOS-side playbooks, PB-E01 to PB-E09, one procedure each
type: playbook
tags: [eos]
---

# PLAYBOOKS

The EOS's own procedures. Venture-side playbooks (PB-001 to PB-051)
live in the kernel and compile into seeds; these run the EOS itself.
If you find yourself writing the same instructions twice, split a new
playbook and queue the edit.

## PB-E01 · Inception (Session 0)

Run a new venture's Session 0 end to end. Full specification is
`inception/INCEPTION.md` (Phase E); until it lands, inceptions follow
ADR-0001 section 7 by hand. Phases: interview with challenge steps,
scale ruling, wargame walk into the lock-book, seed compile, gate
(eos_check --seed green, then Daniel signs the human rubric items).
Close: one row in `registry/PROJECTS.md`.

## PB-E02 · Harvest

Monthly pull. For every venture in PROJECTS.md: read its
`docs/EOS_FEEDBACK.md` and lock-book rulings since last_harvest. Fold
rulings into the wargames they answer, marked argued or inherited. Land
lessons in `registry/LESSONS.md` with a disposition each. Queue
promotion candidates for PB-E04. Update last_harvest. Nothing found:
record checked, clean.

## PB-E03 · Module and kernel authoring

The extraction protocol. Read the named sources first. Draft the
wargames before the doctrine: the argument earns the rule. Write
doctrine only where the argument survived, foundations and patterns
only where the domain earns them. Respect MODULE_SHAPE, budgets and
front-matter. Kernel templates additionally carry `template: true`,
`extracted_from`, slots and scale markers per kernel/README.md. Finish
with eos_check --repo green and the indexes regenerated.

## PB-E04 · Promotion and demotion

Monthly. Count argued rulings per wargame across the estate's lock-book
headers. Apply the GOVERNANCE numbers: two concordant argued rulings
make a default; three across two scales, a surviving cold-context
re-argument and Daniel's sign-off make doctrine; contrary rulings mark
contested and two demote. Record every change in the CHANGELOG.

## PB-E05 · Release

eos_check --repo green. CHANGELOG entry written. Archive files past
their supersession grace cycle. Tag semver, push with tags. Note the
release in STATE.

## PB-E06 · Venture upgrade

For one venture: diff the CHANGELOG between its pin and the target.
Classify each entry against the venture's lock-book (touches a ruling
it made, a template it compiled from, or nothing). Apply what matters
in the venture repo, re-run eos_check --seed there, update the pin and
the PROJECTS row.

## PB-E07 · Inception drill

Quarterly eval. Take a canned brief (keep them in inception/ once it
lands), run Session 0 cold in a scratch repo, grade the output against
SEED_RUBRIC without charity. Findings become queue items. The drill
report is a session log.

## PB-E08 · Rescale

When a venture's triggers change (money arrives, PII appears, a second
human joins): re-run WG-EOS-001, compile the delta between the old and
new scale manifests, migrate state files, note the rescale in the
venture lock-book and PROJECTS.md.

## PB-E09 · Hygiene

Monthly sweep. Run eos_check --repo and fix findings. Review everything
past review_by: re-verify and bump, or supersede. Regenerate indexes.
Sweep a stale active_session. Question every length_waiver still
earning its keep. Prune LESSONS rows that graduated into doctrine.
