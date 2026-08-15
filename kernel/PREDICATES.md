---
summary: The controlled vocabulary of pack activation predicates, grouped by subject so two names for one fact sit next to each other, each with what settles it
type: kernel
tags: [eos]
---

# PREDICATES

Every name a pack, Doctrine or Wargame may put in `applies_when`,
`challenge_triggers` or `engages_when`. Checks S021 and S022 hold those
surfaces to this file, so none can invent a predicate without adding it
here first.

The point is not bookkeeping. A predicate is a fact, and two packs
naming one fact differently split the estate: a venture recording one
spelling loads one pack and silently misses the other, which
`python -m tools.eos activate` will show you and nothing else will. That
happened. `security-privacy` declared `handles_personal_data` and
`legal-licensing` declared `processes_personal_data`, which are one
answer to interview question 9, and both packs defined it in almost the
same words. ADR-0010 merged them.

So the rows below are grouped by subject rather than by pack. Two names
for one fact land next to each other, where somebody adding a third will
see them.

## Venture facts and task facts

The third column says what settles a predicate, and it takes one of four
shapes.

A number is a question in `inception/INTERVIEW.md`. Those are **venture
facts**: true of the venture itself, settled once at Session 0, and the
same tomorrow. They are what `eos activate --facts` is for, and what a
compiled seed's pack walk rests on.

`task` means a **task fact**: true of a piece of work rather than of the
venture. Whether this change edits source, adds a dependency or renames
a documented page is not knowable at Session 0 and is not stable
afterwards. Those are settled per task, from the record or the diff,
which is what `eos context` reads.

Of the 128 predicates here, 67 are venture facts, 33 are task facts, one
is always true, two are explicit operator requests and 25 are pressure
facts. That split is worth knowing before anyone builds a
Session 0 flow expecting to settle all of them: it cannot, and a flow
that pretends otherwise asks the operator questions that have no answer
yet. A pack activating only on task facts does not belong in a venture's
compiled walk at all; it activates when the work arrives.

`always` means true of every governed venture by construction, so
nothing has to settle it.

`operator` means an explicit request in the current session. It defaults
false and is never inferred from prose.

`pressure` means a Wargame engagement fact. It is settled when that fork
enters scope: at Session 0 if a confirmed workstream already requires the
choice, otherwise on the task that reaches it. Unknown high-consequence
pressure is asked or included; unknown routine pressure remains a
candidate.

## How to add one

Add the row here, in the group its subject belongs to, before putting it
in a pack. Read the group first. If an existing predicate is already
true in the same circumstances, use it and let two packs share it, which
is normal and is what `handles_personal_data` now does. Sharing a
predicate is not a coupling between packs; it is two packs agreeing
about the world.

A predicate should be a fact somebody can answer yes or no about, not a
judgement about the work. `has_database` is a fact.
`needs_careful_design` is not.

An `applies_when` list names alternative entrances to the same surface: one
true fact makes it applicable, all false facts make it inapplicable, and no
true fact with at least one unknown keeps it unknown. `engages_when` uses the
same any-of rule for decision pressure. A rule that genuinely needs two facts
together gets one named compound predicate whose settling question proves
both; a list does not silently mean `and`.

Every row needs all four cells, including what settles it. A predicate
nobody can settle activates nothing and cannot be tested.

Retired names are listed at the end and must not be reused. A retired
spelling silently activates nothing, which is the expensive direction.

## Data about people

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `handles_personal_data` | security-privacy, legal-licensing | 9 | the system collects, stores or transmits data about identifiable people |
| `handles_analytics_identifier` | data-analytics | 9 | analytics carries an identifier that can be tied back to a person or device |
| `collects_contact_details` | marketing-growth | 9 | the venture gathers an address, number or handle it can contact somebody on |

## Secrets and reach outside itself

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `holds_credentials` | security-privacy | 14 | the repository or its runtime holds a secret, key or token |
| `has_external_egress` | security-privacy | 17 | code can reach the network beyond the venture |
| `consumes_external_api` | api-integration | 17 | the venture calls somebody else's service |
| `receives_webhooks` | api-integration | 17 | somebody else's service calls in |
| `exposes_service_boundary` | api-integration | 5 | the venture offers an interface another system calls |
| `publishes_events` | api-integration | 5 | the venture emits events others consume |
| `has_vendor_holding_identity_or_money` | architecture | 17 | a third party holds the venture's identities or its money |
| `studies_external_source` | legal-licensing | task | work reads a product, repository, game or document we do not own, to learn from it |

