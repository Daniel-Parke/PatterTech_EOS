---
summary: Derived index of every built pack, the always-loaded metadata surface
type: index
tags: [eos]
derived: true
---

# PACK INDEX

The always-loaded knowledge surface. One row per **built** pack: what it
covers, what pulls it in, and how big its body is. Nothing else in
`packs/` is loaded until a row here activates.

Derived file. Written by hand in this build and flagged derived so the
gap stays visible; `python -m tools.eos check --write-index` owns it
once the generator is repointed at `packs/`. Do not hand-edit it after
that: fix `PACK.md` front-matter and the opening paragraph, then
regenerate.

Domains without a pack are not omissions here. Every domain, built or
not, carries an honest row in `registry/CAPABILITIES.md`, generated
from `registry/coverage.json`.

| Pack | Purpose | Activation | Status | Body lines |
| --- | --- | --- | --- | --- |
| `packs/agentic-development/PACK.md` | How to shape agent work: which of ten topologies to run, how to bound it, how to verify it, how to feed it context. The simplest topology that satisfies the task, and anything above a single agent names the pressure that forced it. | Agent, subagent, tool, harness and orchestration surfaces; designing or diagnosing an agent workflow. Predicates: `builds_agent_workflow`, `orchestrates_multiple_agents`, `designs_agent_harness`, `defines_agent_tools`. | built | 256 |
| `packs/api-integration/PACK.md` | Work at a service boundary: the HTTP and RPC APIs we publish or consume, webhook receivers, event contracts, and the way any of them change. | API, schema and webhook directories, OpenAPI, AsyncAPI and protobuf files, route and handler files; publishing, changing or consuming a boundary. Predicates: `exposes_service_boundary`, `consumes_external_api`, `receives_webhooks`, `publishes_events`. | built | 241 |
| `packs/architecture/PACK.md` | Structure inside a venture's own code: where module boundaries live and how they are enforced, which decisions get written down, what proves a build, where data rests, how deep a vendor may reach. | Import and dependency contract files, migration directories, decision records, module and service directories; moving a module, choosing a datastore, integrating a vendor. Predicates: `has_server_code`, `has_multiple_modules`, `has_database`, `has_cross_language_contract`, `has_vendor_holding_identity_or_money`. | built | 328 |
| `packs/coding/PACK.md` | How code is written and accepted in a venture repository: where the oracle comes from, how behaviour is pinned before structure moves, how failures reach callers, and what has to pass before a change merges. | Source, test, build and lint configuration in a venture repo; IMPLEMENT, FIX, REFACTOR and CHORE tasks, and review or merge decisions on them. Predicates: `edits_source`, `reviews_change`, `decides_merge`. | built | 287 |
| `packs/delivery-testing/PACK.md` | How a venture proves its code works: which double stands in for a dependency, where the oracle comes from, when tests get written, and how flakes and quality numbers are handled. | Test trees, doubles, CI workflow files, coverage and retry configuration; every FIX, FEAT and REFACTOR, and any task the router rules R2 or higher. Predicates: `ships_code`, `has_test_suite`. | built | 230 |
| `packs/devops-reliability/PACK.md` | How a venture changes and operates a running system: schema migrations, restore proof, service level objectives and error budgets, progressive rollout, feature flags, incident practice and infrastructure cost. | Migration directories, pipeline and infrastructure configuration, rollout objects, SLO and alert definitions, backup scripting; deploys, rollbacks, incidents, capacity and cost work. Predicates: `deploys_to_environment`, `stores_persistent_data`, `runs_schema_migrations`. | built | 315 |
| `packs/security-privacy/PACK.md` | How our work resists prompt injection, protects secrets, protects personal data, and gets approval before consequential external actions. The canonical home for four protected-set subjects. | Any agent running tools, any repository holding credentials, any system handling personal data, any code that can reach the network. Predicates: `runs_agents`, `holds_credentials`, `handles_personal_data`, `has_external_egress`. | built | 241 |
| `packs/ui-ux/PACK.md` | Interface work: what an interface must achieve for the people using it, and how to choose a design philosophy for a surface rather than inherit one. Accessibility and token discipline bind; visual style does not. | Surface, component, route, style, token and story files; designing a flow, building a component, restyling, accessibility work, interface review. Predicate: `has_user_interface`. | built | 252 |

Eight built packs, 2,150 body lines. The pack contract is
`packs/PACK_SHAPE.md`; a domain that cannot meet its definition of done
stays a registry row and is never described as implemented.
