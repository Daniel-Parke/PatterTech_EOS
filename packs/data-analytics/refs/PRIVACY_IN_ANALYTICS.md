---
summary: What the analytics layer may hold about a person, the identifier ladder behind B3, UK duties, and how to read a differential privacy claim
type: foundation
tags: [data, pii, security]
kind: fact
scope: estate
sources: [EV-0041, EV-0225]
volatility: slow
review: on-change-of:EV-0225
---

# Privacy in analytics reference

Level-three material behind binding requirement B3. Threat modelling,
access control and secret handling sit in
`packs/security-privacy/PACK.md`; this file covers only what the
analytics layer is allowed to hold and why.

## The cheapest control is not collecting it

Every source in this pack's research is about protecting data you have
already gathered, and none of them opens with the question of whether to
gather it. Ask it first. A column that never lands needs no lawful
basis, no retention rule, no deletion path and no privacy budget.

## The identifier ladder

Work down this list and stop at the first rung that answers the
question you actually have.

1. **No identifier.** Aggregate counts by dimension. Answers most
   product questions.
2. **Per-session surrogate.** Enough for funnel and conversion analysis
   within a visit, useless for retention.
3. **Stable surrogate key.** A key minted by your system with no meaning
   outside it. Answers retention and cohort questions. This is the
   default under D8.
4. **Salted hash of a natural identifier.** Use when the analytics layer
   has to join to a system you do not control. The salt is a secret and
   the hash is still personal data if you can reverse the join.
5. **The natural identifier itself.** Email address, account number,
   postcode. Requires a recorded lawful basis under B3 and a stated
   reason why rungs one to four do not answer the question.

Copying a source column forward because it was in the source is how
rung five gets reached by accident. That is the failure B3 exists to
prevent.

## UK duties, in short

- A lawful basis is recorded before processing, and it is a recorded
  decision rather than a privacy notice paragraph (EV-0225).
- A named complaints path exists for data subjects, which is statutory
  rather than good practice (EV-0225).
- The ceremony around all of this scales with risk to people: full
  assessments are for high-risk processing, and documentation is
  proportionate (EV-0041). A two-person venture doing aggregate product
  analytics on surrogate keys is not at the top of that scale, and
  pretending otherwise produces paperwork instead of protection.

Scope note. The Act's commencement is phased and the regulator's
guidance interpreting it was still being published through 2026. This
file has an on-change trigger for that reason. Nothing here is legal
advice; it is the engineering consequence of duties recorded in the
ledger.

## Reading a differential privacy claim

Differentially private counts, sums, means, variances and quantiles with
budget accounting are available as Apache-2.0 libraries, so the barrier
is design rather than implementation (`EV-0321`). Before
believing any such claim, in your own system or a vendor's, ask:

- **What is the privacy unit?** One row, one user, one user per day. The
  guarantee means completely different things for each.
- **What are the parameters?** A claim without its parameters stated is
  not a claim (`EV-0320`).
- **Who limits contribution?** The primitives assume each user
  contributes a bounded number of rows per partition and do not enforce
  it. Contribution limiting is the caller's job, and getting it wrong
  voids the guarantee silently. This is the load-bearing caveat.
- **What does the implementation do that the proof does not cover?**
  Evaluation is layered rather than a single number, and the hazards
  that open between the mathematics and the running software are named
  explicitly in the guidance (`EV-0320`).

For a small venture the usual honest answer is that this machinery is
not the right control, and collecting less is. Aggregate statistics are
all it covers; it does nothing for row-level sharing or for
re-identification risk in an event stream.

## Retention

Retention is a rule the contract carries (B1), not a convention. State
the period per table, state what happens at the end of it, and make the
deletion a scheduled job rather than an intention. A retention rule with
no job is the same shape of failure as a quality rule with no gate.
