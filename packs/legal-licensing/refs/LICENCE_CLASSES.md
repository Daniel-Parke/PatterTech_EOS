---
summary: The three-bucket allowlist with its reasons, the expression grammar that matters, and what to do with the values a scan actually returns
type: guide
tags: [security, delivery, tooling]
kind: fact
scope: estate
sources: [FRAG-LEGAL-LICENSING-01, FRAG-LEGAL-LICENSING-02, FRAG-LEGAL-LICENSING-05, FRAG-LEGAL-LICENSING-06, FRAG-LEGAL-LICENSING-07, FRAG-LEGAL-LICENSING-12]
volatility: slow
review: on-change-of:https://spdx.org/licenses/
review_by: 2027-11
---

# Reference: licence classes and the expressions that carry them

Level-three detail behind D1 and B2 in `packs/legal-licensing/PACK.md`.
The buckets below are a starting position for a venture that hosts a
service and publishes some libraries. Each venture copies the shape and
rewrites the reasons for its own promise, because the reason is the
part that transfers (FRAG-LEGAL-LICENSING-06).

## The three buckets

**Bucket one, freely usable.** Permissive licences asking for notice
and attribution and nothing more. Reason: the only obligation is to
keep a notice, which a build step can discharge, and the drafting
gradient puts explicit patent handling and simple notice at the top of
this family (FRAG-LEGAL-LICENSING-07). Automatic pass in CI, no
decision record, attribution collected into the artefact's notice file.

**Bucket two, usable with a recorded decision.** Weak reciprocal
licences whose obligations attach to the files they cover rather than
to the larger work, and any licence whose obligations we can name but
have to discharge deliberately. Reason: the obligation is real and
bounded, so it needs a decision and a place to put the source offer or
the notice, not a ban. CI flags, a human decides, the decision lands in
the venture's decision record with the component name and the
identifier.

**Bucket three, stop.** Strong reciprocal licences reaching the larger
work, network copyleft where we host a modified version, anything with
a field-of-use restriction, anything with no licence at all, and
anything the scan could not identify. Reason for the last two: absence
of a licence means exclusive copyright, and an unidentified component
is indistinguishable from an unlicensed one until someone looks
(FRAG-LEGAL-LICENSING-12). Blocking finding. Either the component goes,
or the question goes to a lawyer under B7.

The bucket is decided against the identifier, once, centrally. It is
never re-argued at the point of use. What is argued at the point of use
is only whether this venture performs the triggering event, which is
`packs/legal-licensing/guides/GD-LEGAL-001-copyleft-trigger.md`.

## The expression grammar that matters

Four constructs carry all the weight (FRAG-LEGAL-LICENSING-02):

| Construct | Means | What to do |
| --- | --- | --- |
| `AND` | every listed licence applies at once | discharge every obligation in the set, not the easiest one |
| `OR` | the recipient chooses | make the choice, record it, store one identifier |
| `WITH` | a named exception attaches | read the exception, it often moves the bucket |
| `+` | that version or later | pin what you actually rely on |

Precedence runs `+`, then `WITH`, then `AND`, then `OR`, with
parentheses overriding. The grammar is syntax and not semantics: a
well-formed expression tells you what a file claims about itself and
never whether the combination is lawful.

## The inventory step

D2 needs a concrete step or it is advice. The default is a full-tree
scan by a detector that compares licence texts against a curated
database and reads package manifests in the same pass
(FRAG-LEGAL-LICENSING-10), configured to emit one row per component
with path, identifier expression and detection confidence, written to a
file the merge gate reads. Which detector is a preference. Two things
are not: the scan covers the whole tree rather than the direct
dependencies, because the finding that matters is usually transitive,
and the output is routed to a person rather than compared against a
threshold.

## The values a scan actually returns

The tidy grammar does not cover the two values most real scan output
lands on. Treat them explicitly:

- `NOASSERTION`: the tool declined to conclude. Not a licence. Blocking
  under B2 until a person resolves it to an identifier or names the
  component in the decision record.
- `NONE`: no licence statement was found. This is the exclusive
  copyright case, and it is bucket three
  (FRAG-LEGAL-LICENSING-12).
- Empty or absent: same handling as `NONE`, and additionally evidence
  the inventory step is not doing its job.
- A licence not on the list: a `LicenseRef` with the full text stored
  alongside it, then bucket it by reading the text
  (FRAG-LEGAL-LICENSING-01).

## Three axes, not one

A rule that says use an open source licence and stops there has
collapsed three independent questions (FRAG-LEGAL-LICENSING-01):

- Does the licence restrict the wrong things? That is the openness
  criteria, and it is a definition of eligibility rather than a risk
  rating.
- Is it well drafted? A separate panel judgement, and a licence can
  pass the first test and still be rated poorly here
  (FRAG-LEGAL-LICENSING-07).
- Does it fit our promise? Only the venture can answer, and it is the
  question the imported buckets silently assume.

The identifier registry keeps openness and free-software status as two
separate flag columns on purpose and declines to merge them into one
verdict. A bucket table that merges them is making a claim its source
refuses to make.

## The network case, spelled out

The published three-bucket policies reason about source releases and
binary distribution (FRAG-LEGAL-LICENSING-06). A hosted service
distributes nothing, so those categories return no answer rather than a
permissive one. Network copyleft runs the other way: a modified version
reached by users over a network must offer them the corresponding
source, with no distribution needed (FRAG-LEGAL-LICENSING-05). If the
venture hosts, bucket three has to name that case explicitly or the
allowlist has a hole exactly where the money is.
