---
summary: Derived view of the domain coverage matrix, every field in full
type: registry
tags: [eos]
status: active
review_by: 2027-02
derived: true
---

# CAPABILITIES

Derived from `registry/coverage.json` by
`python -m tools.eos check --write-index`. Do not hand-edit.

**Built: 21. Registry-only: 1.** A registry-only
row is not coverage, and this view says so first.

## Not built

### hardware

- **Why not**: No venture currently demands hardware doctrine. PatterOS is pre-EOS and dormant, with its last commit on 2026-06-18, so a hardware pack would be written from nothing and reviewed by nobody. Recorded here rather than silently deferred, per ADR-0002.
- **Would activate on**: Selecting, sizing or provisioning physical kit, and the firmware or driver work that follows it.
- **Estate relevance**: PatterOS is the only hardware-adjacent repo in the estate and it is dormant. No governed venture touches hardware.
- **Evaluation**: None. The domain is not built, so there is nothing to evaluate. It earns a pack when a venture demands one.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:venture-requiring-hardware-doctrine

## Built

### AI-ML-and-LLM-development

- **Pack**: `packs/ai-ml-llm/`
- **Activation**: Shipping a product feature built on a model: prompts inside product code, retrieval, evaluation harnesses, inference cost and model choice. Predicates: calls_a_model, changes_prompt_or_model, builds_retrieval, evaluates_model_output, ships_model_output.
- **Worked example**: `packs/ai-ml-llm/exemplars/EX-AIML-001-classifier-prompt-swap.md`
- **Evaluation**: packs/ai-ml-llm/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/ai-ml-llm.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: PatterStudio runs a LangGraph orchestrator and PatterStage dispatches agent runs. Neither has EOS coverage, and both are live.
- **Owner**: EOS integrator
- **Review trigger**: 2027-02
- **Evidence**: 27 rows, EV-0242, EV-0243, EV-0244, EV-0245, EV-0246, EV-0247, EV-0248, EV-0249, EV-0250, EV-0251, EV-0252, EV-0253, EV-0254, EV-0255, EV-0256, EV-0257, EV-0258, EV-0259, EV-0260, EV-0261, EV-0262, EV-0263, EV-0264, EV-0265, EV-0266, EV-0267, EV-0268

### API-and-integration-design

- **Pack**: `packs/api-integration/`
- **Activation**: Paths: api directories, OpenAPI, AsyncAPI and protobuf files, schema directories, webhook and connector directories, route and handler files. Task types: publishing or changing a service boundary, adding a webhook receiver, consuming a third-party API, changing an event payload, deprecating an endpoint. Predicates: exposes_service_boundary, consumes_external_api, receives_webhooks, publishes_events.
- **Worked example**: `packs/api-integration/exemplars/EX-API-001-invoices-api-change.md`, `packs/api-integration/exemplars/EX-API-002-stripe-versioning.md`
- **Evaluation**: packs/api-integration/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/api-integration.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: Venture A serves three surfaces over one API and takes vendor webhooks; WiseWattage integrates Clerk and Stripe; PatterTech_App exposes a subscribe endpoint.
- **Owner**: EOS integrator
- **Review trigger**: 2027-12
- **Evidence**: 24 rows, EV-0122, EV-0123, EV-0124, EV-0125, EV-0126, EV-0127, EV-0128, EV-0129, EV-0130, EV-0131, EV-0132, EV-0133, EV-0134, EV-0135, EV-0136, EV-0137, EV-0138, EV-0139, EV-0140, EV-0141, EV-0142, EV-0143, EV-0144, EV-0145

### PatterTech-house