## Who may do what

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `authenticates_people` | identity-access | 6 | a person proves who they are before the venture acts for them, whether it checks the credential itself or delegates it |
| `serves_multiple_tenants` | identity-access | 2 | one running system holds data for more than one customer organisation, and one must not see another's |
| `has_privileged_access_path` | identity-access | 11 | an account or route can reach data or actions it does not own: administrator, support impersonation, break-glass |
| `changes_authorisation_rule` | identity-access | task | the work adds or changes a permission, a role, a policy or a tenant scope |

## Code and how it changes

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `edits_source` | coding | task | the work changes source code |
| `reviews_change` | coding | task | somebody reviews a change before it lands |
| `decides_merge` | coding | task | somebody decides whether a change merges |
| `ships_code` | delivery-testing | task | code reaches somebody other than its author |
| `has_test_suite` | delivery-testing | 18 | the venture has automated tests |
| `adds_dependency` | legal-licensing | task | the work brings in third-party code |
| `vendors_code` | legal-licensing | task | third-party code is copied into the tree |
| `publishes_code` | legal-licensing | 5 | the venture's code is made available to others |
| `accepts_contribution` | legal-licensing | 11 | code arrives from someone outside the venture |
| `builds_release_artefact` | supply-chain-integrity | task | the work produces something meant to be installed or run off the machine that built it: a package, an image, an installer, a signed bundle |
| `consumes_prebuilt_artefact` | supply-chain-integrity | task | the work brings in a binary, image, archive or model file nobody here built from source they can read. `adds_dependency` is about code a reader can open; this is about what they cannot |

## Shape of the system

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `has_server_code` | architecture | 6 | something runs that is not the user's own device |
| `has_multiple_modules` | architecture | 18 | the tree has parts that could be built or deployed apart |
| `has_database` | architecture | 6 | the venture stores structured data it queries |
| `has_cross_language_contract` | architecture | 18 | two languages agree on a shape at a boundary |
| `encodes_domain_rule` | business-logic-modelling | 18 | a rule of the business is written in code |
| `models_money` | business-logic-modelling | 7 | amounts of money are represented and arithmetic is done on them |
| `models_time` | business-logic-modelling | 18 | dates, durations or time zones carry meaning |
| `has_lifecycle_state` | business-logic-modelling | 18 | a thing moves through named states |

## Running it

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `deploys_to_environment` | devops-reliability | 10 | the venture is put somewhere it runs |
| `stores_persistent_data` | devops-reliability | 6 | state outlives a single run and matters if lost |
| `runs_schema_migrations` | devops-reliability | task | the shape of stored data changes over time |
| `hosts_service` | legal-licensing | 5 | people reach the software over a network |

## Moving and reprocessing data

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `ingests_external_data` | data-engineering | 17 | the venture takes data in from a system it does not own and lands it somewhere of its own. `consumes_external_api` is calling somebody's service; this is keeping what comes back |
| `runs_scheduled_pipeline` | data-engineering | 18 | data processing runs on a schedule or a trigger rather than in response to a user request |
| `processes_event_time_data` | data-engineering | 18 | records carry a time at which the thing happened, distinct from the time they arrived |
| `reprocesses_data` | data-engineering | task | the work reruns a period already processed: a retry, a correction or a backfill |

## Agents, models and lanes

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `runs_agents` | security-privacy | always | an agent runs tools in the repository. True of every governed venture by construction, because the seed exists so agents can work in it |
| `builds_agent_workflow` | agentic-development | 18 | the venture builds something that drives an agent |
| `orchestrates_multiple_agents` | agentic-development | 18 | more than one agent runs against shared work |
| `designs_agent_harness` | agentic-development | 18 | the venture builds the scaffolding an agent runs inside |
| `defines_agent_tools` | agentic-development | 18 | the venture defines the tools an agent may call |
| `fans_work_across_lanes` | agentic-swarm | task | work is split across lanes running at once |
| `cuts_a_build_partition` | agentic-swarm | task | somebody divides a build into disjoint paths |
| `integrates_parallel_lanes` | agentic-swarm | task | somebody merges what parallel lanes produced |
| `writes_a_lane_packet` | agentic-swarm | task | a lane is given its brief in writing |
| `calls_a_model` | ai-ml-llm | 18 | the venture calls a language or other model at runtime |
| `changes_prompt_or_model` | ai-ml-llm | task | a prompt or a model identifier changes |
| `builds_retrieval` | ai-ml-llm | 18 | the venture retrieves documents to put in front of a model |
| `evaluates_model_output` | ai-ml-llm | task | model output is judged against something |
| `ships_model_output` | ai-ml-llm | 5 | model output reaches a person or another system |

