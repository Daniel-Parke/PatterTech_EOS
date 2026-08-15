---
summary: How the research-knowledge pack was assembled, the predicates it proposes, what the corpus disagrees about and what it could not close
kind: record
scope: eos-internal
type: guide
tags: [eos, data, content]
review: on-change-of:packs/research-knowledge
---

# Research notes: research and knowledge base

## Where the material came from

One research pass on 2026-08-15, against the
`research-and-knowledge-base` row in `registry/coverage.json` as it
stood before this pack existed. That row stated the case for the pack
and the warning about it in the same sentence: the practice already
exists in this repository unpacked, in `kernel/templates/LENS.tpl.md`,
an evidence ledger of several hundred records with a schema, and
`registry/lessons.json`, and a pack written only from our own practice
has one source and that source is us.

So the sweep was pointed outward on purpose. Seventeen sources were
fetched at source and recorded in
`packs/research-knowledge/research/sources.fragment.json`, across five
bodies of published practice that already own parts of this problem:

- **Reporting and synthesis method.** PRISMA 2020, the Cochrane
  handbook chapters on searching, on prospective approaches and on
  missing results.
- **Evidence grading.** The GRADE approach, the Oxford levels.
- **Provenance and citation.** W3C PROV-O, the FAIR principles, the
  Citation File Format.
- **Supersession and decay.** The reference-rot study, RFC 7089.
- **Untrusted content addressed to a reader.** NIST AI 100-2 E2025, the
  2023 indirect prompt injection paper, and the two pages on the
  `llms.txt` convention that disagree with each other.

Two Wikipedia policies were read for the source-class definitions and
for the burden-of-evidence rule, which is the only published governance
model for an open knowledge base with decades of adversarial use behind
it.

Fourteen sources the pack cites were already in `registry/evidence.json`
and are cited by their existing EV ids rather than re-recorded: EV-0055,
EV-0097, EV-0124, EV-0171, EV-0212, EV-0213, EV-0219, EV-0242, EV-0247,
EV-0259, EV-0260, EV-0331, EV-0358 and EV-0473. Every one of the
seventeen new URLs was checked against the ledger before the fragment
file was written, and none of them deduplicates against an existing row.

## Predicates proposed

Four new names, all belonging in the **Evidence and deciding** group of
`kernel/PREDICATES.md`, which is where `reads_for_decision`,
`cites_user_claim` and `runs_experiment` already sit. The vocabulary is
integrator-owned, so these are proposals: check S021 will fail on
`packs/research-knowledge/PACK.md` until they are added, and that
failure is expected.

| predicate | settled by | true when |
| --- | --- | --- |
| `researches_before_building` | 18 | the venture has to establish facts about something outside its own control before it can build on them, so research is one of the material workstreams rather than something that happens incidentally |
| `keeps_a_knowledge_base` | 18 | the venture maintains a body of written findings that somebody other than its author reads in order to decide something |
| `records_external_claim` | task | this piece of work writes a claim taken from outside the venture into somewhere durable that others will read |
| `supersedes_a_source` | task | a source that something already recorded rests on has changed version, moved, or stopped resolving |

Both venture facts are settled by interview question 18, what the
material workstreams are, which is the question that already settles
`has_test_suite`, `encodes_domain_rule` and `builds_retrieval`. Neither
is answerable from question 5, because a knowledge base can be entirely
internal and never be a surface the venture ships.

Both task facts are settled from the record or the diff, like
`studies_external_source` and `reads_for_decision`, because whether a
given change writes down an outside claim or retires a dead source is
not knowable at Session 0 and is not stable afterwards.

**Two existing predicates are reused rather than respelled**, which is
the point of the vocabulary being controlled:

- `studies_external_source`, owned by `legal-licensing` and already
  defined as work reading a product, repository, game or document we do
  not own in order to learn from it. That is exactly the condition B2
  needs. Adding a `reads_untrusted_source` alongside it would have been
  the `processes_personal_data` mistake a second time, and ADR-0010 is
  the record of what that cost.
- `reads_for_decision`, owned by `data-analytics` and defined as
  somebody reading data to decide something. A body of findings read to
  decide is the same fact about the work, so the two packs share it.

Two names were considered and dropped. `cites_external_source` was
dropped as a near-synonym of `records_external_claim` that would have
split on whether the citation was formal. `maintains_evidence_ledger`
was dropped because it names a mechanism rather than a fact, and
`keeps_a_knowledge_base` is the fact underneath it.