- **Pack**: `packs/pattertech-house/`
- **Activation**: A venture that has explicitly adopted PatterTech house style. It never activates by default. Predicates: adopts_pattertech_house.
- **Worked example**: `packs/pattertech-house/exemplars/EX-HOUSE-001-services-section.md`
- **Evaluation**: packs/pattertech-house/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/pattertech-house.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: PatterTech_Website and PatterStudio share the Cherenkov brand through a hand port, and the house visual language has no single home.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:WCAG-2.2
- **Evidence**: 14 rows, EV-0389, EV-0390, EV-0391, EV-0392, EV-0393, EV-0394, EV-0395, EV-0396, EV-0397, EV-0398, EV-0399, EV-0400, EV-0401, EV-0402

### UI-UX-accessibility-and-design-systems

- **Pack**: `packs/ui-ux/`
- **Activation**: Paths: surface, app, ui, component, page, route, style, design-system, token and story files, token sources and generated outputs. Task types: designing a surface or flow, building a component, restyling, accessibility work, interface review, design-system adoption, dashboard layout, front-end performance. Predicates: has_user_interface.
- **Worked example**: `packs/ui-ux/exemplars/EX-UIUX-001-two-surfaces-one-spine.md`
- **Evaluation**: packs/ui-ux/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/ui-ux.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: PatterTech_Website, Venture A's three surfaces, WiseWattage's dashboards and PatterStage's control plane are four different design philosophies in one estate, which is why the pack compares rather than prescribes.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:WCAG-2.2
- **Evidence**: 15 rows, EV-0227, EV-0228, EV-0229, EV-0230, EV-0231, EV-0232, EV-0233, EV-0234, EV-0235, EV-0236, EV-0237, EV-0238, EV-0239, EV-0240, EV-0241

### agentic-development-and-orchestration

- **Pack**: `packs/agentic-development/`
- **Activation**: Paths: agent and subagent definitions, instruction and prompt files, tool and MCP definitions, harness runners, workflow graphs, guardrail registration, checkpoint stores, trace configuration. Task types: designing an agent workflow, adding or removing a subagent, changing a tool surface, setting run budgets, adding a checkpoint or approval, diagnosing a looping or stalling agent. Predicates: builds_agent_workflow, orchestrates_multiple_agents, designs_agent_harness, defines_agent_tools.
- **Worked example**: `packs/agentic-development/exemplars/EX-AGENT-001-logging-migration.md`
- **Evaluation**: packs/agentic-development/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/agentic-development.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: Every EOS session runs under this pack, and PatterStage dispatches agent runs while PatterStudio runs a LangGraph orchestrator. The most load-bearing pack in the estate.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:agent-sdk-major-release
- **Evidence**: 13 rows, EV-0109, EV-0110, EV-0111, EV-0112, EV-0113, EV-0114, EV-0115, EV-0116, EV-0117, EV-0118, EV-0119, EV-0120, EV-0121

### agentic-swarm-and-graph-engineering

- **Pack**: `packs/agentic-swarm/`
- **Activation**: Paths: the claim file, partition artefacts, lane briefs and packets, worktree layout, orchestration scripts and workflow files, and the graph-build method a venture seed compiles from its kernel template. Task types: deciding whether to fan out at all, cutting a partition from a product map, writing or reviewing a lane packet, sizing lanes, choosing between a script and model-driven delegation, setting the run budget, merging lanes, reviewing what a lane produced, diagnosing a run that cost more than it returned. Predicates: fans_work_across_lanes, cuts_a_build_partition, integrates_parallel_lanes, writes_a_lane_packet.
- **Worked example**: `packs/agentic-swarm/exemplars/EX-SWARM-001-eos-v2-1-partition.md`
- **Evaluation**: packs/agentic-swarm/CHECKS.md, the reviewable criteria for this domain, split into rows a script can decide today and rows that need a reviewer. No acceptance drill exists: packs/agentic-swarm/research/DRILL_PROPOSAL.md states the shape one would take and says plainly that it is proposed and not frozen, so no cold agent has been graded on this pack.
- **Estate relevance**: The EOS builds itself this way and nothing else does yet. The v2 build ran two parallel lanes and the v2.1 build fanned wider over a dependency graph; those runs are the only evidence the pack has of its own architecture. No venture has used it. ADR-0006 decision 4 sends its executable half into ORG seeds through a kernel template, so a venture meets it at Genesis rather than through the EOS.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:agent-harness-major-release
- **Evidence**: 15 rows, EV-0006, EV-0010, EV-0053, EV-0105, EV-0107, EV-0108, EV-0109, EV-0111, EV-0112, EV-0167, EV-0169, EV-0178, EV-0219, EV-0244, EV-0251