## What a person sees and touches

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `has_user_interface` | ui-ux | 5 | a person interacts with the venture through a surface it draws |
| `has_native_ui` | native-client | 5 | the interface is drawn by a native toolkit rather than a browser |
| `has_forms` | writing-content | 5 | a person types into fields the venture validates |
| `ships_a_binary` | native-client | 5 | the venture distributes something that is installed |
| `has_local_write_store` | native-client | 6 | the device holds writes of its own |
| `distributes_via_app_store` | native-client | 17 | distribution goes through a store with its own rules |

## Words

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `writes_user_facing_text` | writing-content | task | text the venture's users read is written or changed |
| `writes_venture_documentation` | writing-content | task | documentation about the venture is written |
| `writes_eos_internal_prose` | writing-content | task | prose inside the EOS itself is written |
| `reuses_external_style_guidance` | writing-content | task | style guidance from outside is carried into the venture |
| `ships_second_locale` | writing-content | 5 | the venture is offered in more than one language |
| `publishes_docs` | docs-dx | 5 | documentation is published to readers |
| `documents_executable_surface` | docs-dx | task | documentation describes something a reader will run |
| `emits_user_visible_failure` | docs-dx | task | the venture shows a person a failure |
| `renames_or_deletes_documented_page` | docs-dx | task | a documented page moves or goes |
| `adopts_pattertech_house` | pattertech-house | 1 | the venture adopts PatterTech's house style |

## Money and the market

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `sets_a_price` | business-model-pricing | 7 | somebody decides what to charge |
| `publishes_a_price` | business-model-pricing | 7 | a price is stated publicly |
| `sells_to_consumers` | business-model-pricing | 2 | buyers are individuals rather than organisations |
| `sells_by_subscription` | business-model-pricing | 2 | payment recurs |
| `sells_to_public_sector` | business-model-pricing | 2 | buyers are public bodies |
| `bundles_or_discounts` | business-model-pricing | 7 | price varies by package or by deal |
| `reports_commercial_metrics` | business-model-pricing | 12 | commercial performance is reported |
| `has_paying_customers` | support-operations | 2 | somebody has paid and expects the thing to work |
| `plans_growth_spend` | marketing-growth | 8 | money is committed to reaching more people |

## Reaching people

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `publishes_public_content` | marketing-growth | 5 | the venture publishes content anyone can read |
| `sends_marketing_message` | marketing-growth | 17 | the venture sends a message somebody did not ask for individually |
| `reports_channel_effect` | marketing-growth | 12 | the effect of a channel is measured and reported |
| `runs_public_tracker` | support-operations | 5 | issues or incidents are tracked where users can see them |

## Evidence and deciding

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `publishes_analytics_table` | data-analytics | 5 | a table others read for decisions is published |
| `defines_events` | data-analytics | 18 | the venture defines what gets recorded when something happens |
| `runs_experiment` | data-analytics, product-discovery | task | a change is tried against a comparison |
| `reads_for_decision` | data-analytics | task | somebody reads data to decide something |
| `proposes_capability` | product-discovery | task | somebody proposes the venture should do a new thing |
| `prioritises_work` | product-discovery | task | somebody decides what comes first |
| `cites_user_claim` | product-discovery | task | a claim about users is used as evidence |
| `writes_acceptance_criteria` | product-discovery | task | somebody writes down what done means |
| `researches_before_building` | research-knowledge | 18 | facts about something outside the venture's control have to be established before it can build on them, so research is a material workstream |
| `keeps_a_knowledge_base` | research-knowledge | 18 | the venture maintains written findings that somebody other than their author reads in order to decide something |
| `records_external_claim` | research-knowledge | task | the work writes a claim taken from outside the venture somewhere durable that others will read |
| `supersedes_a_source` | research-knowledge | task | a source something already rests on has changed version, moved, or stopped resolving |

## Customers and incidents

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `has_customer_inbound` | support-operations | 2 | people contact the venture unprompted |
| `has_customer_visible_incident` | support-operations | 10 | a failure was visible to somebody outside the venture |
| `reports_support_metric` | support-operations | 12 | support performance is reported |
| `single_responder` | support-operations | 11 | one person carries the response |

## Doctrine and Wargame pressure

