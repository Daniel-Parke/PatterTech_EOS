---
id: WG-LEGAL-004
summary: How rights arrive with inbound code, sign-off against agreement against employment against nothing, and where agent authorship sits
kind: wargame
type: wargame
tags: [delivery, eos, security, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-LEGAL-006, DOC-LEGAL-007, DOC-LEGAL-012]
applies_when: [accepts_contribution]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: asserted
sources: [EV-0345, EV-0348, EV-0352]
review: on-change-of:https://developercertificate.org/
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-LEGAL-004: How do rights arrive with inbound code?

## Decision question and stakes

Code arrives from outside the venture: a contributor, a contractor, a
snippet from a public repository, or an agent. The fork is what evidence
we hold that we may use it, and where that evidence lives.

## Doctrines or coverage gap under pressure

- `DOC-LEGAL-006` (default): Inbound work carries a provenance assertion.
- `DOC-LEGAL-007` (binding): Consequential questions stop here and go to a lawyer.
- `DOC-LEGAL-012` (default): Vendored code carries its licence text and a provenance note at the moment it is copied.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Who wrote it, and were they paid by us at the time?
- Will we ever need to relicense without asking everyone?
- Do we need an explicit patent position?
- How much friction can the contribution flow carry before people stop
  contributing?
- Can the evidence be checked by a machine?

Applicability is `accepts_contribution`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Certification per commit

Assume `A. Certification per commit` was selected and the outcome failed. Test this option's stated failure mechanism first: , evidence sitting in the history, and a check a cold agent can run. Costs: it is an assertion by the contributor rather than a grant to the project, it presumes the project already has an inbound licence, and it carries no patent grant and no warranty.

### Premortem for B. A signed agreement

Assume `B. A signed agreement` was selected and the outcome failed. Test this option's stated failure mechanism first: friction at the door, a document to maintain, and identity handling. We hold no primary source for this option and no comparison of the two on outcomes, so the case for it rests on assertion.

### Premortem for C. Employment or contract terms

Assume `C. Employment or contract terms` was selected and the outcome failed. Test this option's stated failure mechanism first: it covers only those people, it is invisible in the repository, and a contractor's default position is not always what a venture assumes.

### Premortem for D. Nothing recorded

Assume `D. Nothing recorded` was selected and the outcome failed. Test this option's stated failure mechanism first: absence of a licence means exclusive copyright, and a public repository being forkable grants no right to use what is in it (EV-0348). The cost is invisible until the code is load-bearing, which is exactly when it is unaffordable to remove.

## Decision rule

- Any contribution from outside the venture: A. B6 in
  `packs/legal-licensing/PACK.md` is that default, and a departure is
  written down before the contribution lands, not after.
- Paid contributors: C for the underlying rights, and A anyway so the
  repository carries its own evidence.
- Plausible future relicensing, or a corporate contributor who asks
  about patents: B, and take advice on the wording. Drafting a rights
  agreement is escalation trigger two under B7.
- Code copied from a public repository: A cannot be signed by us on
  someone else's behalf. Treat it as a vendored dependency under D5 and
  record where it came from, or do not copy it.
- Never D.

## Safe default

A. It costs one line, a hook checks it, and the evidence is in the
history where an auditor and an agent can both read it.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Who wrote it, and were they paid by us at the time?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A. It costs one line, a hook checks it, and the evidence is in the history where an auditor and an agent can both read it.

**Exit condition:** Stop or roll back the selected branch when , evidence sitting in the history, and a check a cold agent can run. Costs: it is an assertion by the contributor rather than a grant to the project, it presumes the project already has an inbound licence, and it carries no patent grant and no warranty, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Who wrote it, and were they paid by us at the time?

## Counter-evidence and transfer limits

### Evidence boundary

The certification route is a primary source, short and unambiguous
(EV-0345). Option B has no primary source in this pack
and no outcome comparison exists in anything read at this cutoff, so
the choice between A and B currently rests on assertion. That is also
why the authority audit under ADR-0008 moved B6 from binding to
default: the failure it prevents is real, and the basis under it is a
ruling of ours rather than law, a standard or a measurement.
### Preserved reasoning: Agent-written commits

They carry the same sign-off, from the person directing the run. This
is not a claim that the output is authored by that person. Ownership of
machine-generated output is being answered in staged public reports by
a national authority and is not settled, with no equivalent UK
determination located at this cutoff
(EV-0352). The position the pack takes is narrow:
record provenance, do not assume authorship, and do not put a
copyright assertion on machine output that nobody has tested.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
