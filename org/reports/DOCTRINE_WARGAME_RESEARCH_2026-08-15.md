---
summary: Fixed-lens research packet for the first Doctrine and Wargame pressure backlog
type: org
tags: [eos, wargame]
---

# Doctrine and Wargame research packet

## LENS-0002: fixed contract

**Approved purpose.** Support T-0026 and ADR-0014 by testing eleven proposed
standing rules and twenty-five named pressure cases against current official
primary sources and existing EOS coverage. This packet recommends dispositions.
It creates no Doctrine, Wargame, relation, evidence row or pack.

**Sources in.** The UK Ministry of Defence Analysis-Led Wargaming Framework;
Carnegie Mellon Software Engineering Institute ATAM material; NIST
combinatorial-testing material; official Polars, pandas, NumPy, Numba and
DuckDB documentation; W3C design principles and WCAG 2.2; Google SRE; NIST
SSDF; SLSA; and Google's published agent-system scaling study. Current
versions, retrieval dates and governing terms are recorded per source.

**Acquisition.** Public web retrieval from the publishing organisation's own
site or repository on 2026-08-15. Where a source is a living page rather than
a fixed release, the packet says so. Existing EOS evidence and pack material
is inspected locally and read-only to find duplication and conflict.

**Lenses in.** What each source can support as a durable standing rule; what
pressures make that rule unsafe or incomplete; which existing EOS procedure
already covers the decision; the cheapest discriminating test; evidence
strength; applicability; counter-evidence; and the boundary between durable
principle and dated stack fact.

**Lenses out.** No verbatim code or assets; no expressive text; no
source-identifying visual style; no private-repository wording or paths; no
commercial, personal, authentication or deployment detail; no inference from
popularity; no package version promoted into timeless Doctrine; no tainted
material; and no claim that a vendor's own benchmark proves a universal rule.

**Escalation order.** Observe the public source, then read its official
documentation, then inspect official tests or source only if the documentation
cannot settle the question. Do not decompile. Do not use third-party summaries
as evidence.

**Destinations.** Candidate findings are mapped to existing packs and
procedures, a proposed DOC or WG destination, or a recorded rejection. Any
later integration must create one evidence row per retained source and one
operator-approved lesson row per decision under PB-E11. This report is not
either ledger.

**Approval and freeze.** The operator approved the source families, eleven
standing candidates and pressure-led admission policy in T-0026 and ADR-0014.
This contract was written before opening the external sources. It remains
fixed for this study.

## Method and control boundary

This is the research packet, not a completed PB-E11 integration. It follows
PB-E11 steps 1, 3 and 4: the lens was fixed first, findings are classified,
limits and counterclaims are explicit, and existing EOS material has been
checked for conflict and duplication. The source register below uses one row
per public artefact and records the organisation, title, version or retrieval
state, date and licence.

The lane was authorised to write this report and nothing else. It therefore
did not write evidence rows, lesson rows or frozen source copies. The public
pages were read live on 2026-08-15. That is a deliberate scope limit, but it
means PB-E11 step 2 is not yet satisfied. Before any finding moves into a DOC,
WG, relation or pack, the integrator must:

1. freeze or otherwise content-address the exact retained artefact;
2. create one evidence row for each retained source, without grouping URLs;
3. record the licence evidence and access date on that row;
4. take the bounded operator decisions required by PB-E11 step 5; and
5. create one lesson row per accepted or rejected decision before integration.

No recommendation below is authority. `Fact` means the cited source states or
demonstrates it. `Interpretation` is this study's reading of that fact.
`Recommendation` is an EOS proposal. Figures from vendors and project
maintainers remain source claims unless independently measured.

## Source register

The version is fixed where the publisher supplies one. `Living page` means
the page had no immutable release identifier and was read on the retrieval
date. Licence pages used only to establish terms are metadata authorities,
not substantive evidence sources.

