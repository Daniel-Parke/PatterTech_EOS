---
summary: Activation, outcomes and decision map for the legal-licensing Doctrine and Wargames
type: pack
tags: [security, pii, delivery]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [adds_dependency, vendors_code, publishes_code, hosts_service, accepts_contribution, handles_personal_data, studies_external_source]
activation_paths: [**/LICENCE*, **/LICENSE*, **/NOTICE*, **/requirements*.txt, **/package-lock.json, **/uv.lock, **/Cargo.lock, **/pyproject.toml, **/*privacy*, **/*terms*]
volatility: slow
review: none
sources: [EV-0041, EV-0069, EV-0225, EV-0337, EV-0338, EV-0339, EV-0340, EV-0341, EV-0342, EV-0343, EV-0344, EV-0345, EV-0346, EV-0347, EV-0348, EV-0349, EV-0350, EV-0351, EV-0352]
display_name: Licensing and Legal Boundaries
category: practice-governance
id_namespace: LEGAL
depends_on: [security-privacy]
---


# Licensing and Legal Boundaries

This pack routes a venture's legal and licensing questions: what a
dependency's licence lets us ship, what our repositories declare, where
inbound code came from, what may lawfully be carried away from a source
we studied, and what a UK privacy notice must say before data is
collected. It activates on dependency, packaging, licence, study and
personal-data changes. It is routing and checking, not legal advice, and
it names four situations that stop and go to a lawyer.

## Not legal advice, and where the evidence lives

Nothing here is legal advice, and no rule below is a legal opinion about
any specific situation. The pack makes the facts of a licensing or
data-protection position visible and checkable, and routes the questions
it cannot answer to a qualified human. B7 is that boundary, and it binds.

The evidence import is done. The twenty-five rows frozen in
`packs/legal-licensing/research/sources.fragment.json`, each carrying a
version, licence, access date, maintenance state and review trigger, are
in `registry/evidence.json` as EV-0337 to EV-0352 for the licensing
batch and EV-0496 to EV-0504 for the extraction cases, and every
citation below uses the ledger id. The fragment file stays in the
research directory as the batch the import was made from, and the
synthesis behind the pack is in
`packs/legal-licensing/research/NOTES.md`. This pack cites ids, never
restates the versioned facts, and never copies source prose, since
several of these sources are readable and not reusable.

## Activation

**Paths.** Root `LICENCE`, `LICENSE` and `NOTICE` files; a `LICENSES/`
directory; `REUSE.toml` and `.reuse/`; dependency manifests and
lockfiles; vendored source directories such as `third_party/` and
`vendor/`; SBOM and scan outputs; `CONTRIBUTING.md`; privacy notice,
cookie and terms pages; any records of processing.

**Task types.** Adding, upgrading or vendoring a dependency. Choosing or
changing an outbound licence. Publishing a repository or a package.
Accepting a contribution from outside the venture. Studying an external
product, repository, game or postmortem before building. Shipping
anything that collects personal data. Placing a product on the EU
market. Answering a letter that alleges infringement, or any regulator
contact.

**Keywords, fallback only.** Licence, license, copyright, GPL, AGPL,
copyleft, SPDX, attribution, NOTICE, patent grant, CLA, DCO, sign-off,
privacy notice, GDPR, ICO, data subject, retention, terms of service.
Keywords are the weakest signal and never override the predicates.

**Applicability predicates.**

| Predicate | True when |
| --- | --- |
| adds_dependency | the change introduces or upgrades a third-party component |
| vendors_code | source is copied into the repo rather than resolved by a package manager |
| publishes_code | an artefact leaves the venture as a repository, package or binary |
| hosts_service | people reach the software over a network |
| accepts_contribution | code arrives from someone outside the venture |
| handles_personal_data | the system collects, stores or transmits data about identifiable people. Shared with the security-privacy pack, which attaches its own duties to the same fact |
| places_on_eu_market | the product is made available in the EU in the course of a commercial activity |
| studies_external_source | work reads a product, repository, game or document we do not own, to learn from it |

A documentation-only change, or a change that touches no manifest, no
licence file, no personal data and no external source, loads nothing
beyond the first paragraph.

`studies_external_source` has no path trigger, because the artefacts a
study produces are named by the Study workflow rather than by this pack.
It is a task-type predicate and the task declares it.

## Outcomes and non-goals

**Outcomes.** Every component in a shipped artefact has a licence
identity someone recorded, not one a tool guessed. The obligations that
identity carries are either discharged or written down as a decision
with a date. Inbound code has a stated origin. A study of somebody
else's product records how the source was acquired and what was carried
away, before the carrying happens. Before data about a person is
collected, that person can read what happens to it. The four expensive
questions reach a lawyer while they are still cheap.

