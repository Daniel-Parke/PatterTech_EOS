---
summary: May an item close without an answer, and on whose clock?
kind: guide
authority: default
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0041]
review: on-change-of:ISO-10002-revision
type: guide
tags: [ops, product, pii]
review_by: 2027-08
---

# GD-SUPPORT-002: May an item close without an answer, and on whose clock?

## The question

Two maintained sources give opposite instructions. A large public
tracker closes unreproducible reports after twenty days of silence and
marks anything untouched for ninety as stale
(FRAG-SUPPORT-OPERATIONS-04). The complaints standard says the loop
closes only once the complainant has been told the outcome
(FRAG-SUPPORT-OPERATIONS-05). Both are defensible, for different
relationships. The failure is letting a ticketing tool's default answer
the question by accident.

## It depends on

- **Whether the reporter is under contract or paying.** This is the
  load-bearing factor and it is not close.
- **Who holds the missing information.** A timer punishes the person
  who cannot supply what was never asked for.
- **Whether the channel is public.** A closed public issue is still
  readable and reopenable; a closed email is gone.
- **The cost of a lost real bug** against the cost of a queue that
  grows faster than it drains.
- **Retention duty.** A closed ticket is still personal data, and how
  long it is kept is a separate decision from when it closed (EV-0041,
  PACK.md B6).

## Options

### A. Close on silence, with a timer
Unreproducible or information-starved items close automatically after a
stated silence, and stale items are labelled after a longer one
(FRAG-SUPPORT-OPERATIONS-04). Buys a finite queue with no human cost
and a defensible answer to "why is this still open". Costs real bugs:
the maintainers of the project that runs the best-known implementation
have filed complaints about their own bot closing important issues,
which is honest counter-evidence from inside the practice.

### B. Close on answer only
Nothing closes until the reporter has been told an outcome, even if the
outcome is "we cannot reproduce this and are stopping here"
(FRAG-SUPPORT-OPERATIONS-05). Buys fairness that survives a challenge,
and it is what a paying relationship is owed. Costs a standing human
obligation that scales linearly with volume.

### C. Needs-info with a due date, then a human decision
The item sits in a needs-info state carrying the date its next action
is due. On that date a person decides: chase, close with an answer, or
convert to a defect on the evidence already held. Buys most of A's
finiteness while keeping B's answer step. Costs a recurring review
slot, which is the thing that actually gets skipped.

### D. Split by channel, with the policy written per channel
Public tracker takes A. Anything from a paying customer takes B.
Everything else takes C. The policy is written down per channel before
any timer is switched on. Buys the right answer per relationship. Costs
one more thing to configure and one more thing to keep true.

## Decision rule

If the reporter pays, B. If the channel is a public tracker with
volunteer reporters, A is available and the timer values are stated in
the channel's own documentation, not inherited silently. If the item is
merely missing information and the reporter is reachable, C. Choose D
whenever more than one channel exists, which is almost always.

Never apply a timer to a complaint, and never apply one to any item
where the venture is the party that failed to ask a question.

## Default

D, with C as the behaviour for anything that does not clearly sit in A
or B. Needs-info items carry `next_action_due` as a date strictly after
the day they were triaged, which is what makes the state reviewable
rather than a parking space. Retention of closed items follows the
privacy pack and is set once, per channel, not per ticket.

## Worked rulings

- **support-operations exemplar (2026-08, argued)**: three of forty
  items lacked any reproduction detail and were set to needs-info with
  a due date four days out, under C. Two billing complaints were run
  under B with acknowledgement timestamps recorded and no timer field
  present at all, so that no later tooling change could quietly apply
  one. See
  `packs/support-operations/exemplars/EX-SUPPORT-001-one-inbox-week.md`.
- **The stale bot is contested by its own operators (external,
  inherited)**: A is recorded here with that objection attached rather
  than cleaned up, because a guide that hides the strongest objection
  to an option is not a guide.
