---
summary: How a venture decides licence questions at all, standing verdict against per-file declaration against certified process against scan and review
type: guide
tags: [security, delivery, tooling]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [FRAG-LEGAL-LICENSING-06, FRAG-LEGAL-LICENSING-07, FRAG-LEGAL-LICENSING-08, FRAG-LEGAL-LICENSING-10, FRAG-LEGAL-LICENSING-11]
review: on-change-of:https://www.apache.org/legal/resolved.html
review_by: 2028-01
---

# GD-LEGAL-002: Which compliance posture does this venture run?

## The question

Four materially different philosophies exist for keeping licensing
under control. They are not stages of maturity and they are not
alternatives to each other in every respect: two of them compose well.
The fork is which one carries the weight, because that decides what a
cold agent can check and what still needs a person.

## It depends on

- How many items per year, and what are the stakes per item?
- Does the venture publish, or only consume?
- Is there more than one person, and will there be next year?
- Can the answer be checked in CI, or does it need judgement each time?
- What happens to the arrangement when nobody remembers making it?

## Options

### A. The standing verdict

A small group decides once that licences fall into buckets, and
everyone downstream applies the verdict mechanically
(FRAG-LEGAL-LICENSING-06). A permissive family gradient published as
machine-readable data is the same idea, imported rather than read
(FRAG-LEGAL-LICENSING-07). Buys: high volume handled at near zero cost
per item, and no argument at the point of use. Costs: the verdict
encodes the decider's situation, so importing categories without their
reason produces a rule that misfires and then gets defended.

### B. Declare, do not detect

Licensing becomes a property of each file: identifier and copyright in
the header, a sibling file where comments are impossible, full texts
collected in one directory, bulk cases by glob, and a lint step that
turns the question into a CI pass or fail
(FRAG-LEGAL-LICENSING-08). Buys: the only pattern here a cold agent
satisfies without judgement, and evidence that lives in the repository.
Costs: real per-file overhead, and it proves declarations are present
and consistent, never that they are correct.

### C. Certify the process

Name where in the lifecycle compliance decisions happen, who makes
them, and show the arrangement survives the person who set it up
(FRAG-LEGAL-LICENSING-11). Buys: the sustainability question, which
nothing else here asks. Costs: written for organisations with staff to
assign roles to. A one-person venture satisfies the letter in an
afternoon and learns nothing, and self-certification against your own
checklist is the failure mode a standard is meant to prevent.

### D. Scan and review

A detector compares full licence texts against a curated database and
picks up copyrights, manifests and declared dependencies in one pass,
producing an inventory (FRAG-LEGAL-LICENSING-10). Buys: coverage of a
dependency tree nobody could read by hand. Costs: it reports what files
claim about themselves. Treated as a verdict producer it manufactures
false confidence, and its accuracy is unmeasured.

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

## Default

A plus D, with B on anything published, and C read once as a prompt
rather than adopted. That combination is what
`packs/legal-licensing/PACK.md` encodes in D1, D2 and D3.

## Evidence boundary

Every source here is a standard, a policy or a maintainer document, and
none is a measurement. No source read compares the four postures on
outcomes, and no source reports whether organisations running any of
them have fewer licence incidents (FRAG-LEGAL-LICENSING-11). The
gradient ratings are the collective judgement of a group of lawyers,
not a measurement and not a legal opinion for any specific use
(FRAG-LEGAL-LICENSING-07). The detection accuracy claim is a vendor
claim with no published figure (FRAG-LEGAL-LICENSING-10). The decision
rule above is therefore an argument about cost and checkability, and it
should be read as one.

## Worked rulings

- **PatterTech EOS legal-licensing pack (2026-08, argued)**: A plus D
  as the spine, B for published repositories, C deferred until a second
  person joins. Argued from the cost asymmetry: A and D are cheap per
  item, B is cheap only where the artefact is public, and C prices a
  role structure a venture does not have.
- **PatterTech EOS itself (2026-08, inherited)**: A plus D. This
  repository publishes documentation with almost no dependency tree, so
  B would be ceremony over prose files.
