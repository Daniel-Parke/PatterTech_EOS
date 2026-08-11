---
summary: The EOS-side playbooks, PB-E01 to PB-E12, the mode procedures and the monthly pass
type: org
tags: [eos]
---

# PLAYBOOKS

The EOS's own procedures under the v2 kernel. Venture-side procedure
templates live in `kernel/templates/org/PLAYBOOKS.tpl.md` and compile
into seeds; these run the EOS itself. Every session starts from the
router's ruling against `org/policy.json`, opens a task record where the
work is gate-bearing, and leaves derived views to the integrator.

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

1. Open a task record under `org/tasks/` if the work is gate-bearing:
   anything touching the protected set, and anything a reviewer must
   later be able to find. Otherwise the commit message is the record
   (ADR-0008). Where there is a record, declare the facts and let the
   router rule; the ruling is stored on the record and read from there,
   never recomputed per session.
2. Implement with tests and documentation in the same change.
3. Run the affected tests, widening on low confidence.
4. Close: re-route against the actual diff, which resolves upward only.
   A diff that rules R2 or above needs a record, so open one then if you
   did not open one at the start. Merge on green. The task joins the
   sampled-review pool unless the routing reasons demand independent
   review.

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

## The monthly pass

Four procedures used to hold four monthly cadence rows. They run as one
sitting now, four sections in this order (ADR-0008).

1. **Harvest**, PB-E02. New material comes in first.
2. **Promotion review**, PB-E04. It reads what the harvest queued.
3. **Experiment sweep**, PB-E10. It sits beside the promotion review and
   takes the same judgement.
4. **Hygiene**, PB-E09. Last, because it regenerates the derived views
   after the first three have moved things.

Close the pass by updating its `last_run` in `org/cadence.json`. A
section that found nothing says checked and clean in one line. A section
that was skipped is a finding, and it records why it was skipped.

## What is not on a calendar

Everything else fires on an event, and each procedure names its own
event. The inception drill and the projects review
used to hold quarterly rows and neither had fired once since v1. A
calendar trigger nobody honours is not a control, so both were
re-pointed at the events that warrant them (ADR-0008). The study
workflow and the venture check-in have never been on a calendar: one
starts when Daniel points at a source, the other when a venture asks.

## PB-E01 · Inception (Session 0)

Run a new venture's Session 0 end to end per `inception/INCEPTION.md`,
which is the v2 walk, phases A to E. Gate: seed checks green, then Daniel signs the
human rubric items. Close: one row in `registry/PROJECTS.md`.

## PB-E02 · Harvest

Section one of the monthly pass. For every governed venture in
`registry/PROJECTS.md`: read its feedback file and its lock-book rulings
since the last pass. Fold argued rulings into the packs and guides that
own the decision, as graded evidence with one ledger row per source.
Queue promotion candidates for section two.

The procedure is unchanged. What changed is where it records. A folded
ruling appends a row to `registry/lessons.json` with origin harvest,
naming the venture it came from. `registry/LESSONS.md` is the derived
view of that file and is never hand-edited. The row shape is fixed by
the ledger's schema, not restated here; a harvest row carries no
evidence id and no lens contract, which is what separates it from a
study row.

The read is a read and nothing else. It opens two files in repositories
the estate already governs, writes nothing back, asks the venture for
nothing and owes it no report, which is why it stands beside the
hands-off boundary rather than against it (ADR-0006, decision 6). The
venture is told as much in its own seed:
`kernel/templates/EOS_FEEDBACK.tpl.md` says the harvest reads that file
monthly and never writes in it, so the channel is one the venture was
handed and is free to leave empty. Wanting something looked at is
PB-E12's job, and the harvest never offers.

Nothing found: record checked and clean, and stop.

## PB-E03 · Pack and kernel authoring