## How the rules were graded

ADR-0008 sets the test: binding needs a basis in law, standard or
empirical evidence, and the rule must prevent a concrete failure that is
serious or hard to reverse. Six cleared it and several did not.

- **B1, B3, B4 and B5** bind on `basis: standard`. Each rests on
  published guidance from a maintained body, each prevents a failure
  that is discovered late and cannot be repaired by care afterwards, and
  each names the predicate that has to be true for it to apply at all.
- **B2** does not bind on its own authority. The floor is
  `packs/security-privacy` B1, which is a protected-set item, and B2
  states only the research-specific case that floor does not obviously
  cover. It is written to sit under that requirement rather than beside
  it, and it must not be read as this pack legislating in the security
  pack's territory.
- **B6** is the weakest of the six and is labelled so in the pack. Its
  basis is one project policy plus this estate's practice, and its
  removal rule had to be changed on import, from may be removed to is
  marked unsourced, because the original depends on a history that most
  venture knowledge bases do not have. A rule adapted on import is not
  the rule the source evidenced, and the pack says so.

Three candidates were demoted to defaults rather than binding:

- **Two readers on inclusion.** The support is one handbook's
  expectation, not a controlled comparison, and the cost of getting it
  wrong is a missed source rather than a wrong one. It is a default.
- **Freeze a copy at first read.** This one is close. The mechanism is
  well evidenced and the failure is silent, which argues for binding.
  It stayed a default because a venture with a well-archived,
  version-pinned source set can meet B4 without it, and a binding rule
  that a compliant venture has to record an exception to is a badly
  drawn rule.
- **A timebox on the search half.** No source backs it at all. It is in
  the defaults table with that stated, as a starting point to be
  corrected by observation.

One candidate was left out of the pack entirely. A minimum source count
per claim was proposed and rejected: it is satisfiable by padding, the
one standard that speaks to it refuses to give a threshold and gives the
cost of each limit instead, and a number would have become the thing
people optimised.

## What the corpus disagrees about

**Whether primary sources should be preferred.** The clearest published
definition of the three source classes is cautious about primary
sources: they carry straightforward description, and interpretation of
them needs a secondary source. For a software venture that ordering
partly inverts, because the specification and the source code are
primary and the secondary reading is where the error enters. The pack
takes the classification and the rule about attributing interpretation,
and explicitly refuses the preference ordering, with the reason in
`packs/research-knowledge/refs/source-classes.md`. That is an
adaptation and not a finding, and both files say so.

**Whether search limits cost anything.** One chapter states that
searching a single database is inadequate and that date cut-offs picked
for convenience are advised against, and in the same passage records
that language
limits usually change nothing, naming three fields where they do. The
reconciliation the pack uses is that the answer is per-limit and
per-field, which is why the default is to record each limit with what it
might have cost rather than to forbid or permit limits generally.

**Whether the navigation convention works at all.** The proposal reports
adoption by several major labs. The one practitioner review available
reports that no provider documents reading the file at inference time
and that its presence had no measurable effect on citation likelihood.
Adoption and inference-time reading are different claims, so the two are
not strictly contradictory, but neither is evidenced well enough to
build on. The pack's answer holds either way: treat the file as an
interested party's claim about itself.

**Whether indirect injection is defensible.** The 2023 paper states
mitigations were lacking. Later ledger rows report out-of-band defences
cutting attack success substantially (EV-0214) and name structural
patterns that fix the action set before untrusted text is seen
(EV-0473), while both official taxonomies still decline to claim a
complete defence. The pack does not re-argue this; it points at
`packs/security-privacy` GD-SEC-001, which does.

## Questions the research could not close

1. **Nothing measures whether any of this improves a venture's
   decisions.** Every source evidences a mechanism, and none evidences
   an outcome for this population. This is the largest hole in the pack
   and it sits under all six binding requirements.
2. **The whole method transfer is inference.** PRISMA, GRADE, the Oxford
   levels and the Cochrane handbook were built for a field where the
   unit of evidence is a published study and where registries and
   regulators reveal what was not written up. A venture has none of
   that. No source evidences that the discipline survives the move.
3. **The rapid-review literature was not readable.** That is where the
   best empirical answer to GD-RESEARCH-001 lives, because it measures
   what abbreviating a full search actually costs. The publisher
   returned 403 to automated access on the day of the sweep, so no
   record exists and the fork is argued without it. This is the first
   thing the next pass should fix.