### architecture-and-system-design

- **Pack**: `packs/architecture/`
- **Activation**: Paths: import and dependency contract files, migration directories, decision-record directories, C4 or arc42 artefacts, module and service directories, webhook handlers, public API schema files. Task types: adding or moving a module, declaring a boundary, choosing a datastore, splitting a deployable, integrating a vendor, proving a restructure changed nothing. Predicates: has_server_code, has_multiple_modules, has_database, has_cross_language_contract, has_vendor_holding_identity_or_money.
- **Worked example**: `packs/architecture/exemplars/EX-ARCH-001-billing-catalogue-boundary.md`
- **Evaluation**: packs/architecture/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/architecture.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: Venture A runs one record core with three surfaces, WiseWattage a Polars pipeline behind an API, PatterStudio a monorepo with import-linter rings. All three are live architecture decisions.
- **Owner**: EOS integrator
- **Review trigger**: 2027-02
- **Evidence**: 18 rows, EV-0146, EV-0147, EV-0148, EV-0149, EV-0150, EV-0151, EV-0152, EV-0153, EV-0154, EV-0155, EV-0156, EV-0157, EV-0158, EV-0159, EV-0160, EV-0161, EV-0162, EV-0163

### business-logic-and-domain-modelling

- **Pack**: `packs/business-logic-modelling/`
- **Activation**: Modelling a domain: entities, invariants, state machines, eligibility and pricing rules, and where that logic is allowed to live. Predicates: encodes_domain_rule, models_money, models_time, has_lifecycle_state.
- **Worked example**: `packs/business-logic-modelling/exemplars/EX-BLM-001-subscription-renewal.md`
- **Evaluation**: packs/business-logic-modelling/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/business-logic-modelling.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: Venture A's grant and record model and WiseWattage's tariff and battery logic are the estate's two hardest domain models, both written without shared method.
- **Owner**: EOS integrator
- **Review trigger**: 2027-09
- **Evidence**: 18 rows, EV-0269, EV-0270, EV-0271, EV-0272, EV-0273, EV-0274, EV-0275, EV-0276, EV-0277, EV-0278, EV-0279, EV-0280, EV-0281, EV-0282, EV-0283, EV-0284, EV-0285, EV-0286

### business-model-pricing-and-operations

- **Pack**: `packs/business-model-pricing/`
- **Activation**: Pricing and packaging decisions, billing models, unit economics and back-office process. Predicates: sets_a_price, publishes_a_price, sells_to_consumers, sells_by_subscription, sells_to_public_sector, bundles_or_discounts, reports_commercial_metrics.
- **Worked example**: `packs/business-model-pricing/exemplars/EX-BMP-001-first-consumer-subscription.md`
- **Evaluation**: packs/business-model-pricing/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/business-model-pricing.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: WiseWattage has billing behind a feature flag and PatterPower is a commercial plan with a financial model. Neither has EOS coverage.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:DMCC-Part-4-Chapter-2-commencement
- **Evidence**: 18 rows, EV-0287, EV-0288, EV-0289, EV-0290, EV-0291, EV-0292, EV-0293, EV-0294, EV-0295, EV-0296, EV-0297, EV-0298, EV-0299, EV-0300, EV-0301, EV-0302, EV-0303, EV-0304

### coding-and-software-construction

