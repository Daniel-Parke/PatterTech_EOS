---
summary: The cited sources whose licence is unknown or not stated, what the provenance sweep confirmed and what it did not
type: registry
tags: [eos, security]
status: active
review: 2026-11
---

# LICENCE RESIDUALS

ADR-0006 decision 7 puts this repository under Apache-2.0 and puts a
provenance sweep behind it. Part of that sweep is an honest residual
list: the sources we cite whose licence nobody has confirmed. This is
that list. It exists so a publication decision starts from facts rather
than from a hope.

Two rules held while it was written, and they are the ADR's own. No
source was re-fetched. No licence was invented. Every line below is a
reading of what `registry/evidence.json` already records, counted
against the ledger as it stood on 2026-08-10 at 504 rows.

## What the ledger says

504 records. Ninety carry a `licence_evidence` line, which is somebody
looking at the page and writing down what it said, all recorded on
2026-08-08. The other 414 carry a licence value that is the recording
agent's word for it. A named licence with no evidence line is probably
right, and probably right is what the ADR says not to record as fact.

172 records carry no usable licence, and the split matters:

- **Sixty-six say the source states none.** Fifty-three of those were
  looked at on 2026-08-08 and the absence was confirmed, which makes it
  a fact rather than a gap. You know where you stand: fair quotation and
  the use of facts is all you have. The other thirteen have never been
  looked at. Twelve of them arrived with the swarm import on 2026-08-10
  and the thirteenth is EV-0449, which was added just after the check
  and missed it.
- **A hundred and six say the licence is unrecorded.** Not one has been
  looked at. Most carry a parenthetical guess about the publisher's
  copyright, and a guess in brackets is still a guess. Nine of them say
  in as many words that the row was not read at source. These tell you
  nothing.

The remaining 332 records name a licence. Some of those names are
restrictive rather than open: all rights reserved, proprietary,
paywalled, or a publisher's copyright with paraphrase-only noted. Those
are not residuals. They are answered questions with a restrictive
answer, and they are out of scope here. No count is given for them,
because there is no mechanical line between a restrictive name and a
permissive one and any number would be an artefact of where somebody
drew it.

## What the sweep covered

Each pack lane swept its own read surface: a scan for carried
quotation, a read of every passage that restates a source under a
no-derivatives or all-rights-reserved licence, and a sort of its cited
ids by whether the licence line has an observation behind it. The
fragments are at `packs/<pack>/research/provenance.fragment.json` and
each one carries its own reasoning, which this file does not restate.

All twenty-one packs were swept on 2026-08-10. The table below is not
the fragments' arithmetic. The fragments come in three shapes and count residuals
slightly differently, so this is recounted from the ledger instead: one
row per pack, the evidence rows whose `cited_by` names that pack, and
how many of those land in table A and table B. Recounted on 2026-08-11,
and a reader with the ledger open can reproduce every cell.

| Pack | Cited rows | States none | Unrecorded |
| --- | --- | --- | --- |
| `packs/agentic-development/` | 50 | 28 | 0 |
| `packs/agentic-swarm/` | 62 | 18 | 3 |
| `packs/ai-ml-llm/` | 37 | 6 | 4 |
| `packs/api-integration/` | 34 | 7 | 4 |
| `packs/architecture/` | 40 | 4 | 17 |
| `packs/business-logic-modelling/` | 30 | 1 | 9 |
| `packs/business-model-pricing/` | 25 | 1 | 11 |
| `packs/coding/` | 42 | 3 | 11 |
| `packs/data-analytics/` | 24 | 2 | 10 |
| `packs/delivery-testing/` | 37 | 9 | 5 |
| `packs/devops-reliability/` | 24 | 1 | 4 |
| `packs/docs-dx/` | 25 | 2 | 7 |
| `packs/legal-licensing/` | 30 | 0 | 13 |
| `packs/marketing-growth/` | 25 | 6 | 4 |
| `packs/native-client/` | 28 | 0 | 4 |
| `packs/pattertech-house/` | 31 | 0 | 7 |
| `packs/product-discovery/` | 23 | 0 | 3 |
| `packs/security-privacy/` | 30 | 3 | 9 |
| `packs/support-operations/` | 22 | 1 | 2 |
| `packs/ui-ux/` | 27 | 0 | 3 |
| `packs/writing-content/` | 22 | 0 | 3 |

