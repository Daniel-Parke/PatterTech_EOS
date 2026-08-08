---
summary: Licensing, inbound provenance and UK data-protection routing for a venture, and the four situations that stop and go to a lawyer
type: playbook
tags: [security, pii, delivery]
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [adds_dependency, vendors_code, publishes_code, hosts_service, accepts_contribution, processes_personal_data]
volatility: slow
review: 2027-04
sources: [EV-0041, EV-0069, EV-0225, EV-0337, EV-0338, EV-0339, EV-0340, EV-0341, EV-0342, EV-0343, EV-0344, EV-0345, EV-0346, EV-0347, EV-0348, EV-0349, EV-0350, EV-0351, EV-0352]
---

# legal-licensing

This pack routes the legal and licensing questions a venture meets in
normal work: what a dependency's licence lets us ship, what our own
repositories declare, where inbound code came from, and what a UK
privacy notice must say before data is collected. It activates on
dependency, packaging, licence and personal-data changes. It is routing
and checking, not legal advice, and it names the four situations where
the answer is to stop and instruct a lawyer.

## Not legal advice, and where the evidence lives

Nothing here is legal advice, and no rule below is a legal opinion about
any specific situation. The pack makes the facts of a licensing or
data-protection position visible and checkable, and routes the questions
it cannot answer to a qualified human. B7 is that boundary, and it binds.

Every FRAG-LEGAL-LICENSING id points at a row in
`packs/legal-licensing/research/sources.fragment.json` carrying that
source's version, licence, access date, maintenance state and review
trigger. Those rows are frozen and awaiting integrator import into
`registry/evidence.json`, which assigns their final EV ids. Cited EV ids
already sit in the ledger. This pack cites ids, never restates the
versioned facts, and never copies source prose, since several of these
sources are readable and not reusable.

## Activation

**Paths.** Root `LICENCE`, `LICENSE` and `NOTICE` files; a `LICENSES/`
directory; `REUSE.toml` and `.reuse/`; dependency manifests and
lockfiles; vendored source directories such as `third_party/` and
`vendor/`; SBOM and scan outputs; `CONTRIBUTING.md`; privacy notice,
cookie and terms pages; any records of processing.

**Task types.** Adding, upgrading or vendoring a dependency. Choosing or
changing an outbound licence. Publishing a repository or a package.
Accepting a contribution from outside the venture. Shipping anything
that collects personal data. Placing a product on the EU market.
Answering a letter that alleges infringement, or any regulator contact.

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
| processes_personal_data | the system collects, stores or transmits data about identifiable people |
| places_on_eu_market | the product is made available in the EU in the course of a commercial activity |

A documentation-only change, or a change that touches no manifest, no
licence file and no personal data, loads nothing beyond the first
paragraph.

## Outcomes and non-goals

**Outcomes.** Every component in a shipped artefact has a licence
identity someone recorded, not one a tool guessed. The obligations that
identity carries are either discharged or written down as a decision
with a date. Inbound code has a stated origin. Before data about a
person is collected, that person can read what happens to it. The four
expensive questions reach a lawyer while they are still cheap.

**Non-goals.** This pack does not give legal advice and does not
interpret a licence for a specific fact pattern. It does not own
security controls, threat modelling, secret handling or data
minimisation, which sit in the security-privacy pack. It does not own
contracts, company law, employment, tax, trademarks or disputes. It
does not rate licences itself, and it does not maintain the identifier
list; both are imported (EV-0337,
EV-0343).

## Binding requirements

Seven bind. Each names its predicate, its basis, its evidence and the
failure it prevents. Where the basis is decision rather than law or
standard, that is stated: it binds because the estate ruled it.

Three artefacts are named, because a rule pointing at an unnamed
document is not checkable. The **inventory** is the machine-produced
list of components and their licence expressions. `LICENCE_DECISION.md`
at the venture root is the **decision record**, one dated entry per
finding. The **privacy notice** is a file in the repository, published
where the person giving the data can read it.

**B1. Every repository declares its own licence.** `publishes_code`. A
licence file at the root and a declared SPDX expression in the project
manifest, using an identifier from the list or an explicit `LicenseRef`
(EV-0337). Prevents publishing something nobody has
permission to use, because silence means exclusive copyright and the
hosting platform's terms grant no right to use or redistribute
(EV-0348). Basis: standard.

**B2. No dependency enters without a recorded licence expression, and
absence is a blocking finding.** `adds_dependency`, `vendors_code`. Each
component in the inventory carries an SPDX expression. A value of
`NOASSERTION`, `NONE` or empty blocks the merge until it is resolved or
named in `LICENCE_DECISION.md` (EV-0338). The entry
names the path, states that no licence was found, and states that this
means exclusive copyright rather than an unknown to fill in later
(EV-0348). Basis: standard.

**B3. An OR expression is resolved to one identifier before merge.**
`adds_dependency`. `MIT OR GPL-2.0-only` is a choice the project has to
make and record; the raw expression never survives into the inventory
verdict column (EV-0338). Prevents carrying an unmade
choice into a shipped artefact, where the obligations that apply are
undetermined. Basis: standard.

**B4. Copyleft entering anything we ship or host takes a written
decision before merge, not at release.** `hosts_service`,
`publishes_code`, `adds_dependency`. The entry in `LICENCE_DECISION.md`
names the component, its exact identifier, the event that would fire the
obligation, in the words distribution, network interaction or
combination, and the disposition. AGPL section 13 attaches to a modified
version reached by users remotely over a network, with nothing
distributed (EV-0341). Prevents
the standard miss: a policy written around source and binary
distribution is silent on a hosted service, which is the shape most
ventures ship (EV-0342, scoped to one foundation's
promise about its own releases). Basis: standard.

