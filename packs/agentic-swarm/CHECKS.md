---
summary: What a reviewer or a script can verify about a graph build, split into executable today and judgement
kind: record
scope: estate
sources: [EV-0006, EV-0053, EV-0108, EV-0109, EV-0111]
type: checks
tags: [eos, arch, delivery, testing]
review: on-change-of:agent-harness-major-release
---

# CHECKS: agentic swarm

Evaluation criteria for a graph build. Each row says what is checked,
against which requirement, and whether a script can decide it today.
The subject of most of these checks is the partition artefact, the lane
packets and the run journal, so a run with none of those is not
checkable at all, which is itself the first finding.

## Executable today

These reduce to a parse, a set operation or a count. No model in the
loop.

| Id | Check | Against |
| --- | --- | --- |
| C1 | A partition artefact exists and is committed before the first lane's first write, by timestamp | B1 |
| C2 | Every lane row names files owned, interfaces consumed, interfaces published, and lanes depended on | B1 |
| C3 | Lane write sets are pairwise disjoint, and their union excludes every artefact on the hub list | B1 |
| C4 | The hub list is non-empty where the graph has any file with more than one inbound dependency group | B1 |
| C5 | Every packet carries all nine fields, and the escape field names a return status rather than describing one | B2 |
| C6 | Every path, id and symbol in a packet's write set and read set resolves in the tree at dispatch time | B2 |
| C7 | Every return validates against the declared schema, and a non-conforming return is rejected rather than parsed | B3 |
| C8 | Every return carries files changed, checks run with verbatim output, not-done items, unknowns, spend, and one of the four terminal statuses | B3 |
| C9 | No lane's write set includes a test file, fixture, evaluation script or CI configuration for the node it is judged by | B7 |
| C10 | The verifier artefact's creation timestamp precedes the first lane's dispatch | B7 |
| C11 | Lane count is at most two where no decidable oracle is declared on the run record | B7, D1 |
| C12 | The run record carries a global token and spend ceiling, a per-node cap, and an explicit delegation depth | B6 |
| C13 | Each lane has its own worktree and branch, and the merge order is recorded before the first merge | B9 |
| C14 | Every dependency name added by any lane resolves in the registry, checked at the gate | B10 |
| C15 | The claim set is committed before dispatch and covers every lane's write set | D5 |
| C16 | The journal holds one entry per node with packet, return, status, spend, timing and artefact references, in start order | D12 |
| C17 | Per-package diff width is under the ceiling stated in the packet | D7 |
| C18 | Lane count above five carries a recorded reason on the run record | D1 |
| C19 | The pack cites no vendor version number, model name or price outside a profile file | pack law |
| C20 | Every rule in `packs/agentic-swarm/PACK.md` names a failure and carries at least one evidence id that resolves in `registry/evidence.json` | pack law |

C5 and C8 are the two most worth automating first. They are the cheapest
to check and they sit on the two failures that produce silent bad
merges: a lane guessing what the packet meant, and an integrator reading
a dead lane as a clean result.

## Judgement, for a reviewer

These need a person, and saying so is more honest than pretending a
script decides them.

- **Is the cut real?** C3 proves the write sets do not overlap. It says
  nothing about whether the lanes share an assumption, which is the
  failure that produces changes that compile and contradict.
- **Is the oracle any good?** C10 proves the verifier existed first. A
  schema validator that accepts almost anything satisfies it and
  verifies nothing (EV-0111). Ask what it would have caught.
- **Has the oracle been shown to bite?** Ask for one seeded fault it
  fails on. A green suite that has never been seen red has not been
  shown capable of turning red.
- **Was this work worth fanning out?** The single most valuable review
  question and the one no checker answers. Compare against a
  single-agent control on a sample.
- **Is the escape being used?** A run with zero insufficiency returns
  across a dozen lanes means either the packets were unusually good or
  the lanes are guessing. Read two returns and decide which.
- **Did anything cross a lane boundary as instruction?** C7 sees the
  schema. Whether a lane's prose talked the integrator into something
  is a reading (B4).
- **Is the reviewer stronger than the writer?** C-level checks see that
  a reviewer ran. Whether it was capable of judging the work is a
  person's call, and a weaker reviewer damages correct work.
- **Did the run land?** Generation speed is visible and landing is not.
  Read agent-done-to-merged time and fourteen-day rework rate before
  believing the run was fast.

## Suite level

Beyond a single run: any claim that one swarm configuration beats
another states n and the spread. Single-run pass@1 varies by several
percentage points at fixed configuration, so a one-run comparison is
not evidence. Keep a small standing evaluation set, of the order of
twenty representative cases, and re-run it whenever the topology or the
packet template changes. Suite existence is executable; suite quality is
judgement.

## Not checked here

Prompt wording inside a lane, model choice, harness selection, test
timing, and the security posture of a lane's sandbox. The first three
are out of scope for this pack. Test timing belongs to
`packs/delivery-testing/PACK.md` and the sandbox to
`packs/security-privacy/PACK.md`.