**Non-goals.** This pack does not give legal advice and does not
interpret a licence for a specific fact pattern. It does not own
security controls, threat modelling, secret handling or data
minimisation, which sit in the security-privacy pack. It does not own
contracts, company law, employment, tax, trademarks or disputes. It
does not rate licences itself, and it does not maintain the identifier
list; both are imported (EV-0337,
EV-0343). It does not own the Study workflow: how a source is chosen,
read and turned into a lesson belongs to that playbook, and this pack
owns only what may lawfully be carried out of it.

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-LEGAL-001](doctrines/DOC-LEGAL-001-every-repository-declares-its-own-licence.md) (default)
<a id="B2"></a>
- `B2` to [DOC-LEGAL-002](doctrines/DOC-LEGAL-002-no-dependency-enters-without-a-recorded-licence-expression.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-LEGAL-003](doctrines/DOC-LEGAL-003-an-or-expression-is-resolved-to-one-identifier-before.md) (default)
<a id="B4"></a>
- `B4` to [DOC-LEGAL-004](doctrines/DOC-LEGAL-004-copyleft-entering-anything-we-ship-or-host-takes-a-written.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-LEGAL-005](doctrines/DOC-LEGAL-005-before-any-personal-data-is-processed-the-notice-and-the.md) (binding)
<a id="B6"></a>
- `B6` to [DOC-LEGAL-006](doctrines/DOC-LEGAL-006-inbound-work-carries-a-provenance-assertion.md) (default)
<a id="B7"></a>
- `B7` to [DOC-LEGAL-007](doctrines/DOC-LEGAL-007-consequential-questions-stop-here-and-go-to-a-lawyer.md) (binding)
<a id="D1"></a>
- `D1` to [DOC-LEGAL-008](doctrines/DOC-LEGAL-008-a-three-bucket-allowlist-keyed-on-identifiers-with-the.md) (default)
<a id="D2"></a>
- `D2` to [DOC-LEGAL-009](doctrines/DOC-LEGAL-009-the-scanner-produces-the-inventory-and-a-person-produces.md) (default)
<a id="D3"></a>
- `D3` to [DOC-LEGAL-010](doctrines/DOC-LEGAL-010-per-file-declaration-for-anything-published.md) (default)
<a id="D4"></a>
- `D4` to [DOC-LEGAL-011](doctrines/DOC-LEGAL-011-permissive-outbound-unless-there-is-a-stated-reason-to.md) (default)
<a id="D5"></a>
- `D5` to [DOC-LEGAL-012](doctrines/DOC-LEGAL-012-vendored-code-carries-its-licence-text-and-a-provenance.md) (default)
<a id="D6"></a>
- `D6` to [DOC-LEGAL-013](doctrines/DOC-LEGAL-013-ceremony-scales-with-risk-to-people.md) (default)
<a id="D7"></a>
- `D7` to [DOC-LEGAL-014](doctrines/DOC-LEGAL-014-record-the-eu-market-position-once-with-the-reasoning-and.md) (default)
<a id="D8"></a>
- `D8` to [DOC-LEGAL-015](doctrines/DOC-LEGAL-015-the-routing-loop-has-a-budget-and-the-run-records-what-it.md) (default)
<a id="D9"></a>
- `D9` to [DOC-LEGAL-016](doctrines/DOC-LEGAL-016-nothing-is-studied-until-how-it-was-acquired-the-terms.md) (default)
<a id="D10"></a>
- `D10` to [DOC-LEGAL-017](doctrines/DOC-LEGAL-017-the-session-that-reads-the-source-and-the-lanes-that-build.md) (default)
- source `preferences:001` to [DOC-LEGAL-018](doctrines/DOC-LEGAL-018-mit-for-a-small-library-with-no-patent-exposure-apache-2-0.md) (preference)
- source `preferences:002` to [DOC-LEGAL-019](doctrines/DOC-LEGAL-019-which-scanner.md) (preference)
- source `preferences:003` to [DOC-LEGAL-020](doctrines/DOC-LEGAL-020-the-process-certification-checklist-read-once-as-a-prompt.md) (preference)
- source `preferences:004` to [DOC-LEGAL-021](doctrines/DOC-LEGAL-021-notice-wording-and-reading-level.md) (preference)
- source `preferences:005` to [DOC-LEGAL-022](doctrines/DOC-LEGAL-022-whether-the-repositorys-own-automated-health-checks-watch.md) (preference)

## Decision map

| Fork | What it decides | Wargame |
| --- | --- | --- |
| Can we use this dependency for what we actually ship | Whether copyleft triggers here at all | `packs/legal-licensing/wargames/WG-LEGAL-001-copyleft-trigger.md` |
| How does this venture decide licence questions at all | Standing verdict, per-file declaration, certified process, or scan and review | `packs/legal-licensing/wargames/WG-LEGAL-002-compliance-posture.md` |
| What licence does this repository carry outbound | The promise we make downstream | `packs/legal-licensing/wargames/WG-LEGAL-003-outbound-licence.md` |
| How do inbound rights arrive | Sign-off, agreement, employment, or nothing | `packs/legal-licensing/wargames/WG-LEGAL-004-inbound-rights.md` |
| What may a study carry away from a source we do not own | Black box, filtered reading, licensed carriage, or nothing | `packs/legal-licensing/wargames/WG-LEGAL-005-lawful-extraction.md` |