A row cited by two packs is counted in both, so the columns do not sum
to the totals above.

`packs/agentic-swarm/` swept last. Its pack lane filed no fragment, so
the sweep was run over its read surface afterwards. Its sources are most
of what moved the numbers in this file: of the 55 rows the 2026-08-10
import added, EV-0450 to EV-0504, 46 are cited by that pack and 9 by
`packs/legal-licensing/`.

## What the sweep did not do

- It fetched nothing, so it confirmed no licence. It sorted what the
  ledger already holds into fact and assertion.
- It cannot prove a negative. A quotation scan that returns nothing
  proves there are no quotation marks and no close restatement in the
  passages read. It does not prove that no expression was carried from
  a source nobody flagged.
- It says nothing about the 414 records whose licence is asserted with
  no observation behind it. Most name well-known project licences and
  are probably right. That is the queue to work down, and it is the
  number to watch rather than the 172 below.

No lane reported expression carried from a source. The only changes any
fragment asked for are citation work, and they are in the section below.
Several named the one file in their pack to re-read first if the sweep
is ever repeated, and those are in the fragments.

## How to read the tables

Column three of table B is the ledger's own words, kept verbatim so the
guess and the fact stay distinguishable. Observed means a
`licence_checked` date exists, which means somebody read the page.

The split is mechanical, so you can check it. A record is in table A
when its whole licence value is `not-stated`, meaning the source was
read and states none. It is in table B when the value says unknown, or
begins not-verified. Everything else names a licence, whether or not
anybody looked. The ledger used to spell the table A value three ways,
`not-stated`, `not stated` and `not-stated on page`; that drift was
normalised to `not-stated` on 2026-08-11 and the membership of the
table did not change.

Which pack cites which id is not repeated here. That mapping is
`cited_by` in `registry/evidence.json`, it is derived, and a second
copy of it in this file would be the one that went stale.

## Table A. The source states no licence, 66 records