| Ref | Organisation and artefact | Version or state | Retrieved | Licence and reuse posture |
| --- | --- | --- | --- | --- |
| R01 | UK Ministry of Defence, [Analysis-Led Wargaming Framework](https://assets.publishing.service.gov.uk/media/69f346fe95de5140ec7eef3c/ALWF_DEWH_Booklet.pdf), reached through the [Defence Experimentation and Wargaming Hub](https://www.gov.uk/guidance/defence-experimentation-and-wargaming-hub) | Booklet marked Crown copyright 2025; GOV.UK page updated 2026-05-01 | 2026-08-15 | Crown copyright. The GOV.UK page states Open Government Licence v3.0 except where otherwise indicated. Paraphrase, attribute, and retain the Crown and licence notice. |
| R02 | Carnegie Mellon University Software Engineering Institute, [The Architecture Tradeoff Analysis Method](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/) | CMU/SEI-98-TR-008, 1998-07-01 | 2026-08-15 | CMU copyright and SEI permission terms. Link and paraphrase. Do not reproduce the method's tables, diagrams or substantial wording without permission. |
| R03 | US National Institute of Standards and Technology, [SP 800-142, Practical Combinatorial Testing](https://csrc.nist.gov/pubs/sp/800/142/final) | Final, October 2010, DOI 10.6028/NIST.SP.800-142 | 2026-08-15 | US Government publication. NIST requests attribution and disclaims endorsement and warranty. Check marked third-party material before reuse. |
| R04 | US National Institute of Standards and Technology, [Combinatorial Testing project](https://www.nist.gov/programs-projects/combinatorial-testing) | Living project page updated 2025-03-26 | 2026-08-15 | US Government information subject to the NIST copyright and disclaimer notice. |
| R04A | US National Institute of Standards and Technology, [ACTS downloadable tools](https://csrc.nist.gov/Projects/automated-combinatorial-testing-for-software/downloadable-tools) | Current tool page | 2026-08-15 | US Government information subject to the NIST notice. Tool-specific terms must be checked before carrying software. |
| R05 | Polars project, [Lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/) | Living documentation; current Python release 1.41.0 published 2026-05-22 | 2026-08-15 | Documentation wording is not carried. Polars source is MIT-licensed, with stated third-party notices. Link and paraphrase the docs. |
| R06 | Polars project, [Coming from pandas](https://docs.pola.rs/user-guide/migration/pandas/) | Living documentation; read against release 1.41.0 | 2026-08-15 | Same posture as R05. Treat project performance comparisons as maintainer claims, not independent measurements. |
| R07 | pandas project, [Enhancing performance](https://pandas.pydata.org/docs/user_guide/enhancingperf.html) | pandas 3.0.5 documentation | 2026-08-15 | pandas code is BSD-3-Clause. Documentation is cited and paraphrased; no examples are copied. |
| R08 | NumPy project, [Interoperability with NumPy](https://numpy.org/doc/stable/user/basics.interoperability.html) | NumPy 2.5 manual | 2026-08-15 | NumPy is BSD-3-Clause with separately listed bundled components. Link and paraphrase. |
| R09 | Numba project, [Performance tips](https://numba.readthedocs.io/en/stable/user/performance-tips.html) | Stable documentation; read against release 0.65.1, commit `9e3087a`, published 2026-04-24 | 2026-08-15 | Numba is BSD-2-Clause. Examples are pedagogical and are not copied or treated as benchmarks. |
| R10 | Numba project, [Deprecation notices](https://numba.readthedocs.io/en/latest/reference/deprecation.html) | Living documentation; read against release 0.65.1 | 2026-08-15 | Same posture as R09. The moved CUDA target has its own project and terms and needs a separate row if later retained. |
| R11 | DuckDB project, [Python API overview](https://duckdb.org/docs/stable/clients/python/overview) | DuckDB 1.5.5 stable documentation | 2026-08-15 | DuckDB source is MIT-licensed. Documentation is linked and paraphrased. |
| R12 | DuckDB project, [How to tune workloads](https://duckdb.org/docs/current/guides/performance/how_to_tune_workloads) | Living current documentation; read against 1.5.5 | 2026-08-15 | Same posture as R11. Maintainer guidance is evidence of supported behaviour, not comparative outcome evidence. |
| R13 | Apache Software Foundation, [Spark SQL performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning) | Apache Spark 4.2.0, released 2026-07-14 | 2026-08-15 | Apache-2.0 for Spark, with bundled third-party notices. Link and paraphrase. |
| R14 | World Wide Web Consortium, [Web Platform Design Principles](https://www.w3.org/TR/design-principles/) | W3C Group Note, 2026-02-24 | 2026-08-15 | W3C permissive document licence on the source page. A Group Note is not a W3C-endorsed Recommendation. Attribute and do not imply endorsement. |
| R15 | World Wide Web Consortium, [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/) | W3C Recommendation, revised 2024-12-12 | 2026-08-15 | W3C Document Licence. Cite the Recommendation; do not copy normative text into EOS rules when a link is sufficient. |
| R16 | World Wide Web Consortium, [ARIA in HTML](https://www.w3.org/TR/html-aria/) | Current W3C Recommendation | 2026-08-15 | W3C document terms on the source page. Link and paraphrase. |
| R17 | World Wide Web Consortium Web Accessibility Initiative, [ARIA Authoring Practices, Read Me First](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) | Living Authoring Practices guidance | 2026-08-15 | W3C document terms on the source page. Treat examples as guidance, not as a substitute for user-agent testing. |
| R18 | Google, [Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) | Web edition of the 2016 SRE book | 2026-08-15 | CC BY-NC-ND 4.0 for the online book. Paraphrase only, preserve attribution, and do not carry diagrams or adapted tables. |
| R19 | Google, [Site Reliability Engineering, Simplicity](https://sre.google/sre-book/simplicity/) | Web edition of the 2016 SRE book | 2026-08-15 | CC BY-NC-ND 4.0. Paraphrase only. |
| R19A | Google, [Site Reliability Engineering, Service Best Practices](https://sre.google/sre-book/service-best-practices/) | Web edition of the 2016 SRE book | 2026-08-15 | CC BY-NC-ND 4.0. Paraphrase only. |
| R20 | Google, [Site Reliability Engineering, Data Integrity](https://sre.google/sre-book/data-integrity/) | Web edition of the 2016 SRE book | 2026-08-15 | CC BY-NC-ND 4.0. Paraphrase only. |
| R21 | Google, [Site Reliability Workbook, Incident Response](https://sre.google/workbook/incident-response/) | Web edition of the 2018 SRE Workbook | 2026-08-15 | CC BY-NC-ND 4.0. Paraphrase only. |
| R22 | Google, [Site Reliability Engineering, Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) | Web edition of the 2016 SRE book | 2026-08-15 | CC BY-NC-ND 4.0. Paraphrase only. |
| R23 | US National Institute of Standards and Technology, [SP 800-218, Secure Software Development Framework v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | Final v1.1, February 2022. A v1.2 revision was draft on the retrieval date | 2026-08-15 | US Government publication under the NIST copyright and disclaimer notice. Use v1.1 as the final standard and add an event review for the draft's finalisation. |
| R24 | OpenSSF SLSA project, [SLSA v1.2 specification](https://slsa.dev/spec/v1.2/) | Approved v1.2, announced 2025-11-24 | 2026-08-15 | Community Specification Licence 1.0. |
| R24A | OpenSSF SLSA project, [Provenance](https://slsa.dev/spec/v1.2/provenance) | Approved SLSA v1.2 provenance specification | 2026-08-15 | Community Specification Licence 1.0. |
| R25 | OpenSSF SLSA project, [Supply-chain threats](https://slsa.dev/spec/v1.2/threats) | Approved SLSA v1.2 threat model | 2026-08-15 | Community Specification Licence 1.0. Attribute and avoid any implication that OpenSSF endorses EOS. |
| R26 | Google-affiliated authors, [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296) | arXiv v3, revised 2026-04-08 | 2026-08-15 | arXiv non-exclusive distribution licence 1.0, not CC BY. Cite and paraphrase only. Do not treat the earlier Google blog summary as the current paper version. |

Release and source licence links were checked on the projects' official
repositories. They establish metadata only. They do not turn documentation
claims into independent benchmark evidence.

## Findings by source

The source register is the direct-observation record. The table below keeps
sourced fact apart from study interpretation and recommendation. The class is
PB-E11's finding class, not a score for the source as a whole.

| Ref and class | Sourced fact | Counterclaim or unknown | Interpretation and transfer limit | Recommendation and intended EOS destination |
| --- | --- | --- | --- | --- |
| R01 `does-well` | The framework starts with research questions and hypotheses, joins design to an analysis and data-collection plan, uses playtests, then analyses, reports, exploits and refines the result. It treats usable findings as the product of a wargame. | The booklet describes a developing minimum viable framework in a UK defence setting. It does not validate an EOS schema or prescribe a number of scenarios. | The lifecycle transfers. Defence roles, terminology and scale do not. The result argues for better decision and evidence structure, not a larger file count. | Add the lifecycle fields to the advanced WG authoring contract and checks. Use it in every newly admitted or refreshed WG. Do not copy the booklet's form or language. |
| R02 `does-well` | ATAM evaluates an architecture through business drivers, quality-attribute scenarios, risks, non-risks, sensitivity points and trade-off points. | A normal evaluation takes trained facilitators, architects and stakeholders over several days. The source is a method report, not comparative outcome evidence. | Scenario and sensitivity thinking transfers to a small venture. The ceremony and workshop duration do not. | Use the lightweight concepts in architecture and cross-domain WG fields: forces, affected qualities, sensitivity, trade-off, evidence and ruling. Link rather than reproduce SEI material. |
| R03 `does-well` | NIST describes t-way combinatorial testing as a way to cover interactions among a small number of parameters with far fewer tests than exhaustive enumeration, and discusses cost and strength trade-offs. | Interaction coverage is not correctness. A wrong parameter model, omitted constraint or weak oracle can make a complete covering array useless. | The technique fits option matrices with several independent axes. It does not justify generating every pair of words found in two Doctrines. | Add optional constrained interaction coverage to the WG backlog audit and delivery-testing references. Require an oracle and exclusions beside any generated set. |
| R04 `does-well` | The NIST project reports studies with large test-count reductions and comparable fault detection for modelled interaction faults. | The reported 20 to 700 fold reductions are project summaries across selected studies, not an EOS benchmark and not a guarantee for arbitrary software. | Direction transfers, magnitude does not. | Retain only if a later evidence row labels the figures as NIST project claims. Do not use the figures as a Doctrine threshold. Destination: delivery-testing evidence and the WG coverage audit. |
| R04A `merely-different` | ACTS supports constraints and variable-strength interaction coverage. | Tool support cannot discover missing variables, invalid equivalence classes or the correct expected result. | It is one implementation of the R03 technique, not the standard or a required EOS dependency. | Reference it as an optional authoring aid. Do not add it to the EOS runtime or default stack without a separate build decision. |
| R05 `does-well` | Polars documents that its lazy API exposes a query plan to optimisation, including predicate and projection pushdown, while eager execution remains useful for exploratory and intermediate inspection. | The documentation comes from the project and does not prove Polars is faster or more suitable for every workload. Lazy plans can make execution and ordering less obvious. | The durable lesson is to select execution mode from the workload and observability need. `Polars first` is only a scoped, dated profile. | Destination: a dated data-compute stack profile and data-compute WG, with representative measurement before a change of engine or execution mode. |
| R06 `merely-different` | Polars documents Arrow-oriented memory, no pandas-style index, eager and lazy modes, streaming support and optional GPU execution as material differences from pandas. | A migration page is written to help adoption of Polars. Its performance comparisons are maintainer claims and ecosystem compatibility can dominate engine design. | The engines carry different semantics, not a simple slow-to-fast ranking. | Destination: the engine-selection WG. Record semantic compatibility, dependency ecosystem, memory, execution mode and measured workload as separate forces. |
| R07 `does-well` | pandas documents conversion through `to_numpy()` for typed array computation and notes that Numba compilation overhead can outweigh gains on small data, with larger inputs more likely to benefit. | Its size examples are instructional, not universal break-even points. Conversion can copy data or change representation. | A dataframe-to-array boundary and a JIT decision must be profiled on representative data. The published example size must not become an EOS threshold. | Destination: data representation-boundary and acceleration WGs. Keep pandas when its semantics or ecosystem are the contract. |
| R08 `does-well` | NumPy documents array interoperability protocols and DLPack. Same-device exchange can avoid a copy; GPU-to-CPU exchange needs a copy because NumPy itself does not provide GPU execution. | Protocol support does not guarantee zero-copy layout, matching dtype, numerical equivalence or ownership safety for every producer. | Representation movement is an architectural boundary with cost and correctness consequences. It is not a low-level implementation detail once data is large. | Destination: the dataframe-to-array or solver-boundary WG, with explicit dtype, layout, device, copy, ownership and tolerance checks. |
| R09 `does-well` | Numba advises profiling with real data, prefers nopython compilation for supported code, and documents that fast-math relaxes numerical rules while parallel execution applies only where supported. | The examples are pedagogical. Compilation delay, unsupported features and altered floating-point behaviour can remove or reverse the benefit. | JIT is an earned optimisation. `Numba by default` is unsafe without a measured hotspot and a numerical oracle. | Destination: acceleration WG and dated compute profile. Require baseline, compile-inclusive and steady-state timings plus correctness tolerances. |
| R10 `does-poorly` | Numba's built-in CUDA target is deprecated and development moved to the separate `numba-cuda` package. | The move does not show that GPU acceleration is unsuitable. It shows that a named tool route can change independently of the principle. | A timeless `Numba plus GPU` Doctrine would already be stale. | Prohibit package-specific GPU wording in Doctrine. Put current GPU routes in dated stack facts and give them event-based review. |
| R11 `does-well` | DuckDB documents an in-process analytical engine that can query pandas, Polars and Arrow objects directly and return those forms or NumPy arrays. | Interoperability does not make DuckDB the correct transactional store, service database or high-concurrency query service. | It is a useful local query-engine option between in-memory frames and distributed compute. | Destination: analytical engine-selection WG and dated data-compute profile. Keep storage purpose and concurrency explicit. |
| R12 `does-well` | DuckDB documents spilling for grouping, joining, sorting and windows, while naming workloads and aggregates where several blocking operators or memory behaviour still cause limits. | `Out of core` is not `unbounded`, and local disk, query shape and concurrency materially affect results. | Working-set size and operator shape decide whether a local engine is sufficient. | Destination: execution-mode and engine-selection WGs. Test the actual query on representative data and record peak memory, spill, time and failure behaviour. |
| R13 `merely-different` | Spark 4.2.0 documents cache, partition, join, statistics and adaptive-query tuning for distributed SQL workloads. | Distribution adds shuffle, coordination, operational and reproducibility costs. The documentation does not position Spark as an upgrade from local engines for small work. | Spark is selected when measured distribution pressure exists, not because a dataset is described as large. | Destination: analytical engine-selection WG. Require evidence that one-node and out-of-core routes fail the stated objective before selecting a distributed engine. |
| R14 `does-well` | The W3C Group Note prioritises user needs and intent, broad device and mode support, compatibility, minimal data and simple designs, while recognising that high-level and low-level needs can conflict. | It is a Group Note, not an endorsed Recommendation, and it offers principles rather than conformance tests. | It supports a default philosophy, not a binding technical control. | Destination: normalise the existing user- and task-shaped interface rule into DOC relations. Use WCAG and HTML standards, not this Note, for binding conformance claims. |
| R15 `does-well` | WCAG 2.2 is a technology-neutral W3C Recommendation with individually testable success criteria and conformance levels. The Recommendation states that it cannot cover every disability need. | Passing WCAG is not proof that a product is usable or accessible to every user. | WCAG is a floor and evidence vocabulary, not the complete user outcome. | Retain existing EV-0027, add an event review rather than a duplicate row, and link semantic HTML Doctrine and UI assurance procedures to it. |
| R16 `does-well` | ARIA in HTML defines when roles and attributes are permitted or discouraged on HTML elements. | A syntactically permitted role does not implement keyboard interaction, focus management or usable behaviour. | Native semantics should be the default, with ARIA used to express missing semantics rather than to overwrite working HTML casually. | Destination: semantic HTML DOC and the semantic DOM versus custom-control WG. Keep current UI accessibility assurance as the test route. |
| R17 `does-well` | The APG warns that native controls include behaviour, while assigning an ARIA role is a promise the author must fulfil and does not itself add keyboard behaviour or styling. It calls for testing relevant assistive-technology and browser combinations. | APG patterns are examples and guidance, not proof that a copied custom widget works for a product's users. | Custom controls carry a continuing behaviour and test obligation. | Destination: refresh component sourcing and accessibility assurance relations, and admit a WG for semantic DOM or canvas and custom interaction where native controls cannot express the job. |
| R18 `does-well` | Google SRE recommends starting from what users care about, choosing a small representative set of indicators, setting objectives from those needs, and avoiding a 100 per cent target so an error budget exists. | This is Google practice from a hyperscale web context, not a controlled comparison. Some products have safety or integrity floors that an error budget cannot spend. | User journeys and objectives transfer. Google's numbers and organisational shape do not. | Destination: merge with existing reliability-measure and error-budget procedures. Do not create a second SLO rule. |
| R19 `does-well` | The SRE simplicity chapter treats unnecessary code and complexity as a reliability cost and argues for removing work that does not earn its operation and maintenance burden. | Simplicity is not one deployable at any price. Regulatory, isolation, capacity and ownership pressures can make distribution the simpler operational truth. | It supports the existing `one deployable until earned` rule, bounded by measurable split pressures. | Destination: relation to the existing deployment-shape procedure and its architecture WG. No new standing rule text is needed. |
| R19A `does-well` | Google's service guidance favours small, understandable releases and keeps exploratory code explicitly separate from software that reaches users. | Small changes can still be irreversible, and a spike can become de facto production through copying or prolonged use. | Size and reversibility are different axes. A spike needs a deletion or hardening boundary, not a relaxed definition of production. | Destination: refresh the existing test-timing and discovery-depth WGs for spike versus hardened vertical slice. |
| R20 `does-well` | The data-integrity chapter distinguishes replication and backup from demonstrated recoverability and makes end-to-end restoration testing central. | A tested database restore does not prove DNS, secrets, dependencies or the whole service can be rebuilt. | The EOS already carries the correct distinction in WG-OPS-003. | Destination: refresh or add evidence relations to WG-OPS-003 only. Do not create a duplicate restoration WG. |
| R21 `does-well` | The incident guidance places assessment and mitigation before root-cause work, uses named coordination and communication roles, and records live state for handover and later review. | The role structure assumes several responders. It does not specify a universal hotfix gate for a solo operator or small venture. | Restore service first, but retain supervision, impact checks, a known-good path and rollback. A hotfix is a different gate, not no gate. | Destination: new incident-hotfix versus normal-gate WG under delivery and reliability, linked to existing release control and incident records. |
| R22 `does-well` | The cascading-failure chapter describes graceful degradation that preserves minimum useful output, and stresses that rare degradation paths need to be simple, exercised, monitored and switchable. | Degradation is unsafe where it weakens privacy, authorisation, integrity or consequential-action approval. Rare paths rot when they are not tested. | `Fail closed` and `degrade honestly` are both conditional defaults. The deciding pressure is the protected property. | Destination: new fail-closed versus honest-degradation WG, with protected-set floors and explicit exercise evidence. |
| R23 `does-well` | SSDF v1.1 defines outcome-oriented practices and a common vocabulary intended to fit different development lifecycles through risk, mission and resource tailoring. | It does not prescribe exact tools, gates or a uniform assurance level. The next revision was still draft on the retrieval date. | Use SSDF to state outcomes and coverage, not to justify a particular product or ceremony. | Keep EV-0037 and add an event review for the final v1.2 revision. Destination: security and supply-chain relations, not a duplicate standard summary. |
| R24 `does-well` | SLSA v1.2 provides source and build tracks with incremental levels of assurance. | A level describes properties of the source or build process, not product quality, producer intent or safe use. | Progressive assurance transfers if each claimed level is verified at admission. | Keep EV-0038 but correct its licence to Community Specification Licence 1.0 and replace its distant date with an event review. Destination: supply-chain provenance WG relations. |
| R24A `does-well` | SLSA provenance is verifiable information about where, when and how an artefact was produced. | Provenance can accurately describe a malicious or flawed production process. | Provenance proves an origin claim within its trust model. It does not remove producer trust. | Destination: refresh GD-SUPPLY-001 and the provenance versus producer-trust pressure relation. Do not say an attestation verifies artefact safety. |
| R25 `does-well` | The SLSA threat model explicitly names threats addressed by levels and threats outside scope, including a producer intentionally submitting bad code, selection attacks and insecure use of a correct artefact. | The model is a framework, not outcome measurement. Recursive treatment of dependencies can become costly and incomplete. | The stated non-goals are as important as the controls. | Keep EV-0549. Use it to sharpen the provenance WG and threat-shaped security DOC relation. No new evidence row is needed unless the frozen artefact differs. |
| R26 `does-well` | Version 3 reports 260 configurations over six benchmarks, five architectures and three model families. It reports an 80.8 per cent gain on a decomposable finance task, a 70 per cent loss on sequential planning, coordination overhead on tool-heavy tasks, error propagation without central verification, and 87 per cent held-out architecture selection. The fitted capability model reports R-squared 0.373, rising to 0.413 with grounded capability. | These are benchmark results, not a repository-software study. Relative results depend on the model families, harness, task graph and oracle. The paper is a preprint and its fitted model leaves most variance unexplained. | The transferable direction is that decomposability, tool load, baseline capability and verifier placement decide topology. The exact cut-offs are not universal. | Supersede or refresh EV-0452 from v1 to v3 and correct its licence. Destination: refresh the existing agent-topology WGs, not a new swarm Doctrine. |

## What the source set changes

Three conclusions survive the transfer limits.

First, a Doctrine should not claim to be true without conditions. In EOS terms
it is a scoped default with evidence, applicability and named pressure tests.
Binding remains reserved for the safety floors and other rules that earn it
under GOVERNANCE. A package choice, visual preference or architecture shape is
not binding merely because it is often sensible.

Second, one advanced Wargame form is enough. ALWF supports a lifecycle from
question through exploitation; ATAM supports forces, quality attributes and
sensitivity; NIST supports constrained interaction coverage. These are
complementary fields in one procedure type, not three types of scenario. A WG
should be able to carry:

- the decision question and scope;
- the Doctrines or defaults under pressure;
- options, forces and affected qualities;
- applicability and disqualifying conditions;
- hypotheses, observables and an evidence-collection plan;
- constraints and interactions, with excluded combinations explained;
- the cheapest discriminating test and the full assurance route;
- the ruling, confidence, residual risk, review trigger and supersession; and
- exploitation: which relation, Doctrine, profile or local ruling changes.

Third, named software belongs on a dated profile. The durable compute rule is
to keep the highest-level sufficient representation, preserve an ecosystem
contract where it matters, measure representative work before acceleration,
and distribute only on demonstrated pressure. The current profile may select
Polars, pandas, NumPy, Numba, DuckDB, Spark or another maintained tool, but a
versioned package name is not timeless Doctrine.

## Reconciliation of the eleven standing candidates

`Merge or link` means normalise the current normative atom into the first-class
DOC registry and point to the existing procedure. It does not mean write the
same rule again in a new prose file.

| Candidate | Current EOS coverage and source result | Disposition before authorship |
| --- | --- | --- |
| 1. Representative measurement | The principle appears in individual performance and reliability decisions, but no one standing atom defines the baseline, representative data or workload, acceptance measure and hardware context together. R05, R07, R09, R12, R13 and R18 all make context material. | **Admit one new scoped DOC.** Default wording should require representative measurement before a material performance, capacity or tool claim. A spike may use a cheaper sample if its mismatch is recorded. Link every compute WG to it. |
| 2. Scoped data-compute defaults | GD-DATA-004 covers analytical storage, not dataframe, query or numerical execution. The official docs show distinct semantics and changing package routes. | **Split durable rule from dated profile.** Admit a DOC for the measured promotion ladder. Put the current local-tabular default and versions in a `STACK-*` profile. Do not put `Polars first`, a version or a data-size threshold in timeless Doctrine. |
| 3. Semantic HTML | The UI pack has component sourcing and accessibility assurance, but no explicit standing native-semantics-first atom. R16 and R17 support the default; R15 supplies the conformance floor. | **Admit one new DOC.** Use native HTML semantics and behaviour first. ARIA or a custom interaction must name the missing native capability and carry keyboard, focus and assistive-technology tests. Link the new custom-control WG. |
| 4. User- and task-shaped interface philosophy | GD-UIUX-001 already decides per surface from audience, task, session and failure cost and deliberately refuses an estate-wide visual default. R14 supports that direction. | **Merge or link.** Promote the existing normative atom into DOC form without new prose. Keep PatterTech house style opt-in and subordinate to user, task, accessibility and measured performance. |
| 5. One deployable until distribution is earned | GD-ARCH-001 and WG-ARCH-001 already hold the modular-monolith default and measured split pressures. R19 supports the cost-of-complexity direction but adds no new fork. | **Merge or link.** Normalise the current rule and relation. Do not create another monolith Doctrine or architecture file. |
| 6. Small, reversible, evidenced changes | Product-discovery's reversible-test rules, GD-DISC-001 and WG-DEL-007 already separate cheap learning from gate-bearing work. R19A sharpens the spike boundary. | **Merge or link, then refresh relations.** Keep size, reversibility and evidence as separate axes. Add a relation to the spike-versus-hardened WG rather than another general delivery rule. |
| 7. Journey-, objective- and restoration-led reliability | GD-DEVOPS-003, GD-DEVOPS-004 and WG-OPS-003 already cover error budgets, user impact and evidenced restore. R18 and R20 reinforce them. | **Merge three existing atoms, do not make one compound DOC.** Relate user journey to SLI and objective, objective to change policy, and persistent data to restoration proof. Compound prose would hide different activation predicates. |
| 8. Threat-shaped security | The security pack, its threat catalogue, GD-SEC-003 and supply-chain threat material already make controls proportional to surface and protected property. R23 and R25 support outcome and threat boundaries. | **Merge or link.** Normalise the existing rule, retain binding safety floors, and route disputes to domain WGs. Do not weaken a floor because a general threat model scored it low. |
| 9. Simplest sufficient agent topology | GD-AGENT-001 and GD-SWARM-001 already start with one bounded agent and promote on decomposability, context, oracle, side-effect and restart pressures. R26 v3 is a needed evidence refresh, not a new rule. | **Merge or link and refresh evidence.** Supersede EV-0452's v1 facts and wrong licence. Do not create a second swarm Doctrine. |
| 10. Fully described evaluation harnesses | GD-AIML-001, GD-AIML-003, GD-AGENT-004, WG-DEL-006 and delivery-test requirements already separate task, data, scorer, oracle and independence. | **Merge or link.** One DOC atom should point to the existing harness and judge procedures. Add no new procedure until a pressure escapes those choices. |
| 11. Golden paths with tested escape routes | The capability registry deliberately keeps platform engineering registry-only until the estate has a second team. Existing profiles, seed routes and individual WGs provide defaults and local escape decisions, but the approved source set contains no platform outcome evidence. | **Defer first-class DOC authorship.** Keep the capability and its second-team review trigger. Individual defaults still need tested escape routes, but calling that a platform Doctrine now would evade ADR-0014 decision five. |

## Exact pressure-backlog dispositions

The labels below are the four labels fixed by ADR-0014. `existing WG
refreshed` includes a current `GD-*` procedure that ADR-0012 maps to the
unified semantic Wargame kind while preserving its public identity. This
packet does not recommend renaming those IDs. `new WG` is an admission result,
not a demand for one file per row. Closely coupled rows may share one advanced
WG if each pressure remains independently addressable and ruleable.

### Data compute

| No. and named pressure | Disposition | Existing coverage, reason, cheapest discriminator and destination |
| --- | --- | --- |
| 1. Polars/pandas/DuckDB/Spark | `new WG` | Current analytical-storage guidance does not choose a compute engine. Admit an analytical engine-selection WG under the existing data surface. Cheapest discriminator: run one representative query or pipeline at target scale and record semantic fit, wall time, peak memory or spill, operational surface and integration cost. R05 to R07 and R11 to R13 apply. |
| 2. dataframe-to-array or solver boundary | `new WG` | No current procedure owns representation movement, dtype, layout, ownership, device or numerical tolerance. Admit a representation-boundary WG. Cheapest discriminator: a round trip over representative data that records copies, dtype and layout changes, peak memory, result tolerance and boundary cost. R07 and R08 apply. |
| 3. NumPy/Numba/native/GPU | `new WG` | The acceleration ladder is absent and a general `Numba plus GPU` default is stale on arrival. Admit an acceleration WG. Cheapest discriminator: profile the baseline, then compare compile-inclusive first run and steady state under the same correctness oracle. Record fast-math or device changes separately. R08 to R10 apply. |
| 4. eager/lazy/streaming/out-of-core and reproducibility | `new WG` | Existing storage guidance does not settle execution mode, and reproducibility is not a synonym for out-of-core execution. Admit or combine an execution-mode WG with case 1. Cheapest discriminator: repeat the target pipeline with pinned inputs and seed, record plan, ordering, peak memory, spill, duration and output hash or tolerance across two clean runs. R05, R12 and R13 apply. |

### Web and UI

| No. and named pressure | Disposition | Existing coverage, reason, cheapest discriminator and destination |
| --- | --- | --- |
| 5. static/SSR/CSR/islands/PWA/native | `new WG` | GD-NAT-001 covers native-client architecture, but no live web procedure owns the complete delivery fork and retired WG-WEB IDs cannot be revived. Admit a new web-delivery WG and relate native outcomes to GD-NAT-001. Cheapest discriminator: implement one representative route and measure first useful content, interaction, navigation, accessibility tree, offline requirement, cache behaviour and operational complexity on target devices. |
| 6. Novice versus expert density | `relation covered without new file` | GD-UIUX-001 already asks the question per surface and includes first-time, expert, task and failure-cost pressures. Relate the user-and-task DOC to it. Cheapest discriminator: task completion, error and search time with representative novice and expert users. A new density file would duplicate a live procedure and a retired identity. |
| 7. semantic DOM/ARIA versus canvas/custom controls | `new WG` | GD-UIUX-002 and GD-UIUX-003 cover component source and assurance depth, but not the rendering and interaction boundary when native semantics cannot express the product. Admit a semantic-versus-custom-interaction WG. Cheapest discriminator: keyboard-only and accessibility-tree inspection of the hardest representative interaction, followed by named screen-reader and browser pairs if custom behaviour remains. R15 to R17 apply. |
| 8. house style and motion versus audience, accessibility and performance | `relation covered without new file` | GD-UIUX-001, GD-UIUX-003, GD-HOUSE-001 and the UI pack's motion floor already separate audience, optional house taste, reduced motion and measured performance. Add explicit conflict relations. Cheapest discriminator: representative-user task check plus reduced-motion and low-end target-device frame and loading measurements. A new WG would restate current procedures. |

### Architecture and data flow

| No. and named pressure | Disposition | Existing coverage, reason, cheapest discriminator and destination |
| --- | --- | --- |
| 9. modular monolith versus services | `existing WG refreshed` | GD-ARCH-001 already defaults to one deployable and names earned split pressures; WG-ARCH-001 covers boundary enforcement. Refresh the semantic WG with ATAM-style quality, sensitivity and reversal fields and link the standing DOC. Cheapest discriminator: map change coupling, deployment cadence, isolation, ownership and capacity from recent work, then test one proposed seam without splitting deployment. R02 and R19 apply. |
| 10. synchronous versus queue/event/stream | `new WG` | WG-ARCH-004 covers background-work machinery and GD-DATAENG-001 covers ingestion modes, but neither owns the general interaction contract across latency, ordering, retry, consistency and replay. Admit a messaging-and-flow WG. Cheapest discriminator: failure-inject one representative operation and measure latency, duplicate handling, ordering, retry, replay and user-visible state. |
| 11. storage-engine selection | `new WG` | WG-ARCH-002 chooses access style, WG-ARCH-008 topology and GD-DATA-004 analytical storage. None chooses transactional, analytical, search, graph, object or time-series engine from workload and recovery needs. Admit a storage-engine WG. Cheapest discriminator: replay a representative read/write trace and a restore or rebuild path against the simplest two candidates. |
| 12. local/cloud/hybrid/offline and consistency | `new WG` | GD-NAT-002 covers offline client writes but not whole-system placement, data ownership and consistency across local, hosted and hybrid operation. Admit a locality-and-consistency WG and relate the native procedure. Cheapest discriminator: disconnect during a representative write journey, reconnect, reconcile concurrent changes and measure data loss, conflict visibility and recovery effort. |

### Workflow and delivery

| No. and named pressure | Disposition | Existing coverage, reason, cheapest discriminator and destination |
| --- | --- | --- |
| 13. spike versus hardened vertical slice | `existing WG refreshed` | WG-DEL-007 already sends exploratory work to an explicit spike branch and brings retained work back through the router; GD-DISC-001 scales discovery by reversibility. Refresh it with a named deletion, promotion and evidence boundary. Cheapest discriminator: build the narrowest end-to-end path, then list the hardening work that would be required before any artefact reaches users. R19A applies. |
| 14. doubles/sandbox/live and oracle independence | `existing WG refreshed` | WG-DEL-005 and WG-DEL-006 already cover fidelity and independent truth. Refresh their relation and add service-contract drift as a pressure. Cheapest discriminator: run the same contract against the selected double and the nearest available real boundary, then introduce one seeded mismatch that an independent oracle must catch. |
| 15. incident hotfix versus normal gates | `new WG` | Release control and review gates assume normal delivery. No current WG describes the bounded incident override while retaining safety floors, known-good state, impact checks and rollback. Admit an incident-hotfix WG under delivery and reliability. Cheapest discriminator: a timed staging drill that applies and rolls back one representative urgent fix while preserving the non-waivable checks. R21 applies. |
| 16. build/buy/managed service versus portability and incident access | `new WG` | WG-ARCH-007 covers vendor seams and GD-SUPPLY-004 covers vendoring code, but neither decides capability ownership or proves that an operator can diagnose, export and recover during provider failure. Admit a capability-ownership WG in architecture with supply-chain relations. Cheapest discriminator: perform an outage, export and restore exercise against the leading managed option and estimate the smallest owned alternative. |

### Reliability and supply chain

| No. and named pressure | Disposition | Existing coverage, reason, cheapest discriminator and destination |
| --- | --- | --- |
| 17. fail closed versus honest degradation | `new WG` | Individual rules fail closed, but there is no cross-domain procedure for retaining minimum useful service without weakening privacy, authorisation, integrity or approval floors. Admit a degradation WG. Cheapest discriminator: inject loss of one dependency and verify the promised minimum journey, truthful status, monitoring, kill switch and protected properties. R22 applies. |
| 18. observability versus privacy | `new WG` | The coverage registry identifies observability as an unowned capability, while privacy rules constrain what telemetry may contain. This is a high-consequence uncovered tension. Admit an observability-and-privacy WG under reliability with security activation. Cheapest discriminator: diagnose one seeded incident from redacted telemetry and test the same records for secret, personal-data and cross-tenant leakage. |
| 19. provenance/SBOM versus producer trust | `existing WG refreshed` | GD-SUPPLY-001 already decides provenance strength, and EV-0549 records the producer-intent limit. Refresh the semantic WG to state what provenance and an SBOM establish, what they do not, and who verifies them at admission. Cheapest discriminator: verify a correctly attested artefact whose source or selected dependency is deliberately policy-bad. R24, R24A and R25 apply. |
| 20. dependency freshness versus known-good deployment | `existing WG refreshed` | GD-SUPPLY-003 already holds the freshness and cooldown fork, while GD-DEVOPS-002 holds staged release and rollback. Add a hard relation between them and a security-fix exception test. Cheapest discriminator: take one representative security update through the cooldown exception, suite, canary or flag, rollback and incident reconstruction path. |

### AI and governance

| No. and named pressure | Disposition | Existing coverage, reason, cheapest discriminator and destination |
| --- | --- | --- |
| 21. deterministic workflow/single agent/swarm | `existing WG refreshed` | GD-AGENT-001 and GD-SWARM-001 already cover the topology ladder. Refresh EV-0452 to paper v3 and add tool-load and central-verification pressures. Cheapest discriminator: compare one bounded single-agent baseline with the smallest justified decomposition under the same task set, model budget and external verifier. R26 applies. |
| 22. local/hosted/hybrid models | `new WG` | GD-AIML-005 covers model choice, cost and retirement but not inference locality, data movement, device capacity, provider outage or hybrid fallback. Admit a model-hosting WG under AI-ML. Cheapest discriminator: run the same frozen evaluation set locally and hosted, then simulate network or provider loss and record quality, latency, cost, data route and recovery. |
| 23. deterministic/human/model judges | `existing WG refreshed` | GD-AIML-003 and WG-DEL-006 already answer the scorer and independence questions. Refresh their relation and keep deterministic scoring first where correctness is decidable. Cheapest discriminator: calibrate each proposed judge against the same human-labelled sample, report agreement, disagreement, order effects, abstention and cost. |
| 24. golden path versus autonomy | `rejected with reason` | Reject WG admission in this programme. The platform-engineering capability is registry-only by ADR-0014 because the estate has one operator and no internal teams consuming a platform. Existing stack, seed and domain WGs already provide local defaults and escape decisions. Reopen only on the recorded second-team trigger, then test completion, failure recovery and escape-route cost for one consumer task. |
| 25. local exception versus doctrine promotion | `relation covered without new file` | GOVERNANCE already separates a newer local ruling from estate authority, requires overlap and a generalisability note before contesting a default, and defines the promotion ladder. ADR-0014 adds pressure-led admission. Add DOC-to-ruling and promotion-evidence relations only. Cheapest discriminator: two argued venture rulings with overlapping applicability, independent evidence and a documented conflict. A new WG would create a second governance path. |

The disposition count is 14 `new WG`, 7 `existing WG refreshed`, 3
`relation covered without new file`, and 1 `rejected with reason`. This is not
a file target. Cases 1 and 4 may share an analytical-compute WG, and other
adjacent cases may combine after schema rehearsal, provided their separate
decision questions, tests and rulings remain addressable.

## Conflict and duplication pass

### Duplicates to link, not rewrite

- EV-0027 already records WCAG 2.2. R15 should refresh its event trigger if
  needed, not create another WCAG row.
- EV-0037 already records SSDF v1.1. R23 should add a review event for the
  draft revision becoming final, not duplicate v1.1.
- EV-0038 already records SLSA v1.2. It needs licence correction and a tighter
  source boundary, not a second general SLSA row.
- EV-0096 already records Google's error-budget policy. R18 is retained only
  if the SLO chapter's user-journey finding is cited separately.
- EV-0423 already records Google incident management. R21 is retained only
  for distinct workbook claims used by the hotfix WG.
- EV-0549 already records the SLSA v1.2 threat model and its producer-intent
  limit. R25 must reuse that row.
- GD-UIUX-001, GD-ARCH-001, GD-DISC-001, WG-DEL-005, WG-DEL-006,
  WG-DEL-007, GD-DEVOPS-003, GD-DEVOPS-004, WG-OPS-003, GD-SUPPLY-001,
  GD-SUPPLY-003, GD-AGENT-001, GD-SWARM-001 and GD-AIML-003 already own
  several proposed rules and forks. Their public IDs and paths stay stable.

### Contradictions that must be resolved

1. **EV-0452 is stale and its licence is wrong.** It records arXiv v1 from
   2025-12-09, 180 configurations and four domains under CC BY 4.0. The
   current paper is v3 from 2026-04-08, 260 configurations and six benchmarks,
   and the arXiv page carries the non-exclusive distribution licence. Any
   current guide figures derived from v1, including 80.9 rather than 80.8 per
   cent, must be checked against v3 before reuse.
2. **EV-0038 leaves the SLSA licence `unknown exact`.** The v1.2 specification
   states Community Specification Licence 1.0, consistent with EV-0549. The
   row should be corrected with licence evidence.
3. **A timeless `Polars plus NumPy plus Numba` Doctrine would conflict with
   ADR-0014.** Package choice and versions belong in a dated stack profile.
   The durable DOC may define the measured promotion ladder only.
4. **Graceful degradation can conflict with protected fail-closed floors.**
   The new WG must make privacy, authorisation, integrity and consequential
   approval disqualifiers or guarded conditions, not options of equal weight.
5. **Retired web IDs cannot carry new guidance.** WG-WEB-006 and
   WG-WEB-007 remain retired even where the concepts recur. New admitted
   web WGs receive new live identities under the integrator's allocation.

### Tensions that are real but not contradictions

- Lazy, streaming, out-of-core and distributed execution trade visibility,
  memory, ordering, cost and operational complexity. None dominates without a
  workload.
- Semantic HTML is the default, but canvas and custom interaction can be the
  only sufficient representation for some editing, visualisation or spatial
  tasks. The exception earns behaviour and assistive alternatives.
- Small changes improve review and recovery, but incident mitigation sometimes
  has to move faster. The hotfix route keeps fewer, stronger checks and a
  tested rollback rather than removing the gate.
- Provenance establishes production facts within a trust model. It cannot
  establish benign producer intent or product correctness.
- A swarm can improve a decomposable task and sharply damage a sequential or
  tool-heavy one. This is exactly why topology remains a Wargame rather than a
  universal multi-agent preference.
- Accessibility conformance is necessary evidence and still incomplete as a
  user outcome. WCAG, behaviour tests and user testing answer different
  questions.

### Pack admission results

- **Scientific and reproducible computing remains registry-only.** The packet
  supplies more than three maintained primary sources and a genuine
  contradicting choice, but this lane did not establish two materially
  distinct executable local examples, a sanitised exemplar, a reviewable drill
  or the admission boundary required by ADR-0014. Dated compute profiles and
  WGs should stay under the existing data surface for this tranche.
- **Platform engineering remains registry-only.** The second-team activation
  trigger has not fired, which is why case 24 is rejected for this programme.
- **No new web, UI, reliability, supply-chain or AI pack is needed.** The
  admitted WGs have live destination packs or cross-pack ownership. The
  observability gap can start as a reliability WG with security activation;
  pack admission waits for a repeated broader capability pressure.

## Evidence retention and ledger actions

Retention follows PB-E11's test: keep a source only if removing it would change
a decision. Every retained artefact gets its own row after a frozen copy or
content identity exists.

| Action | Sources | Reason |
| --- | --- | --- |
| Add if the WG form changes | R01, R02, R03 | They independently support analysis lifecycle, trade-off and sensitivity structure, and constrained interaction coverage. R04's headline reductions and R04A's tool choice are not needed to settle the schema. |
| Add with admitted compute content | R05, R06, R07, R08, R09, R10, R11, R12, R13 | Each settles a different engine, boundary, acceleration, deprecation or execution claim. Keep rows separate and mark project comparisons as maintainer evidence. |
| Add with admitted UI content | R14, R16, R17 | They settle user-first design status, native semantic constraints and the behaviour obligation of custom ARIA. Reuse EV-0027 for R15. |
| Add only where the distinct claim is used | R18, R19A, R21, R22 | User-led SLOs, spike separation, incident mitigation and graceful degradation each change a proposed rule or WG. R19 and R20 merely reinforce current procedures and do not pass the retention threshold. |
| Reuse or correct | R23 through EV-0037; R24 through corrected EV-0038; R25 through EV-0549; R26 through refreshed EV-0452 | Existing rows own the sources or source families. Correct facts and terms rather than mint duplicates. R24A needs its own row if the provenance page is directly cited. |
| Do not add | R04, R04A, R19, R20 | Their absence does not change the recommended disposition. Keep them in this packet as checked context, not as ledger weight. |

Licence evidence must distinguish source-code terms from documentation terms.
An MIT, BSD or Apache code repository does not by itself license the wording of
its documentation. The safe integration posture is attribution, links and
fresh paraphrase. In particular:

- reproduce no SEI diagrams, tables or substantial method wording without
  written permission;
- adapt no Google SRE diagrams or prose under CC BY-NC-ND;
- copy no wording from the agent paper under arXiv's distribution-only terms;
- preserve W3C and NIST attribution and avoid endorsement claims;
- inspect third-party notices before carrying any project asset or code; and
- carry no private-repository wording, local paths, commercial detail,
  personal data or exact deployment facts into EOS.

## Negative results worth keeping

- No primary source supports a file-count target for Wargames.
- No source supports Polars, pandas, DuckDB, Spark, NumPy, Numba, native code
  or GPU as an unconditional winner.
- No published row supplies a universal dataset-size threshold for changing
  engines or enabling JIT or distributed compute.
- No source makes WCAG conformance equivalent to accessibility or usability.
- No source makes provenance equivalent to producer trust or artefact safety.
- No source makes multi-agent coordination a general improvement.
- The approved source set does not earn a platform-engineering pack or DOC.
- This packet does not meet the scientific-computing pack gate.

These rejections should become lesson rows if the operator accepts them. That
prevents the same unsupported proposals returning later as new work.

## Bounded operator decision batch

No lesson or content integration should infer approval from this report. The
smallest useful decision batch is:

1. **Standing rules.** Accept three new scoped DOC candidates
   (representative measurement, measured data-compute promotion, semantic
   HTML), merge or link candidates 4 to 10, and defer candidate 11?
   Recommendation: yes. Alternative: defer all new DOCs and build only WGs,
   which leaves the safe defaults invisible. If deferred, author nothing.
2. **Pressure backlog.** Accept the exact 25 dispositions, while allowing one
   advanced WG to cover adjacent admitted rows where both remain separately
   addressable? Recommendation: yes. Alternative: one file per pressure,
   which is easier to count but creates duplicate decision context. If
   deferred, retain the backlog as proposals only.
3. **Data profile.** Approve a dated local-tabular stack profile whose starting
   point is Polars for new local analytical work, pandas where its ecosystem or
   semantics are the contract, NumPy at a justified array boundary, Numba only
   for a measured hotspot, DuckDB for local analytical query and spill, and
   Spark only on demonstrated distribution pressure? Recommendation: yes,
   subject to versions and review triggers at integration. Alternative: a
   tool-neutral profile, which is more durable but does not answer the user's
   request for a useful default. Reject putting those names in timeless DOC.
4. **Evidence integrity.** Approve correction of EV-0038 and EV-0452 and the
   one-source-per-row additions only when their dependent content is admitted?
   Recommendation: yes. Alternative: retain stale rows, which would make the
   new content less reliable than the sources used to write it.

## Dependency-ordered expansion plan

### Gate 0: substrate and evidence integrity

1. Wait for the resolver, DOC/WG schemas, relation schema, compatibility
   layer, migration ledger and generated-view path required by ADR-0014.
2. Correct EV-0038 and EV-0452 first, since current content already relies on
   them.
3. Freeze retained public sources and create the approved evidence and lesson
   rows. Do not retain R04, R04A, R19 or R20 as ledger weight.
4. Confirm the public ID allocator excludes every retired WG identity and that
   existing GD and WG identities remain stable.

### Tranche 1: make the safe defaults visible

1. Admit the three scoped DOC candidates if approved.
2. Normalise candidates 4 to 10 from their existing normative atoms. Link
   rather than copy their prose.
3. Add the dated data-compute profile. Give package versions dated or
   event-based review triggers and an explicit applicability boundary.
4. Leave the golden-path candidate registry-only with its second-team trigger.

### Tranche 2: close the highest-consequence pressures

1. Author the incident-hotfix, fail-closed-versus-degradation and
   observability-versus-privacy WGs.
2. Refresh provenance-versus-producer-trust and dependency-freshness relations.
3. Author the semantic-versus-custom-interaction WG because accessibility loss
   is hard to detect after a rendering architecture has settled.
4. Run the protected-set conflict check before any of these becomes live.

### Tranche 3: build the compute decision family

1. Author engine selection and execution mode together or as two linked WGs.
2. Author representation-boundary and acceleration WGs.
3. Use the same sanitised representative pipeline across their worked
   examples, but keep each decision and result independently ruleable.
4. Keep the scientific-computing capability registry-only. Re-run its pack
   admission gate only when two qualifying executable local examples and a
   drill exist.

### Tranche 4: architecture, workflow, web and AI

1. Refresh deployment shape, spike hardening, doubles and oracle WGs.
2. Author messaging and flow, storage engine, locality and consistency, and
   capability ownership WGs.
3. Author web delivery and model-hosting WGs.
4. Refresh agent topology and judge selection after the evidence corrections.
5. Add relation-only coverage for density, house style and Doctrine promotion.

### Tranche 5: integrate and prove the graph

1. Resolve every new DOC, WG, profile, evidence row and relation through the
   public resolver and compatibility aliases.
2. Regenerate all derived views from canonical sources. Never hand-edit an
   index.
3. Prove every high-consequence DOC conflict reaches at least one WG or dated
   fallback, and every WG reaches its evidence, DOCs, destinations and review
   trigger.
4. Run migration rehearsal, schema tests, graph checks, full pytest and
   `python -m tools.eos check --repo` without opening the sealed benchmark.

## Acceptance criteria for the content tranche

- The twenty-five named pressures appear once each with exactly one approved
  disposition.
- The eleven standing candidates each resolve to a new scoped DOC, an existing
  normalised atom, or a recorded deferral. No candidate is duplicated in prose.
- Every retained source has one evidence row with organisation, exact title,
  version or commit, access date, licence evidence, fact, counterclaim,
  applicability limit, maintenance state and destination.
- EV-0038 states the exact SLSA licence and EV-0452 states paper v3 facts and
  the arXiv distribution licence. No current guide retains an unchecked v1
  figure.
- Every newly admitted WG uses the unified advanced form and records pressures,
  options, forces, affected qualities, evidence plan, constraints, cheapest
  discriminator, ruling, residual risk, review and exploitation.
- Every existing refreshed procedure keeps its GD or WG ID and public path.
  No retired ID becomes live, and no retired file is treated as guidance.
- Package names and versions occur in dated profiles or evidence, not timeless
  Doctrine. Every profile states the ecosystem and workload boundary.
- Every high-consequence conflict has a WG or a dated, reviewable fallback.
  Protected safety floors cannot be selected away by a default.
- The observability and privacy WG proves diagnostic usefulness and data
  minimisation together on a seeded incident.
- The incident route preserves non-waivable checks, known-good state, impact
  observation and rollback under a timed drill.
- Custom web interaction carries keyboard, focus, semantic or equivalent
  accessibility, and assistive-technology evidence appropriate to the claim.
- Compute worked examples report baseline, representative input, environment,
  copies or representation changes, correctness oracle, first-run and
  steady-state timing, memory and failure behaviour where relevant.
- Local or private observations are rewritten at concept level only after
  privacy and licence review. The public diff contains no local paths, personal
  data, commercial detail, copied expressive prose or source assets.
- Scientific computing and platform engineering remain registry-only unless a
  later, separately approved admission record proves their triggers.
- Canonical registries, generated views, cold migration fixtures, graph checks,
  tests and the repository checker all agree on the same live content.

## Research conclusion

The user's visible concern is real, but the gap is not `only two Wargames`.
The live estate already contains many decision procedures under stable GD and
WG identities. The gaps are that standing defaults are hard to see, the
procedures do not yet share one rich Wargame contract, several important
cross-domain pressures are absent, and the relation graph does not expose what
is already covered.

The evidence supports a substantial first expansion without manufacturing
scenarios. Three new scoped Doctrines, a dated compute profile, up to fourteen
admitted pressure WGs with sensible consolidation, seven refreshes and three
relation-only cases would make the intended model visible. The one rejected
case is useful too: it keeps platform engineering out until the estate has a
real consumer rather than a desire for symmetry.
