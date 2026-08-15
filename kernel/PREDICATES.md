---
summary: The controlled vocabulary of pack activation predicates, grouped by subject so two names for one fact sit next to each other
type: kernel
tags: [eos]
---

# PREDICATES

Every name a pack may put in `applies_when`. Check S021 holds pack
front-matter to this file, so a pack cannot invent a predicate without
adding it here first.

The point is not bookkeeping. A predicate is a fact about a venture, and
two packs naming one fact differently split the estate: a venture
recording one spelling loads one pack and silently misses the other,
which `python -m tools.eos activate` will show you and nothing else
will. That happened. `security-privacy` declared `handles_personal_data`
and `legal-licensing` declared `processes_personal_data`, which are one
answer to interview question 9, and both packs defined it in almost the
same words. ADR-0010 merged them.

So the rows below are grouped by subject rather than by pack. Two names
for one fact land next to each other, where somebody adding a third will
see them.

## How to add one

Add the row here, in the group its subject belongs to, before putting it
in a pack. Read the group first. If an existing predicate is already
true in the same circumstances, use it and let two packs share it, which
is normal and is what `handles_personal_data` now does. Sharing a
predicate is not a coupling between packs; it is two packs agreeing
about the world.

A predicate should be a fact an operator can answer yes or no about the
venture, not a judgement about the work. `has_database` is a fact.
`needs_careful_design` is not.

Retired names are listed at the end and must not be reused. A retired
spelling silently activates nothing, which is the expensive direction.

## Data about people

| predicate | packs | true when |
| --- | --- | --- |
| `handles_personal_data` | security-privacy, legal-licensing | the system collects, stores or transmits data about identifiable people |
| `handles_analytics_identifier` | data-analytics | analytics carries an identifier that can be tied back to a person or device |
| `collects_contact_details` | marketing-growth | the venture gathers an address, number or handle it can contact somebody on |

## Secrets and reach outside itself

| predicate | packs | true when |
| --- | --- | --- |
| `holds_credentials` | security-privacy | the repository or its runtime holds a secret, key or token |
| `has_external_egress` | security-privacy | code can reach the network beyond the venture |
| `consumes_external_api` | api-integration | the venture calls somebody else's service |
| `receives_webhooks` | api-integration | somebody else's service calls in |
| `exposes_service_boundary` | api-integration | the venture offers an interface another system calls |
| `publishes_events` | api-integration | the venture emits events others consume |
| `has_vendor_holding_identity_or_money` | architecture | a third party holds the venture's identities or its money |
| `studies_external_source` | legal-licensing | work reads a product, repository, game or document we do not own, to learn from it |

## Code and how it changes

| predicate | packs | true when |
| --- | --- | --- |
| `edits_source` | coding | the work changes source code |
| `reviews_change` | coding | somebody reviews a change before it lands |
| `decides_merge` | coding | somebody decides whether a change merges |
| `ships_code` | delivery-testing | code reaches somebody other than its author |
| `has_test_suite` | delivery-testing | the venture has automated tests |
| `adds_dependency` | legal-licensing | the work brings in third-party code |
| `vendors_code` | legal-licensing | third-party code is copied into the tree |
| `publishes_code` | legal-licensing | the venture's code is made available to others |
| `accepts_contribution` | legal-licensing | code arrives from someone outside the venture |

## Shape of the system

| predicate | packs | true when |
| --- | --- | --- |
| `has_server_code` | architecture | something runs that is not the user's own device |
| `has_multiple_modules` | architecture | the tree has parts that could be built or deployed apart |
| `has_database` | architecture | the venture stores structured data it queries |
| `has_cross_language_contract` | architecture | two languages agree on a shape at a boundary |
| `encodes_domain_rule` | business-logic-modelling | a rule of the business is written in code |
| `models_money` | business-logic-modelling | amounts of money are represented and arithmetic is done on them |
| `models_time` | business-logic-modelling | dates, durations or time zones carry meaning |
| `has_lifecycle_state` | business-logic-modelling | a thing moves through named states |

## Running it

| predicate | packs | true when |
| --- | --- | --- |
| `deploys_to_environment` | devops-reliability | the venture is put somewhere it runs |
| `stores_persistent_data` | devops-reliability | state outlives a single run and matters if lost |
| `runs_schema_migrations` | devops-reliability | the shape of stored data changes over time |
| `hosts_service` | legal-licensing | people reach the software over a network |

## Agents, models and lanes

