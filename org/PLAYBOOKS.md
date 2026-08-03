---
summary: The EOS-side playbooks, PB-E01 to PB-E10, one v2 procedure each
type: org
tags: [eos]
---

# PLAYBOOKS

The EOS's own procedures under the v2 kernel. Venture-side procedure
templates live in `kernel/templates/org/PLAYBOOKS.tpl.md` and compile
into seeds; these run the EOS itself. Every session starts from the
router's ruling against `org/policy.json`, records work in an
org/tasks/ record where the mode requires one, and leaves derived
views to the integrator.

## PB-E01 · Inception (Session 0)

Run a new venture's Session 0 end to end per `inception/INCEPTION.md`.
The v2 rewrite lands in phase P5; until then the v1 walk applies,
compiling v2 seeds. Gate: seed checks green, then Daniel signs the
human rubric items. Close: one row in `registry/PROJECTS.md`.

## PB-E02 · Harvest

Monthly pull. For every governed venture in PROJECTS: read its
feedback file and lock-book rulings since last_run. Fold argued
rulings into the packs and guides that own the decision, as graded
evidence with one ledger row per source. Queue promotion candidates
for PB-E04. Update last_run in org/cadence.json. Nothing found:
record checked, clean.

## PB-E03 · Pack and kernel authoring

The graded evidence path replaces wargame-first. Start with a fresh
research batch, one evidence row per source with licence and access
date. Argue guides before any doctrine line cites them; write binding
rules only where basis and evidence grade earn them. Respect the pack
definition of done and the per-kind metadata minima. Finish with
checks green and the derived views regenerated.

## PB-E04 · Promotion review

Monthly sampling under the graded change path: sample five governance
items (experimental edits, exceptions, contested rules); expire
experiments past their 90-day window. Promotion: default to binding
candidate on two argued rulings from two ventures, or one plus a
source with basis standard or evidence grade controlled; binding
requires an ADR and Daniel. Contrary rulings against binding rules
trigger review, never automatic demotion; law and standard based
rules change only through RFC or ADR citing the changed source.

## PB-E05 · Release

Full check run green, semantic series included. CHANGELOG entry
written; required drills and benchmark gates satisfied; files past
their supersession grace archived. Tag semver, push with tags. The
policy's guard.validated may say true only while a current adapter
validation report from the bypass suite is committed (it lands in
P4); without one every guarded class stays manual-only.

## PB-E06 · Venture upgrade

For one venture: diff the CHANGELOG between its pin and the target.
Classify each entry against the venture's lock-book and records.
Apply what matters in the venture repo, re-run the seed checks there,
update the pin and the PROJECTS row.

## PB-E07 · Inception drill

Quarterly eval. Take a canned brief from inception/briefs/, run
Session 0 cold in a scratch repo, grade the output against
SEED_RUBRIC without charity. Findings become task records.

## PB-E08 · Rescale

When a venture's triggers change (money arrives, PII appears, a
second human joins): re-rule the scale, compile the delta between the
old and new seed manifests, migrate state files, note the rescale in
the venture lock-book and PROJECTS.

## PB-E09 · Hygiene

Monthly sweep: run python -m tools.eos check --repo with the semantic
and freshness series and fix findings. Re-verify or supersede
everything past review. Regenerate derived views. Close or discard
dead task records; recover expired claims only with liveness
evidence. Sample the exception ledger and flag expired standing
exceptions.

## PB-E10 · Experiment sweep

Monthly, beside the promotion review: read each lifecycle
experimental item against its recorded hypothesis; keep with
evidence, promote through the graded path, or revert. Set at most one
new deliberate experiment.
