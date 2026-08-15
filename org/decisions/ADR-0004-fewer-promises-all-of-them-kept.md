---
summary: Two rungs not three, exceptions are ADRs, pack budgets measured where loading actually happens, and the two controls that were described but never ran
type: decision
tags: [eos]
status: accepted
decided_by: Daniel Parke
date: 2026-08-08
---

# ADR-0004: fewer promises, all of them kept

The operator ruled on 2026-08-08, during the pre-release review of
`feat/eos-v2-agentic-development`, when the audits showed the repository
describing more control than it implements. The ruling: build the controls
that protect something, delete the ones that only exist on paper, and set
budgets where they can be measured. This amends `GOVERNANCE.md` and
`kernel/POLICY_SPEC.md`. ADR-0002 and ADR-0003 stand.

## Context

The pre-release audits found four mechanisms described in governing files
and absent from the code.

**Protected-set refusal never ran.** `tools/eos/cli.py` filtered routing
reasons for the factor `protected-set`; the router emits
`protected-set-contact`. The strings never matched, so the only `return 3`
in the codebase was unreachable. `AGENTS.md`, `kernel/POLICY_SPEC.md` and
`tools/CLI_CONTRACTS.md` all described enforcement that had never executed
once.

**Claim refusal was never written.** `taskops.create_task` and
`update_task` did no claim check at all, and nothing in the tree emitted
the `{refused: true, reason, claim_set_ref}` shape that
`tools/CLI_CONTRACTS.md`, `AGENTS.md` and `TOUR.md` all specify. The
never-list in the router file said a session not named in `org/claims.json`
may not create task records. Nothing stopped one.

**The RFC rung had no records and no directory.** `org/rfcs/` does not
exist. `GOVERNANCE.md` made it rung two of a three-rung change path, gave
it an id scheme and an eighty-line cap, and routed the de-protected
contracts through it. In the whole v2 build, not one was written.

**The exception ledger was specified and never implemented.**
`kernel/POLICY_SPEC.md` calls an expired standing exception a checker
finding and `PB-E09` says to sample the ledger. `org/exceptions.jsonl`
does not exist and no code reads it. It is the only sanctioned route back
down from an upward-only tier ruling, so the one escape hatch in the risk
model was a document.

Separately, the pack organ budget was wrong by a factor of two. It caps a
pack at "about eight hundred" lines across all organs. Excluding
`research/`, packs run 1,112 to 2,274 lines, median 1,384. Every pack
violates it and nothing checks it.

## Decision

**1. Build the two controls that protect something.**

Protected-set refusal and claim refusal are implemented, with tests that
fail if either stops working. A protected-set touch without `--adr` exits
3 and names the file that matched. A task write by a session not in the
committed claim set, or by a lane whose claims do not cover the path,
exits 1 with the documented refusal payload.

**2. Two rungs, not three. Exceptions are ADRs.**

The RFC rung is removed. The graded change path is an experimental edit or
an ADR. Everything the RFC path carried moves to the ADR path: changes to
pack shape, guide format, ID schemes and the front-matter schema; changes
to law-based and standard-based rules; and standing exceptions to the risk
router.

A standing tier exception is now an accepted ADR with an expiry date,
recorded in `org/decisions/` like any other decision, rather than a row in
a file nothing reads. This costs a little more per exception and buys a
mechanism that exists. The `RFC-NNN` id scheme and `org/exceptions.jsonl`
are withdrawn.

The argument for three rungs was that an RFC is cheaper than an ADR. That
was never tested, because no RFC was ever written; what the third rung
actually bought was a plausible-looking path that no one took and a
directory that never existed.

Amends `GOVERNANCE.md`: the graded change path, precedence rule four, the
de-protected set, the ID schemes and the line budgets. Amends
`kernel/POLICY_SPEC.md`: standing exceptions.

**3. Pack budgets are measured where loading happens.**

The all-organs cap is withdrawn. Nothing ever loads a whole pack, so
total disk size was never the cost it claimed to measure. Progressive
disclosure gives three real limits, and those are the ones that bind:

- the first paragraph, always in context, stays under eighty words;
- `PACK.md`'s body, loaded on activation, stays under five hundred lines;
- one guide, loaded on demand, stays under one hundred and fifty lines.

The first two were already stated and the third is new. A pack may hold as
many guides and refs as its domain earns, because an agent reads one of
them at a time.

## Consequences

- Three files stop describing controls that do not exist.
- The exception path costs an ADR. If that proves too heavy in practice,
  the evidence will be exceptions that should have been recorded and were
  not, and that is a better problem than the current one, where the
  mechanism cannot be used at all.
- Two guides currently exceed the new per-guide budget and will be
  trimmed or waived on their next edit.

## Scope

This authorises the `GOVERNANCE.md` and `kernel/POLICY_SPEC.md` amendments
named above and nothing else in the protected set. Release remains a
separate approval under ADR-0002. `main` is untouched.
