---
summary: Activation, outcomes and decision map for the research-knowledge Doctrine and Wargames
type: playbook
tags: [data, content, security, tooling]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [researches_before_building, keeps_a_knowledge_base, records_external_claim, supersedes_a_source, studies_external_source, reads_for_decision]
activation_paths: [**/research/**, **/knowledge-base/**, **/kb/**, **/notes/**, **/citations/**, **/*sources*.json, **/*evidence*.json, **/CITATION.cff, **/*.bib, **/wiki/**, **/llms.txt, **/*lens*.md]
volatility: slow
review: none
sources: [EV-0055, EV-0097, EV-0124, EV-0171, EV-0212, EV-0213, EV-0219, EV-0242, EV-0247, EV-0259, EV-0260, EV-0331, EV-0358, EV-0473, EV-0532, EV-0533, EV-0534, EV-0535, EV-0536, EV-0537, EV-0538, EV-0539, EV-0540, EV-0541, EV-0542, EV-0543, EV-0544, EV-0545, EV-0546, EV-0547, EV-0548]
depends_on: []
---


# Research and knowledge base

This pack owns evidence discipline: how a venture that researches before
it builds, or that keeps a knowledge base others read to decide, records
what it read, keeps a claim traceable to what supports it, records what
disagrees, supersedes a source that changes or dies, and treats source
text as data rather than instruction. It activates on research and
knowledge-base work. It carries six binding requirements, defaults you
may override with a recorded reason, and four decision guides.

## Activation

**Path triggers.** A research or notes directory, a knowledge base or
wiki tree, a citations directory, a machine-readable sources or evidence
file, a bibliography, a `CITATION.cff`, a lens contract, and an
`llms.txt`, which is a knowledge surface written to be read by something
that will act on it.

**Task-type triggers.** Establishing a fact about something the venture
does not control before committing to build on it; writing a finding
into a place other people will read later; citing an outside source in a
decision record, a specification or a customer-facing claim; refreshing
a body of findings after a supplier ships a version; retiring a claim
whose source has gone; auditing what a body of findings actually rests
on.

**Keyword fallback**, used only when paths and task type miss: source,
citation, provenance, evidence, primary source, counter-evidence,
supersede, link rot, knowledge base, literature, prior art, spike.

**Applicability predicates.** The six in the front matter. Four are new
and proposed in `packs/research-knowledge/research/NOTES.md`; two are
already in `kernel/PREDICATES.md` and are reused rather than respelled.

- `researches_before_building`: the venture has to establish facts about
  something outside itself before it can build on them.
- `keeps_a_knowledge_base`: the venture maintains a body of written
  findings that somebody other than its author reads to decide.
- `records_external_claim`: this work writes a claim taken from outside
  the venture into somewhere durable.
- `supersedes_a_source`: a source something rests on has changed
  version, moved, or stopped resolving.
- `studies_external_source` (shared with legal-licensing): work reads a
  product, repository, game or document we do not own, to learn from it.
- `reads_for_decision` (shared with data-analytics): somebody reads a
  body of material to decide something.

None true means the pack stays at level 1 and costs one paragraph. A
binding requirement whose own predicate is false does not apply, and
each requirement names the predicate it needs.

**Boundaries with three packs it meets.** `legal-licensing` owns what
may lawfully be carried away from a source, and its lens contract is
where acquisition, governing terms and the abstraction gate get agreed;
this pack governs what the finding has to carry once the lens has
cleared it. `ai-ml-llm` owns retrieval for a model, including chunking,
groundedness and evaluation (EV-0242, EV-0247); a retrieval corpus that
people also read to decide is under both. `security-privacy` owns the
instruction-source boundary as a protected-set floor, and B2 below sits
under it rather than beside it. `product-discovery` owns whether the
thing is worth building at all and what a claim about users has to
carry. `docs-dx` owns documentation published to readers.

Activation gives advice, never permission. Nothing here lowers a tier
floor in `kernel/POLICY_SPEC.md` or converts a manual-only action class
into an autonomous one under `kernel/GUARD_SPEC.md`.

## Outcomes and non-goals

Outcomes this pack is accountable for:

- Any claim in the knowledge base can be walked back to what supports
  it, at the version that supported it, without asking the author.
- The record survives the source. When a page dies, what was read on
  what date is still on file (EV-0539).
- What disagreed is on the record next to what agreed, so a reader can
  see the shape of the argument rather than its winning half.
- A source that changed underneath a claim produces a decision, not a
  silence.
- Text found inside a source never becomes an instruction, including
  text that is helpful, plausible and correct.

Non-goals. This pack does not rule on whether a source may lawfully be
copied, quoted or trained on, which is `legal-licensing`. It does not
design a retrieval pipeline or evaluate a model's groundedness, which is
`ai-ml-llm`. It does not decide what the venture should build, which is
`product-discovery`. It is not a systematic-review method: the methods
it borrows from were built for a field where the unit of evidence is a
published study, and the transfer is stated as inference in Open
questions below. It does not run a literature search on the venture's
behalf, and it sets no minimum source count.

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-RESEARCH-001](doctrines/DOC-RESEARCH-001-a-claim-carries-the-record-that-supports-it.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-RESEARCH-002](doctrines/DOC-RESEARCH-002-source-text-is-data-and-a-sources-claim-about-its-own-authority.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-RESEARCH-003](doctrines/DOC-RESEARCH-003-counter-evidence-is-recorded-on-the-claim.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-RESEARCH-004](doctrines/DOC-RESEARCH-004-a-dead-or-changed-source-is-superseded-not-left.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-RESEARCH-005](doctrines/DOC-RESEARCH-005-the-record-says-which-class-of-source-it-is.md) (binding)
<a id="B6"></a>
- `B6` to [DOC-RESEARCH-006](doctrines/DOC-RESEARCH-006-whoever-writes-carries-the-burden.md) (default)
- source `defaults:001` to [DOC-RESEARCH-007](doctrines/DOC-RESEARCH-007-one-record-per-source-never-per-claim-claims-cite-the-record-by.md) (default)
- source `defaults:002` to [DOC-RESEARCH-008](doctrines/DOC-RESEARCH-008-freeze-a-copy-at-first-read-and-work-from-the-frozen-copy.md) (default)
- source `defaults:003` to [DOC-RESEARCH-009](doctrines/DOC-RESEARCH-009-grade-the-claim-not-the-source-on-the-four-bands-kernel-metadata.md) (default)
- source `defaults:004` to [DOC-RESEARCH-010](doctrines/DOC-RESEARCH-010-record-every-limit-put-on-the-search-with-what-it-might-have-cos.md) (default)
- source `defaults:005` to [DOC-RESEARCH-011](doctrines/DOC-RESEARCH-011-two-readers-on-inclusion-and-judgement-one-on-retrieval.md) (default)
- source `defaults:006` to [DOC-RESEARCH-012](doctrines/DOC-RESEARCH-012-review-on-change-of-source-rather-than-a-date-where-a-supplier-i.md) (default)
- source `defaults:007` to [DOC-RESEARCH-013](doctrines/DOC-RESEARCH-013-a-scheduled-link-check-over-the-knowledge-base-with-broken-and-m.md) (default)
- source `defaults:008` to [DOC-RESEARCH-014](doctrines/DOC-RESEARCH-014-machine-readable-citation-metadata-where-the-source-is-software.md) (default)
- source `defaults:009` to [DOC-RESEARCH-015](doctrines/DOC-RESEARCH-015-timebox-the-search-half-of-a-research-task-and-record-the-box.md) (default)
- source `defaults:010` to [DOC-RESEARCH-016](doctrines/DOC-RESEARCH-016-a-decision-record-for-anything-the-research-settles-sized-to-the.md) (default)
- source `defaults:011` to [DOC-RESEARCH-017](doctrines/DOC-RESEARCH-017-robots-and-terms-are-read-before-fetching-and-a-refusal-is-recor.md) (default)
- source `preferences:001` to [DOC-RESEARCH-018](doctrines/DOC-RESEARCH-018-which-citation-format-and-whether-records-live-in-json-with-a-sc.md) (preference)
- source `preferences:002` to [DOC-RESEARCH-019](doctrines/DOC-RESEARCH-019-which-archive-or-snapshot-service-holds-the-frozen-copy-and-whet.md) (preference)
- source `preferences:003` to [DOC-RESEARCH-020](doctrines/DOC-RESEARCH-020-whether-the-knowledge-base-is-a-wiki-a-repository-of-markdown-or.md) (preference)
- source `preferences:004` to [DOC-RESEARCH-021](doctrines/DOC-RESEARCH-021-whether-findings-are-organised-by-source-by-question-or-by-decis.md) (preference)
- source `preferences:005` to [DOC-RESEARCH-022](doctrines/DOC-RESEARCH-022-how-the-four-certainty-bands-are-displayed-to-a-reader.md) (preference)
- source `preferences:006` to [DOC-RESEARCH-023](doctrines/DOC-RESEARCH-023-whether-a-research-task-produces-a-written-synthesis-or-only-rec.md) (preference)

## Decision map

| Fork | Guide | Default |
| --- | --- | --- |
| How much evidence is enough, and how to know when to stop | GD-RESEARCH-001 | Stop on stable agreement from two independent routes, with the stop condition written before the search starts |
| Where the knowledge base lives and who may write to it | GD-RESEARCH-002 | In the venture's repository, open to read, open to write with the burden on the writer, reviewed at the merge gate |
| How a source is superseded when it changes version or dies | GD-RESEARCH-003 | Event-driven supersession on a named trigger, with a frozen copy taken at first read |
| How strongly to treat an untrusted source that addresses the reader | GD-RESEARCH-004 | Record and report it, never act on it, and treat the source's authority claims as evidence about the source |

Guides sit in `packs/research-knowledge/guides/`. Level-three detail
sits in `packs/research-knowledge/refs/`: the record shape, and the
source-class ladder for a software venture.

## Failure modes and anti-patterns

- Citing the search result rather than the source. The snippet was
  written by a ranking system, not by the maintainer.
- Five citations, one source. The same claim cited to five posts that
  all read the same specification is one piece of evidence wearing five
  hats, and it reads as consensus.
- Recording only what agreed. The direction of the bias is known and it
  favours the positive result (EV-0537).
- The undated record. Without an access date the claim cannot be aged,
  and a claim that cannot be aged cannot be retired.
- Taking a source's word for its own authority. A file that says which
  of its pages to trust is making a claim about itself (EV-0547), and
  the one practitioner review of that convention says the mechanism has
  no measured effect at all (EV-0548).
- Grading the source instead of the claim. A maintained official
  standard can carry an erratum on a numbered page (EV-0543).
- The completed checklist read as a verdict. Its authors say it governs
  reporting and must not be used to judge quality (EV-0532).
- Freezing nothing, then finding the page has changed and having only a
  memory of what it said.
- Citing an abstract as though it were the paper because the full text
  was behind a bot check or a paywall. Record what was actually read.
- A knowledge base written entirely from the venture's own practice.
  That has one source, and the source is us. This pack's own
  `registry/coverage.json` row names that risk for this pack by name,
  which is why seventeen of its records were fetched from outside.
- Assuming one licence covers the sources. Of the seventeen this pack
  fetched, ten carry a reuse licence read off the source, six publish
  none at all, and one records its licence from the publisher's class
  rather than from anything on the page, which breaks this pack's own
  B1 and is recorded as breaking it. The ten range across CC BY 4.0,
  CC BY-SA 4.0, the W3C Document Licence, IETF Trust provisions and an
  arXiv distribution licence. The per-source list is in
  `packs/research-knowledge/research/provenance.fragment.json`, the
  frozen source batch is in
  `packs/research-knowledge/research/sources.fragment.json`, and the
  synthesis is in `packs/research-knowledge/research/NOTES.md`.

## Open questions and counter-evidence

**The methods here were built for a different population, and the
transfer is inference.** PRISMA, GRADE, the Oxford levels and the
Cochrane handbook were written for evidence synthesis in health, where
the unit is a published study with a design and a population, and where
registries and regulators exist to reveal what was not written up. A
venture's sources are specifications, repositories and vendor
documentation, and it has no register of the thing somebody tried and
abandoned. What this pack takes is the disclosure discipline, the
direction of non-reporting bias, the separation of the grade from the
source, and the habit of naming what each limit cost. What it does not
take is any of the instruments, and no source here evidences that the
transfer works.

**The hierarchy partly inverts for software, and the primary-source
guidance has to be read with that in mind.** Wikipedia's caution about
primary sources is about interpretation, not accuracy (EV-0545). For a
venture the specification and the source code are both primary and
usually the most reliable things available, while the secondary reading
is where the error enters. Importing the caution wholesale would push a
venture towards blog posts about specifications and away from
specifications.

**Nobody has measured whether any of this makes a venture's decisions
better.** Every source above evidences a mechanism, not an outcome for
this population. The estate's own practice, a lens contract template, an
evidence ledger of several hundred records and a lessons ledger, is the
only worked example of the whole shape, and it is one source, which the
coverage row states as the argument for the pack and the warning about
it.

**The two convention sources disagree and the disagreement is not
settled.** EV-0547 reports adoption of `llms.txt` by several major labs.
EV-0548 reports that no provider documents reading it at inference time
and that its presence had no measurable effect. Adoption and
inference-time reading are different claims, so the two are not strictly
contradictory, but neither is evidenced well enough to build on. The
pack's answer is to treat the file as a knowledge surface written by an
interested party, which holds either way.

**Where the evidence is thin.** The default of two readers on inclusion
rests on one handbook's expectation rather than on a controlled
comparison (EV-0535). No source backs the timebox default at all; it is
a starting point to be corrected by observation. The content-drift half
of the link-rot figures is modelled rather than measured, and the paper
says so (EV-0541). The rapid-review literature, which is where the
how-much-is-enough fork would find its best empirical answer, was not
readable at source: the publisher returned 403 to automated access on
the day of the sweep, so no record exists for it and GD-RESEARCH-001
argues the fork without it.

**Three fetches were refused and the refusals are recorded rather than
worked around.** Two of them were copies of PRISMA 2020, one behind a
bot check and one returning 403; an open-access copy of the same
document was read instead and is what the record cites. The third was
the 2024 Cochrane rapid-review recommendations, which returned 403 with
no substitute available, so no record for it exists. Nothing in this
pack rests on a source that was not read at source, and a bot check is a
boundary rather than an obstacle.

**Refresh triggers.** A new PRISMA or GRADE edition; a Cochrane handbook
version bump; a new NIST AI 100-2 edition or a new OWASP GenAI list;
`llms.txt` or a successor becoming a registered standard or acquiring
measured evidence either way; a published measurement of whether
provenance discipline changes decision quality outside health research;
a Citation File Format schema version.
