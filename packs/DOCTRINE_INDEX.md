---
summary: Derived catalogue of every atomic Doctrine and its authority
type: index
tags: [eos]
derived: true
---

# DOCTRINE_INDEX

Derived from the atomic files under each pack. Edit a Doctrine
record, then run `python -m tools.eos check --write-index`.

| id | authority | standing statement | applies when | challenge triggers | pack | review |
| --- | --- | --- | --- | --- | --- | --- |
| DOC-AGENT-001 | binding | One writer. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-002 | binding | Irreversible or externally visible acts pass a human checkpoint. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-003 | binding | Evaluation is separate from generation, and the evaluator holds external truth. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-004 | binding | Checkpoint state is a trust boundary. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-005 | default | Every loop is bounded. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-006 | default | Any topology above direct single-agent is recorded. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-007 | default | Runs are traceable. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-008 | default | Start at direct single-agent with a strong oracle. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-009 | default | Harness richness tracks the model's demonstrated gaps. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-010 | default | Context arrives just in time, by progressive disclosure. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-011 | default | Tool capability order: explicit tools, then bash, then generated code, then MCP. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-012 | default | Continuity across context windows rides on artifacts and git history, not on compaction alone. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-013 | default | Cheap guardrails run beside the work and trip a wire, and cross-cutting policy sits at the runner rather than inside an agent. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-014 | default | Memory is a swappable store behind one interface with an explicit trimming policy. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-015 | default | Evaluation suites start at twenty to fifty tasks harvested from real failures, scored with pass@k and pass^k. | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-016 | preference | Event-sourced conversation state over ad-hoc message history (EV-0050, EV-0001). | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-017 | preference | Functional composition before graph builders, reaching for a graph only when the graph earns itself (EV-0078). | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-018 | preference | Condensers that always preserve the opening events (EV-0080). | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AGENT-019 | preference | Mechanical stuck detection with thresholds tuned per model (EV-0082). | builds_agent_workflow | operator_requests_doctrine_review | agentic-development | on-change-of:agent-sdk-major-release |
| DOC-AIML-001 | binding | Every eval result carries the prompt template identity and the model identifier. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-002 | binding | A private held-out set exists, and the tuning path never reads it. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-003 | binding | Model identifiers are pinned to a version the provider has undertaken not to move, with the retirement date recorded beside the call site. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-004 | binding | A judge is validated against human labels before its score decides anything. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-005 | binding | Consequential model output is reviewed by a person before it takes effect. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-006 | default | Grade a sample by hand before writing the rubric. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-007 | default | Report paired differences with a stated minimum detectable effect. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-008 | default | Retrieval before fine-tuning for anything that is a fact. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-009 | default | Lexical retrieval first, embeddings earn their place. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-010 | default | Split retrieval metrics by stage. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-011 | default | Keep dataset, solver and scorer as separate versioned things. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-012 | default | Order every prompt stable prefix first, variable suffix last, and assert the cache hit rate. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-013 | default | An eval run is reproducible without the network. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-014 | default | Run a machine-repeatable eval before a model-facing change ships. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-015 | default | Score abstention, and report the abstention rate beside accuracy. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-016 | preference | Compiled prompt optimisation against hand-written legible context. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-017 | preference | Trained cascade routing against model self-assessment routing. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-AIML-018 | preference | Which evaluation framework, and where the eval lives. | calls_a_model | operator_requests_doctrine_review | ai-ml-llm | 2027-02 |
| DOC-API-001 | binding | A breaking-change check runs in CI against a committed baseline, and fails the build. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-002 | binding | Webhook receivers authenticate the exact raw request before parsing, reject stale deliveries, and process accepted deliveries idempotently against a pinned payload version. | receives_webhooks | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-003 | binding | Money-touching mutating endpoints define all four idempotency parameters, not just a header. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-004 | binding | Deprecation and removal are two dated events, and removal is never the earlier one. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-005 | default | Errors use application/problem+json. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-006 | default | Cursor pagination with opaque tokens, no offset. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-007 | default | Idempotency-Key as the header name. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-008 | default | CloudEvents envelope for events. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-009 | default | BACKWARD_TRANSITIVE for any log a consumer can rewind. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-010 | default | Schema-derived property tests against the contract. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-011 | default | Rate limit policy advertised separately from the live budget. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-012 | default | Webhook signatures over the triple id.timestamp.payload with a versioned prefix. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-013 | default | The contract is machine-readable and lives in the repo. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-014 | default | The compatibility promise is declared before the first change. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-015 | preference | Contract-first with a definition language such as TypeSpec (EV-0145) when the boundary is public or has several consumers; code-first generation when it is internal, because a spec emitted from the handlers cannot drift from them. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-016 | preference | An executable ruleset (EV-0137) rather than a style document, noting that Spectral listed no OpenAPI 3.2 support at the access date. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-017 | preference | GraphQL only where selection-based delivery solves a demonstrated client problem, and then with the schema surface monitored against real production queries (EV-0142). | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-API-018 | preference | One problem-type URI namespace per venture, so error types are greppable across services. | exposes_service_boundary | operator_requests_doctrine_review | api-integration | 2027-12 |
| DOC-ARCH-001 | binding | A declared boundary is machine-checked in CI from the first week. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-002 | binding | Generated contract artefacts are produced deterministically from a committed source and CI fails when they drift. | has_cross_language_contract | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-003 | binding | A typed client verifies that a response succeeded before treating the response body as data. | consumes_external_api | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-004 | default | One deployable, one database, modules enforced in the build. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-005 | default | Split only on a measured signal, never on a label. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-006 | default | Boundary tool matched to the stack. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-007 | default | C4 container and component views authored in Structurizr DSL. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-008 | default | Derived values are computed, not stored. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-009 | default | Background jobs run on a durable database claim queue. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-010 | default | Identity, money and handover-bound vendors sit behind an adapter the venture owns, with a written exit route. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-011 | default | One database until a second real owner or a volume-asymmetric feed appears, and records never mingle with readings. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-012 | default | Every persisted table names its consumer and its retention plan before it lands. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-013 | default | Proof of harmless change is a byte-stable output canary where output is deterministic. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-014 | default | A decision that closes a door is recorded as a MADR record with two or more considered options. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-015 | default | Builds are reproducible from pinned inputs, and verified by rebuilding. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-016 | preference | Run a Bounded Context Canvas and a Context Mapping pass before declaring a boundary (EV-0098, EV-0099, EV-0100). | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-017 | preference | Create a port only where a second driver or a second device is genuinely plausible. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-018 | preference | Name the specific event pattern in use rather than saying event-driven. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-019 | preference | Raw SQL behind a repository layer, over an ORM, when the data is hot. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-ARCH-020 | preference | Defer domain grouping and per-domain gateways until service count makes them a real problem. | has_server_code | operator_requests_doctrine_review | architecture | 2027-02 |
| DOC-BLM-001 | binding | Money is an integer count of minor units carrying its currency code. | models_money | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-002 | binding | A timestamp that will be compared or advanced carries a zone identifier, not just an offset. | models_time | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-003 | default | Start with no model and earn the next step. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-004 | default | An aggregate boundary is a transactional consistency boundary and nothing else. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-005 | default | A lifecycle with forbidden transitions is an explicit machine, and an illegal transition raises rather than doing nothing quietly. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-006 | default | One time dimension until somebody has actually had to answer a two-dimensional question. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-007 | default | Choose the narrowest temporal type that holds the fact. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-008 | default | Rules stay in code until they change on a different clock from the code. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-009 | default | Conversion between domain money and any external money happens in one adapter. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-010 | default | State-stored until replay is the requirement. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-011 | default | A constraint expressible in the constructor or the type is expressed there. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-012 | default | A state change and its outbound message are committed together or not at all. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-013 | default | A change that publishes or consumes events names which of the four patterns it means. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-014 | preference | Ubiquitous language naming, the ddd-crew canvases and the starter process as thinking aids. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-015 | preference | Event storming as the discovery method. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-016 | preference | Object-shaped or function-shaped domain layers. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-017 | preference | Property-based tests for domain invariants. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BLM-018 | preference | A small purpose-built evaluator over a standards-grade engine. | encodes_domain_rule | operator_requests_doctrine_review | business-logic-modelling | 2027-09 |
| DOC-BMP-001 | binding | The headline price includes every unavoidable charge. | publishes_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-002 | binding | A consumer subscription can be entered knowingly and left easily. | sells_to_consumers | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-003 | binding | Revenue is recognised, never counted at the bank. | bundles_or_discounts | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-004 | binding | Tax thresholds are watched as pricing events. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-005 | default | Open on a named practice with its condition and a revisit date. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-006 | default | A price change is announced with its cause, and the cause is cost or delivered value. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-007 | default | Trial length starts near a week and is tested across the whole funnel. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-008 | default | Retention is reported as a cohort curve, and lifetime value is never revenue over blended churn. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-009 | default | Every commercial number travels with its definition. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-010 | default | A survey-derived price is a bracket, never the decision. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-011 | default | Unit cost is allocated before a margin is claimed. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-012 | default | The repricing trigger is written before it fires. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-013 | default | Payment terms are written down, because they exist either way. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-014 | default | No pattern from the regulator's almost-always-harmful list. | publishes_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-015 | preference | Price endings. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-016 | preference | Tier count and tier names. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-017 | preference | Whether a public price exists at all. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-BMP-018 | preference | Publishing the commercial policy in a public handbook. | sets_a_price | operator_requests_doctrine_review | business-model-pricing | on-change-of:DMCC-Part-4-Chapter-2-commencement |
| DOC-COD-001 | binding | The oracle that judges a change is authored independently of the implementation under test. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-002 | binding | A gate oracle is observed failing before its green result counts as acceptance evidence. | decides_merge | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-003 | binding | Behaviour is pinned before structure moves. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-004 | binding | The error path is handled, never discarded. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-005 | binding | On a published interface, distinguishable failures are declared and versioned. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-006 | binding | A diff-aware machine gate runs before every merge. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-007 | default | Human review is scoped by risk, not applied as a blanket. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-008 | default | Review approves on the health gradient. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-009 | default | Trunk-based flow. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-010 | default | Monorepo per venture until tooling cost forces otherwise. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-011 | default | Refactor when a pending change demands it. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-012 | default | A dumb pipeline before a clever one. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-013 | default | Write the oracle before the implementation wherever the condition can be stated. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-014 | default | Cap the size of a work package, and keep packages of a similar size. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-015 | default | Declare distinguishable failures on internal interfaces too, where more than one caller exists. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-016 | preference | Conventional Commits. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-017 | preference | Naming beyond concept selection. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-018 | preference | Duplication thresholds. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-COD-019 | preference | Test volume. | edits_source | operator_requests_doctrine_review | coding | 2027-02 |
| DOC-DATA-001 | binding | No column that can identify a living person lands in the analytics layer without a recorded lawful basis and a named complaints path. | handles_analytics_identifier | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-002 | binding | The randomisation unit, the primary metric and the stopping rule are written down before traffic starts. | runs_experiment | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-003 | binding | Sample ratio mismatch is checked and reported before any experiment result is read, and a failed check voids the result. | runs_experiment | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-004 | default | Object-action event names, with anything varying per occurrence in a property. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-005 | default | Staging, intermediate and marts layering, one prefix per layer. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-006 | default | Fixed horizon, unless a sequential method is chosen deliberately and written into the stopping rule. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-007 | default | Below the traffic for a properly powered test, do not run one. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-008 | default | One managed warehouse until the working set argues otherwise. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-009 | default | Contracts on public models only. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-010 | default | Use pre-experiment covariates where a stable unit was observed before the test. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-011 | default | Identify by surrogate or hashed key in the analytics layer. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-012 | default | Every published table and every tracked event has one named owner, and its schema, quality rules, freshness expectation and owner live in one document. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-013 | default | A quality gate failure blocks publication. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-014 | default | A fact model declares its grain in words before it declares columns. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-015 | preference | The contract file format. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-016 | preference | The casing convention for event names and columns (EV-0319). | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-017 | preference | The quality tool. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-018 | preference | Whether marts are wide entities or star-shaped, and whether dimensions carry surrogate keys. | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-019 | preference | The dashboard method, as long as one is committed to and the panels answer a named question (EV-0240). | publishes_analytics_table | operator_requests_doctrine_review | data-analytics | 2027-11 |
| DOC-DATA-020 | default | A material compute, capacity or tool-selection claim starts from a correctness-checked baseline measured on a representative workload in a recorded environment. | reads_for_decision | operator_requests_doctrine_review working_set_exceeds_memory has_profiled_numeric_kernel | data-analytics | 2027-02 |
| DOC-DATA-021 | default | Data compute starts at the highest-level sufficient representation and moves to arrays, compiled kernels, alternate engines or distributed execution only when representative measurement proves the current boundary insufficient. | reads_for_decision | requires_tabular_engine_choice crosses_dataframe_array_boundary has_profiled_numeric_kernel working_set_exceeds_memory | data-analytics | 2027-02 |
| DOC-DATAENG-001 | binding | Every hop between two systems states its delivery guarantee, and a sink that is not idempotent or transactional is treated as at-least-once. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-002 | binding | Reprocessing a window replaces a bounded unit or merges on a declared key. Bare append is not a reprocessing strategy. | reprocesses_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-003 | binding | A pipeline over event-time data declares its lateness horizon and where arrivals past it go. Nothing is dropped silently. | processes_event_time_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-004 | default | The processing window comes from the scheduler or from the data, never from the run's own clock, and it is written down with the output. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-005 | default | Backfill is the scheduled pipeline given different dates. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-006 | default | Log-based change capture over polling, where the venture is allowed to read the source's log. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-007 | default | The partition value is derived by the engine from a real column, or in exactly one place in code, and never written by hand at the call site. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-008 | default | One bounded window per run, sized so a single window can be reprocessed inside the schedule interval. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-009 | default | Start in batch. Move a step to streaming only when a named decision cannot wait for the next run. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-010 | default | Every run records its window, the input position it read to, the row counts in and out, and the version of the code that ran. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-011 | default | Rejected and very-late records go to a quarantine table with the reason and the raw payload, not to a log line. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-012 | preference | The table format. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-013 | preference | Whether the merge key is the source's natural key or a hash of it. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-014 | preference | The orchestrator, and whether the window arrives as a CLI flag or a configuration value. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-015 | preference | Compaction cadence and small-file policy, until the read time complains. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DATAENG-016 | preference | Whether quarantine is a table per source or one table with a source column. | ingests_external_data | operator_requests_doctrine_review | data-engineering | 2028-04 |
| DOC-DEL-001 | binding | A check is never weakened to make it pass. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-002 | binding | Every double standing in for a dependency outside the venture's control has a contract suite that runs the same cases against the double and the real implementation, on a stated cadence. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-003 | binding | Flake is a named state with an owner, never hidden behind retries. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-004 | binding | A check named as a gate can actually fail, and states its threshold, its scope and its command. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-005 | binding | Whatever selection is in force, every test runs against every changeset at some point. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-006 | default | Double preference order. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-007 | default | Test timing by change class. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-008 | default | Verification staged by risk and stability. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-009 | default | Doubles for something inside the repository get a contract suite where the boundary crosses a lane or has a second consumer. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-010 | default | A quarantined test expires in thirty days. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-011 | default | Mutation testing runs diff-scoped at review time. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-012 | default | Test selection from the diff and the import graph pre-merge, the remainder post-merge. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-013 | default | Property tests are seeded and replayable in CI. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-014 | default | Contract verification gates deploys for services we own, and monitors services we do not. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-015 | preference | Assert what a user of the interface can see, over internals (EV-0092, EV-0090). | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-016 | preference | Optimise for confidence per test rather than layer ratios (EV-0094), read against the flake cost of bigger tests (EV-0196). | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-017 | preference | Where a published schema exists, generate conformance and negative cases from it rather than writing examples by hand (EV-0189). | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEL-018 | preference | Keep one assertion idea per test, so a failure names itself. | ships_code | operator_requests_doctrine_review | delivery-testing | 2028-02 |
| DOC-DEVOPS-001 | binding | Backwards-incompatible schema change ships as expand, migrate, contract, in separate deploys. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-002 | binding | Recovery is forward-only and the change record says so. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-003 | binding | CI runs a migration linter that fails the build on destructive and backwards-incompatible findings, and the change record names the risk class of every migration in the change. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-004 | binding | Every service carries at least one SLI and SLO as a machine-readable object. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-005 | binding | A restore drill runs on cadence and produces a dated evidence record with a measured elapsed time, a validation query and a result. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-006 | binding | Every incident above the agreed threshold gets an owned postmortem with a deadline, a timeline reconstructed from evidence, and follow-ups filed as tickets. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-007 | binding | Every feature flag declares an owner and an expiry date at creation, and long-term dependencies are taken only on stable observability signals. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-008 | default | Progressive rollout with an automated abort condition for user-facing change. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-009 | default | An error budget policy in the shape the SRE Workbook describes, paraphrased. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-010 | default | Cost allocation tags on every deployed resource. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-011 | default | A golden-path scaffold for new services, registering ownership at creation. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-012 | default | Migrations applied before application start, idempotent, advisory-locked, failing closed. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-013 | default | Policy checks expressed as code where the inputs are already machine-readable. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-014 | preference | Failure drills beyond restore, once restore itself is boring. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-015 | preference | Unit-economics reporting, cost per active user or per job. | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-016 | preference | A periodic platform self-assessment across investment, adoption, interfaces, operations and measurement, treating the improvement list as the output and the level as noise (EV-0205). | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-017 | preference | Automated flag removal that rewrites the syntax tree when a flag reaches its terminal state (EV-0209). | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DEVOPS-018 | preference | Experiment flags governed by asymmetric gating, where goal metrics drive the ship decision and guardrails block only on significant harm (EV-0059). | deploys_to_environment | operator_requests_doctrine_review | devops-reliability | 2027-04 |
| DOC-DISC-001 | binding | Claims about people that a model produced are labelled unverified. | cites_user_claim | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-002 | binding | An experiment fixes its stopping rule, metric, segmentation and sample before data arrives. | runs_experiment | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-003 | default | A discovery record exists and names the decision it unblocks. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-004 | default | The problem is stated without naming the proposed solution. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-005 | default | Every signal names a threshold and a source that exists. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-006 | default | All four risks are retired explicitly, viability in writing. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-007 | default | Every number carries its own provenance. | cites_user_claim | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-008 | default | The record ends in BUILD, TEST or KILL. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-009 | default | Depth is set by reversibility, not by the size of the request. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-010 | default | Elicit outcomes, not features. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-011 | default | Carry more than one candidate solution before committing. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-012 | default | Say whether you are diverging or converging, and separate them in time. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-013 | default | Prefer throughput of cheap reversible tests over accuracy of ranking, where there is traffic to read. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-014 | default | Give a model the structuring job on real human input, never the origination job on invented input. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-015 | default | Reason about the worst case of a small sample, not its average. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-016 | default | Recruit by frame, then by count. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-017 | default | Write acceptance criteria in EARS clause order once the problem is settled. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-018 | preference | The specific numbers. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-019 | preference | RICE, reduced to its confidence multiplier. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-020 | preference | Opportunity solution trees as the drawing. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-021 | preference | Double diamond vocabulary. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DISC-022 | preference | Where the record lives. | proposes_capability | operator_requests_doctrine_review | product-discovery | 2028-06 |
| DOC-DOCS-001 | default | Internal links and anchors resolve, checked in CI, and the check blocks. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-002 | default | A renamed or deleted page leaves a redirect, or every reference to it is updated in the same change. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-003 | default | Every executable snippet either runs in CI or carries an explicit declaration of why it does not. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-004 | binding | Generated reference is verified as regenerated, not hand-edited. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-005 | default | Every user-visible failure names the condition, the caller-relevant identity, and what to do next. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-006 | default | Every repository carries an agent entry file at the conventional root path, and the commands it names are covered by B3. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-007 | default | Use the four documentation forms as a diagnostic, never as a folder layout. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-008 | default | A README answers five questions: what it is, why it exists, how to use it, what state it is in, and where to go next. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-009 | default | A curated changelog with a running Unreleased section. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-010 | default | A failure that suggests a fix declares how confident it is. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-011 | default | External link checking is advisory, never blocking. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-012 | default | Coverage before style. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-013 | default | Prose rules ship as suggestions and are promoted on evidence. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-014 | preference | House prose rules beyond the mechanical subset. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-015 | preference | Which static site generator, or none. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-016 | preference | Whether explanation lives beside reference or apart. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-DOCS-017 | preference | Whether documentation lives with the code or in its own repository. | publishes_docs | operator_requests_doctrine_review | docs-dx | 2028-04 |
| DOC-HOUSE-001 | preference | The container comes from the content, not from the layout. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-002 | preference | Sections open flush left, with the mark in a fixed order. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-003 | preference | Animation stays on the compositor whitelist. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-004 | preference | Motion is judged by moving area and scroll coupling. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-005 | preference | Reading matter never animates and never glows. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-006 | preference | The dark register buys itself back in the smallest type. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-007 | preference | Figures are positioned from data. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-008 | preference | Every number has exactly one home. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-009 | default | Dark-first, single register, with a formal surface ladder. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-010 | default | The full graded light system for a luminous brand, fields only otherwise. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-011 | default | A surface ladder of four to six steps, derived in a perceptually uniform space. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-012 | default | A reading measure at the low end of the usual advice. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-013 | default | Three type roles, three families as the ceiling. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-014 | default | One delegated pointer listener for surface reactivity. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-015 | default | Spend the design budget on the first screen. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-016 | default | Platform hygiene. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-017 | preference | Cyan as the live accent, with the Cherenkov story behind it, and amber as the authority and quote voice. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-018 | preference | The andon line: one accent hairline across the top of the chrome, and a quiet header call to action to pay for it. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-019 | preference | Plate numbering as a mono figure number joined to its caption by a short hairline, and the reticle as four corner ticks around a single calibrated artefact. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-020 | preference | A journal index rather than a card grid on hubs, so two entries read as a curated record rather than a thin feed. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-HOUSE-021 | preference | A colophon rather than a closing call-to-action slab, written fresh per page, and one warm interlude per long read, spent on the thesis moment. | adopts_pattertech_house | operator_requests_doctrine_review | pattertech-house | on-change-of:WCAG-2.2 |
| DOC-IDENT-001 | binding | Deny unless something permitted, and decide at one layer. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-002 | default | The tenant boundary is enforced below the code that serves the request. | serves_multiple_tenants | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-003 | binding | Validate a token's signature, issuer, audience and expiry on every request, using an algorithm fixed by the verifier. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-004 | binding | An identity token is never accepted as an access token. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-005 | binding | A session identifier is never forwarded as a bearer credential. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-006 | binding | Session identifiers come from a cryptographic generator. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-007 | binding | Reissue the session identifier whenever privilege changes. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-008 | binding | Invalidate the server-side session at logout. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-009 | default | The privileged path is named, alarmed and reviewed. | has_privileged_access_path | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-010 | binding | An authorisation change ships with the refusal that proves it. | changes_authorisation_rule | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-011 | default | Start with record ownership plus a small fixed role set; move model only when a real rule cannot be expressed. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-012 | default | Reach for relationships when sharing crosses the ownership tree, and for attributes when the rule depends on facts about the record or the environment. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-013 | default | One decision point, in process, until latency, reuse across services or an audit requirement argues otherwise. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-014 | default | Delegate authentication to a provider rather than storing passwords. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-015 | default | Server-side sessions in cookies for a first-party browser surface; tokens for anything else. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-016 | default | Shared tables with a tenant key and a database-enforced predicate, until a customer's own keys, data location or backup policy buys them a dedicated store. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-017 | default | Both an idle limit and an absolute session limit, inside the graded ranges, with the higher-privilege surface on the shorter one. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-018 | default | A refusal answers the same way everywhere, and the choice between 403 and 404 is made once and written down. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-019 | default | At least two break-glass credentials, neither depending on the identity provider, tested at least every ninety days. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-020 | preference | Which policy engine, if any. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-021 | preference | Whether roles are rows in a table or values in an enum. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-022 | preference | Whether the permission check reads as a decorator, a middleware or a call at the top of a service function, so long as B1 holds and there is one of them. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-023 | preference | Which refusal code, so long as it is one code. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-024 | preference | Session and token lifetimes within the graded ranges. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-IDENT-025 | preference | Whether tenant context travels as a request-scoped variable or an explicit argument, so long as it comes from the credential. | authenticates_people | operator_requests_doctrine_review | identity-access | 2029-02 |
| DOC-LEGAL-001 | default | Every repository declares its own licence. | publishes_code | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-002 | binding | No dependency enters without a recorded licence expression, and absence is a blocking finding. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-003 | default | An OR expression is resolved to one identifier before merge. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-004 | binding | Copyleft entering anything we ship or host takes a written decision before merge, not at release. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-005 | binding | Before any personal data is processed, the notice and the registration are both done. | handles_personal_data | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-006 | default | Inbound work carries a provenance assertion. | accepts_contribution | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-007 | binding | Consequential questions stop here and go to a lawyer. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-008 | default | A three-bucket allowlist keyed on identifiers, with the reason written next to each bucket. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-009 | default | The scanner produces the inventory and a person produces the verdict. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-010 | default | Per-file declaration for anything published. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-011 | default | Permissive outbound unless there is a stated reason to reciprocate. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-012 | default | Vendored code carries its licence text and a provenance note at the moment it is copied. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-013 | default | Ceremony scales with risk to people. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-014 | default | Record the EU market position once, with the reasoning, and re-check it before 2026-09-11 and before 2027-12-11. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-015 | default | The routing loop has a budget, and the run records what it spent. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-016 | default | Nothing is studied until how it was acquired, the terms attached to it and the governing law are written down. | studies_external_source | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-017 | default | The session that reads the source and the lanes that build are different, and the build lanes get the lesson, never the source. | studies_external_source | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-018 | preference | MIT for a small library with no patent exposure, Apache-2.0 where patents matter, with the drafting rating as the tiebreak between otherwise equal candidates (EV-0343). | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-019 | preference | Which scanner. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-020 | preference | The process-certification checklist read once as a prompt about sustainability, which is the only part of it a one-person venture cannot answer trivially (EV-0347). | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-021 | preference | Notice wording and reading level. | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-LEGAL-022 | preference | Whether the repository's own automated health checks watch for the licence file, which reads the repository's actual state rather than its self-description (EV-0069). | adds_dependency | operator_requests_doctrine_review | legal-licensing | 2027-04 |
| DOC-MKTG-001 | binding | The lawful basis is stored with the address, not asserted about the list. | collects_contact_details | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-002 | binding | Every marketing message carries a refusal route that works without a conversation. | sends_marketing_message | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-003 | binding | A refusal suppresses before the next send, mechanically. | sends_marketing_message | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-004 | default | One named growth philosophy per venture, recorded before spend. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-005 | default | A growth plan names its reinvestment step. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-006 | default | Effect comes from a randomised holdout, or the number is labelled. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-007 | default | Attribution distributes a measured total, it never produces one. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-008 | default | A funnel number ships with its definition as configuration. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-009 | default | Every published page has a named human owner and a stated purpose. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-010 | default | Structured data describes what the reader can see. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-011 | default | Crawler directives are a release-gated artefact. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-012 | default | Deliverability is a preflight gate before a first send. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-013 | default | Reach to category non-buyers is the opening bet for a small brand. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-014 | default | Each activity declares a time horizon. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-015 | default | Field performance is a marketing constraint on public surfaces. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-016 | preference | Channel mix, and whether any of it is paid. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-017 | preference | Pull rather than push, as in the public handbook at EV-0095, where the audience has a reading habit. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-018 | preference | Publishing the marketing handbook itself, as at EV-0055 or EV-0095. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-019 | preference | Taking a stance rather than hedging, which is what stops machine-drafted content reading like everyone else's. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-020 | preference | Treating documentation and marketing content as one artefact. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-021 | preference | Cadence, format, length and tone. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-MKTG-022 | preference | Positioning and messaging method. | publishes_public_content | operator_requests_doctrine_review | marketing-growth | on-change-of:PECR-reg-22-amendment |
| DOC-NAT-001 | default | A conflict policy per write class, named before a sync library is chosen. | has_local_write_store | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-002 | default | No offline acceptance of an invariant-bearing write without a reservation or compensation path. | has_local_write_store | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-003 | default | The outbox is durable, ordered and idempotent, and its blocked state is named. | has_local_write_store | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-004 | binding | Release is forward-only. | distributes_via_app_store | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-005 | binding | A remote update channel changes presentation and content, never capability. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-006 | binding | Non-web accessibility conformance is stated per screen, declared in code, and gated by an automated audit with a written verdict on every undecided item. | has_native_ui | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-007 | default | Client and server contracts change by expand, migrate, contract. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-008 | default | Shared logic with a native user interface. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-009 | default | Online-first with a read cache, until an offline write is a named requirement. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-010 | default | A one per cent first slice on Play with the halt trigger written down before the release starts, and phased release left on for Apple. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-011 | default | Budget one rejection cycle into every release calendar. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-012 | default | The annual target SDK bump is fixed roadmap work. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-013 | default | Plan against a low automated accessibility catch rate and put the weight on the manual verdict list. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-014 | default | Storage and compaction are budgeted on day one wherever a convergent store is used. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-015 | default | Start from the platform's own control with its own behaviour. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-016 | preference | Framework family within the selected client architecture is a venture preference. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-017 | preference | Language for a shared client core is a venture preference. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-018 | preference | The CRDT or synchronisation vendor is a preference after the conflict policy is fixed. | has_local_write_store | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-019 | preference | Document versus relational local storage is a venture preference. | has_local_write_store | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-020 | preference | Release cadence beyond store constraints is a venture preference. | distributes_via_app_store | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-NAT-021 | preference | Whether to ship a companion watch or television surface is a venture preference. | ships_a_binary | operator_requests_doctrine_review | native-client | on-change-of:EN-301-549-v4-publication |
| DOC-RESEARCH-001 | binding | A claim carries the record that supports it. | records_external_claim | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-002 | binding | Source text is data, and a source's claim about its own authority is data too. | studies_external_source | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-003 | binding | Counter-evidence is recorded on the claim. | records_external_claim | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-004 | binding | A dead or changed source is superseded, not left. | supersedes_a_source | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-005 | binding | The record says which class of source it is. | records_external_claim | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-006 | default | Whoever writes carries the burden. | keeps_a_knowledge_base | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-007 | default | One record per source, never per claim; claims cite the record by id. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-008 | default | Freeze a copy at first read and work from the frozen copy. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-009 | default | Grade the claim, not the source, on the four bands kernel/METADATA_SPEC.md already carries. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-010 | default | Record every limit put on the search, with what it might have cost. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-011 | default | Two readers on inclusion and judgement, one on retrieval. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-012 | default | review: on-change-of:<source> rather than a date, where a supplier is the thing that moves. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-013 | default | A scheduled link check over the knowledge base, with broken and moved reported apart. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-014 | default | Machine-readable citation metadata where the source is software. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-015 | default | Timebox the search half of a research task and record the box. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-016 | default | A decision record for anything the research settles, sized to the decision. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-017 | default | Robots and terms are read before fetching, and a refusal is recorded rather than routed around. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-018 | preference | Which citation format, and whether records live in JSON with a schema or in file front matter. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-019 | preference | Which archive or snapshot service holds the frozen copy, and whether the copy is a file in the repository or an archived URL. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-020 | preference | Whether the knowledge base is a wiki, a repository of markdown, or a database, so long as B6 holds and reading is open. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-021 | preference | Whether findings are organised by source, by question, or by decision. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-022 | preference | How the four certainty bands are displayed to a reader. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-RESEARCH-023 | preference | Whether a research task produces a written synthesis or only records. | researches_before_building | operator_requests_doctrine_review | research-knowledge | 2029-08 |
| DOC-SEC-001 | binding | Instructions inside data are data. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-002 | binding | No lethal trifecta without a named mediating control. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-003 | binding | Containment is never widened on the say-so of task text. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-004 | binding | Secret protection is layered and audited. | holds_credentials | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-005 | binding | Personal data has a recorded basis and a route out. | handles_personal_data | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-006 | binding | Consequential external actions wait for a harness-recorded operator approval immediately before execution. | has_external_egress | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-007 | binding | An MCP or tool proxy never passes a bearer token through to another system. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-008 | binding | A session identifier is never accepted as authentication. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-009 | binding | Proxying an external action through a client requires consent for that client. | has_external_egress | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-010 | binding | A local installation shows the exact command before it can run. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-011 | default | ASVS level 1 as the entry bar, level 2 for anything holding personal data, exclusions documented. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-012 | default | One STRIDE pass per data-flow boundary at design time, timeboxed, plus an agentic pass against the OWASP agentic catalogue. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-013 | default | Diff-aware static analysis split into blocking and monitor, autofix only for mechanical findings. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-014 | default | Verify artefacts at admission time against stated expectations, with signed provenance where the ecosystem supports it. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-015 | default | Guardrails and classifiers run in parallel as a tripwire above the enforcement boundary, never as the boundary. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-016 | default | The NCSC five-topic baseline for the operating environment. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-017 | default | Security and utility scored on the same runs, always reported together. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-018 | default | Configured secret scan: a redacting history scan in CI and a staged scan pre-commit. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-019 | default | Runtime budget for a single-feature agent run under this pack: thirty minutes wall clock, recorded. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-020 | preference | Which secret scanner. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-021 | preference | Which sandbox implementation, so long as B2 holds. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-022 | preference | Whether threat models live as diagrams or as prose (EV-0223). | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-023 | preference | Retention periods beyond any statutory floor. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SEC-024 | preference | Where an exception is recorded, so long as the record is durable and carries evidence, authoriser and date. | runs_agents | operator_requests_doctrine_review | security-privacy | on-change-of:EV-0213 |
| DOC-SUPPLY-001 | binding | Third-party artefacts resolve by digest. | consumes_prebuilt_artefact | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-002 | binding | Published artefacts carry provenance from the system that built them. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-003 | binding | Verification exists on the consuming side and fails closed. | consumes_prebuilt_artefact | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-004 | binding | The publish path is separate, and nothing untrusted shares it. | builds_release_artefact | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-005 | default | A cooldown window before adopting a newly published version, with security fixes deliberately exempted. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-006 | default | Generate the bill of materials from the lock file, not by scanning a built tree. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-007 | default | Record what the bill of materials could not see. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-008 | default | Short-lived signing identity where the ecosystem supports it. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-009 | default | Check the release path for discontinuity at admission. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-010 | default | Reproducibility where the toolchain gives it cheaply. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-011 | default | Read the repository, not its self-description, before depending on it. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-012 | default | One release path, used for every release, including the urgent one. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-013 | preference | Which bill-of-materials format. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-014 | preference | Where attestations are stored, so long as a consumer can find them from the artefact digest alone. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-015 | preference | Whether the cooldown sits in the install client or the update bot. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-016 | preference | How long the window is, beyond being non-zero and written down. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPLY-017 | preference | Whether release notes list dependency changes, or a generated diff does. | publishes_code | operator_requests_doctrine_review | supply-chain-integrity | 2027-06 |
| DOC-SUPPORT-001 | default | A customer-facing message never reports a bypassed check as passing. | has_customer_visible_incident | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-002 | binding | A support inbox is a personal-data store and is run as one. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-003 | default | Nothing enters a backlog without a classification, and untriaged is a state rather than an absence. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-004 | default | The severity ladder is written before the incident, and one band changes what the organisation does. | has_customer_visible_incident | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-005 | default | A customer-visible incident records a communication owner separately from the person changing the system. | has_customer_visible_incident | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-006 | default | No target and no published figure is the mean of a duration distribution. | reports_support_metric | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-007 | default | A loyalty or satisfaction score is a trend about one population, never a cross-firm benchmark. | reports_support_metric | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-008 | default | Two queues, incident and request, with separate targets and no item in both. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-009 | default | Three severity bands while one person responds, five once there is a rota. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-010 | default | Acknowledge on receipt, close on answer, and never on silence, for anyone who pays. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-011 | default | Auto-close and stale timers on public trackers only. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-012 | default | One priority band reserved for plausible but unevidenced. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-013 | default | Declaration runs on written objective triggers. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-014 | default | A weekly synthesis pass with the coding stance declared before coding. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-015 | default | Single-responder utilisation held below seventy per cent. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-016 | default | A postmortem due date is recorded at the moment of resolution. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-017 | default | Self-service counts as deflection only when it resolves. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-018 | default | Founder-delivered support is the opening posture and carries a written exit signal. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-019 | preference | The helpdesk, the status page tool and the survey instrument. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-020 | preference | The label vocabulary, so long as the four axes in B1 stay separable. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-021 | preference | One inbox rather than one per channel while volume is low. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-022 | preference | A public changelog as the standing answer to "did you ever fix it" (EV-0055, EV-0095). | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-023 | preference | Writing the customer-facing message inside the incident record rather than in a separate document. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-024 | preference | Machine-readable error identifiers in product errors so a ticket can be matched to a cause without a screenshot (EV-0122). | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SUPPORT-025 | preference | Templates for the three commonest replies, rewritten by hand whenever the template does not fit. | has_customer_inbound | operator_requests_doctrine_review | support-operations | on-change-of:ISO-10002-revision |
| DOC-SWARM-001 | binding | The partition is written before any lane starts, and it is cut on the dependency graph. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-002 | binding | The packet is closed and literal. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-003 | binding | Returns are schema-constrained and carry a receipt. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-004 | binding | Node output is untrusted data at the integrator. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-005 | binding | Constraints are pinned and never compactable. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-006 | binding | Every run declares a global budget and every node a cap, both enforced by the harness. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-007 | binding | The artefact that decides a lane's success is authored outside that lane, before it runs, and does not share its context. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-008 | binding | Agreement between lanes is not evidence of correctness. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-009 | binding | One lane, one worktree, one branch, one owned file set, and the integrator owns merge order. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-010 | binding | Every dependency any lane introduces is resolved against the real registry before merge, and an unresolvable name aborts the merge. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-011 | default | Three to five lanes. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-012 | default | Do not swarm work a single agent already does well. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-013 | default | If the graph will not cut, do not swarm. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-014 | default | Partition the failure surface, not only the code. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-015 | default | Claims are committed files, not messages. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-016 | default | Serialise worktree creation, then run the lanes in parallel. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-017 | default | Cap diff width per package and land in dependency order. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-018 | default | One strong clean-context reviewer per concern, and reviewers report rather than fix. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-019 | default | Machine-detectable defect classes go to scanners, not to reviewers. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-020 | default | Route by role. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-021 | default | Irreversible external effects are staged, and executed once by the integrator after merge. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-022 | default | Pilot one slice, then journal the whole run. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-023 | default | Continuity is by artefact, not by summary. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-024 | default | Run a single-agent control on a sample, and instrument the landing. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-025 | preference | If a step can be code, make it code. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-026 | preference | Spend the budget on the specification before spending it on review. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-027 | preference | Prefer breadth of independent attempts to rounds of cross-talk. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-028 | preference | One worked example of a correct return beats five rules about edge cases in a packet. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-SWARM-029 | preference | Name nodes by their artefact, so a trace reads as a work breakdown rather than a call stack. | fans_work_across_lanes | operator_requests_doctrine_review | agentic-swarm | on-change-of:agent-harness-major-release |
| DOC-UIUX-001 | binding | Conformance is stated as named criteria, not confidence. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-002 | binding | The six cheap failure classes are gated individually. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-003 | binding | Every interactive component maps to an APG pattern or documents its deviation with a behaviour test. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-004 | default | Do not add a script that claims to repair accessibility at runtime. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-005 | binding | Do not infer assistive-technology use without the person's consent. | handles_personal_data | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-006 | binding | Tokens are defined once and generated; derived files are never hand-edited. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-007 | default | The claim is evidenced by a real-browser run with pinned tags, plus a written verdict on every incomplete. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-008 | default | Every component declares its interaction states. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-009 | default | One named philosophy per surface, recorded before pixel work. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-010 | default | Headless behaviour layer plus own visual layer. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-011 | default | Field performance is a design constraint on public surfaces. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-012 | default | Assume automated accessibility coverage of roughly a third. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-013 | default | On a native platform, the system control with system behaviour is the starting point. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-014 | default | Honour reduced-motion preferences globally. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-015 | default | Content stays visible without JavaScript. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-016 | default | A dashboard commits to a method. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-017 | preference | A small component surface over a large one (EV-0239). | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-018 | preference | Graded browser compatibility over binary support (EV-0062, EV-0063). | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-019 | preference | An evidence gate before a component is admitted to a shared kit (EV-0103). | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-020 | preference | Written context carried inside a dashboard rather than in a wiki (EV-0240). | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-021 | preference | A reading grid with one default measure and opt-in wider bleeds, so a component is correct wherever it is dropped. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-022 | preference | One tokenised easing curve per project. | has_user_interface | operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2 |
| DOC-UIUX-023 | default | Use meaningful native HTML semantics and behaviour first; a custom interaction names the missing native capability and proves its keyboard, focus and assistive-technology behaviour. | has_user_interface | requires_non_semantic_custom_control operator_requests_doctrine_review | ui-ux | on-change-of:WCAG-2.2-or-WAI-ARIA-APG |
| DOC-WRIT-001 | binding | No user-facing sentence is assembled by string concatenation. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-002 | binding | Plural and gender selection resolves per locale through CLDR categories, never from the English pair. | ships_second_locale | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-003 | binding | Every blocking error identifies what failed and states the required input or the next action. | has_forms | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-004 | binding | Licence obligations on external style guidance are recorded before the guidance informs a house guide. | reuses_external_style_guidance | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-005 | default | A pseudo-locale build passes before any string reaches a translator. | ships_second_locale | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-006 | default | An error renders adjacent to its cause, does not fire before the person has finished, and never destroys what they typed. | has_forms | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-007 | default | Human error text and machine error bodies are separate artefacts. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-008 | default | One banned-and-preferred term list runs in CI over user-facing strings and documentation, and only one prose linter exists in the repository. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-009 | default | Prose in this repository follows the voice law. | writes_eos_internal_prose | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-010 | default | No readability formula gates a merge, a release or a review. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-011 | default | Front-load the answer, lead with the verb, one instruction per step. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-012 | default | Literal language in anything the reader must act on. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-013 | default | Write for the lowest literacy in the audience, not the median. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-014 | default | Layout slack sized for two to three times expansion on strings under ten characters. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-015 | default | Sentence case for headings and interface labels. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-016 | default | A comprehension claim is tested with real readers before it is made. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-017 | default | Venture documentation follows the plain-language defaults above. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-018 | preference | Report a readability score at all. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-019 | preference | Tone varying with the reader's emotional state, celebration copy reading differently from a failed payment (EV-0448). | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-020 | preference | Serial comma, spacing after a full stop, contraction density. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-021 | preference | Writing about people treated as a first-class section of a style guide rather than an appendix (EV-0448). | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |
| DOC-WRIT-022 | preference | A short house term list over a full termbase, until the term list is demonstrably not enough. | writes_user_facing_text | operator_requests_doctrine_review | writing-content | on-change-of:CLDR-plural-categories |

516 live Doctrine atoms.
