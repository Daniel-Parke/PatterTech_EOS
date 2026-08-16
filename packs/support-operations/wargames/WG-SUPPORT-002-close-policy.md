---
id: WG-SUPPORT-002
summary: May an item close without an answer, and on whose clock?
kind: wargame
type: wargame
tags: [eos, ops, pii, product, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-SUPPORT-002]
applies_when: [has_customer_inbound]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0041]
review: on-change-of:ISO-10002-revision
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-SUPPORT-002: May an item close without an answer, and on whose clock?

## Decision question and stakes

Two maintained sources give opposite instructions. A large public
tracker closes unreproducible reports after twenty days of silence and
marks anything untouched for ninety as stale
(EV-0424). The complaints standard says the loop
closes only once the complainant has been told the outcome
(EV-0425). Both are defensible, for different
relationships. The failure is letting a ticketing tool's default answer
the question by accident.

## Doctrines or coverage gap under pressure

- `DOC-SUPPORT-002` (binding): A support inbox is a personal-data store and is run as one.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `has_customer_inbound`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Close on silence, with a timer
Unreproducible or information-starved items close automatically after a
stated silence, and stale items are labelled after a longer one
(EV-0424). Buys a finite queue with no human cost
and a defensible answer to "why is this still open". Costs real bugs:
the maintainers of the project that runs the best-known implementation
have filed complaints about their own bot closing important issues,
which is honest counter-evidence from inside the practice.

### B. Close on answer only
Nothing closes until the reporter has been told an outcome, even if the
outcome is "we cannot reproduce this and are stopping here"
(EV-0425). Buys fairness that survives a challenge,
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

## Failure premises

### Premortem for A. Close on silence, with a timer

Assume `A. Close on silence, with a timer` was selected and the outcome failed. Test this option's stated failure mechanism first: and a defensible answer to "why is this still open". Costs real bugs: the maintainers of the project that runs the best-known implementation have filed complaints about their own bot closing important issues, which is honest counter-evidence from inside the practice.

### Premortem for B. Close on answer only

Assume `B. Close on answer only` was selected and the outcome failed. Test this option's stated failure mechanism first: a standing human obligation that scales linearly with volume.

### Premortem for C. Needs-info with a due date, then a human decision

Assume `C. Needs-info with a due date, then a human decision` was selected and the outcome failed. Test this option's stated failure mechanism first: a recurring review slot, which is the thing that actually gets skipped.

### Premortem for D. Split by channel, with the policy written per channel

Assume `D. Split by channel, with the policy written per channel` was selected and the outcome failed. Test this option's stated failure mechanism first: one more thing to configure and one more thing to keep true.

## Decision rule

If the reporter pays, B. If the channel is a public tracker with
volunteer reporters, A is available and the timer values are stated in
the channel's own documentation, not inherited silently. If the item is
merely missing information and the reporter is reachable, C. Choose D
whenever more than one channel exists, which is almost always.

Never apply a timer to a complaint, and never apply one to any item
where the venture is the party that failed to ask a question.

## Safe default

D, with C as the behaviour for anything that does not clearly sit in A
or B. Needs-info items carry `next_action_due` as a date strictly after
the day they were triaged, which is what makes the state reviewable
rather than a parking space. Retention of closed items follows the
privacy pack and is set once, per channel, not per ticket.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Whether the reporter is under contract or paying.** This is the load-bearing factor and it is not close.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** D, with C as the behaviour for anything that does not clearly sit in A or B. Needs-info items carry `next_action_due` as a date strictly after the day they were triaged, which is what makes the state reviewable rather than a parking space. Retention of closed items follows the privacy pack and is set once, per channel, not per ticket.

**Exit condition:** Stop or roll back the selected branch when and a defensible answer to "why is this still open". Costs real bugs: the maintainers of the project that runs the best-known implementation have filed complaints about their own bot closing important issues, which is honest counter-evidence from inside the practice, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Whether the reporter is under contract or paying.** This is the load-bearing factor and it is not close.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****Whether the reporter is under contract or paying.** This is the load-bearing factor and it is not close.** and ****Who holds the missing information.** A timer punishes the person who cannot supply what was never asked for.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
