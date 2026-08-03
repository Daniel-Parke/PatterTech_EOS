---
summary: Derived view of the domain coverage matrix, every capability with its honest status
type: registry
tags: [eos]
status: active
review_by: 2026-11
derived: true
---

# CAPABILITIES

Derived view of `registry/coverage.json`, which is canonical. Every
relevant EOS capability has a row here, built or not. An omission is a
row, never a silence, and a backlog row is not coverage.

Written by hand in this build and flagged derived so the gap stays
visible; the generator takes it over when the tooling lane repoints.
Do not hand-edit it after that: fix `registry/coverage.json` and
regenerate.

8 domains are built. 13 are registry-only, each with a recorded reason.

## Built

| Capability | Pack | Evidence rows | Worked example | Evaluation | Estate relevance | Owner | Review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agentic-development-and-orchestration | `packs/agentic-development/` | 13 (EV-0109 to EV-0121) | packs/agentic-development/exemplars/EX-AGENT-001-logging-migration.md | packs/agentic-development/CHECKS.md, plus the frozen acceptance drill in packs/agentic-development/research/DRILL_PROPOSAL.md | Every EOS session runs under this pack, and PatterStage dispatches agent runs while PatterStudio runs a LangGraph orchestrator. The most load-bearing pack in the estate. | EOS integrator | on-change-of:agent-sdk-major-release |
| API-and-integration-design | `packs/api-integration/` | 24 (EV-0122 to EV-0145) | packs/api-integration/exemplars/invoices-api-change.md and packs/api-integration/exemplars/stripe-versioning.md | packs/api-integration/CHECKS.md, plus the frozen acceptance drill in packs/api-integration/research/DRILL_PROPOSAL.md | AutoWatt serves three surfaces over one API and takes vendor webhooks; WiseWattage integrates Clerk and Stripe; PatterTech_App exposes a subscribe endpoint. | EOS integrator | 2027-12 |
| architecture-and-system-design | `packs/architecture/` | 18 (EV-0146 to EV-0163) | packs/architecture/exemplars/billing-catalogue-boundary.md | packs/architecture/CHECKS.md, plus the frozen acceptance drill in packs/architecture/research/DRILL_PROPOSAL.md | AutoWatt runs one record core with three surfaces, WiseWattage a Polars pipeline behind an API, PatterStudio a monorepo with import-linter rings. All three are live architecture decisions. | EOS integrator | 2027-02 |
| coding-and-software-construction | `packs/coding/` | 20 (EV-0164 to EV-0183) | packs/coding/exemplars/EX-COD-001-webhook-silent-failure.md | packs/coding/CHECKS.md, plus the frozen acceptance drill in packs/coding/research/DRILL_PROPOSAL.md | Every venture that ships code. This is the pack most tasks in the estate will load. | EOS integrator | 2027-02 |
| delivery-testing-and-quality | `packs/delivery-testing/` | 13 (EV-0184 to EV-0196) | packs/delivery-testing/exemplars/EX-DEL-001-drifted-fake-and-a-lying-suite.md | packs/delivery-testing/CHECKS.md, plus the frozen acceptance drill in packs/delivery-testing/research/DRILL_PROPOSAL.md | AutoWatt and WiseWattage both carry suites with drifted doubles; the test-timing ablation sets this pack's defaults from measured evidence. | EOS integrator | 2027-08 |
| devops-platform-and-reliability | `packs/devops-reliability/` | 15 (EV-0197 to EV-0211) | packs/devops-reliability/exemplars/EX-DEVOPS-001-email-to-contacts.md | packs/devops-reliability/CHECKS.md, plus the frozen acceptance drill in packs/devops-reliability/research/DRILL_PROPOSAL.md | WiseWattage runs on Railway with Postgres and cron, AutoWatt targets AWS eu-west-2, PatterTech_App runs Docker Compose locally. Production safety is protected-set material and lives here. | EOS integrator | 2027-04 |
| security-privacy-and-safety | `packs/security-privacy/` | 15 (EV-0212 to EV-0226) | packs/security-privacy/exemplars/poisoned-integration-guide.md | packs/security-privacy/CHECKS.md, plus the frozen acceptance drill in packs/security-privacy/research/DRILL_PROPOSAL.md | The canonical home for four protected-set subjects: prompt-injection resistance, secret protection, data protection and approval for consequential external actions. It binds every venture and every EOS session. | EOS integrator | on-change-of:EV-0213 |
| UI-UX-accessibility-and-design-systems | `packs/ui-ux/` | 15 (EV-0227 to EV-0241) | packs/ui-ux/exemplars/two-surfaces-one-spine.md | packs/ui-ux/CHECKS.md, plus the frozen acceptance drill in packs/ui-ux/research/DRILL_PROPOSAL.md | PatterTech_Website, AutoWatt's three surfaces, WiseWattage's dashboards and PatterStage's control plane are four different design philosophies in one estate, which is why the pack compares rather than prescribes. | EOS integrator | on-change-of:WCAG-2.2 |

Activation conditions are in `packs/INDEX.md` and in each pack's own
Activation section; the full text for every row is in
`registry/coverage.json`.

## Registry-only

These are not implemented and are never described as implemented. No stub
directory exists for any of them.