The graded evidence path replaces wargame-first. Start with a fresh
research batch, one evidence row per source with licence and access
date. Argue guides before any doctrine line cites them; write binding
rules only where basis and evidence grade earn them. Respect the pack
definition of done and the per-kind metadata minima. Finish with
checks green and the derived views regenerated.

## PB-E04 · Promotion review

Section two of the monthly pass, under the graded change path: sample
five governance items (experimental edits, exceptions, contested rules);
expire experiments past their 90-day window. Promotion: default to
binding candidate on two argued rulings from two ventures, or one plus a
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

On request, and only on request: a venture asks for a newer pin. Diff
the CHANGELOG between its pin and the target. Classify each entry
against the venture's lock-book and records. Apply what matters in the
venture repo, re-run the seed checks there, update the pin and the
PROJECTS row.

The projects review used to point here on a quarterly row that never
fired once. It fires now when a repository joins the estate or a venture
changes status, and it is a read of `registry/PROJECTS.md` against
`estate/repos.json` for anything that has stopped being true, not an
upgrade of anything.

## PB-E07 · Inception drill

Fires when a seed is compiled, or when the inception walk changes; not
on the calendar (ADR-0008). Take a canned brief from inception/briefs/,
run Session 0 cold in a scratch repo, grade the output against
SEED_RUBRIC without charity. Findings become task records.

## PB-E08 · Rescale

When a venture's triggers change (money arrives, PII appears, a
second human joins): re-rule the scale, compile the delta between the
old and new seed manifests, migrate state files, note the rescale in
the venture lock-book and PROJECTS.

## PB-E09 · Hygiene

Section four of the monthly pass, and last, because it regenerates the
derived views after the other three have moved things. Run
python -m tools.eos check --repo with the semantic and freshness series
and fix findings. Re-verify or supersede everything past review.
Regenerate derived views. Close or discard dead task records; recover
expired claims only with liveness evidence. Sample the standing tier
exceptions recorded in `org/decisions/` and flag any past its expiry
date.

Then drain the sampled-review pool, which is the catcher `GOVERNANCE.md`
names for work that merges without a task record (ADR-0008, decision 3).
List everything the express and standard lanes merged since the last
pass, records and record-free commits alike, and read every fifth one in
commit order against three questions: does the message carry the whole
record, would the router have ruled that diff R2 or above on the facts
in it, and does anything in it reach the protected set? A commit that
should have carried a record gets one opened now, dated for when the
work landed, and the miss is a finding of the pass. The failure this
catches is the one ADR-0008 took on knowingly: a change whose reasoning
nobody can reconstruct. One in five is the starting rate the
venture-side REVIEWER charter carries
(`kernel/templates/org/roles/REVIEWER.tpl.md`) and not a measurement;
move it when a pass has evidence either way, and record what the
evidence was.

## PB-E10 · Experiment sweep

Section three of the monthly pass, beside the promotion review: read
each lifecycle experimental item against its recorded hypothesis; keep
with evidence, promote through the graded path, or revert. Set at most
one new deliberate experiment.

## PB-E11 · Study an exemplar

Daniel points at a source and says what to study it for. Nothing else
starts this, and nothing schedules it. The whole procedure runs in one
session, which is the only session that sees the raw source.

**1. Agree the lens contract, before reading anything.** One page from
`kernel/templates/LENS.tpl.md`: what the source is, at its exact version
or commit; how it was lawfully acquired; the governing licence or terms
and the jurisdiction that applies; the lenses in, named aspect by
aspect; the lenses out, always including no verbatim code or assets, no
expressive text, no source-identifying look and no tainted material; the
escalation order, which is observe, then docs, then tests, then source,
and never decompile without a recorded lawful basis; and where the
findings land. Daniel approves the contract in the room. Without an
approved contract there is no study, because the contract is the record
that makes the study defensible afterwards.

