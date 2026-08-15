---
summary: The Session 0 master playbook, phases A to E, from idea to signed seed
type: kernel
tags: [eos]
---

# INCEPTION · Session 0

The full specification of PB-E01. One session in the new venture's repo.
The output is a compiled, checked, signed seed that a cold agent can
build from, plus one row in registry/PROJECTS.md.

The operator is in the room at phase A, phase B and phase E. Phases C
and D run without them, so the session collects every judgement it
needs while they are present.

Ground rules. The agent transcribes and challenges; it never invents,
and an unanswered question is a recorded question. A fork the walk hits
that no guide covers takes the draft-guide route of
inception/WALK_ORDER.md and Session 0 carries on, because a missing
guide is the estate's gap and not the venture's blocker. If the session
dies mid-way, the files written so far are the resume state.

Two paths exist: the full one below, and inception/EXPRESS_INCEPTION.md
for an S venture whose risk triggers are all silent. Read the gate in
that file first; any money, personal data, auth or deployment answer
routes here.

## Session 0 writes to main

Session 0 commits straight to main in the venture repo, from the first
commit to the signed sign-off block, and that is correct rather than
tolerated. The rule it looks like it breaks is the venture
constitution's Part II article 7, main is always releasable and merges
come through the gates the ruled tier demands. That article does not
exist until phase D compiles it: there is no constitution to obey and
no ruled tier to gate against while the thing that would rule is still
being written.

The exemption is the whole of Session 0 and it ends at the gate. Article
7 governs the first commit after sign-off. An S venture compiles no
constitution at all and the line still holds for it, with branch
discipline starting at its first build task. Without this stated
somewhere, the first review session reads Session 0's history as a run
of unreviewed merges instead of as the compile it was.

## Phase A · Interview

Run inception/INTERVIEW.md end to end, the three challenge steps
included. The output is the venture brief content, the trigger list,
the risk-surface answers phase B turns into policy, and the list of
material workstreams Genesis later cuts its work from. Open no template
until the operator has confirmed the restatement and ruled on the
strictly smaller version.

## Phase B · Scale, shape and risk surface

Three rulings, taken with the operator.

1. Scale, WG-EOS-001: S or ORG.
2. Repo shape, WG-EOS-002. Create or claim the repo per the ruling and
   put `* text=auto eol=lf` in .gitattributes before anything else
   lands.
3. The risk surface. The interview's answers on money, personal data,
   auth, public surface and deployment stop being prose here and become
   concrete path patterns for the venture's policy file: which
   directories are reversible, which are sensitive, which are
   protected. Name real paths the venture will hold; a venture with no
   code yet names the paths its stack profile creates, and the
   first-build task corrects them if the stack lands differently.

The scale and repository-shape outcomes go into `docs/RULINGS.json` as
argued `RUL-*` records with one-line reasons. The lock-book header carries
the resulting scale and repository pin, not duplicate ruling rows. The
risk-surface map carries to phase D as the fill for the policy's
path_patterns lists. A path pattern never sets a tier by itself; it is
a signal the factor table cites, per kernel/POLICY_SPEC.md.

## Phase C · Pack activation walk

Build and order the walk per inception/WALK_ORDER.md, which owns the
tri-state facts, the always-walk set, dependency order and selection
gate. Match the interview facts through `eos doctrine match` or
`eos wargame match`. Applicable Doctrine summaries load automatically;
full atoms load only when the operator needs their reasoning. Run a
Wargame only when a pressure, conflict, gap or explicit operator request
engages it.

Every candidate Wargame receives a selected, omitted or candidate entry
with a reason in `docs/RULINGS.json`; only executed Wargames receive a
`RUL-*` outcome. The activated packs go in the lock-book's
`packs_adopted` list, and house style activates only by adoption there.

## Phase D · Compile

Compile per inception/COMPILE.md, which owns every rule of it: the
inputs, the prune, the fill and the table of what fills each slot, the
policy fill, the front-matter rewrite, the deferrals, the Genesis forms,
the assemble, the distillation and the report. Nothing about the compile
is restated here, because a compile rule written in two places goes
stale in one of them.

## Phase E · Gate

Run `python -m tools.eos check --seed <venture path>` from the EOS
repo. Every auto item in kernel/SEED_RUBRIC.md must be green before a
human judges anything. Then the operator signs the human items, headed
by H1, the cold-start test: a fresh session, given only the seed and
the first open task, completes it with zero questions. H1 failing
blocks the gate, and the fix is better files and a fresh cold session
rather than a warmer prompt.

Sign-off lands at the foot of docs/COMPILE_REPORT.md. Then append the
venture's row to registry/PROJECTS.md in the EOS repo, the one
sanctioned cross-repo write, carrying the pin, scale, packs adopted
and status.

Then the launch decision, and it is the operator's: either Genesis runs,
or the sign-off block carries one line saying why not.
inception/GENESIS.md specifies the phase.

Without Genesis, an S venture starts working from docs/TASKS.md and an
ORG venture boots from org/START.md with its work in task records. With
it, both start from the work packages. The first retro banks whatever
Session 0 got wrong into docs/EOS_FEEDBACK.md, and PB-E02 does the rest.
