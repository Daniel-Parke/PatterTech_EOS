---
summary: How rights arrive with inbound code, sign-off against agreement against employment against nothing, and where agent authorship sits
type: guide
tags: [security, delivery]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: asserted
sources: [EV-0345, EV-0348, EV-0352]
review: on-change-of:https://developercertificate.org/
---

# GD-LEGAL-004: How do rights arrive with inbound code?

## The question

Code arrives from outside the venture: a contributor, a contractor, a
snippet from a public repository, or an agent. The fork is what evidence
we hold that we may use it, and where that evidence lives.

## It depends on

- Who wrote it, and were they paid by us at the time?
- Will we ever need to relicense without asking everyone?
- Do we need an explicit patent position?
- How much friction can the contribution flow carry before people stop
  contributing?
- Can the evidence be checked by a machine?

## Options

### A. Certification per commit

The contributor asserts that they wrote the change and may submit it,
or that it derives from work they are entitled to submit under a
compatible licence, or that someone who so certified passed it to them
unmodified, and they accept that the record is public and permanent
(EV-0345). One sign-off line per commit, hook-checked.
The line is the one the certification defines: the `Signed-off-by`
prefix, the contributor's real name, and their address in angle
brackets, one per commit and never in a squashed summary only. Buys:
near zero process cost, evidence sitting in the history, and a check a
cold agent can run. Costs: it is an assertion by the
contributor rather than a grant to the project, it presumes the project
already has an inbound licence, and it carries no patent grant and no
warranty.

### B. A signed agreement

An explicit grant of rights, usually with a patent position and
sometimes with the right to relicense. Buys: the ability to change
licence later without hunting every contributor, and an explicit patent
and moral-rights position. Costs: friction at the door, a document to
maintain, and identity handling. We hold no primary source for this
option and no comparison of the two on outcomes, so the case for it
rests on assertion.

### C. Employment or contract terms

Rights arrive through the engagement, not through the repository. Buys:
nothing extra to run for people we already pay. Costs: it covers only
those people, it is invisible in the repository, and a contractor's
default position is not always what a venture assumes.

### D. Nothing recorded

Take the code and carry on. Buys: no process. Costs: absence of a
licence means exclusive copyright, and a public repository being
forkable grants no right to use what is in it
(EV-0348). The cost is invisible until the code is
load-bearing, which is exactly when it is unaffordable to remove.

## Decision rule

- Any contribution from outside the venture: A. B6 in
  `packs/legal-licensing/PACK.md` binds this.
- Paid contributors: C for the underlying rights, and A anyway so the
  repository carries its own evidence.
- Plausible future relicensing, or a corporate contributor who asks
  about patents: B, and take advice on the wording. Drafting a rights
  agreement is escalation trigger two under B7.
- Code copied from a public repository: A cannot be signed by us on
  someone else's behalf. Treat it as a vendored dependency under D5 and
  record where it came from, or do not copy it.
- Never D.

## Default

A. It costs one line, a hook checks it, and the evidence is in the
history where an auditor and an agent can both read it.

## Agent-written commits

They carry the same sign-off, from the person directing the run. This
is not a claim that the output is authored by that person. Ownership of
machine-generated output is being answered in staged public reports by
a national authority and is not settled, with no equivalent UK
determination located at this cutoff
(EV-0352). The position the pack takes is narrow:
record provenance, do not assume authorship, and do not put a
copyright assertion on machine output that nobody has tested.

## Evidence boundary

The certification route is a primary source, short and unambiguous
(EV-0345). Option B has no primary source in this pack
and no outcome comparison exists in anything read at this cutoff, so
the choice between A and B currently rests on assertion. That is why
this guide is authority default rather than binding on the choice
itself, while the pack binds only the weaker claim that some provenance
assertion exists.

## Worked rulings

- **PatterTech EOS legal-licensing pack (2026-08, argued)**: A, with B
  routed to a lawyer if it is ever wanted. Argued from cost and
  checkability, and recorded as resting on assertion rather than
  evidence.
- **PatterTech EOS itself (2026-08, inherited)**: A for every commit
  including agent runs, since this repository already treats provenance
  as a habit.
