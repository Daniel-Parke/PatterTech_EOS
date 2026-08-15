---
id: GD-LEGAL-002
summary: How a venture decides licence questions at all, standing verdict against per-file declaration against certified process against scan and review
kind: wargame
type: wargame
tags: [delivery, eos, security, tooling, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-LEGAL-008, DOC-LEGAL-009, DOC-LEGAL-010]
applies_when: [adds_dependency]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0342, EV-0343, EV-0344, EV-0346, EV-0347]
review: on-change-of:https://www.apache.org/legal/resolved.html
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-LEGAL-002: Which compliance posture does this venture run?

## Decision question and stakes

Four materially different philosophies exist for keeping licensing
under control. They are not stages of maturity and they are not
alternatives to each other in every respect: two of them compose well.
The fork is which one carries the weight, because that decides what a
cold agent can check and what still needs a person.

## Doctrines or coverage gap under pressure

- `DOC-LEGAL-008` (default): A three-bucket allowlist keyed on identifiers, with the reason written next to each bucket.
- `DOC-LEGAL-009` (default): The scanner produces the inventory and a person produces the verdict.
- `DOC-LEGAL-010` (default): Per-file declaration for anything published.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- How many items per year, and what are the stakes per item?
- Does the venture publish, or only consume?
- Is there more than one person, and will there be next year?
- Can the answer be checked in CI, or does it need judgement each time?
- What happens to the arrangement when nobody remembers making it?

Applicability is `adds_dependency`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. The standing verdict

A small group decides once that licences fall into buckets, and
everyone downstream applies the verdict mechanically
(EV-0342). A permissive family gradient published as
machine-readable data is the same idea, imported rather than read
(EV-0343). Buys: high volume handled at near zero cost
per item, and no argument at the point of use. Costs: the verdict
encodes the decider's situation, so importing categories without their
reason produces a rule that misfires and then gets defended.

### B. Declare, do not detect

Licensing becomes a property of each file: identifier and copyright in
the header, a sibling file where comments are impossible, full texts
collected in one directory, bulk cases by glob, and a lint step that
turns the question into a CI pass or fail
(EV-0344). Buys: the only pattern here a cold agent
satisfies without judgement, and evidence that lives in the repository.
Costs: real per-file overhead, and it proves declarations are present
and consistent, never that they are correct.

### C. Certify the process

Name where in the lifecycle compliance decisions happen, who makes
them, and show the arrangement survives the person who set it up
(EV-0347). Buys: the sustainability question, which
nothing else here asks. Costs: written for organisations with staff to
assign roles to. A one-person venture satisfies the letter in an
afternoon and learns nothing, and self-certification against your own
checklist is the failure mode a standard is meant to prevent.

### D. Scan and review

A detector compares full licence texts against a curated database and
picks up copyrights, manifests and declared dependencies in one pass,
producing an inventory (EV-0346). Buys: coverage of a
dependency tree nobody could read by hand. Costs: it reports what files
claim about themselves. Treated as a verdict producer it manufactures
false confidence, and its accuracy is unmeasured.

## Failure premises

### Premortem for A. The standing verdict

Assume `A. The standing verdict` was selected and the outcome failed. Test this option's stated failure mechanism first: per item, and no argument at the point of use. Costs: the verdict encodes the decider's situation, so importing categories without their reason produces a rule that misfires and then gets defended.

### Premortem for B. Declare, do not detect

Assume `B. Declare, do not detect` was selected and the outcome failed. Test this option's stated failure mechanism first: real per-file overhead, and it proves declarations are present and consistent, never that they are correct.

### Premortem for C. Certify the process

Assume `C. Certify the process` was selected and the outcome failed. Test this option's stated failure mechanism first: written for organisations with staff to assign roles to. A one-person venture satisfies the letter in an afternoon and learns nothing, and self-certification against your own checklist is the failure mode a standard is meant to prevent.

### Premortem for D. Scan and review

Assume `D. Scan and review` was selected and the outcome failed. Test this option's stated failure mechanism first: it reports what files claim about themselves. Treated as a verdict producer it manufactures false confidence, and its accuracy is unmeasured.

## Decision rule

- Consuming a dependency tree, any size: A for the verdict, D for the
  inventory that feeds it. Neither works alone.
- Publishing anything: add B for the published repository. This is what
  makes the claim checkable rather than asserted.
- Not publishing: repository-level declaration is enough, and B is
  overhead you are paying for nobody.
- One person: skip C as a certification and read it once as a
  question about what happens when you forget. Revisit when a second
  person arrives.
- Never D alone. A scan that ran and reported nothing is the most
  common way a compliance step passes while proving nothing.

## Safe default

A plus D, with B on anything published, and C read once as a prompt
rather than adopted. That combination is what
`packs/legal-licensing/PACK.md` encodes in D1, D2 and D3.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **How many items per year, and what are the stakes per item?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A plus D, with B on anything published, and C read once as a prompt rather than adopted. That combination is what `packs/legal-licensing/PACK.md` encodes in D1, D2 and D3.

**Exit condition:** Stop or roll back the selected branch when per item, and no argument at the point of use. Costs: the verdict encodes the decider's situation, so importing categories without their reason produces a rule that misfires and then gets defended, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: How many items per year, and what are the stakes per item?

## Counter-evidence and transfer limits

### Evidence boundary

Every source here is a standard, a policy or a maintainer document, and
none is a measurement. No source read compares the four postures on
outcomes, and no source reports whether organisations running any of
them have fewer licence incidents (EV-0347). The
gradient ratings are the collective judgement of a group of lawyers,
not a measurement and not a legal opinion for any specific use
(EV-0343). The detection accuracy claim is a vendor
claim with no published figure (EV-0346). The decision
rule above is therefore an argument about cost and checkability, and it
should be read as one.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