| Capability | Why no pack | Activation | Estate relevance | Owner | Review |
| --- | --- | --- | --- | --- | --- |
| product-discovery-and-strategy | scheduled for Wave B in this build. The venture brief and interview in inception/ are the only current coverage, and they ask questions rather than teach method. | Writing a product brief, spec, roadmap or acceptance walk-through; deciding what to build before deciding how. | Both AutoWatt and Guth wrote product bibles with no EOS guidance behind them, and the Website's content strategy has no owner. | EOS integrator | on-change-of:wave-B-pack-completion |
| business-logic-and-domain-modelling | scheduled for Wave B in this build. The architecture pack covers where boundaries go, not how to model what sits inside them. | Modelling a domain: entities, invariants, state machines, eligibility and pricing rules, and where that logic is allowed to live. | AutoWatt's grant and record model and WiseWattage's tariff and battery logic are the estate's two hardest domain models, both written without shared method. | EOS integrator | on-change-of:wave-B-pack-completion |
| data-analytics-and-experimentation | scheduled for Wave B in this build. The benchmark protocol in benchmark/PROTOCOL.md is the only measurement discipline the EOS currently owns, and it is scoped to the kernel comparison. | Analytics instrumentation, metric definition, dashboards, and the design of A/B tests or holdouts. | PatterTech_App plans Umami analytics and a consent ledger; no venture currently runs an experiment, so the need is near rather than urgent. | EOS integrator | on-change-of:wave-B-pack-completion |
| AI-ML-and-LLM-development | scheduled for Wave B in this build. Distinct from the agentic-development pack, which covers how we build with agents rather than how a venture ships model-backed features. | Shipping a product feature built on a model: prompts inside product code, retrieval, evaluation harnesses, inference cost and model choice. | PatterStudio runs a LangGraph orchestrator and PatterStage dispatches agent runs. Neither has EOS coverage, and both are live. | EOS integrator | on-change-of:wave-B-pack-completion |
| marketing-growth-content-and-SEO | scheduled for Wave B in this build | Public content, search metadata, campaigns, lifecycle email and landing pages. | PatterTech_Website is live and public, and PatterTech_App plans a self-hosted mailing list with a consent ledger. Nothing governs either. | EOS integrator | on-change-of:wave-B-pack-completion |
| business-model-pricing-and-operations | scheduled for Wave B in this build | Pricing and packaging decisions, billing models, unit economics and back-office process. | WiseWattage has billing behind a feature flag and PatterPower is a commercial plan with a financial model. Neither has EOS coverage. | EOS integrator | on-change-of:wave-B-pack-completion |
| documentation-and-developer-experience | scheduled for Wave B in this build | READMEs, API documentation, onboarding paths, and the ergonomics of a venture's own tooling. | Every repo in the estate carries hand-rolled documentation of uneven quality, and the audit found stale documentation is the estate's most common defect class. | EOS integrator | on-change-of:wave-B-pack-completion |
| native-client-design | scheduled for Wave B in this build. The ui-ux pack already names the platform accessibility route for native surfaces, so the gap is method rather than conformance. | iOS, Android or desktop client work, including platform accessibility profiles. | No venture ships a native client today. PatterHome runs a web frontend against a local box, which is the closest the estate comes. | EOS integrator | on-change-of:wave-B-pack-completion |
| customer-support-and-feedback-operations | scheduled for Wave B in this build | Support inboxes, ticketing, feedback triage, status pages and the loop back into the backlog. | WiseWattage has real users and handles support ad hoc. AutoWatt will need this at Genesis close. | EOS integrator | on-change-of:wave-B-pack-completion |
| legal-licensing-and-compliance-routing | scheduled for Wave B in this build. Seeded from the licence flags already gathered across 241 evidence rows. | Licence choice, third-party licence compatibility, regulatory routing, and which duties attach to which data. | The evidence ledger already carries a per-source licence column that is load-bearing for what may be copied, and PatterOS ships Apache-2.0 with reserved marks. The routing rules are unwritten. | EOS integrator | on-change-of:wave-B-pack-completion |
| writing-and-content-design | scheduled for Wave B in this build. Until the pack lands, the voice law survives in two enforceable places: the router's closing paragraph in AGENTS.md, and check E004, which fails em-dashes and flags exclamation marks and cliches. | Any prose written for a venture or for this repo, at three scopes: binding for EOS-internal prose, default for venture documentation, preference for brand voice. | Every repo writes prose, and the v1 voice module is now archived at archive/v1/doctrine/voice/. | EOS integrator | on-change-of:wave-B-pack-completion |
| PatterTech-house | scheduled for Wave B in this build. Authority is capped at preference by the metadata rules, adoption is per venture, and the 18s against 12s conduit contradiction resolves here with every numeric budget in exactly one file. | A venture that has explicitly adopted PatterTech house style. It never activates by default. | PatterTech_Website and PatterStudio share the Cherenkov brand through a hand port, and the house visual language has no single home. | EOS integrator | on-change-of:wave-B-pack-completion |
| hardware | No venture currently demands hardware doctrine. PatterOS is pre-EOS and dormant, with its last commit on 2026-06-18, so a hardware pack would be written from nothing and reviewed by nobody. Recorded here rather than silently deferred, per ADR-0002. | Selecting, sizing or provisioning physical kit, and the firmware or driver work that follows it. | PatterOS is the only hardware-adjacent repo in the estate and it is dormant. No governed venture touches hardware. | EOS integrator | on-change-of:venture-requiring-hardware-doctrine |

Evidence pointers for every registry-only row are empty on purpose: no
research batch has run for these domains, so there is nothing to cite.
The evaluation column in `registry/coverage.json` says what will create
them. Hardware is the one row that is not waiting on a wave: it waits on
a venture that needs it.