**B5. Before any personal data is processed, the notice and the
registration are both done.** `processes_personal_data`. The privacy
notice file exists before the collecting surface ships, and carries
every Article 13 item, including both statutory complaint routes, to
the controller and to the Commissioner
(EV-0349, EV-0225). Separately, the registration
self-assessment is run and its outcome recorded, either the charge paid
or the schedule exemption named (EV-0350). Prevents two
independent failures: collecting data with no lawful notice, and
missing a charge duty that exists whatever the notice says. Basis: law.

**B6. Inbound work carries a provenance assertion.**
`accepts_contribution`. One sign-off line per commit, in the form the
certification defines, a real name and a reachable address, checked by
a hook (EV-0345). Agent-written commits are included,
because
authorship of machine output is unsettled and provenance is the part we
can record (EV-0352). Prevents code of unknown origin
becoming load-bearing before anyone asks where it came from. Basis:
decision, and see the open question about contributor agreements below.

**B7. Consequential questions stop here and go to a lawyer.** All
predicates. Four triggers, all cheap to detect: copyleft code entering
something we distribute or host in modified form; any relicensing,
licence change or transfer of contributor rights; any personal data
leaving the UK, or any regulator contact including a data subject
complaint that escalates; and any letter alleging infringement. On a
trigger the agent records the facts, stops, and routes to a human
lawyer. Prevents a confident wrong answer in the one place where being
wrong is expensive and no source read settles it. Basis: decision. See
`packs/legal-licensing/refs/ESCALATION.md`.

## Defaults

Each applies unless the venture's lock-book records a reason to depart.

**D1. A three-bucket allowlist keyed on identifiers, with the reason
written next to each bucket.** Freely usable, usable under stated
conditions, never. Decided once, applied mechanically, enforced in CI.
Reason: high volume and low stakes per item is exactly what a standing
verdict is for (EV-0342). Import the shape, not the
categories: the published example bans a licence family outright to
keep a promise about permissive releases, and a venture that makes no
such promise inherits a rule that blocks safe dependencies. See
`packs/legal-licensing/refs/LICENCE_CLASSES.md`.

**D2. The scanner produces the inventory and a person produces the
verdict.** A licence scan is wired as an inventory step routed to a
human, never as a gate that passes silently
(EV-0346). Reason: detection compares texts against a
curated database and reports what a file claims about itself, which is
not a compliance result. Scope note: the accuracy claim on that project
is a vendor claim with no published figure, and accuracy is not
portable between codebases anyway.

**D3. Per-file declaration for anything published.** Tags in file
headers, a sibling file where a comment cannot go, full texts in a
`LICENSES/` directory, bulk cases by glob, and a lint step in CI
(EV-0344). Reason: it is the only pattern here a cold
agent satisfies without judgement. Cost: real per-file overhead on a
small repository, which is why repository-level declaration is the
default for anything unpublished. A green lint proves declarations are
present and consistent, never that they are correct.

**D4. Permissive outbound unless there is a stated reason to
reciprocate**, chosen against the ten criteria first
(EV-0339) and the drafting rating second
(EV-0343). Reason: the outbound licence is a promise,
and the cheapest promise to keep has the fewest conditions. See
`packs/legal-licensing/guides/GD-LEGAL-003-outbound-licence.md`.

**D5. Vendored code carries its licence text and a provenance note at
the moment it is copied.** Where it came from, which revision, which
licence, who copied it. Reason: nothing later reconstructs this, and a
directory with no licence file is the hardest finding to clear
(EV-0348).

**D6. Ceremony scales with risk to people.** A full impact assessment is
for high-risk processing (EV-0041). Reason: a venture that writes one
for every form stops writing them.

**D7. Record the EU market position once, with the reasoning, and
re-check it before 2026-09-11 and before 2027-12-11**
(EV-0351).

**D8. The routing loop has a budget, and the run records what it
spent.** One inventory pass, one decision pass, one re-check after the
fix. A run that has not converged inside that budget escalates rather
than iterating. Reason: this is a decision rather than evidence, and it
prevents exhaustive flailing that reads as diligence.

## Preferences

Taste. Depart freely, no reason needed.

- MIT for a small library with no patent exposure, Apache-2.0 where
  patents matter, with the drafting rating as the tiebreak between
  otherwise equal candidates (EV-0343).
- Which scanner. The inventory matters, the tool does not
  (EV-0346).
- The process-certification checklist read once as a prompt about
  sustainability, which is the only part of it a one-person venture
  cannot answer trivially (EV-0347).
- Notice wording and reading level. The checklist is fixed, the prose is
  not (EV-0349).
- Whether the repository's own automated health checks watch for the
  licence file, which reads the repository's actual state rather than
  its self-description (EV-0069).

## Decision map

| Fork | What it decides | Guide |
| --- | --- | --- |
| Can we use this dependency for what we actually ship | Whether copyleft triggers here at all | `packs/legal-licensing/guides/GD-LEGAL-001-copyleft-trigger.md` |
| How does this venture decide licence questions at all | Standing verdict, per-file declaration, certified process, or scan and review | `packs/legal-licensing/guides/GD-LEGAL-002-compliance-posture.md` |
| What licence does this repository carry outbound | The promise we make downstream | `packs/legal-licensing/guides/GD-LEGAL-003-outbound-licence.md` |
| How do inbound rights arrive | Sign-off, agreement, employment, or nothing | `packs/legal-licensing/guides/GD-LEGAL-004-inbound-rights.md` |

Reference material sits in `packs/legal-licensing/refs/`, and a worked
run in `packs/legal-licensing/exemplars/`.

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