These rows engage a decision procedure; they do not decide its outcome.
The two operator rows default false. A pressure row stays unknown until the
fork enters scope, then the operator or task evidence records true or false.

| predicate | packs | settled by | true when |
| --- | --- | --- | --- |
| `operator_requests_doctrine_review` | all | operator | the operator explicitly asks to challenge or review a standing Doctrine |
| `operator_requests_wargame` | all | operator | the operator explicitly asks to run a named Wargame despite no matched pressure |
| `requires_tabular_engine_choice` | data-analytics, data-engineering | pressure | the work must choose between dataframe, analytical SQL or distributed tabular engines |
| `crosses_dataframe_array_boundary` | data-analytics, ai-ml-llm | pressure | tabular data must cross into an array, optimiser, solver or model interface |
| `has_profiled_numeric_kernel` | data-analytics, ai-ml-llm | pressure | measurement identifies a numeric kernel whose implementation materially affects the target |
| `working_set_exceeds_memory` | data-analytics, data-engineering | pressure | the measured working set does not fit the memory available to one process |
| `requires_rendering_mode_choice` | ui-ux, native-client, architecture | pressure | the product must choose among static, server-rendered, client-rendered, islands, installed or progressive delivery |
| `serves_novice_and_expert_users` | ui-ux | pressure | the same task surface must serve both first-time and frequent expert users |
| `requires_non_semantic_custom_control` | ui-ux | pressure | a required interaction cannot be expressed with a meaningful native HTML control alone |
| `house_style_costs_access_or_performance` | pattertech-house, ui-ux | pressure | a house-style choice measurably conflicts with audience need, accessibility or performance |
| `requires_independent_deployability` | architecture | pressure | separately owned parts must release, scale or fail independently |
| `requires_asynchronous_delivery` | architecture, api-integration, data-engineering | pressure | the producer cannot safely wait for the consumer to finish in the same call |
| `requires_storage_engine_choice` | architecture, data-engineering, data-analytics | pressure | materially different access, consistency or operational needs make the storage engine an open decision |
| `requires_offline_or_hybrid_consistency` | architecture, native-client | pressure | writes or reads must remain useful across offline, local, cloud or hybrid partitions |
| `riskiest_assumption_is_unproved` | product-discovery, delivery-testing | pressure | the cheapest next step is governed by an assumption with no representative evidence |
| `test_fidelity_changes_outcome` | delivery-testing | pressure | a double, sandbox or live dependency can produce materially different evidence for the decision |
| `incident_needs_gate_exception` | delivery-testing, devops-reliability | pressure | an active incident makes the normal delivery path too slow for the user harm underway |
| `managed_service_changes_exit_or_access` | architecture, devops-reliability | pressure | buying or managing a service changes portability, evidence access or incident control materially |
| `integrity_floor_reduces_availability` | security-privacy, devops-reliability | pressure | failing closed would remove a user journey that could otherwise degrade honestly |
| `observability_collects_sensitive_data` | devops-reliability, security-privacy | pressure | a proposed telemetry signal contains personal, confidential or authentication data |
| `producer_trust_is_unproved` | supply-chain-integrity, security-privacy | pressure | provenance exists or can exist but the producer's trustworthiness remains materially uncertain |
| `dependency_update_changes_known_good` | supply-chain-integrity, devops-reliability | pressure | a freshness update would replace a deployment whose behaviour and restoration path are already proved |
| `agent_coordination_cost_is_material` | agentic-development, agentic-swarm | pressure | the task could use more than one agent and coordination, merge or verification cost may dominate |
| `model_residency_or_hosting_is_constrained` | ai-ml-llm, security-privacy | pressure | data residency, latency, cost, capability or availability makes local versus hosted model execution material |
| `evaluation_oracle_is_undecided` | ai-ml-llm, delivery-testing | pressure | the work has no agreed deterministic, human or model-based judge for the claimed behaviour |
| `golden_path_needs_escape` | devops-reliability, agentic-development | pressure | the supported path cannot meet a material requirement without an escape route |
| `local_exception_may_generalise` | all | pressure | a venture departure has evidence that may justify changing Doctrine scope or admitting a reusable exception |

## Retired

Never reuse a retired name. A retired spelling matches no pack and
activates nothing, which reads exactly like a fact that is false.

| retired | replaced by | when | why |
| --- | --- | --- | --- |
| `processes_personal_data` | `handles_personal_data` | 2026-08-15, ADR-0010 | one answer to interview question 9, spelled two ways, so a venture recording either loaded one pack and missed the other |
