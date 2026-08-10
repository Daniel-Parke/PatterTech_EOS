---
summary: The S-scale fast path for Session 0, six questions, inherited defaults, two human gate items
type: kernel
tags: [eos]
---

# EXPRESS_INCEPTION

The fast path through Session 0, for a venture whose risk triggers are
all silent. It compiles the same nine-file S seed as the full path and
passes the same auto checks. What it drops is argument nobody needed:
questions whose answers were never going to change a ruling, and a walk
whose every row would have read inherited.

Target: under thirty minutes of the operator's time, in one sitting,
with the operator present throughout because there is nothing left to
do without them.

## When Express is wrong

Stop and run inception/INCEPTION.md in full the moment any of these is
true. The list below is a gate and it binds.

- Money changes hands under the venture's name.
- Personal or regulated data is touched, anyone's.
- Anything authenticates, authorises or holds server-side state.
- Anything is deployed, monitored or backed up with state behind it.
- A second human holds a decision, or the venture could be handed over
  or sold as a unit.

Any yes means the risk surface needs arguing into policy and the walk
needs real rulings. Express cannot produce either. A venture that
trips a trigger halfway through Express does not finish Express; it
restarts at phase A of the full path with the answers already given.

## The six questions

1. What is it, in one paragraph, in your words?
2. Who is it for, and who pays (if anyone)?
3. What surfaces exist: site, app, api, documents?
4. The gate: does any of money, personal or regulated data, auth or
   server state, or a deployment with state apply? Read the list back
   and take a yes or no on each.
5. What may this venture spend, and who approves spend? A number or
   "nothing without me", never silence.
6. What is out of scope, and what does success look like in ninety
   days?

Then one challenge pass, which is not optional. Restate the venture in
two or three sentences and be corrected until the operator says it is
right; the corrected restatement opens the brief. In the same breath
ask for the cheapest way it dies and whether there is a smaller version
they would rather build. Record both verbatim. The three-step challenge
of the full path collapses to this because a venture that answered no
to the gate is already close to the smallest thing that serves anyone.

## What is inherited

Everything else takes its default and says so.

- Scale S, argued, on the strength of question 4.
- Repo shape A, the monorepo, inherited.
- The always-walk set of inception/WALK_ORDER.md, ruled inherited
  throughout, plus the UI and UX pack when the venture has a surface.
  No other pack activates, because activation needs a predicate and the
  gate question proved none holds.
- The policy's path lists take the stack profile's defaults, with the
  whole tree reversible except the policy file itself, which is
  protected. Guard validated stays false, so every guarded class is
  manual-only.

## Compile and gate

Compile per inception/COMPILE.md, unchanged. The deferral rule still
binds: every `set at first build` value needs its first-build lock-in
row in docs/TASKS.md, or check D004 fails the seed.

Run `python -m tools.eos check --seed <venture path>`. Every auto item
must be green, as on the full path; nothing about the fast path relaxes
the machine.

Two human items are signed rather than five: H1, the cold-start test,
and H4, voice on the surfaces a stranger reads first. H2 is already
covered, because the operator corrected the restatement in the room.
H3 has nothing to spot-check, because Express argues one ruling. H5 is
the compiled operators guide at S with no venture-specific rhythm in
it. Record on the sign-off block which items were signed and that the
seed came through Express, so a later reader knows what was and was not
judged.