Level-three detail sits in `packs/legal-licensing/references/`: the licence
classes and their buckets, the escalation triggers and the handover,
and UK data routing. A worked run is in
`packs/legal-licensing/examples/`.

## Failure modes and anti-patterns

- **Importing someone else's categories without their reason.** The
  copied ban misfires, and it gets defended because it is written down
  (EV-0342).
- **A distribution-shaped policy on a hosted product.** Every rule
  reasons about releases; the term that bites triggers on network
  interaction (EV-0341).
- **Treating a green lint as a compliance result.** Conformant
  declarations can be wrong declarations (EV-0344). Its
  sibling: a scan that ran, found nothing and was read as a pass, when
  most real output lands on values the tidy grammar does not cover
  (EV-0338).
- **Copying an OR expression into the inventory.** The choice was never
  made, so no set of obligations is known to apply
  (EV-0338).
- **Reading a fork button as permission.** Platform terms may allow
  viewing and forking while granting no right to use
  (EV-0348).
- **Collapsing three axes into one.** Whether a licence restricts the
  wrong things, whether it is well drafted, and whether it fits our
  promise are separate questions (EV-0337,
  EV-0339, EV-0343).
- **A privacy notice written after launch**, when the duty attaches at
  collection (EV-0349), and its sibling, a good notice
  standing in for a registration duty that exists separately
  (EV-0350).
- **Self-certifying against a checklist you wrote yourself** and calling
  it assurance (EV-0347).
- **The skin change.** Keeping a studied product's proportions, layout
  and feel and repainting the surface, then calling the result
  independent. The mechanic is free to take; that particular expression
  of it is not.
- **One session that read the source and then wrote the replacement.**
  It is the cheapest defence to give away and the hardest to get back,
  and D10 exists for it.
- **Answering an escalation trigger.** An agent that reasons its way to
  a confident answer about a modification boundary has broken B7.
- **Buying a clean result by refusing the work.** A run that declines to
  build the feature has not passed this pack. Every finding here has a
  disposition that ships something: substitute, discharge the
  obligation, or escalate and continue with the rest.

## Open questions and counter-evidence

**The same facts, opposite actions.** Two authoritative sources agree
completely that GPLv2 and GPLv3 do not combine and that the Apache 2.0
patent terms are incompatible with GPLv2 while GPLv3 accepts them. One
reads that as a reason to release under a later copyleft version
(EV-0340); the other reads it as a reason to exclude
that family entirely (EV-0342). Neither is wrong. The
question underneath is which promise you are keeping to your own
downstream, and a venture answers that before adopting either rule.

**Where the AGPL boundary sits is genuinely unresolved.** The licence
text does not say what counts as modification, nor where the program
boundary lies when the component sits behind an internal service
(EV-0341). Read narrowly, an unmodified component run
as a back end triggers nothing extra. That is why B4 requires a written
decision and B7 sends the hard version to a lawyer, rather than the
pack ruling it.

**Contributor agreements against sign-off.** We hold a primary source
for the certification route (EV-0345) and nothing
comparable on agreements, and no source compares the two on outcomes.
B6 rests on cost and on evidence sitting in the history, which is an
argument rather than a measurement.

**Who owns agent-written code.** A national authority is answering
copyrightability and training data as staged, separate inquiries and has
not finished (EV-0352). No equivalent UK determination
was located at this cutoff, so this is unresolved rather than unread.
Record provenance; do not assume authorship.

**The extraction Wargame rests on case law, not on measurement.** D9, D10
and `packs/legal-licensing/wargames/WG-LEGAL-005-lawful-extraction.md`
turn on decided cases and on one advocacy organisation's clean-room
practice, now ledgered as EV-0496 to EV-0504 with court, year and
holding. Two of the nine are tertiary summaries rather than the
opinions, most are United States authority, and none has been tested
against a United Kingdom judgment. That is weaker than the rest of the
pack and the Wargame says so.

**Scanner accuracy is unmeasured.** No figure was found for any
detector, and scanning a repository that declares per file is a
different problem from scanning one that does not
(EV-0346, EV-0344).

**The commercial activity line.** The regulator's summary asserts the
boundary without resolving the cases that matter, such as a sponsored
maintainer or a hosted version of one's own project
(EV-0351). D7 records a position rather than claiming
one is correct. On the same theme of unread detail, only the structure
of the charges regulations was retrieved and not the tier amounts, and
the version read is the text as made, so no fee figure is ever quoted
from this pack (EV-0350).

**Refresh triggers.** Re-argue this pack on: a new identifier list
release; a change to the published third-party policy page; the dates
2026-09-11 and 2027-12-11; further commencement of the 2025 data Act;
the final publication of the copyright authority's third part; and any
successor to the Article 13 text on the statute site.