- **Pack**: `packs/coding/`
- **Activation**: Paths: source, test, build, packaging, lint and static-analysis configuration in a venture repo. Task types: IMPLEMENT, FIX, REFACTOR and CHORE against an existing codebase, and review or merge decisions on them. Predicates: edits_source, reviews_change, decides_merge.
- **Worked example**: `packs/coding/exemplars/EX-COD-001-webhook-silent-failure.md`
- **Evaluation**: packs/coding/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/coding.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: Every venture that ships code. This is the pack most tasks in the estate will load.
- **Owner**: EOS integrator
- **Review trigger**: 2027-02
- **Evidence**: 20 rows, EV-0164, EV-0165, EV-0166, EV-0167, EV-0168, EV-0169, EV-0170, EV-0171, EV-0172, EV-0173, EV-0174, EV-0175, EV-0176, EV-0177, EV-0178, EV-0179, EV-0180, EV-0181, EV-0182, EV-0183

### customer-support-and-feedback-operations

- **Pack**: `packs/support-operations/`
- **Activation**: Support inboxes, ticketing, feedback triage, status pages and the loop back into the backlog. Predicates: has_customer_inbound, has_paying_customers, has_customer_visible_incident, runs_public_tracker, reports_support_metric, single_responder.
- **Worked example**: `packs/support-operations/exemplars/EX-SUPPORT-001-one-inbox-week.md`
- **Evaluation**: packs/support-operations/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/support-operations.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: WiseWattage has real users and handles support ad hoc. Venture A was still in its v1 Genesis design phase at the last look, 2026-07-07, and will need support operations once it carries real users. The EOS does not track venture progress after birth, so read that as a note rather than a date.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:ISO-10002-revision
- **Evidence**: 12 rows, EV-0421, EV-0422, EV-0423, EV-0424, EV-0425, EV-0426, EV-0427, EV-0428, EV-0429, EV-0430, EV-0431, EV-0432

### data-analytics-and-experimentation

- **Pack**: `packs/data-analytics/`
- **Activation**: Analytics instrumentation, metric definition, dashboards, and the design of A/B tests or holdouts. Predicates: publishes_analytics_table, defines_events, runs_experiment, reads_for_decision, handles_analytics_identifier.
- **Worked example**: `packs/data-analytics/exemplars/EX-DATA-001-gated-model-honest-experiment.md`
- **Evaluation**: packs/data-analytics/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/data-analytics.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: PatterTech_App plans Umami analytics and a consent ledger; no venture currently runs an experiment, so the need is near rather than urgent.
- **Owner**: EOS integrator
- **Review trigger**: 2027-11
- **Evidence**: 16 rows, EV-0305, EV-0306, EV-0307, EV-0308, EV-0309, EV-0310, EV-0311, EV-0312, EV-0313, EV-0315, EV-0316, EV-0317, EV-0318, EV-0319, EV-0320, EV-0321

### delivery-testing-and-quality

- **Pack**: `packs/delivery-testing/`
- **Activation**: Paths: test trees, conftest files, anything named for a fake, stub, mock or double, CI workflow files, coverage, mutation and retry configuration. Task types: FIX, FEAT and REFACTOR always, plus any task the router rules R2 or higher. Predicates: ships_code, has_test_suite.
- **Worked example**: `packs/delivery-testing/exemplars/EX-DEL-001-drifted-fake-and-a-lying-suite.md`
- **Evaluation**: packs/delivery-testing/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/delivery-testing.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: Venture A and WiseWattage both carry suites with drifted doubles; the test-timing ablation sets this pack's defaults from measured evidence.
- **Owner**: EOS integrator
- **Review trigger**: 2028-02
- **Evidence**: 13 rows, EV-0184, EV-0185, EV-0186, EV-0187, EV-0188, EV-0189, EV-0190, EV-0191, EV-0192, EV-0193, EV-0194, EV-0195, EV-0196

### devops-platform-and-reliability