| predicate | packs | true when |
| --- | --- | --- |
| `runs_agents` | security-privacy | an agent runs tools in the repository |
| `builds_agent_workflow` | agentic-development | the venture builds something that drives an agent |
| `orchestrates_multiple_agents` | agentic-development | more than one agent runs against shared work |
| `designs_agent_harness` | agentic-development | the venture builds the scaffolding an agent runs inside |
| `defines_agent_tools` | agentic-development | the venture defines the tools an agent may call |
| `fans_work_across_lanes` | agentic-swarm | work is split across lanes running at once |
| `cuts_a_build_partition` | agentic-swarm | somebody divides a build into disjoint paths |
| `integrates_parallel_lanes` | agentic-swarm | somebody merges what parallel lanes produced |
| `writes_a_lane_packet` | agentic-swarm | a lane is given its brief in writing |
| `calls_a_model` | ai-ml-llm | the venture calls a language or other model at runtime |
| `changes_prompt_or_model` | ai-ml-llm | a prompt or a model identifier changes |
| `builds_retrieval` | ai-ml-llm | the venture retrieves documents to put in front of a model |
| `evaluates_model_output` | ai-ml-llm | model output is judged against something |
| `ships_model_output` | ai-ml-llm | model output reaches a person or another system |

## What a person sees and touches

| predicate | packs | true when |
| --- | --- | --- |
| `has_user_interface` | ui-ux | a person interacts with the venture through a surface it draws |
| `has_native_ui` | native-client | the interface is drawn by a native toolkit rather than a browser |
| `has_forms` | writing-content | a person types into fields the venture validates |
| `ships_a_binary` | native-client | the venture distributes something that is installed |
| `has_local_write_store` | native-client | the device holds writes of its own |
| `distributes_via_app_store` | native-client | distribution goes through a store with its own rules |

## Words

| predicate | packs | true when |
| --- | --- | --- |
| `writes_user_facing_text` | writing-content | text the venture's users read is written or changed |
| `writes_venture_documentation` | writing-content | documentation about the venture is written |
| `writes_eos_internal_prose` | writing-content | prose inside the EOS itself is written |
| `reuses_external_style_guidance` | writing-content | style guidance from outside is carried into the venture |
| `ships_second_locale` | writing-content | the venture is offered in more than one language |
| `publishes_docs` | docs-dx | documentation is published to readers |
| `documents_executable_surface` | docs-dx | documentation describes something a reader will run |
| `emits_user_visible_failure` | docs-dx | the venture shows a person a failure |
| `renames_or_deletes_documented_page` | docs-dx | a documented page moves or goes |
| `adopts_pattertech_house` | pattertech-house | the venture adopts PatterTech's house style |

## Money and the market

| predicate | packs | true when |
| --- | --- | --- |
| `sets_a_price` | business-model-pricing | somebody decides what to charge |
| `publishes_a_price` | business-model-pricing | a price is stated publicly |
| `sells_to_consumers` | business-model-pricing | buyers are individuals rather than organisations |
| `sells_by_subscription` | business-model-pricing | payment recurs |
| `sells_to_public_sector` | business-model-pricing | buyers are public bodies |
| `bundles_or_discounts` | business-model-pricing | price varies by package or by deal |
| `reports_commercial_metrics` | business-model-pricing | commercial performance is reported |
| `has_paying_customers` | support-operations | somebody has paid and expects the thing to work |
| `plans_growth_spend` | marketing-growth | money is committed to reaching more people |

## Reaching people

| predicate | packs | true when |
| --- | --- | --- |
| `publishes_public_content` | marketing-growth | the venture publishes content anyone can read |
| `sends_marketing_message` | marketing-growth | the venture sends a message somebody did not ask for individually |
| `reports_channel_effect` | marketing-growth | the effect of a channel is measured and reported |
| `runs_public_tracker` | support-operations | issues or incidents are tracked where users can see them |

## Evidence and deciding

| predicate | packs | true when |
| --- | --- | --- |
| `publishes_analytics_table` | data-analytics | a table others read for decisions is published |
| `defines_events` | data-analytics | the venture defines what gets recorded when something happens |
| `runs_experiment` | data-analytics, product-discovery | a change is tried against a comparison |
| `reads_for_decision` | data-analytics | somebody reads data to decide something |
| `proposes_capability` | product-discovery | somebody proposes the venture should do a new thing |
| `prioritises_work` | product-discovery | somebody decides what comes first |
| `cites_user_claim` | product-discovery | a claim about users is used as evidence |
| `writes_acceptance_criteria` | product-discovery | somebody writes down what done means |

## Customers and incidents

| predicate | packs | true when |
| --- | --- | --- |
| `has_customer_inbound` | support-operations | people contact the venture unprompted |
| `has_customer_visible_incident` | support-operations | a failure was visible to somebody outside the venture |
| `reports_support_metric` | support-operations | support performance is reported |
| `single_responder` | support-operations | one person carries the response |

## Retired

Never reuse a retired name. A retired spelling matches no pack and
activates nothing, which reads exactly like a fact that is false.

| retired | replaced by | when | why |
| --- | --- | --- | --- |
| `processes_personal_data` | `handles_personal_data` | 2026-08-15, ADR-0010 | one answer to interview question 9, spelled two ways, so a venture recording either loaded one pack and missed the other |