**2. Freeze, then read.** If the source is fetched live, take the copy
first and study the frozen copy. The fetch ends before the study begins,
so no context holds the source, this tree and a live network at once,
which is what keeps `packs/security-privacy` B2 satisfied. Study is
read-only. Write the source's evidence row in `registry/evidence.json`
now, with its licence and access date, and cite that id from everything
downstream. One row per source: a second lens on the same source is a
second lesson row citing the same id, not a second evidence row.

**3. Write the findings file,** scratch and venture-agnostic until the
decisions are made. Separate strictly, and never let one class drift
into another: direct observation, sourced fact, interpretation,
inference, recommendation. Tag every finding does-well, does-poorly,
merely-different or unknown. Give every finding its applicability limits
and the conditions that made it work where it was found, because a
practice lifted out of its conditions is the commonest way a study does
harm. Then extract, naming each for what it is: principles, patterns,
implementation techniques, failure modes, decision forks, reference
material.

The retention threshold: an artefact is kept only if its absence would
change a decision. A study that changes nothing says so in one line and
stops there.

**4. Run the conflict pass, before Daniel sees anything.** Map the
findings against the packs and everything inside them, guides, wargames,
refs and exemplars alike; the registries; `org/policy.json` and
`GOVERNANCE.md`; the inception and seed process; and the lessons already
recorded. List duplicates, tensions and contradictions explicitly. A
finding that contradicts a live rule names that rule. Doing this after
adoption instead is how a contradiction gets into the tree and stays
there.

**5. Interview in bounded batches.** Musts first, then wants, small
enough to answer in one sitting. Every question carries why it matters,
the real alternatives, the trade-offs between them, a recommendation,
and the assumption the study will use if the question is deferred.

**6. Record the decisions as lesson rows.** One row per decision in
`registry/lessons.json`, origin study, citing the evidence id from step
two and the lens contract from step one. The row shape is fixed by that
ledger's schema and is not restated here. A rejection is a row too, with
Daniel's reason, so the same idea cannot come back later as though it
were new. Binding is never a disposition this workflow assigns; the most
it can do is propose a binding candidate, and the ladder in
`GOVERNANCE.md` is unchanged.

**7. Integrate approved lessons only,** through the paths that already
exist: a pack edit, a guide, a registry fact, a template change. Each
edit lands in the same commit as its lesson row, so the artefact and the
reason for it never come apart. Where actual code is carried, tag it per
`packs/legal-licensing` D5.

**8. Close.** The lesson row's `informs` link is what makes the lesson
findable when the guidance it touched is next exercised. There is no
follow-up cadence and no review date beyond what the row itself carries.

## PB-E12 · Venture check-in

Venture-initiated only. The EOS never schedules one and never offers
one unasked. It hands off at a venture's birth and does not police what
it seeded (ADR-0006, decision 6). This playbook returns findings and
candidate lessons. It applies nothing and it changes nothing in the
venture.

1. Take the request: which venture, which slice, and what it wants
   looked at. A whole repository is a valid slice and so is one file.
   If the venture has not said what it wants, ask before reading.
2. Read the venture's lock-book first: its pin, its scale, its rulings.
   Guidance newer than that pin is context, not a violation, and a
   venture ruling that argued its fork is that venture's law.
3. Read the slice against current EOS guidance: the packs the lock-book
   activates, plus anything newer that bears on the slice.
4. Return findings. Each one names what diverges, what the divergence
   costs the venture, what changed in the EOS since the pin, and what
   you would do about it. Divergence on its own is not a defect, so say
   which ones matter and why the rest do not.
5. Name the newer guidance the venture could pull in, and point at
   PB-E06 as the way to pull it. The venture asks for that or it does
   not. Do not start it here.
6. Return candidate lessons the other way: anything this venture is
   doing that the estate should learn from goes back in the harvest
   shape, naming the venture. Daniel rules on those through the monthly
   pass. A check-in promotes nothing by itself.
7. Change nothing in the venture repo. The venture decides what to do
   with the findings and is free to do nothing at all.