- **Pack**: `packs/devops-reliability/`
- **Activation**: Paths: migration directories, CI and pipeline configuration, infrastructure as code, container and orchestration manifests, rollout objects, SLO and alert definitions, feature flag configuration, backup scripting, cost configuration. Task types: schema change, deploy, rollback, incident response, capacity or cost work, observability instrumentation. Predicates: deploys_to_environment, stores_persistent_data, runs_schema_migrations.
- **Worked example**: `packs/devops-reliability/exemplars/EX-DEVOPS-001-email-to-contacts.md`
- **Evaluation**: packs/devops-reliability/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/devops-reliability.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: WiseWattage runs on Railway with Postgres and cron, Venture A targets AWS eu-west-2, PatterTech_App runs Docker Compose locally. Production safety is protected-set material and lives here.
- **Owner**: EOS integrator
- **Review trigger**: 2027-04
- **Evidence**: 15 rows, EV-0197, EV-0198, EV-0199, EV-0200, EV-0201, EV-0202, EV-0203, EV-0204, EV-0205, EV-0206, EV-0207, EV-0208, EV-0209, EV-0210, EV-0211

### documentation-and-developer-experience

- **Pack**: `packs/docs-dx/`
- **Activation**: READMEs, API documentation, onboarding paths, and the ergonomics of a venture's own tooling. Predicates: publishes_docs, documents_executable_surface, emits_user_visible_failure, renames_or_deletes_documented_page.
- **Worked example**: `packs/docs-dx/exemplars/EX-DOCS-001-stale-quickstart.md`
- **Evaluation**: packs/docs-dx/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/docs-dx.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: Every repo in the estate carries hand-rolled documentation of uneven quality, and the audit found stale documentation is the estate's most common defect class.
- **Owner**: EOS integrator
- **Review trigger**: 2028-04
- **Evidence**: 16 rows, EV-0044, EV-0322, EV-0323, EV-0324, EV-0325, EV-0326, EV-0327, EV-0328, EV-0329, EV-0330, EV-0331, EV-0332, EV-0333, EV-0334, EV-0335, EV-0336

### legal-licensing-and-compliance-routing

- **Pack**: `packs/legal-licensing/`
- **Activation**: Licence choice, third-party licence compatibility, regulatory routing, and which duties attach to which data. Predicates: adds_dependency, vendors_code, publishes_code, hosts_service, accepts_contribution, processes_personal_data.
- **Worked example**: `packs/legal-licensing/exemplars/EX-LEGAL-001-waitlist-with-a-poisoned-tree.md`
- **Evaluation**: packs/legal-licensing/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/legal-licensing.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: The evidence ledger already carries a per-source licence column that is load-bearing for what may be copied, and PatterOS ships Apache-2.0 with reserved marks. The routing rules are unwritten.
- **Owner**: EOS integrator
- **Review trigger**: 2027-04
- **Evidence**: 16 rows, EV-0337, EV-0338, EV-0339, EV-0340, EV-0341, EV-0342, EV-0343, EV-0344, EV-0345, EV-0346, EV-0347, EV-0348, EV-0349, EV-0350, EV-0351, EV-0352

### marketing-growth-content-and-SEO

- **Pack**: `packs/marketing-growth/`
- **Activation**: Public content, search metadata, campaigns, lifecycle email and landing pages. Predicates: publishes_public_content, collects_contact_details, sends_marketing_message, reports_channel_effect, plans_growth_spend.
- **Worked example**: `packs/marketing-growth/exemplars/EX-MKTG-001-launch-and-first-sequence.md`
- **Evaluation**: packs/marketing-growth/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/marketing-growth.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: PatterTech_Website is live and public, and PatterTech_App plans a self-hosted mailing list with a consent ledger. Nothing governs either.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:PECR-reg-22-amendment
- **Evidence**: 17 rows, EV-0353, EV-0354, EV-0355, EV-0356, EV-0357, EV-0358, EV-0359, EV-0360, EV-0361, EV-0362, EV-0363, EV-0364, EV-0365, EV-0366, EV-0367, EV-0368, EV-0369

### native-client-design

