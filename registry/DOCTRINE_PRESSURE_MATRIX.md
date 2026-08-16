---
summary: Derived estate view of Doctrine relations and Wargame pressure coverage
type: registry
tags: [eos, wargame]
status: active
review_by: 2027-02
derived: true
---

# DOCTRINE_PRESSURE_MATRIX

Derived from Doctrine, DREL and Wargame metadata. It is a view, not
a second relation registry.

## Typed relations

| id | owner | relation | target | conditions | status | Wargame | fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DREL-AGENT-001 | DOC-AGENT-008 | supports | DOC-SWARM-012 | agent_coordination_cost_is_material | covered | WG-AGENT-001 | Run one bounded agent with an external oracle until a decomposable graph and measured control justify coordination. |
| DREL-AIML-001 | DOC-AIML-003 | depends_on | DOC-SEC-005 | model_residency_or_hosting_is_constrained | covered | WG-AIML-001 | Keep protected data on the proved route and retain a deterministic or human fallback until locality, provider and outage constraints are tested. |
| DREL-AIML-002 | DOC-AGENT-003 | supports | DOC-AIML-004 | evaluation_oracle_is_undecided | covered | WG-AIML-004 | Use deterministic external truth where the condition is decidable; otherwise calibrate a human or model judge before its score gates work. |
| DREL-ARCH-001 | DOC-ARCH-011 | tensions_with | DOC-DATA-008 | requires_storage_engine_choice | covered | WG-ARCH-010 | Keep one proved store and isolate the new access pattern behind a rebuildable seam until a representative trace and recovery test justify another engine. |
| DREL-ARCH-002 | DOC-ARCH-010 | depends_on | DOC-SUPPLY-009 | managed_service_changes_exit_or_access | covered | WG-ARCH-012 | Keep capability ownership and the smallest proved exit route with the venture until provider diagnosis, export and restoration are demonstrated. |
| DREL-ARCH-003 | DOC-ARCH-004 | depends_on | DOC-ARCH-005 | requires_independent_deployability | covered | WG-ARCH-013 | Keep one deployable with enforced module seams until ownership, release, isolation or capacity evidence earns one split. |
| DREL-DEL-001 | DOC-SUPPLY-012 | supports | DOC-DEL-001 | incident_needs_gate_exception | covered | WG-DEL-008 | Use the normal release path; if delay causes greater active harm, retain non-waivable checks, known-good state, impact observation and rollback. |
| DREL-DEL-002 | DOC-DEL-006 | depends_on | DOC-DEL-002 | test_fidelity_changes_outcome | covered | WG-DEL-005 | Use the highest-fidelity affordable boundary and prove any double against the same contract and an independent oracle. |
| DREL-HOUSE-001 | DOC-HOUSE-004 | tensions_with | DOC-UIUX-014 | house_style_costs_access_or_performance | covered | WG-UIUX-005 | Remove or reduce the house motion until reduced-motion behaviour and the target-device budget pass. |
| DREL-HOUSE-002 | DOC-HOUSE-015 | tensions_with | DOC-UIUX-011 | house_style_costs_access_or_performance | covered | WG-UIUX-003 | Keep useful content and measured performance; remove house styling that consumes either budget. |
| DREL-NAT-001 | DOC-NAT-009 | supports | DOC-NAT-002 | requires_offline_or_hybrid_consistency | covered | WG-ARCH-011 | Remain online-first and reject invariant-bearing offline writes until conflict, reservation or compensation behaviour is proved. |
| DREL-OPS-001 | DOC-SUPPLY-003 | tensions_with | DOC-DEVOPS-004 | integrity_floor_reduces_availability | covered | WG-DEVOPS-006 | Fail closed for privacy, authorisation, integrity and approval; degrade only a journey that preserves those properties and tells the truth. |
| DREL-OPS-002 | DOC-DEVOPS-004 | tensions_with | DOC-SEC-004 | observability_collects_sensitive_data | covered | WG-DEVOPS-007 | Collect the minimum redacted signal that diagnoses the named journey and reject secret-bearing telemetry. |
| DREL-OPS-003 | DOC-DEVOPS-004 | tensions_with | DOC-SEC-005 | observability_collects_sensitive_data | covered | WG-DEVOPS-007 | Minimise and bound telemetry before collection; do not treat later redaction as the primary privacy control. |
| DREL-RESEARCH-001 | DOC-RESEARCH-003 | supports | DOC-RESEARCH-016 | local_exception_may_generalise | active |  | Keep the departure local until two argued venture rulings overlap in applicability and survive Doctrine admission review. |
| DREL-SUPPLY-001 | DOC-SUPPLY-002 | depends_on | DOC-SEC-014 | producer_trust_is_unproved | covered | WG-SUPPLY-001 | Treat provenance as identity and build-path evidence, then verify producer and policy trust separately before admission. |
| DREL-SUPPLY-002 | DOC-SUPPLY-005 | tensions_with | DOC-DEVOPS-008 | dependency_update_changes_known_good | covered | WG-SUPPLY-003 | Keep the known-good deployment during routine freshness pressure; use the proved security exception, staged observation and rollback when delay is riskier. |
| DREL-UIUX-001 | DOC-UIUX-009 | depends_on | DOC-DISC-016 | serves_novice_and_expert_users | covered | WG-UIUX-003 | Choose the surface philosophy from representative novice and expert task evidence, not an estate-wide density preference. |
| DREL-UIUX-002 | DOC-UIUX-015 | tensions_with | DOC-UIUX-003 | requires_non_semantic_custom_control | covered | WG-UIUX-002 | Keep a meaningful native control or content route until the custom interaction proves equivalent semantics and behaviour. |