| Id | Source | Observed |
| --- | --- | --- |
| EV-0014 | Agent Skills specification | yes, 2026-08-08 |
| EV-0015 | Playwright test retries and flake classification | yes, 2026-08-08 |
| EV-0016 | Playwright --only-changed affected-test selection | yes, 2026-08-08 |
| EV-0017 | Hypothesis property-based testing | yes, 2026-08-08 |
| EV-0031 | SWT-Bench | yes, 2026-08-08 |
| EV-0042 | Agent Client Protocol | yes, 2026-08-08 |
| EV-0044 | AGENTS.md open format | yes, 2026-08-08 |
| EV-0053 | Building a C compiler with Claude agent teams (Anthropic) | yes, 2026-08-08 |
| EV-0057 | dbt model contracts | yes, 2026-08-08 |
| EV-0061 | Stripe API versioning | yes, 2026-08-08 |
| EV-0072 | GitHub Agent HQ | yes, 2026-08-08 |
| EV-0077 | ADK workflow agents docs | yes, 2026-08-08 |
| EV-0078 | Microsoft Agent Framework workflows docs | yes, 2026-08-08 |
| EV-0079 | LangGraph interrupts docs | yes, 2026-08-08 |
| EV-0080 | OpenHands context condenser docs | yes, 2026-08-08 |
| EV-0081 | OpenHands security and confirmation docs | yes, 2026-08-08 |
| EV-0082 | OpenHands stuck detector docs | yes, 2026-08-08 |
| EV-0083 | OpenHands microagents and skills docs | yes, 2026-08-08 |
| EV-0084 | OpenHands sub-agent delegation docs | yes, 2026-08-08 |
| EV-0085 | Effective harnesses for long-running agents (Anthropic) | yes, 2026-08-08 |
| EV-0086 | Effective context engineering for AI agents (Anthropic) | yes, 2026-08-08 |
| EV-0087 | Demystifying evals for AI agents (Anthropic) | yes, 2026-08-08 |
| EV-0088 | Building effective agents (Anthropic) | yes, 2026-08-08 |
| EV-0089 | Harness design for long-running application development (Anthropic) | yes, 2026-08-08 |
| EV-0090 | Playwright best practices | yes, 2026-08-08 |
| EV-0091 | Pact Nirvana adoption guide | yes, 2026-08-08 |
| EV-0092 | Testing Library guiding principles | yes, 2026-08-08 |
| EV-0093 | Testcontainers philosophy | yes, 2026-08-08 |
| EV-0095 | PostHog Handbook | yes, 2026-08-08 |
| EV-0106 | Cognition: Don't Build Multi-Agents | yes, 2026-08-08 |
| EV-0107 | Cognition: Multi-Agents, What's Actually Working | yes, 2026-08-08 |
| EV-0108 | Claude Code Agent Teams docs | yes, 2026-08-08 |
| EV-0112 | How we built our multi-agent research system (Anthropic) | yes, 2026-08-08 |
| EV-0113 | Writing effective tools for AI agents (Anthropic) | yes, 2026-08-08 |
| EV-0114 | Code execution with MCP (Anthropic) | yes, 2026-08-08 |
| EV-0115 | Building agents with the Claude Agent SDK (Anthropic) | yes, 2026-08-08 |
| EV-0119 | Google ADK callbacks docs | yes, 2026-08-08 |
| EV-0120 | Google ADK plugins docs | yes, 2026-08-08 |
| EV-0121 | Microsoft Agent Framework workflow checkpoints docs | yes, 2026-08-08 |
| EV-0126 | GitHub webhook delivery validation documentation | yes, 2026-08-08 |
| EV-0133 | Stripe idempotent requests documentation | yes, 2026-08-08 |
| EV-0135 | Buf breaking-change rule categories | yes, 2026-08-08 |
| EV-0139 | Confluent Schema Registry schema evolution and compatibility | yes, 2026-08-08 |
| EV-0219 | The lethal trifecta for AI agents (Simon Willison) | yes, 2026-08-08 |
| EV-0220 | Claude Code sandboxed Bash tool documentation | yes, 2026-08-08 |
| EV-0244 | Hong, Troynikov and Huber (Chroma), Context Rot: How Increasing Input Tokens Impacts LLM Performance | yes, 2026-08-08 |
| EV-0253 | Panickssery, Bowman and Feng, LLM Evaluators Recognize and Favor Their Own Generations (NeurIPS 2024) | yes, 2026-08-08 |
| EV-0268 | European Commission, General-Purpose AI Code of Practice and the Article 53 and 55 obligations of Regulation (EU) 2024/1689 | yes, 2026-08-08 |
| EV-0360 | Google Workspace Admin Help, Email sender guidelines | yes, 2026-08-08 |
| EV-0364 | Google Analytics Help, Attribution and attribution modelling in Google Analytics 4 | yes, 2026-08-08 |
| EV-0365 | Reforge, Growth Loops are the New Funnels (Balfour, Winters, Kwok, Chen) | yes, 2026-08-08 |
| EV-0366 | PostHog Handbook, Marketing | yes, 2026-08-08 |
| EV-0367 | PostHog docs, Funnels | yes, 2026-08-08 |
| EV-0449 | LangGraph persistence and durable execution documentation (LangChain) | no |
| EV-0457 | LinearB, 8 million pull requests reveal where engineering productivity breaks down | no |
| EV-0458 | Faros AI, AI Code Quality: The Hidden Cost Senior Engineers Pay | no |
| EV-0460 | Run parallel sessions with worktrees (Claude Code documentation) | no |
| EV-0461 | Orchestrate subagents at scale with dynamic workflows (Claude Code documentation) | no |
| EV-0462 | A harness for every task: dynamic workflows in Claude Code (Anthropic) | no |
| EV-0463 | Create custom subagents (Claude Code documentation) | no |
| EV-0464 | claude-code issue 34645: parallel subagents with worktree isolation fail on git config lock contention | no |
| EV-0474 | MCP Security Best Practices | no |
| EV-0475 | LangGraph checkpoint loading has unsafe msgpack deserialisation (CVE-2026-28277) | no |
| EV-0476 | From SQLi to RCE: Exploiting LangGraph's Checkpointer (Check Point Research) | no |
| EV-0491 | Wisdom and Delusion of LLM Ensembles for Code Generation and Repair | no |
| EV-0492 | Defeating Nondeterminism in LLM Inference (Thinking Machines Lab) | no |

