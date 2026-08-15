---
summary: Derived index of every decision guide, one fork each
type: index
tags: [eos, wargame]
derived: true
---

# GUIDE_INDEX

Derived file. Edit guide front-matter, then run
`python -m tools.eos check --write-index`.

| id | question | pack | authority | review |
| --- | --- | --- | --- | --- |
| WG-EOS-001 | What scale of organisational machinery does this venture compile, S or ORG? | inception | default | 2027-07 |
| WG-EOS-002 | One repo, several, or a corner of an existing one? | inception | default | 2027-07 |
| GD-AGENT-001 | Which of the ten agent topologies does this work need, and what pressure justifies promoting past a single agent? | agentic-development | default | on-change-of:agent-sdk-major-release |
| GD-AGENT-002 | How does context reach an agent, and what happens when the window runs out? | agentic-development | default | on-change-of:anthropic-context-engineering-publication |
| GD-AGENT-003 | Should this work be a subagent at all, and if so as a tool, a handoff or a peer worker? | agentic-development | default | on-change-of:agent-sdk-major-release |
| GD-AGENT-004 | What holds the truth that checks an agent's work, and what do you do when nothing does? | agentic-development | default | on-change-of:anthropic-evals-publication |
| GD-SWARM-001 | Should this work be fanned out over lanes at all, or given to one agent? | agentic-swarm | default | on-change-of:agent-harness-major-release |
| GD-SWARM-002 | Where do the cuts go when work is split across lanes, and what is never cut at all? | agentic-swarm | default | on-change-of:agent-harness-major-release |
| GD-SWARM-003 | Does a script hold the fan-out shape, or does a model decide it turn by turn? | agentic-swarm | default | on-change-of:agent-harness-major-release |
| GD-SWARM-004 | What decides that a lane's work is good, and who is allowed to have written it? | agentic-swarm | default | on-change-of:agent-harness-major-release |
| GD-AIML-001 | What evidence accepts or refuses a change to a model-backed feature, offline set, judge, human sample or production telemetry? | ai-ml-llm | default | 2026-11 |
| GD-AIML-002 | Where does the model get the facts, retrieval, whole context, per-query routing or fine-tuning? | ai-ml-llm | default | on-change-of:EV-0245 |
| GD-AIML-003 | Who grades model output, a deterministic scorer, a human, a validated model judge or the user, and what each can settle | ai-ml-llm | default | 2026-12 |
| GD-AIML-004 | How is a prompt maintained over time, hand-written and versioned, few-shot, compiled by an optimiser, or replaced by fine-tuning? | ai-ml-llm | default | 2026-12 |
| GD-AIML-005 | Which model backs this feature and what happens when it retires, one pinned model, a cascade, self-assessed routing or a portfolio? | ai-ml-llm | default | 2027-03 |
| GD-API-001 | Who writes the contract and when: by hand, in a definition language, generated from the handlers, or not at all? | api-integration | advisory | on-change-of:EV-0023 |
| GD-API-002 | How is a boundary allowed to change: add only, declared tier plus gate, explicit version parameter, or pinned date with transformers? | api-integration | advisory | on-change-of:EV-0129 |
| GD-API-003 | How is an inbound webhook trusted: bare-body HMAC, a signed triple, RFC 9421 message signatures, or an asymmetric or provider-native scheme? | api-integration | advisory | on-change-of:EV-0125 |
| GD-API-004 | What shape does a boundary take: REST over OpenAPI, typed RPC, an event stream, or GraphQL? | api-integration | advisory | on-change-of:EV-0023 |
| GD-API-005 | How does a consumer walk a collection: offset paging, opaque cursors, visible keyset, or a hybrid with an estimated total? | api-integration | advisory | on-change-of:EV-0130 |
| GD-ARCH-001 | One deployable, several deployables, or contract-shaped seams inside one process | architecture | default | 2027-03 |
| WG-ARCH-001 | Where module boundaries live, whether convention, a machine contract, the directory tree, or a runtime call graph | architecture | default | 2026-12 |
| WG-ARCH-002 | How the service reaches its data, whether an ORM, raw SQL behind a repository, a query builder, or SQL files compiled to typed access, and where the seam sits | architecture | default | 2027-07 |
| WG-ARCH-003 | Where a derived value is allowed to rest, whether computed on read, cached with a named owner, frozen as an immutable snapshot, or maintained by the write path | architecture | default | 2027-07 |
| WG-ARCH-004 | Where background work runs, whether in the request process, on a durable database claim queue, on an external broker, or on a scheduled pass over state | architecture | default | 2027-07 |
| WG-ARCH-005 | How frontend and backend come to agree on types, whether hand-maintained, generated and gated, one language end to end, or parsed at the edge | architecture | default | 2027-07 |
| WG-ARCH-006 | What proves a change changed nothing, whether a green suite, behaviour pinned first, a byte-stable output canary, or a differential run against the old version | architecture | default | 2027-07 |
| WG-ARCH-007 | How deep a vendor is allowed into the codebase, whether SDK throughout, an owned adapter, the raw protocol, or a generated client | architecture | default | 2027-01 |
| WG-ARCH-008 | Where data rests, whether one shared database, private tables with distinct credentials, one store per deployable, or a records core with a separate readings store | architecture | default | 2027-06 |
| GD-BLM-001 | How much model does this domain earn, from plain procedures to declared decisions? | business-logic-modelling | default | 2027-09 |
| GD-BLM-002 | Where does this rule live, in code, in a table, in a machine or in an engine? | business-logic-modelling | default | on-change-of:DMN-1.7-formal |
| GD-BLM-003 | How is money represented, rounded, allocated and converted at the edges? | business-logic-modelling | binding | on-change-of:ISO-4217-amendment |
| GD-BLM-004 | How much time does this fact carry, which temporal type and how many dimensions? | business-logic-modelling | binding | on-change-of:RFC-9557 |
| GD-BLM-005 | Is the record of truth the current state or the sequence of events? | business-logic-modelling | default | 2027-12 |
| GD-BMP-001 | What information the price is anchored to, and the condition that makes that anchor right here | business-model-pricing | default | 2028-04 |
| GD-BMP-002 | What the buyer is charged per, and what each unit costs in accounting, forecasting and support | business-model-pricing | default | 2028-01 |
| GD-BMP-003 | How a buyer experiences the product before paying, and why the evidence gives a measurement rule rather than a trial length | business-model-pricing | default | on-change-of:multi-firm-trial-length-replication |
| GD-BMP-004 | What opens a price change, what cause is announced with it, and who is protected from the change | business-model-pricing | default | 2028-06 |
| GD-COD-001 | Where does the oracle for this change come from, specification, characterisation, contract or downstream gate? | coding | default | 2027-05 |
| GD-COD-002 | Who reviews a change and how hard, from machine gate only to independent human review at every merge | coding | default | 2027-02 |
| GD-COD-003 | How do callers learn a call failed, opaque errors, one sentinel, a declared taxonomy or typed results? | coding | default | on-change-of:EV-0175 |
| GD-COD-004 | How do you change code nobody can specify, read carefully, pin behaviour, reconstruct a spec or rewrite behind a contract? | coding | default | 2027-10 |
| GD-COD-005 | One repository or several, and how the trunk flows through whichever you pick | coding | default | 2027-08 |
| GD-DATA-001 | Where does the data quality rule live, a declared contract, computed metrics with anomaly detection, both, or no gate at all? | data-analytics | default | 2027-12 |
| GD-DATA-002 | What shape does the analytics model take, a source mirror, layered wide entities, a dimensional star, or one metrics layer over any of them? | data-analytics | default | 2027-12 |
| GD-DATA-003 | How is an experiment allowed to end, a locked fixed horizon, an always-valid sequential test, an asymmetric gate, or no experiment at all? | data-analytics | default | 2028-01 |
| GD-DATA-004 | Where does the analytics data sit, a single managed warehouse, a warehouse over an open table format, a lakehouse, or files and a single-node engine? | data-analytics | default | 2028-01 |
| GD-DATA-005 | How are product events named and validated, hosted SDK defaults, a written convention, a reviewed tracking plan, or a registry that quarantines invalid events? | data-analytics | default | 2028-02 |
| GD-DATAENG-001 | Scheduled batch extract, a subscribed stream, log-based change capture, or polling a modified-at column? | data-engineering | default | 2027-12 |
| GD-DATAENG-002 | Overwrite the partition, merge on a key, append-only with a view that picks the winner, or an idempotent write token? | data-engineering | default | 2028-01 |
| GD-DATAENG-003 | The run's own clock, the scheduler's interval, a high-water mark read from the target, or the event time carried in the record? | data-engineering | default | 2028-02 |
| GD-DATAENG-004 | Drop at the watermark, hold the window open and restate, reprocess a fixed lookback every run, or recompute everything? | data-engineering | default | 2028-03 |
| WG-DEL-005 | Which double stands in for this port: real, container, verified fake, or mock? | delivery-testing | default | 2028-02 |
| WG-DEL-006 | How independent must the oracle be from the code it judges, and who authors it? | delivery-testing | binding | 2028-03 |
| WG-DEL-007 | What has to exist before work fans out, and when checks get written relative to the code | delivery-testing | default | 2028-03 |
| GD-DEVOPS-001 | Reversible migrations, expand-migrate-contract, online schema change, or a freeze window? | devops-reliability | default | 2027-09 |
| GD-DEVOPS-002 | All at once, watched canary, analysis-gated rollout, or flag-decoupled release? | devops-reliability | default | 2027-12 |
| GD-DEVOPS-003 | No budget, advisory budget, enforced budget policy, or calendar change freezes? | devops-reliability | default | 2028-03 |
| GD-DEVOPS-004 | Nothing, delivery keys only, SLO plus customer impact, or a multi-dimension set? | devops-reliability | default | 2028-02 |
| WG-OPS-003 | Trusted snapshots, a restore test with a tick, an evidenced restore drill, or full estate rehearsal? | devops-reliability | binding | 2028-06 |
| GD-DOCS-001 | Where a document's truth lives, and therefore whether it can drift at all | docs-dx | default | 2028-04 |
| GD-DOCS-002 | How a code example in documentation stops lying, and what to do with the ones that cannot run | docs-dx | default | on-change-of:rustdoc-doctest-semantics |
| GD-DOCS-003 | Who writes the changelog, and whether release notes can be derived from history at all | docs-dx | default | on-change-of:keep-a-changelog-beyond-1.1.0 |
| GD-DOCS-004 | What a user-visible failure owes its reader, and how much structure to spend on it | docs-dx | default | on-change-of:rustc-diagnostic-style-guide |
| GD-DOCS-005 | Which documentation checks are allowed to fail a build, and which stay advisory | docs-dx | default | 2028-04 |
| GD-IDENT-001 | Ownership checks, roles, attributes or relationships? The fork the coverage matrix recorded as missing | identity-access | default | 2028-10 |
| GD-IDENT-002 | Server-side session in a cookie, bearer token, token in a cookie behind a front end, or a sender-constrained token? | identity-access | default | 2028-11 |
| GD-IDENT-003 | Hosted identity provider, self-hosted identity server, passwords of your own, or federation to the customer's provider? | identity-access | default | 2028-12 |
| GD-IDENT-004 | Tenant isolation by application filter, by database row policy, by schema, or by a store per tenant? | identity-access | default | 2029-01 |
| GD-LEGAL-001 | Can we use this copyleft dependency for what we actually ship, and what fires the obligation | legal-licensing | default | on-change-of:https://opensource.org/license/agpl-v3 |
| GD-LEGAL-002 | How a venture decides licence questions at all, standing verdict against per-file declaration against certified process against scan and review | legal-licensing | default | on-change-of:https://www.apache.org/legal/resolved.html |
| GD-LEGAL-003 | What licence a repository carries outbound, and which promise that makes to the people downstream | legal-licensing | default | on-change-of:https://blueoakcouncil.org/list |
| GD-LEGAL-004 | How rights arrive with inbound code, sign-off against agreement against employment against nothing, and where agent authorship sits | legal-licensing | default | on-change-of:https://developercertificate.org/ |
| GD-LEGAL-005 | What a study may lawfully carry away from a source we do not own, how deep the reading goes, and who may hold the source while the replacement is written | legal-licensing | default | 2027-04 |
| GD-MKTG-001 | Which growth philosophy does this venture run? | marketing-growth | default | on-change-of:Reforge-and-IPA-primary-text-access |
| GD-MKTG-002 | Where does a lawful marketing address come from, and what may be sent to it? | marketing-growth | binding | on-change-of:PECR-reg-22-amendment |
| GD-MKTG-003 | How is a channel's effect measured, and what may be claimed from it? | marketing-growth | default | on-change-of:GA4-attribution-model-set |
| GD-MKTG-004 | Who owns a published page, and how fast may a venture publish? | marketing-growth | default | on-change-of:Google-spam-policies-revision |
| GD-NAT-001 | Which client architecture does this product take? | native-client | default | 2028-05 |
| GD-NAT-002 | What happens to a write made with no network? | native-client | default | 2028-05 |
| GD-NAT-003 | How does a fix reach a user, given that no release can be taken back? | native-client | default | on-change-of:play-staged-rollout-mechanics |
| GD-NAT-004 | How much accessibility assurance does a non-web surface buy, and against which instrument? | native-client | default | on-change-of:EN-301-549-v4-publication |
| GD-HOUSE-001 | How much light does this surface carry, and which tiers of the graded system are enabled? | pattertech-house | preference | 2028-04 |
| GD-HOUSE-002 | A set of content needs a container. Ledger, plaque, panel, table or prose? | pattertech-house | preference | 2028-05 |
| GD-HOUSE-003 | Does this surface render dark, light, dual or mixed, and what does each cost the reader? | pattertech-house | preference | 2028-06 |
| GD-HOUSE-004 | How austere is this figure, and may any figure in a piece carry a distinguishing device? | pattertech-house | preference | 2028-07 |
| GD-DISC-001 | How much discovery does this decision deserve, a gated phase, a standing cadence, outcome elicitation alone, or ship and instrument? | product-discovery | default | 2028-06 |
| GD-DISC-002 | Where does the evidence about users come from, existing behaviour, talking to people, a controlled experiment, or a model standing in for them? | product-discovery | default | 2028-06 |
| GD-DISC-003 | How do you choose between candidate opportunities, score them, rank by outcome contribution, test them all, or sequence by reversibility? | product-discovery | default | 2028-07 |
| GD-DISC-004 | Once the problem is settled, in what form do the acceptance criteria go, a user story, EARS clause order, an executable test, or a full specification chain? | product-discovery | default | 2028-07 |
| GD-RESEARCH-001 | One authoritative source, a fixed budget, agreement from independent routes, or an exhaustive sweep? | research-knowledge | default | 2029-04 |
| GD-RESEARCH-002 | In the repository under the code gate, an open wiki with a policy, a curated store with one editor, or no separate base at all? | research-knowledge | default | 2029-05 |
| GD-RESEARCH-003 | Wait for something to break, sweep on a calendar, supersede on a named event, or keep the answer continuously live? | research-knowledge | default | 2029-06 |
| GD-RESEARCH-004 | Follow it when it looks helpful, ignore it quietly, record and report it, or refuse to read the class at all? | research-knowledge | default | 2027-06 |
| GD-SEC-001 | In-band detection, a configuration rule, out-of-band enforcement, or OS containment? | security-privacy | default | 2027-03 |
| GD-SEC-002 | Ignore rules alone, a pre-commit scan, a push-path scan, or a managed store with short-lived credentials? | security-privacy | default | 2027-04 |
| GD-SEC-003 | No declared level, a flat entry bar, a graded catalogue by data sensitivity, or per-practice maturity? | security-privacy | default | 2027-06 |
| GD-SEC-004 | Model judgement, a static allowlist, guard-classified verdicts with recorded approval, or manual only? | security-privacy | default | 2027-05 |
| GD-SUPPLY-001 | A checksums file, build-platform provenance, a self-hosted attestation chain, or an independently reproduced build? | supply-chain-integrity | default | 2027-04 |
| GD-SUPPLY-002 | No signature, a personal key, a custodied key, a short-lived identity certificate, or the platform's own signing? | supply-chain-integrity | default | on-change-of:EV-0068 |
| GD-SUPPLY-003 | Floating ranges, continuous auto-merge, a cooldown window with batched moves, digest pins everywhere, or frozen? | supply-chain-integrity | default | 2027-05 |
| GD-SUPPLY-004 | Depend with a pin, vendor the source, fork and maintain, reimplement the slice you need, or use the platform? | supply-chain-integrity | default | on-change-of:EV-0069 |
| GD-SUPPORT-001 | How does inbound get classified, and what keeps the queue finite? | support-operations | default | on-change-of:ISO-10002-revision |
| GD-SUPPORT-002 | May an item close without an answer, and on whose clock? | support-operations | default | on-change-of:ISO-10002-revision |
| GD-SUPPORT-003 | Who declares a customer-visible incident, and on what signal? | support-operations | default | 2028-08 |
| GD-SUPPORT-004 | What do we measure about support, and what may the number be used for? | support-operations | default | 2028-08 |
| GD-UIUX-001 | Which design philosophy does this surface take? | ui-ux | advisory | 2027-10 |
| GD-UIUX-002 | Where do this surface's interactive components come from? | ui-ux | default | 2027-11 |
| GD-UIUX-003 | How much accessibility assurance does this surface buy? | ui-ux | default | on-change-of:WCAG-2.2 |
| GD-UIUX-004 | Where do tokens live and how do they reach each platform? | ui-ux | default | on-change-of:DTCG-format-module |
| GD-WRIT-001 | Which clarity philosophy governs this text, and where the control point sits? | writing-content | default | 2028-09 |
| GD-WRIT-002 | How is a user-facing sentence built so a second locale can express what English never had? | writing-content | default | on-change-of:CLDR-plural-categories |
| GD-WRIT-003 | Which voice applies to this text, and who is allowed to overrule it? | writing-content | default | 2028-09 |
| GD-WRIT-004 | How is prose checked before it merges, and which signals are allowed to block? | writing-content | default | 2028-09 |