- **Pack**: `packs/native-client/`
- **Activation**: iOS, Android or desktop client work, including platform accessibility profiles. Predicates: ships_a_binary, has_native_ui, has_local_write_store, distributes_via_app_store.
- **Worked example**: `packs/native-client/exemplars/EX-NAT-001-offline-booking-client.md`
- **Evaluation**: packs/native-client/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/native-client.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: No venture ships a native client today. PatterHome runs a web frontend against a local box, which is the closest the estate comes.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:EN-301-549-v4-publication
- **Evidence**: 19 rows, EV-0370, EV-0371, EV-0372, EV-0373, EV-0374, EV-0375, EV-0376, EV-0377, EV-0378, EV-0379, EV-0380, EV-0381, EV-0382, EV-0383, EV-0384, EV-0385, EV-0386, EV-0387, EV-0388

### product-discovery-and-strategy

- **Pack**: `packs/product-discovery/`
- **Activation**: Writing a product brief, spec, roadmap or acceptance walk-through; deciding what to build before deciding how. Predicates: proposes_capability, prioritises_work, cites_user_claim, runs_experiment, writes_acceptance_criteria.
- **Worked example**: `packs/product-discovery/exemplars/EX-DISC-001-approvals-inbox-request.md`
- **Evaluation**: packs/product-discovery/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/product-discovery.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: Both Venture A and Guth wrote product bibles with no EOS guidance behind them, and the Website's content strategy has no owner.
- **Owner**: EOS integrator
- **Review trigger**: 2028-06
- **Evidence**: 18 rows, EV-0403, EV-0404, EV-0405, EV-0406, EV-0407, EV-0408, EV-0409, EV-0410, EV-0411, EV-0412, EV-0413, EV-0414, EV-0415, EV-0416, EV-0417, EV-0418, EV-0419, EV-0420

### security-privacy-and-safety

- **Pack**: `packs/security-privacy/`
- **Activation**: Any agent running tools, any repository holding credentials, any system handling personal data, any code that can reach the network. Task types: credential handling, egress, personal-data work, approval design, injection review. Predicates: runs_agents, holds_credentials, handles_personal_data, has_external_egress.
- **Worked example**: `packs/security-privacy/exemplars/EX-SEC-001-poisoned-integration-guide.md`
- **Evaluation**: packs/security-privacy/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/security-privacy.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: The canonical home for four protected-set subjects: prompt-injection resistance, secret protection, data protection and approval for consequential external actions. It binds every venture and every EOS session.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:EV-0213
- **Evidence**: 15 rows, EV-0212, EV-0213, EV-0214, EV-0215, EV-0216, EV-0217, EV-0218, EV-0219, EV-0220, EV-0221, EV-0222, EV-0223, EV-0224, EV-0225, EV-0226

### writing-and-content-design

- **Pack**: `packs/writing-content/`
- **Activation**: Any prose written for a venture or for this repo, at three scopes: binding for EOS-internal prose, default for venture documentation, preference for brand voice. Predicates: writes_user_facing_text, has_forms, ships_second_locale, writes_venture_documentation, writes_eos_internal_prose, reuses_external_style_guidance.
- **Worked example**: `packs/writing-content/exemplars/EX-WRIT-001-order-panel-second-locale.md`
- **Evaluation**: packs/writing-content/CHECKS.md, the reviewable criteria for this domain. The acceptance drill is frozen at benchmark/drills/writing-content.md and has never been run: benchmark/drills/RESULTS.json holds no verdict for it, and ADR-0007 defers running the drills rather than treating them as a release gate.
- **Estate relevance**: Every repo writes prose, and the v1 voice module is now archived at archive/v1-final:doctrine/voice/.
- **Owner**: EOS integrator
- **Review trigger**: on-change-of:CLDR-plural-categories
- **Evidence**: 16 rows, EV-0433, EV-0434, EV-0435, EV-0436, EV-0437, EV-0438, EV-0439, EV-0440, EV-0441, EV-0442, EV-0443, EV-0444, EV-0445, EV-0446, EV-0447, EV-0448
