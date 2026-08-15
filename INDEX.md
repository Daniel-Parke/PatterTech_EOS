---
summary: Derived index of every live file, one row each, grep the tag column
type: index
tags: [eos]
derived: true
---

# INDEX

Derived file. Edit front-matter, then run
`python -m tools.eos check --write-index`. One row per live
file. Frozen trees are not indexed.

| path | type | tags | summary | review |
| --- | --- | --- | --- | --- |
| AGENTS.md | root | eos | The router: entry modes, how a tier is ruled, graph builds and the never-list |  |
| CHANGELOG.md | governance | eos | One entry per release tag, sectioned by area |  |
| CLAUDE.md | root | eos | The router: entry modes, how a tier is ruled, graph builds and the never-list |  |
| GOVERNANCE.md | governance | eos | The law of the EOS, the graded change path, precedence, promotion, the protected set, claims and records, ids, budgets |  |
| OPERATORS_GUIDE.md | guide | eos | The operator's manual for running the EOS: the ten launchers, the commands, what only you can approve, claims, the guard, the cadence, the release gate and what to do when something looks wrong | 2027-03 |
| README.md | root | eos | What the PatterTech EOS is, who it is for, where it stands against its own gates, how the repo is laid out, and how a venture consumes it |  |
| TOUR.md | guide | eos | The teaching surface for EOS 0.4.0, the words it uses in a particular way, what changed from v1, the modes, the risk layers, Genesis, the swarm method, staged verification, the study workflow and the pack system | 2027-08 |
| benchmark/PROTOCOL.md | example | eos testing | Frozen benchmark protocol for the EOS v1 versus v2 comparison, session counts, gates, custody and budget |  |
| benchmark/README.md | example | eos testing | How to run and score one benchmark session, the run_meta.json contract, and the honesty rules |  |
| benchmark/drills/README.md | example | eos testing | What a pack acceptance drill is, how the runner grades one, and what is still missing before any of them can return a verdict |  |
| benchmark/drills/agentic-development.md | example | eos | Cold-agent acceptance drill for the agentic development pack, topology selection under pressure |  |
| benchmark/drills/agentic-swarm.md | example | eos | Single-run cold-agent acceptance drill for the agentic swarm pack, cutting a partition on the dependency graph rather than on the backlog |  |
| benchmark/drills/ai-ml-llm.md | example | eos testing | Cold-agent acceptance drill for the AI, ML and LLM pack, build the gate before tuning the classifier |  |
| benchmark/drills/api-integration.md | example | eos | Single-run cold-agent acceptance drill for the API and integration pack, with deterministic machine-checkable criteria. |  |
| benchmark/drills/architecture.md | example | eos | Single-run cold-agent acceptance drill for the architecture pack, with deterministic machine-checkable criteria |  |
| benchmark/drills/business-logic-modelling.md | example | eos testing | Single-run cold-agent acceptance drill for the business logic and modelling pack, with deterministic machine-checkable criteria |  |
| benchmark/drills/business-model-pricing.md | example | eos testing | Single-run cold-agent acceptance drill for the business model and pricing pack, with deterministic machine-checkable criteria |  |
| benchmark/drills/coding.md | example | eos | Cold-agent acceptance drill for the coding pack, pin then change an undocumented parser |  |
| benchmark/drills/data-analytics.md | example | eos testing | Single-run cold-agent acceptance drill for the data-analytics pack, with deterministic machine-checkable criteria |  |
| benchmark/drills/data-engineering.md | example | eos | Single-run cold-agent acceptance drill for the data-engineering pack, testing idempotent reprocessing, backfill, and late and duplicate records |  |
| benchmark/drills/delivery-testing.md | example | eos | Cold-agent acceptance drill for the delivery, testing and quality pack, checking double choice, contract verification and flake handling |  |
| benchmark/drills/devops-reliability.md | example | eos | Single-run cold-agent acceptance drill for the devops-reliability pack, with deterministic machine-checkable criteria. |  |
| benchmark/drills/docs-dx.md | example | eos testing | Cold-agent acceptance drill for the docs-dx pack, make a stale documented flag fail the build |  |
| benchmark/drills/graders/DEMOTED.md | example | eos testing | Graders removed because an adversarial recheck proved they returned the wrong answer, and the criteria they covered now report manual |  |
| benchmark/drills/identity-access.md | example | eos | Single-run cold-agent acceptance drill for identity, authorisation and tenancy, adding a cross-tenant support role to a service whose tenant scoping is inconsistent |  |
| benchmark/drills/legal-licensing.md | example | eos testing | Proposed cold-agent acceptance drill for the legal, licensing and compliance routing pack |  |
| benchmark/drills/marketing-growth-positioning.md | example | eos | Single-run cold-agent acceptance drill for positioning, testing whether the marketing pack produces a defended position or a feature list with adjectives |  |
| benchmark/drills/marketing-growth.md | example | eos testing | Cold-agent acceptance drill for the marketing-growth pack, one launch surface plus one lifecycle sequence, machine-checked |  |
| benchmark/drills/native-client.md | example | eos testing | Cold-agent acceptance drill for the native-client pack, an offline-capable client with a declared conflict policy and a forward-only release path |  |
| benchmark/drills/pattertech-house.md | example | eos testing | Single-run cold-agent acceptance drill for the PatterTech house style, with deterministic machine-checkable criteria |  |
| benchmark/drills/product-discovery.md | example | eos testing | Cold-agent acceptance drill for the product-discovery pack, frame a solution request back into a testable opportunity |  |
| benchmark/drills/research-knowledge.md | example | eos | Single-run cold-agent acceptance drill for the research and knowledge-base capability, deciding between two approaches on sources of mixed quality and recording what was found |  |
| benchmark/drills/security-privacy.md | example | eos | Proposed cold-agent acceptance drill for the security, privacy and safety pack |  |
| benchmark/drills/supply-chain-integrity.md | example | eos | Single-run cold-agent acceptance drill for the supply-chain and release-integrity capability, frozen before any pack for it was authored, with deterministic machine-checkable criteria. |  |
| benchmark/drills/support-operations.md | example | eos testing | Single-run cold-agent acceptance drill for the support-operations pack, with deterministic machine-checkable criteria |  |
| benchmark/drills/ui-ux-greenfield.md | example | eos | Single-run cold-agent acceptance drill for a greenfield non-PatterTech interface, testing that the pluralism contract survives contact with a brief the house style does not fit |  |
| benchmark/drills/ui-ux.md | example | eos | Cold-agent acceptance drill for the ui-ux pack, two philosophies, one behaviour core, machine-checked |  |
| benchmark/drills/writing-content.md | example | eos testing | Cold-agent acceptance drill for the writing-content pack, make a concatenated error string survive a second locale |  |
| estate/ESTATE_MAP.md | registry | eos | The estate narrative, how the repos relate, which are governed and what the seams between them are | 2026-11 |
| examples/pattertech-website.md | example | web brand | Worked example, the PatterTech website redesign v1 to v4 |  |
| examples/v2-worked-high-assurance.md | example | eos | Worked example, an auth change routed R3 end to end, oracle first, reviewer and operator at the gate |  |
| examples/v2-worked-lean.md | example | eos | Worked example, an Express run end to end in an S venture, from request to commit |  |
| examples/venture-a-seed.md | example | eos | Worked example, the Venture A reseed, the first L-scale compile from the kernel |  |
| inception/COMPILE.md | kernel | eos | The seed compiler's rules, prune, fill and the slot table, policy fill, distil, report, and the never-list |  |
| inception/EXPRESS_INCEPTION.md | kernel | eos | The S-scale fast path for Session 0, six questions, inherited defaults, two human gate items |  |
| inception/GENESIS.md | kernel | eos | The Genesis phase, run in the venture repo after the seed gate, and the development blueprint it produces |  |
| inception/INCEPTION.md | kernel | eos | The Session 0 master playbook, phases A to E, from idea to signed seed |  |
| inception/INTERVIEW.md | kernel | eos | The intake protocol, eighteen questions, the risk-surface set and the three challenge steps |  |
| inception/README.md | kernel | eos | The Session 0 system, the two paths and the files that run them |  |
| inception/WALK_ORDER.md | kernel | eos | How the pack activation walk is built, the always-walk set, the canonical order over every pack and the two ruling budgets |  |
| inception/briefs/BRIEF-S-brochure.md | kernel | eos | Canned drill brief, a sole-trader joinery brochure site, scripted operator answers |  |
| inception/wargames/WG-EOS-001-venture-scale.md | wargame | eos wargame | What scale of organisational machinery does this venture compile, S or ORG? | 2027-07 |
| inception/wargames/WG-EOS-002-repo-shape.md | wargame | eos wargame infra | One repo, several, or a corner of an existing one? | 2027-07 |
| kernel/GUARD_SPEC.md | kernel | eos | The action-time guard, ten guarded classes, four verdicts, non-waivable floors, fail closed |  |
| kernel/METADATA_SPEC.md | kernel | eos | The nine metadata axes, per-kind required minima, derived defaults and compatibility rules |  |
| kernel/POLICY_SPEC.md | kernel | eos | The risk model law, the semantic factor table, tier routing, exceptions and recomputation |  |
| kernel/PREDICATES.md | kernel | eos | The controlled vocabulary of pack activation predicates, grouped by subject so two names for one fact sit next to each other, each with what settles it |  |
| kernel/README.md | kernel | eos | The kernel in v2, the law files and the compile contract |  |
| kernel/SCALE_MATRIX.md | kernel | eos | The v2 seed law, the S and ORG file lists, first-use directories, trigger add-ons |  |
| kernel/SEED_RUBRIC.md | kernel | eos | The pass gate for a compiled seed, auto items keyed to v2 checker ids, human items headed by cold-start |  |
| kernel/adapters/README.md | kernel | eos | The shape of a guard adapter mapping file, key by key, and where each rule about it is written |  |
| kernel/templates/ACCEPTANCE_SPINE.tpl.md | template | eos | Acceptance spine template, the journey walk-through as a suite skeleton that starts failing and goes green journey by journey |  |
| kernel/templates/AGENTS.tpl.md | template | eos | Venture router template, the policy-routed v2 entry, compiled output capped at 40 lines |  |
| kernel/templates/COMPILE_REPORT.tpl.md | template | eos | Compile report template, the seed's ancestry proof and the rubric sign-off record |  |
| kernel/templates/EOS_FEEDBACK.tpl.md | template | eos | Venture feedback file template, the one channel back to the EOS, harvested monthly |  |
| kernel/templates/LENS.tpl.md | template | eos | Lens contract template, the eight parts agreed before an external source is studied and the provenance every lesson carries |  |
| kernel/templates/LOCKBOOK.tpl.md | template | eos | Venture lock-book template, the machine rulings header and the module contract sections |  |
| kernel/templates/OPERATORS_GUIDE.tpl.md | template | eos | Venture operators guide template, the human's manual, v2 launcher library per scale |  |
| kernel/templates/PRODUCT_MAP.tpl.md | template | eos | Product map template, the domain model, contracts, dependency graph and per-journey acceptance conditions Genesis fills |  |
| kernel/templates/RESEARCH_PACKET.tpl.md | template | eos | Research packet template, sourced facts and the decisions they settle, with a stopping condition and a cap |  |
| kernel/templates/TASKS.tpl.md | template | eos | S-scale task list template, the single hand-kept work surface at the smallest scale |  |
| kernel/templates/VENTURE_BRIEF.tpl.md | template | eos | Venture brief template, the business truth the interview produces, challenge steps recorded |  |
| kernel/templates/WORK_PACKAGE.tpl.md | template | eos | Work package template, the objective, contracts, ownership boundary, context packet and acceptance conditions a build lane receives |  |
| kernel/templates/org/CONSTITUTION.tpl.md | template | eos | Venture constitution template, Part I product slot, Parts II and III the protected v2 law |  |
| kernel/templates/org/GRAPH_BUILD.tpl.md | template | eos | Venture graph-build template, how a partition is cut, what a lane brief carries, how the integrator merges and what stops a run |  |
| kernel/templates/org/PLAYBOOKS.tpl.md | template | eos | Venture playbook template, per-mode procedures plus wide build, hardening, incident, upkeep and retro |  |
| kernel/templates/org/QUESTIONS.tpl.md | template | eos | Questions template, the human decision queue and its folding rule |  |
| kernel/templates/org/START.tpl.md | template | eos | Venture boot template, per-mode budgets, ground rules, close only when exceptional |  |
| kernel/templates/org/TEMPLATES.tpl.md | template | eos | Canonical artefact shapes template, task records, spikes, ADRs, questions, incidents |  |
| kernel/templates/org/TESTING.tpl.md | template | eos | Adaptive testing law template, staged verification, timing by change class, the test map, quality signals |  |
| kernel/templates/org/roles/EXECUTOR.tpl.md | template | eos | EXECUTOR charter template, the default owner who plans, implements, tests and documents |  |
| kernel/templates/org/roles/ORACLE.tpl.md | template | eos | ORACLE charter template, independent gate-test author for high-assurance work |  |
| kernel/templates/org/roles/REVIEWER.tpl.md | template | eos | REVIEWER charter template, acceptance judgement, sampled review and bounded repair |  |
| org/PLAYBOOKS.md | org | eos | The EOS-side playbooks, PB-E01 to PB-E12, the mode procedures and the monthly pass |  |
| org/STATE.md | org | eos | Derived state view of claims, operator flags, cadence and machine facts |  |
| org/TASKS.md | org | eos | Derived task table, one row per record under org/tasks/ |  |
| org/decisions/ADR-0001-eos-v1-architecture.md | decision | eos | The founding decision, PatterTech EOS v1.0 architecture and the argument for it |  |
| org/decisions/ADR-0002-eos-v2-adaptive-agentic-development.md | decision | eos | EOS v2 architecture, adaptive agentic development, accepted with eight binding clarifications |  |
| org/decisions/ADR-0003-lightness-and-honest-generation.md | decision | eos | Retained material that misleads an agent is a defect, the archive of record is a tag, and every derived file has a live generator |  |
| org/decisions/ADR-0004-fewer-promises-all-of-them-kept.md | decision | eos | Two rungs not three, exceptions are ADRs, pack budgets measured where loading actually happens, and the two controls that were described but never ran |  |
| org/decisions/ADR-0005-four-corrections-in-the-protected-set.md | decision | eos | Four false statements in protected files, the corrections applied to them, and why they needed a record first |  |
| org/decisions/ADR-0006-genesis-exemplar-learning-and-the-swarm-pack.md | decision | eos | EOS v2.1, the Genesis blueprint phase, the exemplar-learning workflow, the agentic-swarm pack, hands-off ventures and staged verification |  |
| org/decisions/ADR-0007-one-release.md | decision | eos | Hold v2, fold v2.1 into it, release once, strike the two efficiency gates with reasons and retire the sealed suite unopened |  |
| org/decisions/ADR-0008-less-law-better-kept.md | decision | eos | The de-restriction pass, what stops binding and what stays, and what catches each loosened failure instead |  |
| org/decisions/ADR-0009-a-version-that-means-something.md | decision | eos | Re-designate the current line to 0.x, and define the checkable gate that 1.0 has to pass |  |
| org/decisions/ADR-0010-one-name-per-fact.md | decision | eos | A controlled vocabulary for pack activation predicates, grouped by subject, with the first duplicate merged |  |
| org/decisions/ADR-0011-a-role-not-a-name.md | decision | eos | The repository refers to the operator by role rather than by name, with attribution and the record of who ruled as the two exceptions |  |
| org/deviations.md | org | eos | The closed departure log for the EOS v2 build, kept as the audit trail behind the benchmark figures |  |
| org/logs/2026-07/S-0001.md | org | eos | Session S-0001, Phase A, the v0.1 to EOS migration and foundations |  |
| org/logs/2026-07/S-0002.md | org | eos | Session S-0002, Phase B item B1, the kernel org templates extracted |  |
| org/logs/2026-07/S-0003.md | org | eos | Session S-0003, Phase B item B2, the operating model and org state templates extracted |  |
| org/logs/2026-07/S-0004.md | org | eos | Session S-0004, Phase B item B3, the playbooks, operators guide and router templates extracted |  |
| org/logs/2026-07/S-0005.md | org | eos | Session S-0005, Phase B item B4, the scale matrix, seed rubric and live seed gate |  |
| org/logs/2026-07/S-0006.md | org | eos | Session S-0006, Phase C item C1, the compile rules and walk order, dry run recorded |  |
| org/logs/2026-07/S-0007.md | org | eos | Session S-0007, Phase C item C2, the voice module populated |  |
| org/logs/2026-07/S-0008.md | org | eos | Session S-0008, Phase D item D1, the Venture A reseed compiled to green, signature pending |  |
| org/logs/2026-07/S-0009.md | org | eos | Session S-0009, Phase D item D2, the worked example and the first live harvest |  |
| org/logs/2026-07/S-0010.md | org | eos | Session S-0010, Phase E item E1, the inception system completed |  |
| org/logs/2026-07/S-0011.md | org | eos | Session S-0011, Phase E item E2, the S-scale drill report, pass with eight findings |  |
| org/logs/2026-07/S-0012.md | org | eos | Session S-0012, item R1, the FastAPI and full-stack profiles extracted from Venture B |  |
| org/logs/2026-07/S-0013.md | org | eos | Session S-0013, Phase F item F1, the architecture module populated |  |
| org/logs/2026-07/S-0014.md | org | eos | Session S-0014, Phase F item F2, the delivery module populated |  |
| org/logs/2026-07/S-0015.md | org | eos | Session S-0015, Phase F item F3, the devops module populated, Phase F complete |  |
| org/logs/2026-07/S-0016.md | org | eos | Session S-0016, item E3, the S-scale ergonomics from the drill findings |  |
| org/logs/2026-07/S-0017.md | org | eos | Session S-0017, item E4, four web decision rules sharpened for non-house brands |  |
| org/logs/2026-07/S-0018.md | org | eos | Session S-0018, REL, v1.0.0 tagged locally, manual close handed to the operator |  |
| org/logs/2026-07/S-0019.md | org | eos | Session S-0019, the D1 gate closed, G1 and G2 queued, Genesis commissioned |  |
| org/logs/2026-07/S-0020.md | org | eos | Session S-0020, the all-in-one field guide GUIDE.md authored and registered |  |
| org/migration/MIGRATION_MAP.md | org | eos | Every v1 concept and its v2 fate, with the load-bearing rule's new home for anything retired |  |
| org/migration/PLAYBOOK.md | org | eos | The per-venture v1 to v2 migration procedure, three routes, what is preserved, and the consent rule |  |
| org/migration/plans/PatterTech_Website.md | org | eos | PatterTech_Website's read-only plan, fresh v2 S inception whenever the operator wants it |  |
| org/migration/plans/Venture-A.md | org | eos | Venture A's read-only v2 migration plan, the recompile route and what the engine does not yet cover |  |
| org/migration/plans/Venture-C.md | org | eos | Venture C's read-only v2 migration plan, the pin normalisation and the nineteen queue rows |  |
| org/reports/BASELINE_2026-08-15.md | org | eos | The measured state of the tree before the audit, research and expansion mission, as the before half of every later comparison |  |
| org/reports/CONTROL_ENFORCEMENT.md | org | eos | Every material control in the EOS, classified by what actually enforces it, with the file and the test behind each classification |  |
| org/reports/DEFECT_REGISTER_2026-08.md | org | eos | Every defect and contradiction the audit raised, what it turned out to be, and where each one now stands |  |
| org/reports/NEXT_TRANCHE.md | org | eos | What the audit and expansion mission completed, what it deliberately did not, and the dependency-ordered work that follows |  |
| org/reports/V2_FINAL_REPORT.md | org | eos | The v2 build's final report, measured results, residual risks and the release decision the operator owns |  |
| packs/PACK_SHAPE.md | governance | eos | The pack contract, invariant and optional organs, the definition of done, and what stays a registry row |  |
| packs/agentic-development/CHECKS.md | guide | eos arch delivery | What a reviewer or checker can verify about agent workflow design, split into executable today and judgement | 2027-10 |
| packs/agentic-development/PACK.md | guide | eos arch tooling | Which agent topology to run, the invariants that bind every one of them, and how to bound, verify and trace a run | on-change-of:agent-sdk-major-release |
| packs/agentic-development/exemplars/EX-AGENT-001-logging-migration.md | example | eos arch tooling | Worked topology decision record for a coupled logging migration across one service, and why fan-out was refused |  |
| packs/agentic-development/guides/GD-AGENT-001-topology-selection.md | guide | eos arch tooling | Which of the ten agent topologies does this work need, and what pressure justifies promoting past a single agent? | on-change-of:agent-sdk-major-release |
| packs/agentic-development/guides/GD-AGENT-002-context-engineering.md | guide | eos arch tooling | How does context reach an agent, and what happens when the window runs out? | on-change-of:anthropic-context-engineering-publication |
| packs/agentic-development/guides/GD-AGENT-003-spawn-a-subagent.md | guide | eos arch tooling | Should this work be a subagent at all, and if so as a tool, a handoff or a peer worker? | on-change-of:agent-sdk-major-release |
| packs/agentic-development/guides/GD-AGENT-004-verification-oracle.md | guide | eos delivery tooling | What holds the truth that checks an agent's work, and what do you do when nothing does? | on-change-of:anthropic-evals-publication |
| packs/agentic-development/refs/DECISION_RECORD_SHAPE.md | guide | eos arch tooling | The six-section shape of a topology decision record, and what each section must contain | 2027-10 |
| packs/agentic-development/refs/INVARIANTS_AND_BOUNDS.md | guide | eos arch tooling | How to bound a run, trace it, resume it safely, and where the estate's policy and guard take over | on-change-of:agent-sdk-major-release |
| packs/agentic-development/refs/TOPOLOGY_CARD.md | guide | eos arch tooling | The ten topologies by canonical name, the pressure that licenses each, and the evidence behind it | on-change-of:agent-sdk-major-release |
| packs/agentic-development/research/DRILL_PROPOSAL.md | example | eos | Cold-agent acceptance drill for the agentic development pack, topology selection under pressure |  |
| packs/agentic-development/research/NOTES.md | example | eos | Research synthesis for the agentic development and orchestration pack, topologies, context, tools, checkpoints, guardrails |  |
| packs/agentic-swarm/CHECKS.md | guide | eos arch delivery testing | What a reviewer or a script can verify about a graph build, split into executable today and judgement | on-change-of:agent-harness-major-release |
| packs/agentic-swarm/PACK.md | guide | eos arch delivery tooling | How we build software by fanning work over a measured dependency graph, with one integrator and a verifier that predates the lanes | on-change-of:agent-harness-major-release |
| packs/agentic-swarm/exemplars/EX-SWARM-001-eos-v2-1-partition.md | example | eos arch delivery | The partition, packets and merge plan for the EOS v2.1 build, written as it was dispatched |  |
| packs/agentic-swarm/guides/GD-SWARM-001-swarm-or-single-agent.md | guide | eos arch delivery | Should this work be fanned out over lanes at all, or given to one agent? | on-change-of:agent-harness-major-release |
| packs/agentic-swarm/guides/GD-SWARM-002-cut-the-partition.md | guide | eos arch delivery | Where do the cuts go when work is split across lanes, and what is never cut at all? | on-change-of:agent-harness-major-release |
| packs/agentic-swarm/guides/GD-SWARM-003-who-holds-the-plan.md | guide | eos arch tooling | Does a script hold the fan-out shape, or does a model decide it turn by turn? | on-change-of:agent-harness-major-release |
| packs/agentic-swarm/guides/GD-SWARM-004-verifying-a-lane.md | guide | eos delivery testing | What decides that a lane's work is good, and who is allowed to have written it? | on-change-of:agent-harness-major-release |
| packs/agentic-swarm/refs/MERGE_AND_REVIEW.md | guide | eos delivery arch | How lanes land, who decides the order, and the review topology that scales with lane count | on-change-of:agent-harness-major-release |
| packs/agentic-swarm/refs/PACKET_AND_RETURN.md | guide | eos arch tooling | The nine packet fields, the escape, the return schema and the four terminal statuses | on-change-of:agent-harness-major-release |
| packs/agentic-swarm/refs/RISK_REGISTER.md | guide | eos security arch ops | Fifteen risks a graph build carries, with mechanism, evidence, detection signal and control | on-change-of:agent-harness-major-release |
| packs/agentic-swarm/research/DRILL_PROPOSAL.md | example | eos | Proposed cold-agent acceptance drill for the swarm pack, cut a partition and refuse the bad one |  |
| packs/agentic-swarm/research/NOTES.md | guide | eos arch | How the swarm pack was assembled, what the corpus disagrees about, and the questions it could not close | on-change-of:packs/agentic-swarm |
| packs/ai-ml-llm/CHECKS.md | guide | testing delivery tooling | What a reviewer or a script can verify about model-backed work, split into executable today and judgement | 2026-11 |
| packs/ai-ml-llm/PACK.md | playbook | delivery testing data perf | Building on language models, result identity, private held-out sets, pinned model ids, validated judges and a person in front of consequential output | 2027-02 |
| packs/ai-ml-llm/exemplars/EX-AIML-001-classifier-prompt-swap.md | example | testing delivery data | The ai-ml-llm pack applied end to end to a proposed prompt swap on a support ticket classifier, and the model swap after it |  |
| packs/ai-ml-llm/guides/GD-AIML-001-acceptance-evidence.md | guide | testing delivery data | What evidence accepts or refuses a change to a model-backed feature, offline set, judge, human sample or production telemetry? | 2026-11 |
| packs/ai-ml-llm/guides/GD-AIML-002-knowledge-source.md | guide | data perf delivery | Where does the model get the facts, retrieval, whole context, per-query routing or fine-tuning? | on-change-of:EV-0245 |
| packs/ai-ml-llm/guides/GD-AIML-003-who-grades-the-output.md | guide | testing delivery data | Who grades model output, a deterministic scorer, a human, a validated model judge or the user, and what each can settle | 2026-12 |
| packs/ai-ml-llm/guides/GD-AIML-004-prompt-maintenance.md | guide | delivery testing content | How is a prompt maintained over time, hand-written and versioned, few-shot, compiled by an optimiser, or replaced by fine-tuning? | 2026-12 |
| packs/ai-ml-llm/guides/GD-AIML-005-model-lifecycle-and-cost.md | guide | perf delivery ops | Which model backs this feature and what happens when it retires, one pinned model, a cascade, self-assessed routing or a portfolio? | 2027-03 |
| packs/ai-ml-llm/refs/CONTEXT_LAYOUT.md | foundation | perf data delivery | Prompt layout mechanics, the caching against position conflict, context budget and how to measure usable length | on-change-of:EV-0261 |
| packs/ai-ml-llm/refs/EVAL_REPORT.md | foundation | testing delivery data | The fields an eval report must carry, the paired comparison arithmetic, the held-out split and what a verdict may say | on-change-of:EV-0255 |
| packs/ai-ml-llm/refs/MODEL_MIGRATION.md | foundation | ops delivery perf | Pinning model identifiers, recording retirement dates, the migration drill and the scheduled drift check | on-change-of:EV-0260 |
| packs/ai-ml-llm/research/DRILL_PROPOSAL.md | example | eos testing | Cold-agent acceptance drill for the AI, ML and LLM pack, build the gate before tuning the classifier |  |
| packs/ai-ml-llm/research/NOTES.md | example | eos testing | Research synthesis for the AI, ML and LLM pack, four philosophies of building on models, and what should bind |  |
| packs/api-integration/CHECKS.md | guide | delivery ci testing | What a reviewer or checker can verify about API and integration work, split into what runs today and what needs judgement | 2028-02 |
| packs/api-integration/PACK.md | guide | arch security money | Binding requirements, defaults and decision guides for API contracts, webhooks, event payloads and integration change | 2027-12 |
| packs/api-integration/exemplars/EX-API-001-invoices-api-change.md | example | arch money security | A worked change to a live invoices API and its payment webhook, applying the pack end to end from activation to merge |  |
| packs/api-integration/exemplars/EX-API-002-stripe-versioning.md | example | arch money delivery | Stripe's pinned-date versioning read as an exemplar, what it actually costs, and the conditions under which copying it is right |  |
| packs/api-integration/guides/GD-API-001-contract-authoring.md | guide | arch tooling ci | Who writes the contract and when: by hand, in a definition language, generated from the handlers, or not at all? | on-change-of:EV-0023 |
| packs/api-integration/guides/GD-API-002-versioning-and-breaking-change.md | guide | arch ci delivery | How is a boundary allowed to change: add only, declared tier plus gate, explicit version parameter, or pinned date with transformers? | on-change-of:EV-0129 |
| packs/api-integration/guides/GD-API-003-webhook-trust.md | guide | security money arch | How is an inbound webhook trusted: bare-body HMAC, a signed triple, RFC 9421 message signatures, or an asymmetric or provider-native scheme? | on-change-of:EV-0125 |
| packs/api-integration/guides/GD-API-004-boundary-shape.md | guide | arch state realtime | What shape does a boundary take: REST over OpenAPI, typed RPC, an event stream, or GraphQL? | on-change-of:EV-0023 |
| packs/api-integration/guides/GD-API-005-collection-traversal.md | guide | arch perf data | How does a consumer walk a collection: offset paging, opaque cursors, visible keyset, or a hybrid with an estimated total? | on-change-of:EV-0130 |
| packs/api-integration/refs/breaking-change-catalogue.md | example | arch ci delivery | What counts as a breaking change, the compatibility tiers and modes available, and how the gate is wired | on-change-of:EV-0129 |
| packs/api-integration/refs/error-and-limits.md | example | arch content | The error envelope, rate limit advertisement and deprecation signalling a boundary carries, with the contested parts marked | on-change-of:EV-0122 |
| packs/api-integration/refs/idempotency-parameters.md | example | money state | The four decisions an idempotency header does not make, and how they are settled on money-touching paths |  |
| packs/api-integration/refs/webhook-verification.md | example | security money | The verification order, tolerance, rotation and replay controls a webhook receiver needs, with the provider variance that defeats a single implementation |  |
| packs/api-integration/research/DRILL_PROPOSAL.md | example | eos | Single-run cold-agent acceptance drill for the API and integration pack, with deterministic machine-checkable criteria. |  |
| packs/api-integration/research/NOTES.md | example | eos | Decision-relevant synthesis for the API and integration pack, covering contract style, versioning philosophy, webhook security, idempotency and pagination, with the disagreements between mature estates left visible. |  |
| packs/architecture/CHECKS.md | example | arch ci tooling | What a reviewer or checker can verify about architecture work, split into what is executable today and what stays a judgement call |  |
| packs/architecture/PACK.md | guide | arch data infra tooling ci | Architecture pack for boundaries declared and machine-checked, generated contracts drift-gated, webhooks verified over raw bytes, and one deployable with one database until measured evidence says otherwise | 2027-02 |
| packs/architecture/exemplars/EX-ARCH-001-billing-catalogue-boundary.md | example | arch tooling ci | The pack applied end to end to a two-module Python repo where billing may read the catalogue and the catalogue must never know about billing |  |
| packs/architecture/guides/GD-ARCH-001-deployment-shape.md | guide | arch infra | One deployable, several deployables, or contract-shaped seams inside one process | 2027-03 |
| packs/architecture/guides/WG-ARCH-001-boundary-enforcement.md | guide | arch tooling ci | Where module boundaries live, whether convention, a machine contract, the directory tree, or a runtime call graph | 2026-12 |
| packs/architecture/guides/WG-ARCH-002-orm-or-raw-sql.md | guide | arch data | How the service reaches its data, whether an ORM, raw SQL behind a repository, a query builder, or SQL files compiled to typed access, and where the seam sits | 2027-07 |
| packs/architecture/guides/WG-ARCH-003-derived-state.md | guide | arch data state | Where a derived value is allowed to rest, whether computed on read, cached with a named owner, frozen as an immutable snapshot, or maintained by the write path | 2027-07 |
| packs/architecture/guides/WG-ARCH-004-job-execution.md | guide | arch state infra | Where background work runs, whether in the request process, on a durable database claim queue, on an external broker, or on a scheduled pass over state | 2027-07 |
| packs/architecture/guides/WG-ARCH-005-contract-seam.md | guide | arch ci tooling | How frontend and backend come to agree on types, whether hand-maintained, generated and gated, one language end to end, or parsed at the edge | 2027-07 |
| packs/architecture/guides/WG-ARCH-006-change-proof.md | guide | arch testing ci | What proves a change changed nothing, whether a green suite, behaviour pinned first, a byte-stable output canary, or a differential run against the old version | 2027-07 |
| packs/architecture/guides/WG-ARCH-007-vendor-seams.md | guide | arch security money | How deep a vendor is allowed into the codebase, whether SDK throughout, an owned adapter, the raw protocol, or a generated client | 2027-01 |
| packs/architecture/guides/WG-ARCH-008-database-topology.md | guide | arch data infra | Where data rests, whether one shared database, private tables with distinct credentials, one store per deployable, or a records core with a separate readings store | 2027-06 |
| packs/architecture/refs/architecture-description.md | example | arch content | The MADR heading set, the C4 levels worth authoring, the arc42 sections worth borrowing, and the ISO 42010 vocabulary behind them | 2027-05 |
| packs/architecture/refs/boundary-tooling.md | example | arch tooling ci | Contract shapes, config skeletons and known blind spots for import-linter, dependency-cruiser and ArchUnit, plus how each is wired into a build | 2026-11 |
| packs/architecture/refs/evidence-map.md | example | arch content | Which evidence row supports which requirement, what population it observed, and where its licence limits reuse to paraphrase | 2027-04 |
| packs/architecture/research/DRILL_PROPOSAL.md | example | eos | Single-run cold-agent acceptance drill for the architecture pack, with deterministic machine-checkable criteria |  |
| packs/architecture/research/NOTES.md | example | eos | What the evidence supports for the architecture pack, three contrasting philosophies with fit conditions, and the binding versus default versus preference split |  |
| packs/business-logic-modelling/CHECKS.md | implementation | testing money data | What a reviewer or a script can verify about domain modelling work, split into executable today and judgement | 2027-11 |
| packs/business-logic-modelling/PACK.md | playbook | arch data money product | Where a domain rule lives, how much model it earns, and the money, time and lifecycle types that stop it being quietly wrong | 2027-09 |
| packs/business-logic-modelling/exemplars/EX-BLM-001-subscription-renewal.md | example | money data arch | The pack applied end to end to a subscription that renews monthly, prorates a mid-period upgrade and publishes a renewal event |  |
| packs/business-logic-modelling/guides/GD-BLM-001-model-shape.md | guide | arch data product | How much model does this domain earn, from plain procedures to declared decisions? | 2027-09 |
| packs/business-logic-modelling/guides/GD-BLM-002-rule-placement.md | guide | arch product tooling | Where does this rule live, in code, in a table, in a machine or in an engine? | on-change-of:DMN-1.7-formal |
| packs/business-logic-modelling/guides/GD-BLM-003-money-representation.md | guide | money data arch | How is money represented, rounded, allocated and converted at the edges? | on-change-of:ISO-4217-amendment |
| packs/business-logic-modelling/guides/GD-BLM-004-time-modelling.md | guide | data arch product | How much time does this fact carry, which temporal type and how many dimensions? | on-change-of:RFC-9557 |
| packs/business-logic-modelling/guides/GD-BLM-005-state-or-events.md | guide | arch data state | Is the record of truth the current state or the sequence of events? | 2027-12 |
| packs/business-logic-modelling/refs/BOUNDARY_WRITE_UP.md | implementation | arch data product | The field set that makes an aggregate boundary reviewable, what each field is diagnostic of, and the questions that decide a boundary | on-change-of:aggregate-design-canvas-major |
| packs/business-logic-modelling/refs/MONEY_AND_CURRENCY.md | implementation | money data tooling | The money type, the exponent table, rounding and allocation, and the adapter boundary with external systems | on-change-of:ISO-4217-amendment |
| packs/business-logic-modelling/refs/TIME_TYPES.md | implementation | data arch tooling | The temporal type table, zone against offset, elapsed against wall-clock rules, and the two-dimension escalation | on-change-of:RFC-9557 |
| packs/business-logic-modelling/research/DRILL_PROPOSAL.md | example | eos testing | Single-run cold-agent acceptance drill for the business logic and modelling pack, with deterministic machine-checkable criteria |  |
| packs/business-logic-modelling/research/NOTES.md | example | eos testing | What the evidence supports for the business logic and modelling pack, four contrasting philosophies with fit conditions, and the binding versus default versus preference split |  |
| packs/business-model-pricing/CHECKS.md | guide | money product ci | What a reviewer or a script can verify about a pricing decision, split into executable today and judgement | 2028-05 |
| packs/business-model-pricing/PACK.md | playbook | money product eos | How a venture chooses what it sells and what it charges, three pricing practices under one legal and accounting floor | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| packs/business-model-pricing/exemplars/EX-BMP-001-first-consumer-subscription.md | example | money product data | A worked run of the pack, pricing a first UK consumer subscription and repricing it when unit costs rise |  |
| packs/business-model-pricing/guides/GD-BMP-001-price-anchor.md | guide | money product | What information the price is anchored to, and the condition that makes that anchor right here | 2028-04 |
| packs/business-model-pricing/guides/GD-BMP-002-charging-unit.md | guide | money product | What the buyer is charged per, and what each unit costs in accounting, forecasting and support | 2028-01 |
| packs/business-model-pricing/guides/GD-BMP-003-try-before-paying.md | guide | money product | How a buyer experiences the product before paying, and why the evidence gives a measurement rule rather than a trial length | on-change-of:multi-firm-trial-length-replication |
| packs/business-model-pricing/guides/GD-BMP-004-repricing-trigger.md | guide | money product | What opens a price change, what cause is announced with it, and who is protected from the change | 2028-06 |
| packs/business-model-pricing/refs/DECISION_RECORD.md | foundation | money product | The artefacts a pricing decision has to emit, the decision record schema, and what each field is for | 2026-12 |
| packs/business-model-pricing/refs/METRIC_DEFINITIONS.md | foundation | money data | Why commercial metrics carry their own definitions, the house definitions, and the honest weakness in this rule | 2028-08 |
| packs/business-model-pricing/refs/RETENTION_AND_LTV.md | foundation | money data | Why cohort retention rises on its own, why blended churn gives a wrong lifetime value, and what to emit instead | 2029-08 |
| packs/business-model-pricing/refs/UK_OBLIGATIONS.md | foundation | money product | The dated UK legal, tax and payment obligations a price creates, with the trigger that refreshes each one | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| packs/business-model-pricing/research/DRILL_PROPOSAL.md | example | eos testing | Single-run cold-agent acceptance drill for the business model and pricing pack, with deterministic machine-checkable criteria |  |
| packs/business-model-pricing/research/NOTES.md | example | eos testing | What the evidence supports for business model and pricing, three contrasting philosophies with fit conditions, the disagreements, and the binding versus default versus preference split |  |
| packs/coding/CHECKS.md | guide | delivery ci tooling | What a reviewer or a checker can verify about coding work, split into executable today and judgement | 2027-05 |
| packs/coding/PACK.md | playbook | eos delivery testing | How code is written and accepted in a venture repo, oracles, pinning, error paths and the merge gate | 2027-02 |
| packs/coding/exemplars/EX-COD-001-webhook-silent-failure.md | example | delivery testing | The coding pack applied end to end to a webhook receiver that swallows a signature failure and returns success |  |
| packs/coding/guides/GD-COD-001-oracle-strategy.md | guide | testing delivery wargame | Where does the oracle for this change come from, specification, characterisation, contract or downstream gate? | 2027-05 |
| packs/coding/guides/GD-COD-002-review-gate.md | guide | delivery ci wargame | Who reviews a change and how hard, from machine gate only to independent human review at every merge | 2027-02 |
| packs/coding/guides/GD-COD-003-failure-mode-contract.md | guide | arch delivery wargame | How do callers learn a call failed, opaque errors, one sentinel, a declared taxonomy or typed results? | on-change-of:EV-0175 |
| packs/coding/guides/GD-COD-004-pin-then-change.md | guide | testing delivery wargame | How do you change code nobody can specify, read carefully, pin behaviour, reconstruct a spec or rewrite behind a contract? | 2027-10 |
| packs/coding/guides/GD-COD-005-repo-shape.md | guide | arch delivery wargame | One repository or several, and how the trunk flows through whichever you pick | 2027-08 |
| packs/coding/refs/ERROR_PATH.md | foundation | delivery testing | The error-path reference, what counts as handled, how failures are declared, and the checks that catch a swallow | 2028-02 |
| packs/coding/refs/ORACLES.md | foundation | testing delivery | Which oracle each change type needs, what counts as one, and how independence and a demonstrated failure are proved | 2027-05 |
| packs/coding/refs/REVIEW_GATE.md | foundation | delivery ci | What the machine gate must contain, how findings are split, and how a human reads a diff when one does | 2027-02 |
| packs/coding/research/DRILL_PROPOSAL.md | example | eos | Cold-agent acceptance drill for the coding pack, pin then change an undocumented parser |  |
| packs/coding/research/NOTES.md | example | eos | Research synthesis for the coding pack, four construction philosophies, review at scale, and what should bind |  |
| packs/data-analytics/CHECKS.md | guide | data testing delivery | What a reviewer or a checker can verify about analytics, modelling and experiment work, split into executable today and judgement | 2027-08 |
| packs/data-analytics/PACK.md | playbook | eos data testing pii | Analytics data, event taxonomy, model shape, quality gates, experiment statistics and what the analytics layer may hold about a person | 2027-11 |
| packs/data-analytics/exemplars/EX-DATA-001-gated-model-honest-experiment.md | example | data testing product | The data-analytics pack applied end to end to a raw event dump and an experiment whose assignment ratio is broken |  |
| packs/data-analytics/guides/GD-DATA-001-quality-gate-placement.md | guide | data testing delivery | Where does the data quality rule live, a declared contract, computed metrics with anomaly detection, both, or no gate at all? | 2027-12 |
| packs/data-analytics/guides/GD-DATA-002-model-shape.md | guide | data arch | What shape does the analytics model take, a source mirror, layered wide entities, a dimensional star, or one metrics layer over any of them? | 2027-12 |
| packs/data-analytics/guides/GD-DATA-003-experiment-stopping.md | guide | data product testing | How is an experiment allowed to end, a locked fixed horizon, an always-valid sequential test, an asymmetric gate, or no experiment at all? | 2028-01 |
| packs/data-analytics/guides/GD-DATA-004-storage-shape.md | guide | data infra arch | Where does the analytics data sit, a single managed warehouse, a warehouse over an open table format, a lakehouse, or files and a single-node engine? | 2028-01 |
| packs/data-analytics/guides/GD-DATA-005-event-contract.md | guide | data product delivery | How are product events named and validated, hosted SDK defaults, a written convention, a reviewed tracking plan, or a registry that quarantines invalid events? | 2028-02 |
| packs/data-analytics/refs/DATA_CONTRACT.md | foundation | data delivery testing | What a data contract has to carry to satisfy D9 and D10, the rule kinds available, and how a contract fails silently | 2028-08 |
| packs/data-analytics/refs/EXPERIMENT_STATS.md | foundation | data testing product | Experiment mechanics behind B4 and B5, the sample ratio check, power arithmetic, variance reduction and the interpretation errors that produce false conclusions | 2029-08 |
| packs/data-analytics/refs/PRIVACY_IN_ANALYTICS.md | foundation | data pii security | What the analytics layer may hold about a person, the identifier ladder behind B3, UK duties, and how to read a differential privacy claim | on-change-of:EV-0225 |
| packs/data-analytics/research/DRILL_PROPOSAL.md | example | eos testing | Single-run cold-agent acceptance drill for the data-analytics pack, with deterministic machine-checkable criteria |  |
| packs/data-analytics/research/NOTES.md | example | eos testing | Research synthesis for the data, analytics and experimentation pack, covering quality gates, modelling shape, experiment statistics, event design, storage fit and privacy, with the disagreements left visible |  |
| packs/data-engineering/CHECKS.md | guide | data ops ci | What a reviewer or a script can verify about a pipeline in this domain, split into executable today, judgement, and what no check reaches | 2027-11 |
| packs/data-engineering/PACK.md | playbook | data ops state realtime | How data arrives and is reprocessed, delivery guarantees per hop, idempotent reruns, the processing window, backfill, late and duplicate records and partitioning | 2028-04 |
| packs/data-engineering/exemplars/EX-DATAENG-001-orders-backfill.md | example | data ops state | Worked example, a nightly orders pipeline from a third-party system, repaired over six weeks of history after a time-zone bug |  |
| packs/data-engineering/guides/GD-DATAENG-001-ingestion-shape.md | guide | data ops state | Scheduled batch extract, a subscribed stream, log-based change capture, or polling a modified-at column? | 2027-12 |
| packs/data-engineering/guides/GD-DATAENG-002-idempotent-reprocess.md | guide | data ops state | Overwrite the partition, merge on a key, append-only with a view that picks the winner, or an idempotent write token? | 2028-01 |
| packs/data-engineering/guides/GD-DATAENG-003-processing-window.md | guide | data ops state | The run's own clock, the scheduler's interval, a high-water mark read from the target, or the event time carried in the record? | 2028-02 |
| packs/data-engineering/guides/GD-DATAENG-004-late-arrivals.md | guide | data ops realtime | Drop at the watermark, hold the window open and restate, reprocess a fixed lookback every run, or recompute everything? | 2028-03 |
| packs/data-engineering/refs/DELIVERY_GUARANTEES.md | implementation | data ops state | What a hop is, the three guarantees, what each sink type can actually promise, and the fields that record a hop | 2028-05 |
| packs/data-engineering/refs/PARTITIONING.md | implementation | data ops state | Choosing the partition column and width, deriving the value safely, evolving the layout, and the two failure directions | 2028-06 |
| packs/data-engineering/refs/RUN_LEDGER.md | implementation | data ops tooling | The fields a pipeline run records, what each one is for, and the two comparisons that make the ledger worth keeping | 2028-07 |
| packs/data-engineering/research/NOTES.md | example | eos | Research synthesis for the data-engineering pack, covering ingestion shape, delivery guarantees, idempotent reprocessing, the processing window, late arrivals and partitioning |  |
| packs/delivery-testing/CHECKS.md | guide | delivery testing ci | What a reviewer or a checker can verify about delivery and testing work, and which checks run today | 2027-08 |
| packs/delivery-testing/PACK.md | guide | delivery testing ci | Delivery, testing and quality: what binds, what defaults, and which fork routes to which guide | 2028-02 |
| packs/delivery-testing/exemplars/EX-DEL-001-drifted-fake-and-a-lying-suite.md | example | delivery testing ci | A worked run of the pack: a rounding defect, a drifted fake and a clock-dependent test, fixed in order |  |
| packs/delivery-testing/guides/WG-DEL-005-test-doubles.md | wargame | delivery testing arch | Which double stands in for this port: real, container, verified fake, or mock? | 2028-02 |
| packs/delivery-testing/guides/WG-DEL-006-oracle-independence.md | wargame | delivery testing ci | How independent must the oracle be from the code it judges, and who authors it? | 2028-03 |
| packs/delivery-testing/guides/WG-DEL-007-test-timing.md | wargame | delivery testing ci | What has to exist before work fans out, and when checks get written relative to the code | 2028-03 |
| packs/delivery-testing/refs/CONTRACT_SUITES.md | example | delivery testing arch | How to build and run a contract suite that proves a double still matches the real thing |  |
| packs/delivery-testing/refs/FLAKE_AND_DETERMINISM.md | example | delivery testing ci | Flake sources, the determinism budget, the quarantine record and why retries are not a policy |  |
| packs/delivery-testing/refs/QUALITY_SIGNALS.md | example | delivery testing ci | What coverage, mutation score, property tests and test selection actually tell you, and what they cost | 2027-03 |
| packs/delivery-testing/research/DRILL_PROPOSAL.md | example | eos | Cold-agent acceptance drill for the delivery, testing and quality pack, checking double choice, contract verification and flake handling |  |
| packs/delivery-testing/research/NOTES.md | example | eos | Research synthesis for the delivery, testing and quality pack, covering test doubles, mutation practice, property-based testing, contract maturity, flake policy and test selection |  |
| packs/devops-reliability/CHECKS.md | guide | ops delivery ci | What a reviewer or a checker can verify about devops and reliability work, split into executable today and judgement | 2028-01 |
| packs/devops-reliability/PACK.md | guide | ops data infra | Binding devops and reliability practice, migrations, restore proof, SLOs and error budgets, rollout, flags, incidents and cost | 2027-04 |
| packs/devops-reliability/exemplars/EX-DEVOPS-001-email-to-contacts.md | example | ops data migrations | Worked example, replacing users.email_address with a normalised contacts table without a change window |  |
| packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md | guide | ops data migrations | Reversible migrations, expand-migrate-contract, online schema change, or a freeze window? | 2027-09 |
| packs/devops-reliability/guides/GD-DEVOPS-002-release-control.md | guide | ops delivery infra | All at once, watched canary, analysis-gated rollout, or flag-decoupled release? | 2027-12 |
| packs/devops-reliability/guides/GD-DEVOPS-003-error-budget-dial.md | guide | ops delivery | No budget, advisory budget, enforced budget policy, or calendar change freezes? | 2028-03 |
| packs/devops-reliability/guides/GD-DEVOPS-004-reliability-measures.md | guide | ops delivery perf | Nothing, delivery keys only, SLO plus customer impact, or a multi-dimension set? | 2028-02 |
| packs/devops-reliability/guides/WG-OPS-003-restore-proof.md | guide | ops data infra | Trusted snapshots, a restore test with a tick, an evidenced restore drill, or full estate rehearsal? | 2028-06 |
| packs/devops-reliability/refs/FLAG_AND_ROLLOUT_LIFECYCLE.md | implementation | ops delivery infra | Flag registry fields, expiry and terminal value, and the rollout object's failure condition and abort | 2028-03 |
| packs/devops-reliability/refs/MIGRATION_RISK_CLASSES.md | implementation | ops data migrations | The four migration risk classes, which fail the build, and the change record fields that carry them | 2027-09 |
| packs/devops-reliability/refs/RESTORE_DRILL_EVIDENCE.md | implementation | ops data infra | The restore drill procedure, its steady-state hypothesis, and the evidence record a checker can read | 2027-04 |
| packs/devops-reliability/refs/SIGNAL_STABILITY_AND_COST.md | implementation | ops infra money | Observability signal stability tiers and the allocation precondition that makes cost work mean anything | 2027-12 |
| packs/devops-reliability/refs/SLO_AND_ERROR_BUDGET.md | implementation | ops delivery | The machine-readable SLO object, the error budget policy shape, and the aggregate metrics this estate refuses | 2028-02 |
| packs/devops-reliability/research/DRILL_PROPOSAL.md | example | eos | Single-run cold-agent acceptance drill for the devops-reliability pack, with deterministic machine-checkable criteria. |  |
| packs/devops-reliability/research/NOTES.md | example | eos | Research synthesis for the devops-reliability pack, covering migrations, restore proof, SLO governance, incident practice, FinOps, golden paths, progressive delivery and observability stability. |  |
| packs/docs-dx/CHECKS.md | guide | content delivery ci tooling | What a reviewer or a checker can verify about documentation work, split into executable today and judgement | 2027-08 |
| packs/docs-dx/PACK.md | playbook | content voice delivery ci tooling | Documentation and developer experience, where a document's truth lives and which documents can be made to fail a build | 2028-04 |
| packs/docs-dx/exemplars/EX-DOCS-001-stale-quickstart.md | example | content delivery ci tooling | A worked repair of a quickstart that stopped working, applying the pack from activation through to the gate that stops it recurring |  |
| packs/docs-dx/guides/GD-DOCS-001-truth-location.md | guide | content delivery tooling | Where a document's truth lives, and therefore whether it can drift at all | 2028-04 |
| packs/docs-dx/guides/GD-DOCS-002-executable-examples.md | guide | content delivery ci testing | How a code example in documentation stops lying, and what to do with the ones that cannot run | on-change-of:rustdoc-doctest-semantics |
| packs/docs-dx/guides/GD-DOCS-003-changelog-ownership.md | guide | content delivery ci | Who writes the changelog, and whether release notes can be derived from history at all | on-change-of:keep-a-changelog-beyond-1.1.0 |
| packs/docs-dx/guides/GD-DOCS-004-failure-messages.md | guide | content voice delivery | What a user-visible failure owes its reader, and how much structure to spend on it | on-change-of:rustc-diagnostic-style-guide |
| packs/docs-dx/guides/GD-DOCS-005-blocking-checks.md | guide | content delivery ci tooling | Which documentation checks are allowed to fail a build, and which stay advisory | 2028-04 |
| packs/docs-dx/refs/DOC_FORMS.md | foundation | content voice product | The four documentation forms as a diagnostic, the README question set, and what an agent entry file owes a reader | 2028-05 |
| packs/docs-dx/refs/DOC_GATE.md | foundation | content delivery ci tooling | The documentation gate reference, what runs, in what order, blocking or advisory, and how to prove each step works | on-change-of:lychee-exit-codes-or-fragment-checking |
| packs/docs-dx/research/DRILL_PROPOSAL.md | example | eos testing | Cold-agent acceptance drill for the docs-dx pack, make a stale documented flag fail the build |  |
| packs/docs-dx/research/NOTES.md | example | eos testing | Research synthesis for the docs-dx pack, four documentation philosophies, what is checkable, and what should bind |  |
| packs/identity-access/CHECKS.md | guide | auth testing data | What a reviewer or a script can verify about identity, authorisation and tenancy work, executable today versus judgement | 2028-09 |
| packs/identity-access/PACK.md | guide | auth security arch state | Authenticating people, deciding what each may do, and keeping one tenant out of another's data | 2029-02 |
| packs/identity-access/exemplars/EX-IDENT-001-cross-tenant-share.md | example | auth arch data | The pack applied end to end to one feature, sharing a report outside the ownership tree, on a system with two tenants |  |
| packs/identity-access/guides/GD-IDENT-001-authorisation-model.md | guide | auth arch security | Ownership checks, roles, attributes or relationships? The fork the coverage matrix recorded as missing | 2028-10 |
| packs/identity-access/guides/GD-IDENT-002-session-or-token.md | guide | auth security state | Server-side session in a cookie, bearer token, token in a cookie behind a front end, or a sender-constrained token? | 2028-11 |
| packs/identity-access/guides/GD-IDENT-003-provider-or-self-hosted.md | guide | auth arch security | Hosted identity provider, self-hosted identity server, passwords of your own, or federation to the customer's provider? | 2028-12 |
| packs/identity-access/guides/GD-IDENT-004-tenant-isolation.md | guide | auth data arch | Tenant isolation by application filter, by database row policy, by schema, or by a store per tenant? | 2029-01 |
| packs/identity-access/refs/break-glass.md | guide | auth security ops | The emergency access path, why it exists, the eight properties that make it work, and the trade it makes | 2029-03 |
| packs/identity-access/refs/decision-point-placement.md | guide | auth arch | The four points a decision needs, where each can sit, the four outcomes a decision has, and what happens when the decider is unreachable | 2029-04 |
| packs/identity-access/refs/tenant-isolation-mechanics.md | guide | auth data migrations | How a database row policy actually behaves, what walks past it, and the checklist for making a tenant boundary real | 2029-05 |
| packs/identity-access/research/NOTES.md | example | eos | Research synthesis for the identity, authorisation and tenancy pack, the model fork, what should bind, and the predicates proposed |  |
| packs/legal-licensing/CHECKS.md | guide | security pii delivery | What a reviewer or a checker can verify about licensing and data-protection routing, split into executable today and judgement | 2026-12 |
| packs/legal-licensing/PACK.md | playbook | security pii delivery | Licensing, inbound provenance and UK data-protection routing for a venture, and the four situations that stop and go to a lawyer | 2027-04 |
| packs/legal-licensing/exemplars/EX-LEGAL-001-waitlist-with-a-poisoned-tree.md | example | security pii delivery | The pack applied end to end to a small hosted feature whose dependency tree hides a network copyleft term, an unlicensed vendored directory and an unmade choice |  |
| packs/legal-licensing/guides/GD-LEGAL-001-copyleft-trigger.md | guide | security delivery | Can we use this copyleft dependency for what we actually ship, and what fires the obligation | on-change-of:https://opensource.org/license/agpl-v3 |
| packs/legal-licensing/guides/GD-LEGAL-002-compliance-posture.md | guide | security delivery tooling | How a venture decides licence questions at all, standing verdict against per-file declaration against certified process against scan and review | on-change-of:https://www.apache.org/legal/resolved.html |
| packs/legal-licensing/guides/GD-LEGAL-003-outbound-licence.md | guide | security product | What licence a repository carries outbound, and which promise that makes to the people downstream | on-change-of:https://blueoakcouncil.org/list |
| packs/legal-licensing/guides/GD-LEGAL-004-inbound-rights.md | guide | security delivery | How rights arrive with inbound code, sign-off against agreement against employment against nothing, and where agent authorship sits | on-change-of:https://developercertificate.org/ |
| packs/legal-licensing/guides/GD-LEGAL-005-lawful-extraction.md | guide | security delivery | What a study may lawfully carry away from a source we do not own, how deep the reading goes, and who may hold the source while the replacement is written | 2027-04 |
| packs/legal-licensing/refs/ESCALATION.md | guide | security pii | The four triggers that stop the pack and go to a human lawyer, what to hand over, and what to stop doing meanwhile | 2028-03 |
| packs/legal-licensing/refs/LICENCE_CLASSES.md | guide | security delivery tooling | The three-bucket allowlist with its reasons, the expression grammar that matters, and what to do with the values a scan actually returns | on-change-of:https://spdx.org/licenses/ |
| packs/legal-licensing/refs/UK_DATA_ROUTING.md | guide | pii security | The Article 13 notice checklist with both complaint routes, the separate registration duty, and where this pack hands over to security-privacy | on-change-of:https://www.legislation.gov.uk/eur/2016/679/article/13 |
| packs/legal-licensing/research/DRILL_PROPOSAL.md | example | eos testing | Proposed cold-agent acceptance drill for the legal, licensing and compliance routing pack |  |
| packs/legal-licensing/research/NOTES.md | example | eos testing | Research synthesis for the legal, licensing and compliance routing pack, patterns, trade-offs and what should bind |  |
| packs/marketing-growth/CHECKS.md | guide | content seo pii testing | What a reviewer or a script can verify about marketing and growth work, split into executable today and judgement | on-change-of:PECR-reg-22-amendment |
| packs/marketing-growth/PACK.md | playbook | content seo pii brand voice | How a venture reaches and keeps people, four growth philosophies over one consent, refusal and measurement floor | on-change-of:PECR-reg-22-amendment |
| packs/marketing-growth/exemplars/EX-MKTG-001-launch-and-first-sequence.md | example | content seo pii forms | The pack applied end to end, a five-page launch surface and a three-message welcome sequence with consent, suppression and preflight proved |  |
| packs/marketing-growth/guides/GD-MKTG-001-growth-philosophy.md | guide | brand content seo product | Which growth philosophy does this venture run? | on-change-of:Reforge-and-IPA-primary-text-access |
| packs/marketing-growth/guides/GD-MKTG-002-consent-route.md | guide | pii forms content | Where does a lawful marketing address come from, and what may be sent to it? | on-change-of:PECR-reg-22-amendment |
| packs/marketing-growth/guides/GD-MKTG-003-effect-measurement.md | guide | content testing tooling | How is a channel's effect measured, and what may be claimed from it? | on-change-of:GA4-attribution-model-set |
| packs/marketing-growth/guides/GD-MKTG-004-content-provenance.md | guide | content seo voice | Who owns a published page, and how fast may a venture publish? | on-change-of:Google-spam-policies-revision |
| packs/marketing-growth/refs/CONSENT_RECORD.md | implementation | pii forms tooling | The stored shape of a lawful marketing basis, the closed enum, the soft opt-in tests and the suppression store | on-change-of:PECR-reg-22-amendment |
| packs/marketing-growth/refs/DISCOVERY_SURFACE.md | implementation | seo content ci | Crawler directives, sitemaps and structured data as release-gated artefacts, and the folk levers the index operator says are inert | on-change-of:Google-structured-data-guidelines-revision |
| packs/marketing-growth/refs/SEND_PREFLIGHT.md | implementation | pii tooling ci | The gates a sending domain and a message pass before a first bulk send, and the one-click unsubscribe mechanics | on-change-of:Gmail-sender-guidelines-requirements |
| packs/marketing-growth/research/DRILL_PROPOSAL.md | example | eos testing | Cold-agent acceptance drill for the marketing-growth pack, one launch surface plus one lifecycle sequence, machine-checked |  |
| packs/marketing-growth/research/NOTES.md | example | eos testing | Research synthesis for the marketing-growth pack, four growth philosophies, the measurement floor, and what is law versus taste |  |
| packs/native-client/CHECKS.md | implementation | testing a11y delivery | What a reviewer or checker can verify about client work, split into executable today and judgement | on-change-of:EN-301-549-v4-publication |
| packs/native-client/PACK.md | playbook | eos a11y delivery ops state | Software that ships as a binary, four client architectures, the offline write question, forward-only release and the non-web accessibility profile | on-change-of:EN-301-549-v4-publication |
| packs/native-client/exemplars/EX-NAT-001-offline-booking-client.md | example | eos state a11y delivery | The pack applied end to end to a single-surface task client with three write classes, one of them invariant-bearing |  |
| packs/native-client/guides/GD-NAT-001-client-architecture.md | guide | arch delivery a11y | Which client architecture does this product take? | 2028-05 |
| packs/native-client/guides/GD-NAT-002-offline-write-model.md | guide | state data delivery | What happens to a write made with no network? | 2028-05 |
| packs/native-client/guides/GD-NAT-003-release-path.md | guide | delivery ops ci | How does a fix reach a user, given that no release can be taken back? | on-change-of:play-staged-rollout-mechanics |
| packs/native-client/guides/GD-NAT-004-a11y-profile.md | guide | a11y testing product | How much accessibility assurance does a non-web surface buy, and against which instrument? | on-change-of:EN-301-549-v4-publication |
| packs/native-client/refs/A11Y_NON_WEB.md | ux | a11y testing product | The non-web accessibility profile, the unit of conformance, the semantics declaration, clause 11 extras and the audit route | on-change-of:EN-301-549-v4-publication |
| packs/native-client/refs/RELEASE_MECHANICS.md | implementation | delivery ops ci | Store release mechanics side by side, the over-the-air envelope, the kill-switch contract and the distribution clock | on-change-of:play-staged-rollout-mechanics |
| packs/native-client/refs/WRITE_CLASSES.md | pattern | state data delivery | Write classification, the four conflict policies, the reservation pattern and what the outbox must guarantee | 2028-08 |
| packs/native-client/research/DRILL_PROPOSAL.md | example | eos testing | Cold-agent acceptance drill for the native-client pack, an offline-capable client with a declared conflict policy and a forward-only release path |  |
| packs/native-client/research/NOTES.md | example | eos testing | Research synthesis for the native-client pack, four client architectures, three sync philosophies, store release mechanics and the non-web accessibility profile |  |
| packs/pattertech-house/CHECKS.md | guide | web testing tooling a11y | What a reviewer or a script can verify about house work, split into executable today and judgement | 2028-11 |
| packs/pattertech-house/PACK.md | guide | web brand colour motion layout typography | The PatterTech house visual language, adopted by name and never by default, with every house number in one place | on-change-of:WCAG-2.2 |
| packs/pattertech-house/exemplars/EX-HOUSE-001-services-section.md | example | web layout motion content | A services section and closing band built from the house kit, worked against the drill's ten criteria |  |
| packs/pattertech-house/guides/GD-HOUSE-001-light-posture.md | guide | web motion colour brand | How much light does this surface carry, and which tiers of the graded system are enabled? | 2028-04 |
| packs/pattertech-house/guides/GD-HOUSE-002-container-choice.md | guide | web layout density content | A set of content needs a container. Ledger, plaque, panel, table or prose? | 2028-05 |
| packs/pattertech-house/guides/GD-HOUSE-003-polarity-register.md | guide | web colour a11y brand | Does this surface render dark, light, dual or mixed, and what does each cost the reader? | 2028-06 |
| packs/pattertech-house/guides/GD-HOUSE-004-figure-austerity.md | guide | web media imagery content | How austere is this figure, and may any figure in a piece carry a distinguishing device? | 2028-07 |
| packs/pattertech-house/refs/BUDGETS.md | implementation | web motion colour perf layout | The single canonical home for every PatterTech house number, alphas, durations, measures, counts and weights | 2028-08 |
| packs/pattertech-house/refs/KIT.md | pattern | web layout content media nav | Anatomy of the house vocabulary, containers, section furniture, the long-read kit, diagrams, media and chrome | 2028-09 |
| packs/pattertech-house/refs/LIGHT_MECHANICS.md | implementation | web motion colour perf | How the four light tiers are built, the compositor whitelist, the degradation ladder and the token registration they depend on | on-change-of:CSS-Masking-Module-Level-1 |
| packs/pattertech-house/research/DRILL_PROPOSAL.md | example | eos testing | Single-run cold-agent acceptance drill for the PatterTech house style, with deterministic machine-checkable criteria |  |
| packs/pattertech-house/research/NOTES.md | example | eos testing | Three competing visual-language philosophies, what the evidence supports, and where the PatterTech house style is taste rather than fact |  |
| packs/product-discovery/CHECKS.md | guide | product testing tooling | What a reviewer or a script can verify about a discovery record, split into executable today and judgement | 2027-08 |
| packs/product-discovery/PACK.md | playbook | eos product testing | Deciding what to build and whether to build it, problem framing, evidence provenance, the discovery record and the kill verdict | 2028-06 |
| packs/product-discovery/exemplars/EX-DISC-001-approvals-inbox-request.md | example | product testing | The product-discovery pack applied end to end to a feature request for an approvals inbox, ending in a TEST verdict |  |
| packs/product-discovery/guides/GD-DISC-001-discovery-depth.md | guide | product testing wargame | How much discovery does this decision deserve, a gated phase, a standing cadence, outcome elicitation alone, or ship and instrument? | 2028-06 |
| packs/product-discovery/guides/GD-DISC-002-user-evidence-source.md | guide | product testing wargame | Where does the evidence about users come from, existing behaviour, talking to people, a controlled experiment, or a model standing in for them? | 2028-06 |
| packs/product-discovery/guides/GD-DISC-003-choosing-between-opportunities.md | guide | product wargame | How do you choose between candidate opportunities, score them, rank by outcome contribution, test them all, or sequence by reversibility? | 2028-07 |
| packs/product-discovery/guides/GD-DISC-004-acceptance-criteria-form.md | guide | product delivery wargame | Once the problem is settled, in what form do the acceptance criteria go, a user story, EARS clause order, an executable test, or a full specification chain? | 2028-07 |
| packs/product-discovery/refs/DISCOVERY_RECORD.md | foundation | product testing | The fixed shape of a discovery record, its sections, its line grammars, and what counts as a citable source | 2028-07 |
| packs/product-discovery/refs/SAMPLE_AND_SIGNAL.md | foundation | product testing | How many people to talk to, when an experiment can be powered, and what to do below the power floor | 2028-07 |
| packs/product-discovery/research/DRILL_PROPOSAL.md | example | eos testing | Cold-agent acceptance drill for the product-discovery pack, frame a solution request back into a testable opportunity |  |
| packs/product-discovery/research/NOTES.md | example | eos testing | Research synthesis for the product-discovery pack, four schools of discovery, what the evidence actually supports, and what should bind |  |
| packs/research-knowledge/CHECKS.md | guide | data content testing tooling | What a reviewer or checker can verify about research and knowledge-base work, executable today versus judgement | 2029-03 |
| packs/research-knowledge/PACK.md | playbook | data content security tooling | Evidence discipline for a venture that researches before it builds or keeps a knowledge base others read, traceability, counter-evidence, supersession and source text as data | 2029-08 |
| packs/research-knowledge/exemplars/EX-RESEARCH-001-a-source-that-spoke-to-the-reader.md | example | security content data | A live source addressed its AI reader in the imperative during this pack's own source sweep, and what the record did with it |  |
| packs/research-knowledge/guides/GD-RESEARCH-001-when-to-stop.md | guide | data content product | One authoritative source, a fixed budget, agreement from independent routes, or an exhaustive sweep? | 2029-04 |
| packs/research-knowledge/guides/GD-RESEARCH-002-where-the-base-lives.md | guide | data content delivery | In the repository under the code gate, an open wiki with a policy, a curated store with one editor, or no separate base at all? | 2029-05 |
| packs/research-knowledge/guides/GD-RESEARCH-003-superseding-a-source.md | guide | data content migrations | Wait for something to break, sweep on a calendar, supersede on a named event, or keep the answer continuously live? | 2029-06 |
| packs/research-knowledge/guides/GD-RESEARCH-004-a-source-that-speaks-to-you.md | guide | security content data | Follow it when it looks helpful, ignore it quietly, record and report it, or refuse to read the class at all? | 2027-06 |
| packs/research-knowledge/refs/record-shape.md | guide | data content tooling | The fields a source record and a claim record carry, what each one prevents, and where the shape comes from | 2029-09 |
| packs/research-knowledge/refs/source-classes.md | guide | data content product | What counts as a primary source for a software venture, the ladder for common source types, and where the borrowed hierarchy inverts | 2029-10 |
| packs/research-knowledge/research/NOTES.md | guide | eos data content | How the research-knowledge pack was assembled, the predicates it proposes, what the corpus disagrees about and what it could not close | on-change-of:packs/research-knowledge |
| packs/security-privacy/CHECKS.md | guide | security testing tooling | What a reviewer or checker can verify about security, privacy and safety work, executable today versus judgement | 2027-08 |
| packs/security-privacy/PACK.md | guide | security pii tooling | Security, privacy and safety for agent-run work, injection resistance, secrets, data protection and approval | on-change-of:EV-0213 |
| packs/security-privacy/exemplars/EX-SEC-001-poisoned-integration-guide.md | example | security tooling | The pack applied end to end to a feature task whose vendor guide carries planted instructions |  |
| packs/security-privacy/guides/GD-SEC-001-injection-defence.md | guide | security tooling | In-band detection, a configuration rule, out-of-band enforcement, or OS containment? | 2027-03 |
| packs/security-privacy/guides/GD-SEC-002-secret-protection.md | guide | security tooling ci | Ignore rules alone, a pre-commit scan, a push-path scan, or a managed store with short-lived credentials? | 2027-04 |
| packs/security-privacy/guides/GD-SEC-003-assurance-grading.md | guide | security testing | No declared level, a flat entry bar, a graded catalogue by data sensitivity, or per-practice maturity? | 2027-06 |
| packs/security-privacy/guides/GD-SEC-004-external-action-approval.md | guide | security tooling ops | Model judgement, a static allowlist, guard-classified verdicts with recorded approval, or manual only? | 2027-05 |
| packs/security-privacy/refs/data-protection-uk.md | guide | security pii | UK data protection for a small venture, lawful basis register, complaints route, DPIA threshold and what is unsettled | on-change-of:EV-0225 |
| packs/security-privacy/refs/instruction-source-boundary.md | guide | security tooling | What counts as untrusted content, how to report planted instructions, and the escalation artefact format | 2027-09 |
| packs/security-privacy/refs/secret-handling.md | guide | security ci tooling | The deny list, the two scan placements, bypass records and what to do when a secret has already gone | 2027-10 |
| packs/security-privacy/refs/threat-catalogue.md | guide | security arch | STRIDE for the system, the agentic catalogue for the agent, and how both map onto the ten guarded classes | on-change-of:EV-0213 |
| packs/security-privacy/research/DRILL_PROPOSAL.md | example | eos | Proposed cold-agent acceptance drill for the security, privacy and safety pack |  |
| packs/security-privacy/research/NOTES.md | example | eos | Research synthesis for the security, privacy and safety pack, patterns, trade-offs and what should bind |  |
| packs/supply-chain-integrity/CHECKS.md | guide | security delivery testing ci | What a reviewer or a checker can verify about supply chain and release integrity work, executable today versus judgement | 2027-03 |
| packs/supply-chain-integrity/PACK.md | guide | security delivery ci tooling | Whether an artefact is what it claims to be, covering provenance, signing identity, bill-of-materials shape, pinning cadence and the reach of a compromised build system | 2027-06 |
| packs/supply-chain-integrity/exemplars/EX-SUPPLY-001-first-published-release.md | example | security delivery ci tooling | The pack applied end to end to a venture cutting its first public release of a CLI that also consumes a prebuilt binary |  |
| packs/supply-chain-integrity/guides/GD-SUPPLY-001-provenance-and-verification.md | guide | security delivery ci tooling | A checksums file, build-platform provenance, a self-hosted attestation chain, or an independently reproduced build? | 2027-04 |
| packs/supply-chain-integrity/guides/GD-SUPPLY-002-signing-identity.md | guide | security delivery ci tooling | No signature, a personal key, a custodied key, a short-lived identity certificate, or the platform's own signing? | on-change-of:EV-0068 |
| packs/supply-chain-integrity/guides/GD-SUPPLY-003-pinning-cadence.md | guide | security delivery ci tooling | Floating ranges, continuous auto-merge, a cooldown window with batched moves, digest pins everywhere, or frozen? | 2027-05 |
| packs/supply-chain-integrity/guides/GD-SUPPLY-004-vendor-or-depend.md | guide | security delivery arch tooling | Depend with a pin, vendor the source, fork and maintain, reimplement the slice you need, or use the platform? | on-change-of:EV-0069 |
| packs/supply-chain-integrity/refs/admission-checklist.md | guide | security delivery ci tooling | What a verification step actually consists of per ecosystem, and what each check does and does not establish | on-change-of:EV-0038 |
| packs/supply-chain-integrity/refs/build-system-reach.md | guide | security delivery ci ops | What a compromised build can touch, how it gets in, and the containment that is configuration rather than cryptography | on-change-of:EV-0069 |
| packs/supply-chain-integrity/research/NOTES.md | example | eos | Research synthesis for supply chain and release integrity, the three philosophies, what should bind, and the predicates proposed |  |
| packs/support-operations/CHECKS.md | implementation | ops product testing tooling | What a reviewer or a script can verify about support work, split into executable today and judgement | on-change-of:ISO-10002-revision |
| packs/support-operations/PACK.md | playbook | eos ops product pii | Customer support as an operating function, triage before backlog, honest incident communication, and the loop from inbox back into the product | on-change-of:ISO-10002-revision |
| packs/support-operations/exemplars/EX-SUPPORT-001-one-inbox-week.md | example | ops product pii money | The pack applied end to end over one week of forty inbound items for a paid product with sixty customers, including one customer-visible outage |  |
| packs/support-operations/guides/GD-SUPPORT-001-triage-pattern.md | guide | ops product | How does inbound get classified, and what keeps the queue finite? | on-change-of:ISO-10002-revision |
| packs/support-operations/guides/GD-SUPPORT-002-close-policy.md | guide | ops product pii | May an item close without an answer, and on whose clock? | on-change-of:ISO-10002-revision |
| packs/support-operations/guides/GD-SUPPORT-003-declaration-route.md | guide | ops delivery | Who declares a customer-visible incident, and on what signal? | 2028-08 |
| packs/support-operations/guides/GD-SUPPORT-004-support-measurement.md | guide | ops product testing | What do we measure about support, and what may the number be used for? | 2028-08 |
| packs/support-operations/refs/INCIDENT_COMMS.md | implementation | ops voice delivery | The customer-facing update contract, the honesty rules including bypassed checks, audiences, cadence and the communication log shape | 2028-08 |
| packs/support-operations/refs/SEVERITY_AND_DECLARATION.md | implementation | ops delivery | The written severity ladder, the tie-break, the mode-changing band, the three-factor declaration score and the objective triggers | 2028-08 |
| packs/support-operations/refs/SYNTHESIS_PASS.md | implementation | ops product data | The weekly pass that turns an inbox into backlog items, the declared coding stance, the denominator and the theme record | 2028-09 |
| packs/support-operations/refs/TRIAGE_RECORD.md | implementation | ops product pii | The field shape of a triage record, the four independent axes, the queue vocabulary, deduplication and the needs-info clock | on-change-of:ISO-10002-revision |
| packs/support-operations/research/DRILL_PROPOSAL.md | example | eos testing | Single-run cold-agent acceptance drill for the support-operations pack, with deterministic machine-checkable criteria |  |
| packs/support-operations/research/NOTES.md | example | eos testing | Research synthesis for the support-operations pack, covering triage and severity models, response measurement, self-service trade-offs, feedback synthesis and founder-scale realities |  |
| packs/ui-ux/CHECKS.md | implementation | a11y testing tooling | What a reviewer or checker can verify about interface work, split into executable today and judgement | on-change-of:WCAG-2.2 |
| packs/ui-ux/PACK.md | guide | web a11y layout perf | Interface work, one accessibility and token spine under eight design philosophies chosen per surface | on-change-of:WCAG-2.2 |
| packs/ui-ux/exemplars/EX-UIUX-001-two-surfaces-one-spine.md | example | web a11y layout | The pack applied end to end, a service task flow and an operations dashboard sharing one token source and one behaviour layer |  |
| packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md | guide | web density layout | Which design philosophy does this surface take? | 2027-10 |
| packs/ui-ux/guides/GD-UIUX-002-component-sourcing.md | guide | web tooling a11y | Where do this surface's interactive components come from? | 2027-11 |
| packs/ui-ux/guides/GD-UIUX-003-a11y-assurance.md | guide | a11y testing web | How much accessibility assurance does this surface buy? | on-change-of:WCAG-2.2 |
| packs/ui-ux/guides/GD-UIUX-004-token-source.md | guide | tooling brand colour | Where do tokens live and how do they reach each platform? | on-change-of:DTCG-format-module |
| packs/ui-ux/refs/A11Y_FLOOR.md | ux | a11y web forms | The accessibility floor in detail, the six gated classes, tag pinning, incomplete triage and what overlays cannot do | on-change-of:WCAG-2.2 |
| packs/ui-ux/refs/COMPONENT_CONTRACT.md | implementation | web a11y tooling | What a shared component owes its consumers, states manifest, pattern map and the admission gate | 2027-10 |
| packs/ui-ux/refs/LAYOUT_AND_MEASURE.md | foundation | layout density typography | Structural layout rules that hold under any visual philosophy, measures, bleeds, rhythm and density | 2027-11 |
| packs/ui-ux/refs/PERFORMANCE_AND_MOTION.md | ux | perf motion web | Field performance as a design constraint, budgets, measurement and the motion safety rules that carry everywhere | on-change-of:core-web-vitals-metric-set |
| packs/ui-ux/refs/TOKEN_PIPELINE.md | implementation | tooling brand colour | One token source, three layers, generated outputs and the guards that stop values drifting | on-change-of:DTCG-format-module |
| packs/ui-ux/research/DRILL_PROPOSAL.md | example | eos | Cold-agent acceptance drill for the ui-ux pack, two philosophies, one behaviour core, machine-checked |  |
| packs/ui-ux/research/NOTES.md | example | eos | Research synthesis for the ui-ux pack, eight design philosophies, accessibility conformance, tokens and component contracts |  |
| packs/writing-content/CHECKS.md | implementation | content forms testing | What a reviewer or a script can verify about writing and content work, split into executable today and judgement | on-change-of:CLDR-plural-categories |
| packs/writing-content/PACK.md | playbook | voice content a11y forms | Writing and content, message structure and error behaviour bind, voice splits three ways, readability never gates | on-change-of:CLDR-plural-categories |
| packs/writing-content/exemplars/EX-WRIT-001-order-panel-second-locale.md | example | content forms a11y | The pack applied end to end to an order-status panel, a concatenated count and a banner error made survivable in a second language |  |
| packs/writing-content/guides/GD-WRIT-001-clarity-philosophy.md | guide | voice content a11y | Which clarity philosophy governs this text, and where the control point sits? | 2028-09 |
| packs/writing-content/guides/GD-WRIT-002-message-structure.md | guide | content forms tooling | How is a user-facing sentence built so a second locale can express what English never had? | on-change-of:CLDR-plural-categories |
| packs/writing-content/guides/GD-WRIT-003-voice-scope.md | guide | voice brand content | Which voice applies to this text, and who is allowed to overrule it? | 2028-09 |
| packs/writing-content/guides/GD-WRIT-004-prose-gate.md | guide | content ci tooling | How is prose checked before it merges, and which signals are allowed to block? | 2028-09 |
| packs/writing-content/refs/ERROR_CONTRACT.md | ux | forms a11y content | The error-message contract in detail, placement, timing, wording, input survival and the human against machine split | on-change-of:WCAG-2.2 |
| packs/writing-content/refs/I18N_MECHANICS.md | implementation | content forms tooling | Plural categories, text expansion figures, the pseudo-locale gate and what each of them does not catch | on-change-of:CLDR-plural-categories |
| packs/writing-content/research/DRILL_PROPOSAL.md | example | eos testing | Cold-agent acceptance drill for the writing-content pack, make a concatenated error string survive a second locale |  |
| packs/writing-content/research/NOTES.md | example | eos testing | Research synthesis for the writing-content pack, four philosophies of clear text, what is machine-checkable, and what should bind |  |
| registry/CAPABILITIES.md | registry | eos | Derived view of the domain coverage matrix, every field in full | 2027-02 |
| registry/LESSONS.md | registry | eos | Derived view of the lessons ledger, every row with its disposition and reasoning | on-change-of:registry/lessons.json |
| registry/LICENCE_RESIDUALS.md | registry | eos security | The cited sources whose licence is unknown or not stated, what the provenance sweep confirmed and what it did not | 2026-11 |
| registry/PROJECTS.md | registry | eos | The venture directory, what each is pinned to, whether that pin resolves, and when it was last checked | 2026-11 |
| registry/VENDORS.md | registry | eos infra hosting | Trusted third parties, what we trust each for and the exit route | 2027-01 |
| registry/stacks/README.md | registry | eos infra hosting | Stack profiles, what each is for and when to reach for it | 2027-01 |
| registry/stacks/STACK-fastapi-postgres.md | stack | infra hosting data testing | Profile 02, FastAPI on Postgres, shape, caps and hard-won constraints | 2027-01 |
| registry/stacks/STACK-fullstack-app.md | stack | web infra hosting testing ci | Profile 03, Next.js front on FastAPI back, the contract seam and the gate set | 2027-01 |
| registry/stacks/STACK-local-first-pwa.md | stack | web infra perf testing | Profile 04, local-first PWA with a WASM compute core, shape, constraints and the sharp edges Venture C paid for | 2027-02 |
| registry/stacks/STACK-web-static.md | stack | web hosting infra | Profile 01, Next.js static export, shape and constraints | 2027-01 |
| tests/fixtures/activation/BRIEF-example.md | example | eos | A venture brief fragment carrying a facts block, for exercising activate --brief |  |
| tools/CLI_CONTRACTS.md | kernel | eos | Subcommand contracts for python -m tools.eos, inputs, JSON outputs, exit codes |  |
