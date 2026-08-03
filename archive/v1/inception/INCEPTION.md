---
summary: The Session 0 master playbook, phases A to E, from idea to signed seed
type: kernel
status: archived
tags: [eos]
---

# INCEPTION · Session 0

The full specification of PB-E01. One session in the new venture's
repo, the operator present at phases A, B and E. The output is a
compiled, checked, signed seed a cold agent can build from, plus one
row in the EOS projects registry. The worked reference is
examples/autowatt-seed.md.

Ground rules: the agent transcribes and challenges, never invents; the
three-strikes rule binds throughout; if the session dies mid-way, the
files written so far are the resume state and a fresh session continues
from them.

## Phase A · Interview

Run inception/INTERVIEW.md end to end, challenge steps included. The
output is the venture brief content and the trigger list. Do not open
a single template until the operator has confirmed the restatement and
ruled on the smaller version.

## Phase B · Scale and shape

Walk WG-EOS-001 (scale) and WG-EOS-002 (repo shape) with the operator.
Record both rulings, argued, with one-line notes; they open the
lock-book header. Create or claim the repo per the shape ruling; add
`* text=auto eol=lf` to `.gitattributes` before anything else lands.

## Phase C · Wargame walk

Build the walk per inception/WALK_ORDER.md from the trigger list, and
rule each wargame into the lock-book header, argued where a trigger
names the venture, inherited where the triggers are silent. A fork
with no wargame files a draft in the feedback file with the ruling as
its first worked entry. The operator may leave after phase B; collect
the argued rulings that need their judgement while they are present.

## Phase D · Seed compile

Compile per inception/COMPILE.md: prune, fill, front-matter rewrite,
assemble, distil, report. The mechanical core (prune and fill) may be
scripted; the script is part of the session's record. Fill the
ancestry table honestly, including any authored add-ons.

## Phase E · Gate

Run `python tools/eos_check.py --seed <venture path>` from the EOS
repo. All auto items green, then the operator judges the human items of
kernel/SEED_RUBRIC.md, headed by the cold-start test: a fresh session,
given only the seed and the first queue item, completes it with zero
questions. Sign-off lands in the compile report. Then append the
venture's row to `registry/PROJECTS.md` in the EOS repo, the one
sanctioned cross-repo write, with the pin, scale and status.

## After Session 0

S ventures start working (the GO launcher). M ventures run
GENESIS-LITE; L ventures run L1-GENESIS. The first retro banks
whatever Session 0 got wrong into the feedback file; the harvest does
the rest.
