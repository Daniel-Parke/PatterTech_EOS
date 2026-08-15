---
summary: The de-restriction pass, what stops binding and what stays, and what catches each loosened failure instead
type: decision
tags: [eos]
status: accepted
decided_by: Daniel Parke
date: 2026-08-10
---

# ADR-0008: less law, better kept

The operator, 2026-08-10: "We really need to update this governance and in
general all the files to be way less restrictive." This record is that
change. It is separate from ADR-0006 because it is a distinct decision
and bundling unrelated architecture into one record is how a decision
stops being reviewable.

## Context

The EOS was nearly abandoned once for being too slow. v1 measured 20.1
per cent of every line written as ceremony. v2 cut that by 77 per cent
and then accumulated its own: five standing cadences, a claim file that
must be hand-written and committed before a session may write anything,
a task record for every ordinary change, a closed tag vocabulary that
needs a governance edit to extend, line budgets on most file kinds, and
eight metadata axes with per-kind minima that the specification itself
admits are mostly unchecked.

Two facts sharpen the case. First, of roughly 110 binding requirements
across twenty packs, many rest on `basis: decision`, which is the
repository's own word for "we chose this", while the promotion ladder
says authority is earned by evidence. Second, the claim model refused a
lane the right to open its own task record during this very build,
because `org/` belongs to the integrator. That is friction with no
failure behind it.

The honest counter-argument, recorded because it is real: loosening
governance is how the sixty-six false statements got into the tree in the
first place. So every rule this record loosens names what now catches the
failure instead. Where nothing catches it, the rule stays.

## The test

A rule stays **binding** only if both hold:

- it prevents a concrete failure that is serious or hard to reverse, and
- its basis is law, standard or empirical evidence, or it is a
  protected-set safety floor.

Everything else becomes a **default**: do it unless you record why not.
A default is not a suggestion; departing from one leaves a written
reason, and the monthly review samples those reasons.

## What changes

1. **Claims scale with concurrency.** A claim is required when more than
   one session may write at once. A single session working alone is
   implicitly claimed and need not hand-write a claim file first. When
   lanes run in parallel the integrator still commits the claim set
   before dispatch, unchanged, because that is the mechanism that
   prevents two writers on one file and the conflict data behind it is
   strong. *Caught instead by*: for solo work, git history and the
   checker; for parallel work, the unchanged claim refusal.

2. **A lane may open its own task record.** The claim covering a lane's
   product paths also covers its own record under `org/tasks/`. *Caught
   instead by*: the record still names its owner session, and the
   integrator still owns every derived view.

3. **Task records are required for gate-bearing work.** R2 and above,
   anything touching the protected set, and anything a reviewer must
   later find. Ordinary R0 and R1 work records itself in the commit
   message, which is what Express already does. *Caught instead by*: git
   is the log, which ADR-0002 already ruled; the sampled review pool
   reads commits, not only records.

4. **Four monthly cadences become one.** Harvest, hygiene, promotion
   review and the experiment sweep run as a single monthly pass with four
   sections. The quarterly inception drill and estate review become
   on-demand, triggered by a real event (a seed compiled, a repository
   added) rather than by the calendar. *Caught instead by*: the same work
   still happens, in one sitting; the cadence file records the pass, and
   a skipped section is still a finding. Both quarterly rows had never
   fired once since v1, which is evidence that a calendar trigger nobody
   honours is not a control.

5. **Line budgets become warnings, except one.** The forty-line cap on
   `AGENTS.md` and `CLAUDE.md` stays an error, because that file is in
   every agent's context and its cost is paid on every task. Pack bodies,
   guides, task records and review verdicts warn instead of failing.
   *Caught instead by*: the pruning test in `PACK_SHAPE.md` and the
   review passes.

6. **The tag vocabulary opens.** An unknown tag warns instead of failing,
   and the list in `GOVERNANCE.md` becomes the known set rather than the
   permitted set. *Caught instead by*: the warning itself, and hygiene.

7. **Metadata minima shrink to what drives behaviour.** Required
   everywhere: `summary`, `type`, `tags`. Required where they change what
   an agent does: `authority`, `applies_when`, `sources`, `review`.
   The rest of the eight axes become optional and derived where possible.
   *Caught instead by*: nothing was catching them anyway; the
   specification already admits most of its compatibility law is
   unchecked, and this makes the written rule match the enforced one
   rather than shrinking real enforcement.

8. **Authority is audited across the packs.** Every binding requirement
   is tested against the rule above and demoted to default where it
   fails. Roughly a third to a half are expected to move. The audit does
   not touch `packs/security-privacy` B1 to B6 or the production-safety
   rules in `packs/devops-reliability`, which are protected-set floors
   and stay binding whatever their basis field says.

## What does not change

Stated so the loosening cannot be read as general:

- The safety floors. Prompt-injection resistance, secret protection,
  production safety, data protection and approval for consequential
  external actions are untouched, and the action-time guard still fails
  closed.
- Derived files. A file marked derived has a generator and is never
  hand-edited. This rule prevents a failure that has actually happened
  here, twice.
- `org/decisions/` stays append-only with the one sanctioned amendment.
- Supersession stays explicit and bidirectional.
- The promotion ladder. Authority is still earned, binding still needs an
  accepted ADR and the operator, and an argued ruling still counts for more
  than an inherited one.
- The decision budget bands, and the escalation band in particular.

## Consequence to watch

Fewer records means less of the tree's history is in the tree. The
mitigation is that git is the log and the commit message is the record
for ordinary work, which only holds if commit messages stay honest. If
the first monthly pass after this lands finds work it cannot reconstruct,
this decision is the suspect and the fix is to raise the bar for what
counts as gate-bearing, not to reinstate records everywhere.
