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

The PB-E series below is governance work: harvest, review, release,
upgrade. Ordinary development on this repository runs the mode
procedures in the next section. Those were missing entirely until
2026-08-08: `AGENTS.md` routes a session here for the playbook its task
names, and this file held ten governance procedures and no express,
standard or spike lane, so the commonest work in the repo had no
written process at all.

## The mode procedures

One per execution mode, matching
`kernel/templates/org/PLAYBOOKS.tpl.md` so a venture and the EOS run the
same shapes. The mode comes from the router's ruling, never from choice.

### express (R0)

1. Confirm the ruling is R0 and the free band covers every decision in
   sight. A durable decision converts the run to standard, now.
2. Do the work in one run. Targeted checks only: the affected tests,
   plus `python -m tools.eos check --repo` when front-matter moved.
3. Commit with a message that is the whole record. No task record, no
   log, no derived-view regeneration. If the integrator must regenerate
   an index, say so in the message and hand it over.

### standard (R1)

1. Take or open the task record under `org/tasks/`. Declare the facts
   and let the router rule; the ruling is stored on the record and read
   from there, never recomputed per session.
2. Implement with tests and documentation in the same change.
3. Run the affected tests, widening on low confidence.
4. Close: re-route against the actual diff, which resolves upward only,
   then merge on green. The task joins the sampled-review pool unless
   the routing reasons demand independent review.

### exploration (spike)

1. Enter with the question, the timebox and the budget on the record.
   Branch `spike/T-####`. Nothing on that branch merges; the exit is
   discard or harden.
2. Explore freely. Checks may wait, and nothing merges.
3. Exit on answer or timebox: discard, or harden into a standard run.

### high-assurance (R2 and R3)

1. Invariants and a rollback plan on the record before implementation.
2. The acceptance oracle is authored first, hashed and frozen. At R2 it
   may be written in the same session provided no implementation exists
   in context yet; at R3 it is a separate author
   (`packs/delivery-testing/guides/WG-DEL-006-oracle-independence.md`).
3. Independent review, and a person for anything irreversible. The
   guard rules every consequential action at the moment it runs.
4. Amendments to a frozen oracle are append-only, authored by someone
   other than the implementer, and their rate is reviewed at retro.

### parallel

A wrapper, not a mode. The integrator assigns and commits claims before
any lane is dispatched; each lane carries its own mode and its own
claim, and lanes never acquire or mutate one. A session not named in
`org/claims.json` is refused by `task new` and `task update`. Only the
integrator regenerates shared indexes. Every lane branch is merged and
deleted before its phase closes.

## PB-E01 · Inception (Session 0)

Run a new venture's Session 0 end to end per `inception/INCEPTION.md`,
which is the v2 walk, phases A to E. Gate: seed checks green, then Daniel signs the
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
rules change only through an ADR citing the changed source.

## PB-E05 · Release

Full check run green, semantic series included. CHANGELOG entry
written; required drills and benchmark gates satisfied; files past
their supersession grace archived. Tag semver, push with tags. The
policy's guard.validated may say true only while a current adapter
validation report from the bypass suite is committed; without one
every guarded class stays manual-only. The Claude Code mapping carries
one, dated 2026-08-03, so check it is still current rather than
assuming it.

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
evidence. Sample the standing tier exceptions recorded in
org/decisions/ and flag any past its expiry date.

## PB-E10 · Experiment sweep

Monthly, beside the promotion review: read each lifecycle
experimental item against its recorded hypothesis; keep with
evidence, promote through the graded path, or revert. Set at most one
new deliberate experiment.