## Table B. The licence is unrecorded, 106 records

| Id | Source | What the ledger records | Observed |
| --- | --- | --- | --- |
| EV-0038 | SLSA v1.2 | Community Specification License / CC (OpenSSF project); unknown exact | no |
| EV-0041 | UK ICO guidance on AI and data protection | Open Government Licence (typical for ICO); unknown exact | no |
| EV-0059 | GrowthBook Experiment Decision Framework | unknown (GrowthBook core is MIT; EDF is a Pro/Enterprise feature) | no |
| EV-0102 | Structurizr DSL | unknown (Apache-2.0 for structurizr/dsl historically; not confirmed on the docs page) | no |
| EV-0104 | Storybook testing docs | MIT (Storybook); docs licence unknown | no |
| EV-0125 | Standard Webhooks specification | unknown (repository licence file not inspected) | no |
| EV-0131 | Zalando RESTful API Guidelines | unknown (repository licence file not inspected) | no |
| EV-0132 | Microsoft Azure REST API Guidelines | unknown (repository licence file not inspected; repo commonly Apache-2.0 or CC-BY-4.0) | no |
| EV-0140 | GraphQL specification, September 2025 edition | unknown (spec text served under an Open Web Foundation agreement; licence page not retrieved) | no |
| EV-0149 | arc42 architecture documentation template | unknown (site states open source and free including commercial use; specific licence page not inspected) | no |
| EV-0150 | Alistair Cockburn, Hexagonal Architecture (Ports and Adapters) | unknown (author's site, no explicit licence found) | no |
| EV-0152 | Ghemawat, Grandl, Petrovic, Whittaker, Towards Modern Development of Cloud Applications (HotOS '23) | unknown (ACM proceedings; author PDF hosted by SIGOPS) | no |
| EV-0153 | Martin Fowler, MonolithFirst | unknown (martinfowler.com, no open licence stated) | no |
| EV-0154 | MacCormack, Baldwin and Rusnak, Exploring the duality between product and organizational architectures (Research Policy 41(8), 2012) | unknown (publisher copyright; open-access author copy via Harvard DASH) | no |
| EV-0157 | Chris Richardson, Transactional Outbox pattern (microservices.io) | unknown (site copyright, no open licence stated) | no |
| EV-0159 | Shopify Engineering, Deconstructing the monolith | unknown (Shopify site, no open licence stated) | no |
| EV-0160 | Uber Engineering, Domain-Oriented Microservice Architecture | unknown (Uber site, no open licence stated) | no |
| EV-0161 | Stripe documentation, Webhooks and signature verification | unknown (Stripe documentation, proprietary) | no |
| EV-0162 | Chris Richardson, Database per service pattern (microservices.io) | unknown (site copyright, no open licence stated) | no |
| EV-0163 | Martin Fowler, What do you mean by Event-Driven? | unknown (martinfowler.com, no open licence stated) | no |
| EV-0165 | Sadowski, Soderberg, Church, Sipko, Bacchelli, Modern Code Review: A Case Study at Google | unknown (author-hosted preprint; IEEE/ACM proceedings copyright applies to the published version) | no |
| EV-0166 | Bacchelli and Bird, Expectations, Outcomes, and Challenges of Modern Code Review | unknown (publisher-hosted author copy; ICSE 2013 proceedings copyright applies) | no |
| EV-0172 | Potvin and Levenberg, Why Google Stores Billions of Lines of Code in a Single Repository | unknown (ACM copyright; the CACM web version is publicly readable) | no |
| EV-0174 | Yuan et al., Simple Testing Can Prevent Most Critical Failures (OSDI 14) | unknown (USENIX open-access proceedings; USENIX and author copyright) | no |
| EV-0176 | Feitelson, Mizrahi, Noy et al., How Developers Choose Names | unknown (IEEE copyright on the published version; arXiv preprint under arXiv non-exclusive licence) | no |
| EV-0177 | Silva, Tsantalis and Valente, Why We Refactor? Confessions of GitHub Contributors | unknown (ACM copyright on the published version; arXiv preprint under arXiv non-exclusive licence) | no |
| EV-0178 | Fucci et al., A Dissection of the Test-Driven Development Process: Does It Really Matter to Test-First or to Test-Last? | unknown (IEEE copyright on the published version; arXiv preprint under arXiv non-exclusive licence) | no |
| EV-0179 | GitClear, The Maintainability Gap: 2026 AI Code Quality Research | unknown (no reuse licence stated; site terms of service apply) | no |
| EV-0181 | Pearce, Ahmad, Tan, Dolan-Gavitt and Karri, Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions | unknown (IEEE copyright on the published version; arXiv preprint under arXiv non-exclusive licence) | no |
| EV-0183 | trunkbaseddevelopment.com | unknown (no explicit reuse licence found; site copyright Paul Hammant with community contributions) | no |
| EV-0191 | Just, Jalali, Inozemtseva, Ernst, Holmes, Fraser, Are mutants a valid substitute for real faults in software testing? (FSE 2014) | unknown (author-hosted preprint of an ACM paper) | no |
| EV-0193 | Pact can-i-deploy and the Pact Matrix | unknown (docs.pact.io site, Pact Foundation copyright; Pact tooling itself MIT) | no |
| EV-0195 | John Micco, Flaky Tests at Google and How We Mitigate Them (Google Testing Blog) | unknown (Google Testing Blog, no reuse licence stated on page) | no |
| EV-0196 | Jeff Listfield, Where do our flaky tests come from? (Google Testing Blog) | unknown (Google Testing Blog, no reuse licence stated on page) | no |
| EV-0202 | Atlas migration lint analyzers | Apache-2.0 for Atlas community edition; docs terms unknown; some analyzers are Pro-only | no |
| EV-0203 | Principles of Chaos Engineering | unknown (no notice on site; source repo on GitHub) | no |
| EV-0214 | Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents | arXiv default (author licence not confirmed at access); unknown | no |
| EV-0215 | Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents | arXiv default (author licence not confirmed at access); unknown | no |
| EV-0217 | AgentDojo | arXiv default (author licence not confirmed at access); unknown | no |
| EV-0218 | Model Context Protocol security best practices | MIT (Model Context Protocol specification repository); unknown for the rendered site | no |
| EV-0222 | GitHub secret scanning push protection | CC BY 4.0 (GitHub Docs content licence); unknown for product behaviour | no |
| EV-0224 | Microsoft Threat Modeling Tool threat categories (STRIDE) | CC BY 4.0 (Microsoft Learn documentation); unknown for the tool | no |
| EV-0226 | NCSC Small Business Guide to Cyber Security | Open Government Licence (typical for NCSC); unknown exact | no |
| EV-0237 | Overlay Fact Sheet | unknown (no licence or copyright notice shown) | no |
| EV-0240 | Grafana dashboard best practices | unknown (no licence or copyright statement on the page) | no |
| EV-0269 | Vaughn Vernon, Effective Aggregate Design (three-part DDD community essay) | unknown (Domain Language, Inc. and contributors copyright; no open licence stated on the library page or the PDFs) | no |
| EV-0271 | EventStorming (Alberto Brandolini, Avanscoperta) | unknown (site copyright, all rights reserved; the name EventStorming is claimed as the originator's mark and no open licence is stated) | no |
| EV-0282 | TC39 Temporal proposal documentation | unknown (no licence statement on the documentation page; the proposal repository states its own terms) | no |
| EV-0283 | ISO 4217 currency code lists, published by SIX as maintenance agency | unknown (lists published free of charge by the maintenance agency; the ISO 4217 standard text itself is sold by ISO and no reuse licence for the lists is stated on the page) | no |
| EV-0284 | Stripe documentation, supported currencies and amount representation | unknown (Stripe documentation copyright, no open licence stated) | no |
| EV-0285 | Alexis King, Parse, don't validate | unknown (no licence statement on the post) | no |
| EV-0287 | Andreas Hinterhuber, Customer value-based pricing strategies: why companies resist | unknown (Emerald publisher copyright; abstract and secondary summaries consulted, paraphrase only) | no |
| EV-0288 | Paul T. M. Ingenbleek, Ruud T. Frambach and Tammo H. A. Bijmolt, Best Practices for New Product Pricing: Impact on Market Performance and Price Level under Different Conditions | unknown (Wiley publisher copyright; full text paywalled at HTTP 402, abstract and indexing records consulted) | no |
| EV-0289 | Klaus M. Miller, Reto Hofstetter, Harley Krohmer and Z. John Zhang, How Should Consumers' Willingness to Pay Be Measured? An Empirical Comparison of State-of-the-Art Approaches | unknown (SAGE and American Marketing Association copyright; abstract consulted, paraphrase only) | no |
| EV-0290 | Sawtooth Software, Van Westendorp Price Sensitivity Meter explainer | unknown (vendor site, no licence stated) | no |
| EV-0291 | Eric Anderson and Duncan Simester, Effects of $9 Price Endings on Retail Sales: Evidence from Field Experiments | unknown (Springer publisher copyright; abstract and author-hosted copy at Kellogg consulted) | no |
| EV-0292 | The operator Kahneman, Jack L. Knetsch and Richard Thaler, Fairness as a Constraint on Profit Seeking: Entitlements in the Market | unknown (American Economic Association copyright; author-hosted copies at Chicago Booth and MIT consulted, paraphrase only) | no |
| EV-0293 | Sybil Yang and Michael Lynn, More Evidence Challenging the Robustness and Usefulness of the Attraction Effect | unknown (SAGE and American Marketing Association copyright; abstract consulted, paraphrase only) | no |
| EV-0294 | Hema Yoganarasimhan, Ebrahim Barzegary and Abhishek Pani, Design and Evaluation of Optimal Free Trials | unknown (INFORMS copyright on the published version; author-hosted working copy consulted) | no |
| EV-0296 | Peter S. Fader and Bruce G. S. Hardie, How to Project Customer Retention | unknown (publisher copyright; author-hosted copies at Wharton and brucehardie.com consulted, paraphrase only) | no |
| EV-0297 | IFRS 15 Revenue from Contracts with Customers, IFRS Foundation | unknown (IFRS Foundation copyright, trade marks asserted, no open licence stated on the page; paraphrase only) | no |
| EV-0307 | dbt Labs, How we structure our dbt projects | unknown (no licence statement on the page) | no |
| EV-0309 | Armbrust, Ghodsi, Xin and Zaharia, Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics | unknown (no licence statement on the paper) | no |
| EV-0311 | Jordan Tigani, Big Data is Dead (MotherDuck blog) | unknown (no licence statement; vendor blog) | no |
| EV-0312 | Johari, Pekelis and Walsh, Always Valid Inference: Continuous Monitoring of A/B Tests | unknown (arXiv listing; no explicit reuse licence recorded) | no |
| EV-0313 | Kohavi, Deng and Vermeer, A/B Testing Intuition Busters: Common Misunderstandings in Online Controlled Experiments | unknown (ACM proceedings; author copies circulated) | no |
| EV-0314 | Kohavi, Deng, Frasca, Walker, Xu and Pohlmann, Online Controlled Experiments at Large Scale | unknown (ACM proceedings; author copy served by exp-platform.com) | no |
| EV-0316 | Fabijan, Gupchup, Gupta, Omhover, Qin, Vermeer and Dmitriev, Diagnosing Sample Ratio Mismatch in Online Controlled Experiments | unknown (ACM proceedings) | no |
| EV-0320 | NIST SP 800-226, Guidelines for Evaluating Differential Privacy Guarantees | unknown (US Government publication) | no |
| EV-0323 | Tom Johnson, What is Diataxis and should you be using it with your documentation? | unknown (no licence statement found on the page) | no |
| EV-0325 | Aghajani, Nagy, Vega-Marquez, Linares-Vasquez, Moreno, Bavota, Lanza, Software Documentation Issues Unveiled | unknown (IEEE/ACM proceedings copyright; no open-access copy verified) | no |
| EV-0326 | Aghajani, Nagy, Linares-Vasquez, Moreno, Bavota, Lanza, Shepherd, Software Documentation: The Practitioners' Perspective | unknown (ACM Digital Library; the ACM landing page returned 403 to automated fetch) | no |
| EV-0327 | Barik, Smith, Lubick, Holmes, Feng, Murphy-Hill, Parnin, Do Developers Read Compiler Error Messages? | unknown (author-hosted preprint; ICSE 2017 proceedings copyright applies to the published version) | no |
| EV-0329 | Prana, Treude, Thung, Atapattu, Lo, Categorizing the Content of GitHub README Files | unknown (arXiv preprint; check the arXiv licence line before reuse. Springer holds the journal version) | no |
| EV-0336 | DX, Measuring developer productivity with the DX Core 4 | unknown (copyright DX 2026; no reuse licence stated) | no |
| EV-0337 | SPDX License List | unknown (no reuse licence stated on the list landing page; Linux Foundation site terms of use apply) | no |
| EV-0343 | Blue Oak Council Permissive License List | unknown (no reuse licence stated on the list page; the list is also published as JSON and as an npm package) | no |
| EV-0351 | European Commission, summary of the Cyber Resilience Act (Regulation (EU) 2024/2847) | unknown (no reuse notice shown on the page; Commission Decision 2011/833/EU typically applies to Commission documents) | no |
| EV-0362 | Gordon, Zettelmeyer, Bhargava and Chapsky, A Comparison of Approaches to Advertising Measurement: Evidence from Big Field Experiments at Facebook | unknown (INFORMS subscription content; abstract publicly readable) | no |
| EV-0369 | Binet and Field, The Long and the Short of It (IPA) | unknown; IPA and WARC content is paywalled | no |
| EV-0377 | Expo documentation, EAS Update introduction | unknown; no licence stated on the page | no |
| EV-0378 | Kleppmann, Wiggins, van Hardenberg and McGranaghan, `Local-first software: you own your data, in spite of the cloud (Onward! 2019)` | unknown; no explicit licence notice on the essay page, ACM proceedings version under ACM terms | no |
| EV-0383 | PowerSync documentation, Consistency | unknown; no licence stated on the page | no |
| EV-0389 | APCA in a Nutshell (Myndex Research, Advanced Perceptual Contrast Algorithm) | unknown (no reuse licence stated on the documentation page; the algorithm itself is distributed under separate Myndex terms) | no |
| EV-0390 | Adrian Roselli, WCAG3 Contrast as of April 2026 | unknown (personal site, no reuse licence stated) | no |
| EV-0391 | Bateman, Mandryk, Gutwin, Genest, McDine and Brooks, Useful Junk? The Effects of Visual Embellishment on Comprehension and Memorability of Charts (CHI 2010) | unknown (ACM copyright; this is a third-party hosted copy, no reuse licence stated) | no |
| EV-0392 | Dyson and Haselgrove, The influence of reading speed and line length on the effectiveness of reading from screen (International Journal of Human-Computer Studies, 2001) | unknown (Elsevier copyright; abstract page only, paraphrase only) | no |
| EV-0393 | Piepenbrock, Mayr, Buchner, Positive display polarity is advantageous for both younger and older adults (Ergonomics, 2013) | unknown (Taylor and Francis copyright; abstract record only, paraphrase only) | no |
| EV-0397 | Val Head, Designing Safer Web Animation For Motion Sensitivity (A List Apart, issue 428) | unknown (A List Apart retains article copyright; paraphrase only) | no |
| EV-0402 | Lindgaard, Fernandes, Dudek and Brown, Attention web designers: You have 50 milliseconds to make a good first impression (Behaviour and Information Technology, 2006) | unknown (Taylor and Francis copyright; abstract page only, paraphrase only) | no |
| EV-0409 | Mavin, Wilkinson, Harwood and Novak, Easy Approach to Requirements Syntax (EARS), and the official EARS guide | IEEE copyright for the paper; guide site licence not stated, treat as unknown. Paraphrase only | no |
| EV-0432 | Paul Graham, Do Things That Don't Scale | unknown (no licence or copyright notice shown; author copyright assumed, paraphrase only) | no |
| EV-0437 | ASD-STE100 Simplified Technical English, Issue 9 | unknown; the specification PDF is downloadable free from asd-ste100.org after registration, redistribution terms were not verified | no |
| EV-0439 | Plain Language vs Standard Format for Youth Understanding of COVID-19 Recommendations, randomised clinical trial | unknown; PMC open-access article, per-article licence not verified on the page | no |
| EV-0446 | MicrosoftDocs/globalization, How to perform internationalization testing | unknown; public MicrosoftDocs repository, licence file not verified for this path | no |
| EV-0482 | An Experimental Evaluation of the Assumption of Independence in Multiversion Programming (Knight and Leveson) | not-verified; hosted copy, no licence line read | no |
| EV-0483 | Natural Emergent Misalignment from Reward Hacking in Production RL (Anthropic) | not-verified; vendor-hosted PDF | no |
| EV-0496 | Computer Associates International, Inc. v. Altai, Inc., 982 F.2d 693 (2d Cir. 1992), opinion text hosted by BitLaw | unknown (not read at source by this lane) | no |
| EV-0497 | SAS Institute Inc v World Programming Ltd (C-406/10), report and analysis, Society for Computers and Law | unknown (not read at source by this lane) | no |
| EV-0498 | Atari Games Corp. v. Nintendo of America Inc., 975 F.2d 832 (Fed. Cir. 1992), fair use summary published by the United States Copyright Office | unknown (not read at source by this lane; United States Government work) | no |
| EV-0499 | Coders' Rights Project Reverse Engineering FAQ, Electronic Frontier Foundation | unknown (not read at source by this lane) | no |
| EV-0500 | Games registration guidance and Circular 33, Works Not Protected by Copyright, United States Copyright Office | unknown (not read at source by this lane; United States Government work) | no |
| EV-0501 | Tetris Holding, LLC v. Xio Interactive, Inc., 863 F. Supp. 2d 394 (D.N.J. 2012), tertiary summary at the IT Law Wiki | unknown (not read at source by this lane) | no |
| EV-0502 | Apple Computer, Inc. v. Microsoft Corp., 35 F.3d 1435 (9th Cir. 1994), opinion hosted by Justia | unknown (not read at source by this lane) | no |
| EV-0503 | Wal-Mart Stores, Inc. v. Samara Brothers, Inc., 529 U.S. 205 (2000), case summary published by the Berkeley Center for Law and Technology | unknown (not read at source by this lane) | no |
| EV-0504 | Google LLC v. Oracle America, Inc., 141 S. Ct. 1183 (2021), fair use summary published by the United States Copyright Office | unknown (not read at source by this lane; United States Government work) | no |

## Actions the fragments named

One, and it has been done. `packs/coding` and `packs/delivery-testing`
each added the same set of figures on 2026-08-10 with no evidence id
behind it, because the source had not been imported, and each named the
study in prose instead. The two fragments named that source twice, as
FRAG-CODING-21 and as FRAG-DELIVERY-TESTING-14, and asked the import to
bring one in, deduplicate it against the other and cite the assigned id.
The import did exactly that. The source is EV-0480, one row for both
fragment rows, and neither fragment id appears in a pack's read surface
any more.

The tail of it was not a provenance question, and it is closed. Three
passages carrying the figures, in `packs/coding/PACK.md`, in
`packs/coding/guides/GD-COD-001-oracle-strategy.md` and in
`packs/delivery-testing/PACK.md`, went on describing the row as
awaiting import after EV-0480 had landed. That understated what the
ledger held rather than overstating it, which is the harmless
direction, and the correction belonged to those packs. All three now
name the id.

One item is open rather than done, and it is a fetch. The
`packs/legal-licensing` fragment flagged nine rows carried from a
secondary report rather than read at source. They have since been
imported as EV-0496 to EV-0504, and every one of their licence lines
says it was not read at source, so they arrive in table B by their own
admission. Reading them is the work, and re-fetching is the thing this
sweep does not do.

Nothing else in the twenty-one fragments asks anyone to change a line.

## When this goes stale

Compiled from `registry/evidence.json` on 2026-08-10 and re-counted
against it on 2026-08-11, at 504 records both times. It is not a derived
file: no generator writes it and no check compares it against the
ledger, so when the ledger changes somebody has to re-read it. The next
import will change every count above.