4. **Content-drift rates are modelled, not measured.** The reference-rot
   study's authors state they had no real data on how often referenced
   resources change, and assumed representativeness thresholds instead.
   The direction is solid; no rate in the pack rests on the drift half.
5. **No published corpus of vendor-documentation decay exists.** The
   only measured corpus is scholarly web references from 1997 to 2012,
   and vendor documentation fails differently: it keeps its URL and
   rewrites the page. The failure mode a venture actually meets is the
   one nobody has counted.
6. **Whether marking beats removing.** B6's adaptation of the burden
   rule is unevidenced. Nothing measures whether a knowledge base that
   marks unsourced claims ends up better or worse than one that removes
   them.

## Provenance and reuse

Every fragment record carries its own licence as a fact read off the
source rather than as a class assumption, and the residual is honest:
ten of the seventeen carry a licence read off the source, six publish
none at all, and one, the NIST taxonomy, records a licence taken from
the publisher's class because the page carried no statement, which is
the thing B1 forbids and is logged as a failure rather than tidied away.
Two of the six that publish nothing are the pages behind the `llms.txt`
disagreement, so
the pack's most contested pair is also its least reusable pair, which is
recorded in `provenance.fragment.json` rather than glossed.

Nothing in this pack reproduces text from any source. The longest quoted
span anywhere in the read surface is four words, and every finding is a
functional description written so that somebody who had never seen the
source could arrive at the wording from the description. Where a figure
appears, it is a fact cited to its source and not carried expression.

Three sources refused automated access and were not worked around: one
bot check and two 403 responses. Where an open-access copy of the same
document existed it was read instead and is what the record cites. Where
none existed, no record was written and the pack states which conclusion
is weaker as a result.

Two live pages addressed AI readers in the imperative during the sweep.
Neither was acted on, both were recorded, and the encounter is written
up at
`packs/research-knowledge/exemplars/EX-RESEARCH-001-a-source-that-spoke-to-the-reader.md`.

## Citation state, and what the import did

At authoring time the pack body, its guides, its references, its checks
and its exemplar cited `FRAG-RESEARCH-KNOWLEDGE-NN` ids, because
assigning EV ids is the integrator's step under ADR-0002 decision 3 and
this lane must not write to `registry/`. That import has since run. The
read surface now cites the assigned `EV-` ids, and the only FRAG ids
left are in this directory, which check S014 exempts as the pre-import
record.

No record deduplicated against an existing ledger row, so all seventeen
arrived as new rows in one contiguous block, in fragment order:

| fragment | assigned | source |
| --- | --- | --- |
| 01 | EV-0532 | PRISMA 2020 statement |
| 02 | EV-0533 | GRADE Working Group |
| 03 | EV-0534 | OCEBM levels of evidence |
| 04 | EV-0535 | Cochrane Handbook chapter 4 |
| 05 | EV-0536 | Cochrane Handbook chapter 22 |
| 06 | EV-0537 | Cochrane Handbook chapter 13 |
| 07 | EV-0538 | W3C PROV-O |
| 08 | EV-0539 | FAIR guiding principles |
| 09 | EV-0540 | Citation File Format |
| 10 | EV-0541 | Klein and others, reference rot |
| 11 | EV-0542 | RFC 7089, Memento |
| 12 | EV-0543 | NIST AI 100-2 E2025 |
| 13 | EV-0544 | Greshake and others, indirect prompt injection |
| 14 | EV-0545 | Wikipedia, No original research |
| 15 | EV-0546 | Wikipedia, Verifiability |
| 16 | EV-0547 | the llms.txt proposal |
| 17 | EV-0548 | AgentPatterns, llms.txt standard page |

The four proposed predicates were added to the Evidence and deciding
group of `kernel/PREDICATES.md` with the wording in the table above,
lightly edited, and the `research-and-knowledge-base` row in
`registry/coverage.json` moved from `registry-only` to `built`.

Two things about that coverage row are worth a second look and are not
this lane's to change. It carries no `worked_example`, which check S013
reports as an error and which
`packs/research-knowledge/exemplars/EX-RESEARCH-001-a-source-that-spoke-to-the-reader.md`
answers. Its `evidence_sources` list holds the fourteen pre-existing EV
ids the pack reuses plus EV-0214, which the pack does not cite directly,
and none of the seventeen rows the pack's own research contributed.
