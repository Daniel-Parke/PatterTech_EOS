---
summary: The Session 0 master playbook in v2, phases A to E, from idea to signed seed
type: kernel
tags: [eos]
---

# INCEPTION · Session 0

The full specification of PB-E01 under the v2 kernel. One session in
the new venture's repo. The output is a compiled, checked, signed seed
that a cold agent can build from, plus one row in registry/PROJECTS.md.

The operator is in the room at phase A, phase B and phase E. Phases C
and D run without them, so the session collects every judgement it
needs while they are present.

Ground rules. The agent transcribes and challenges; it never invents,
and an unanswered question is a recorded question. A fork the walk hits
that no guide covers files a draft guide in the venture's feedback file
and Session 0 carries on, because a missing guide is the estate's gap
and not the venture's blocker. If the session dies mid-way, the files
written so far are the resume state.

Two paths exist: the full one below, and inception/EXPRESS_INCEPTION.md
for an S venture whose risk triggers are all silent. Read the gate in
that file first; any money, personal data, auth or deployment answer
routes here.

## Phase A · Interview

Run inception/INTERVIEW.md end to end, the three challenge steps
included. The output is the venture brief content, the trigger list,
and the risk-surface answers phase B turns into policy. Open no
template until the operator has confirmed the restatement and ruled on
the strictly smaller version.

## Phase B · Scale, shape and risk surface

Three rulings, taken with the operator.

1. Scale, WG-EOS-001: S or ORG. v1's M and L both compile as ORG.
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

All three go in the lock-book header, argued, with one-line notes. The
risk-surface map carries to phase D as the fill for the policy's
path_patterns lists. A path pattern never sets a tier by itself; it is
a signal the factor table cites, per kernel/POLICY_SPEC.md.

## Phase C · Pack activation walk

Packs replace v1's doctrine modules, so the walk is built from
packs/INDEX.md rather than a wargame index. Build and order it per
inception/WALK_ORDER.md: filter the index rows by the venture's
triggers, test each candidate against its applicability predicates, and
rule the guides that every activated pack names.

Every ruling lands as one row in the lock-book header, in the form
id · ruling · argued|inherited · note. Argued means the venture's facts
were engaged afresh against that guide's fork; inherited means the
default was taken without new argument, which is legitimate whenever
the triggers are silent. Only argued rulings count as promotion
evidence, so an inherited row costs nothing and a falsely argued one
is a lie in the promotion arithmetic. The activated packs go in the
lock-book's packs_adopted list, and house style activates only by
adoption there.

## Phase D · Compile

Compile per inception/COMPILE.md: prune, fill, front-matter rewrite,
assemble, distil, report. Four steps catch people out.

- Prune the fences for the ruled scale only. Both scale markers leave
  in the same pass, whichever way the ruling went.
- Fill the policy file from the risk-surface map, then delete the
  template's `_slots` key. A compiled policy still carrying it fails
  its schema at D007.
- Byte-copy AGENTS.md to CLAUDE.md last, after every other edit.
- Fill the ancestry table honestly, one row per compiled file, the
  JSON files included.

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
and status. An S venture then starts working from docs/TASKS.md; an
ORG venture boots from org/START.md with its work in task records. The
first retro banks whatever Session 0 got wrong into
docs/EOS_FEEDBACK.md, and PB-E02 does the rest.