## Pressure coverage

The accepted backlog is canonical. Wargame engagement metadata and
relation conditions are validated against each row.

| case | named pressure | predicate | consequence | disposition | covering Wargames | relations | fallback or reopen trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Polars/pandas/DuckDB/Spark | requires_tabular_engine_choice | routine | new-wargame | WG-DATA-001 |  | Keep the current proved engine and run one representative query or pipeline before changing it. |
| 2 | dataframe-to-array or solver boundary | crosses_dataframe_array_boundary | high | new-wargame | WG-DATA-002 |  | Keep the higher-level representation until dtype, layout, copy, memory and result tolerance are proved at the boundary. |
| 3 | NumPy/Numba/native/GPU | has_profiled_numeric_kernel | routine | new-wargame | WG-DATA-003 |  | Retain the correctness-checked baseline until compile-inclusive and steady-state measurements justify one promotion. |
| 4 | eager/lazy/streaming/out-of-core and reproducibility | working_set_exceeds_memory | high | new-wargame | WG-DATA-001 |  | Use the simplest repeatable plan that fits; record spill, ordering, peak memory and output agreement before promotion. |
| 5 | static/SSR/CSR/islands/PWA/native | requires_rendering_mode_choice | routine | new-wargame | WG-UIUX-001 |  | Keep meaningful content available without client execution and add runtime only for a measured interaction or offline need. |
| 6 | novice versus expert density | serves_novice_and_expert_users | routine | relation-only | WG-UIUX-003 | DREL-UIUX-001 | Choose density from representative novice and expert task evidence for this surface. |
| 7 | semantic DOM/ARIA versus canvas/custom controls | requires_non_semantic_custom_control | high | new-wargame | WG-UIUX-002 | DREL-UIUX-002 | Keep a meaningful native control or content route until equivalent semantics and interaction behaviour are proved. |
| 8 | house style and motion versus audience, accessibility and performance | house_style_costs_access_or_performance | high | relation-only | WG-UIUX-003 WG-UIUX-005 | DREL-HOUSE-001 DREL-HOUSE-002 | Audience, accessibility and measured target-device performance override optional house styling. |
| 9 | modular monolith versus services | requires_independent_deployability | high | existing-wargame-refreshed | WG-ARCH-001 WG-ARCH-013 | DREL-ARCH-003 | Keep one deployable with enforced module seams until a measured ownership, release, isolation or capacity signal earns a split. |
| 10 | synchronous versus queue/event/stream | requires_asynchronous_delivery | high | new-wargame | WG-ARCH-009 |  | Keep the call synchronous unless waiting is unsafe; when asynchronous, make acknowledgement, retry, ordering and replay explicit. |
| 11 | storage-engine selection | requires_storage_engine_choice | high | new-wargame | WG-ARCH-010 | DREL-ARCH-001 | Keep one proved store until a representative access trace and recovery path justify another engine. |
| 12 | local/cloud/hybrid/offline and consistency | requires_offline_or_hybrid_consistency | high | new-wargame | WG-ARCH-011 | DREL-NAT-001 | Remain online-first and reject invariant-bearing offline writes until conflict and recovery behaviour are proved. |
| 13 | spike versus hardened vertical slice | riskiest_assumption_is_unproved | routine | existing-wargame-refreshed | WG-DEL-007 |  | Use the cheapest representative spike with a named deletion or hardening boundary. |
| 14 | doubles/sandbox/live and oracle independence | test_fidelity_changes_outcome | high | existing-wargame-refreshed | WG-DEL-005 WG-DEL-006 | DREL-DEL-002 | Use the highest-fidelity affordable boundary and prove a double against the real contract with an independent oracle. |
| 15 | incident hotfix versus normal gates | incident_needs_gate_exception | high | new-wargame | WG-DEL-008 | DREL-DEL-001 | Use the normal path unless active user harm justifies a bounded route that retains non-waivable checks and rollback. |
| 16 | build/buy/managed service versus portability and incident access | managed_service_changes_exit_or_access | high | new-wargame | WG-ARCH-012 | DREL-ARCH-002 | Retain the smallest owned interface and proved export, diagnosis and recovery route. |
| 17 | fail closed versus honest degradation | integrity_floor_reduces_availability | high | new-wargame | WG-DEVOPS-006 | DREL-OPS-001 | Fail closed for protected properties and degrade only a truthful journey that preserves them. |
| 18 | observability versus privacy | observability_collects_sensitive_data | high | new-wargame | WG-DEVOPS-007 | DREL-OPS-002 DREL-OPS-003 | Collect the minimum redacted signal that diagnoses the named journey and reject secret or cross-tenant telemetry. |
| 19 | provenance/SBOM versus producer trust | producer_trust_is_unproved | high | existing-wargame-refreshed | WG-SUPPLY-001 | DREL-SUPPLY-001 | Verify producer and policy trust separately from provenance and inventory evidence. |
| 20 | dependency freshness versus known-good deployment | dependency_update_changes_known_good | high | existing-wargame-refreshed | WG-DEVOPS-002 WG-SUPPLY-003 | DREL-SUPPLY-002 | Keep known-good during routine pressure and use a proved staged security exception when delay is riskier. |
| 21 | deterministic workflow/single agent/swarm | agent_coordination_cost_is_material | routine | existing-wargame-refreshed | WG-AGENT-001 WG-SWARM-001 | DREL-AGENT-001 | Start with one bounded agent and an external oracle; add the smallest measured decomposition. |
| 22 | local/hosted/hybrid models | model_residency_or_hosting_is_constrained | high | new-wargame | WG-AIML-001 | DREL-AIML-001 | Keep protected data on the proved route and retain a deterministic or human outage fallback. |
| 23 | deterministic/human/model judges | evaluation_oracle_is_undecided | high | existing-wargame-refreshed | WG-AIML-004 WG-DEL-006 | DREL-AIML-002 | Use deterministic external truth where possible; calibrate any human or model judge before it gates work. |
| 24 | golden path versus autonomy | golden_path_needs_escape | routine | rejected |  |  | on-change-of:estate-gaining-a-second-team |
| 25 | local exception versus doctrine promotion | local_exception_may_generalise | high | relation-only |  | DREL-RESEARCH-001 | Keep the exception venture-local until two argued rulings overlap and an accepted Doctrine review changes estate scope. |

## Uncovered Doctrine challenge triggers

None.
