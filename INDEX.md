---
summary: Derived index of every file, one row each, grep the tag column
type: index
tags: [eos]
derived: true
---

# INDEX

Derived file. Edit front-matter, then run
`python tools/eos_check.py --write-index`. One row per file.

| path | type | tags | summary | review_by |
| --- | --- | --- | --- | --- |
| AGENTS.md | root | eos | The v2 router, entry modes, policy-routed mode entry and the never-list |  |
| archive/v1/doctrine/architecture/DOCTRINE.md | doctrine | arch | The seven binding architecture rules, argued by the estate's ADRs and the WG-ARCH wargames |  |
| archive/v1/doctrine/architecture/README.md | doctrine | arch | Architecture module, seven rules and eight wargames from the estate's ADRs |  |
| archive/v1/doctrine/architecture/templates/ADR_TEMPLATE.md | template | arch eos | The ADR format, copy-exact, the record that carries the why |  |
| archive/v1/doctrine/architecture/wargames/WG-ARCH-001-boundary-enforcement.md | wargame | arch tooling | Where do module boundaries live: convention, machine contract, or the directory tree? | 2027-07 |
| archive/v1/doctrine/architecture/wargames/WG-ARCH-002-orm-or-raw-sql.md | wargame | arch data | ORM, query builder, or raw SQL behind repositories? | 2027-07 |
| archive/v1/doctrine/architecture/wargames/WG-ARCH-003-derived-state.md | wargame | arch data state | Derived values: always computed, cached, or stored as immutable snapshots? | 2027-07 |
| archive/v1/doctrine/architecture/wargames/WG-ARCH-004-job-execution.md | wargame | arch state infra | Background jobs: in-process, a durable database queue, or an external broker? | 2027-07 |
| archive/v1/doctrine/architecture/wargames/WG-ARCH-005-contract-seam.md | wargame | arch ci tooling | How do frontend and backend share types: by hand, generated with a drift gate, or one language? | 2027-07 |
| archive/v1/doctrine/architecture/wargames/WG-ARCH-006-change-proof.md | wargame | arch testing ci | What proves a change changed nothing: green tests, pinned behaviour, or byte-stable output? | 2027-07 |
| archive/v1/doctrine/architecture/wargames/WG-ARCH-007-vendor-seams.md | wargame | arch infra security | Vendor integration: their SDK everywhere, an owned adapter, or the raw protocol? | 2027-07 |
| archive/v1/doctrine/architecture/wargames/WG-ARCH-008-database-topology.md | wargame | arch data infra | One shared database, one per service, or a records core with a separate high-volume store? | 2027-07 |
| archive/v1/doctrine/delivery/DOCTRINE.md | doctrine | delivery testing ci | The six binding delivery rules, test-first by type, ratchets, rubric gates, determinism |  |
| archive/v1/doctrine/delivery/README.md | doctrine | delivery | Delivery module, six rules and four wargames on proof, gates and determinism |  |
| archive/v1/doctrine/delivery/wargames/WG-DEL-001-coverage-level.md | wargame | delivery testing ci | What coverage floor, per surface, and how does it move? | 2027-07 |
| archive/v1/doctrine/delivery/wargames/WG-DEL-002-e2e-weighting.md | wargame | delivery testing ci | How much end-to-end, and which branch does it block? | 2027-07 |
| archive/v1/doctrine/delivery/wargames/WG-DEL-003-vrt-scope.md | wargame | delivery testing web | Visual regression: nothing, component states, or full pages? | 2027-07 |
| archive/v1/doctrine/delivery/wargames/WG-DEL-004-flake-policy.md | wargame | delivery testing ci | When a test flakes: retry, quarantine, or root-cause now? | 2027-07 |
| archive/v1/doctrine/devops/DOCTRINE.md | doctrine | ops | The six binding devops rules, migrations, parity, secrets, runbooks, restores, cost |  |
| archive/v1/doctrine/devops/README.md | doctrine | ops | Devops module, six rules and four wargames on hosting, artefacts, restores and spend |  |
| archive/v1/doctrine/devops/wargames/WG-OPS-001-hosting.md | wargame | ops hosting infra | Managed PaaS, a cloud estate under contract, or self-hosting? | 2027-07 |
| archive/v1/doctrine/devops/wargames/WG-OPS-002-containers.md | wargame | ops infra hosting | Everything in containers, platform-native builds, or a mixed fleet? | 2027-07 |
| archive/v1/doctrine/devops/wargames/WG-OPS-003-backups-and-restore.md | wargame | ops data infra | Trusted snapshots, scheduled restore tests, or full disaster rehearsal? | 2027-07 |
| archive/v1/doctrine/devops/wargames/WG-OPS-004-cost-ceilings.md | wargame | ops infra money | How is spend governed: unwatched, budget-gated, or hard-capped? | 2027-07 |
| archive/v1/doctrine/MODULE_SHAPE.md | governance | eos | What every doctrine module must have, may have, and must never become |  |
| archive/v1/doctrine/README.md | governance | eos | The module map, what is populated, what is queued, and the extraction mandates |  |
| archive/v1/doctrine/voice/DOCTRINE.md | doctrine | voice | The voice law, seven rules with examples, and the banned-list pattern |  |
| archive/v1/doctrine/voice/README.md | doctrine | voice | Voice module, the writing law and the register wargame, compiled into every seed |  |
| archive/v1/doctrine/voice/wargames/WG-VOX-001-audience-register.md | wargame | voice content brand | Which register does this surface speak in? | 2027-07 |
| archive/v1/doctrine/WARGAME_INDEX.md | index | eos wargame | Derived index of every wargame, the surface inception walks |  |
| archive/v1/doctrine/web-design/DOCTRINE.md | doctrine | web | The twelve binding rules for any PatterTech web surface |  |
| archive/v1/doctrine/web-design/foundations/COLOR.md | foundation | web colour | Deriving the surface ladder, accents and measured text tiers |  |
| archive/v1/doctrine/web-design/foundations/LAYOUT_AND_GRID.md | foundation | web layout | The reading grid, measures and bleeds that kill drift |  |
| archive/v1/doctrine/web-design/foundations/LIGHT.md | foundation | web colour motion | The graded light system, field to radiance, with budgets |  |
| archive/v1/doctrine/web-design/foundations/MOTION.md | foundation | web motion | Motion with meaning, reveals, easing and reduced-motion duty |  |
| archive/v1/doctrine/web-design/foundations/TYPOGRAPHY.md | foundation | web typography | Choosing and proving the three faces, scales and measures |  |
| archive/v1/doctrine/web-design/implementation/AGENT_WORKFLOW.md | implementation | web tooling | How an agent works a web project without breaking it |  |
| archive/v1/doctrine/web-design/implementation/QC_GATES.md | implementation | web testing tooling | The executable gates and when each runs |  |
| archive/v1/doctrine/web-design/implementation/TOKENS.md | implementation | web tooling brand | Three token layers and the mirroring contract |  |
| archive/v1/doctrine/web-design/patterns/CONTAINERS.md | pattern | web layout density | Ledger, plaque, panel, table or prose, chosen by content |  |
| archive/v1/doctrine/web-design/patterns/DIAGRAMS.md | pattern | web media | Diagram kit rules, positions from data, labels that never overlap |  |
| archive/v1/doctrine/web-design/patterns/LONGFORM.md | pattern | web content layout | The long-read kit, pacing and numbering as identity |  |
| archive/v1/doctrine/web-design/patterns/MEDIA.md | pattern | web media | Figures, carousels, video facades, audio and document panels |  |
| archive/v1/doctrine/web-design/patterns/NAVIGATION.md | pattern | web nav | Header, footer and index patterns, the journal threading model |  |
| archive/v1/doctrine/web-design/patterns/SECTION_FURNITURE.md | pattern | web layout | Section marks, chapter marks, colophons and the andon line |  |
| archive/v1/doctrine/web-design/templates/REVIEW_CHECKLIST.md | template | web testing | Evidence-based review checklist before shipping |  |
| archive/v1/doctrine/web-design/templates/WG_TEMPLATE.md | template | eos wargame | Copy-exact template for a new wargame in any module |  |
| archive/v1/doctrine/web-design/ux/ACCESSIBILITY.md | ux | web a11y | The accessibility floor, skip link to reduced motion |  |
| archive/v1/doctrine/web-design/ux/FLOWS.md | ux | web nav content | The five page archetypes and their linking strategy |  |
| archive/v1/doctrine/web-design/ux/PERFORMANCE.md | ux | web perf | Budgets and the structural choices that keep pages light |  |
| archive/v1/doctrine/web-design/wargames/WG-WEB-001-surface-register.md | wargame | web colour brand | Dark, light, or dual register? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-002-page-archetype.md | wargame | web nav content | Which vocabulary does this page speak? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-003-container-choice.md | wargame | web layout density | Card, ledger, plaque, table or prose? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-004-motion-budget.md | wargame | web motion | How much may this project move? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-005-ornament-budget.md | wargame | web colour motion brand | How much light does this project carry? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-006-density-and-audience.md | wargame | web density content | How dense, for whom? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-007-static-vs-server.md | wargame | web hosting infra state | Static export or a server? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-008-media-pipeline.md | wargame | web media perf | How do images get to the page? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-009-brand-family-accents.md | wargame | web brand colour | One brand or a family of accents? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-010-type-pairing.md | wargame | web typography brand | How to pick the type trio? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-011-surface-reactivity-budget.md | wargame | web motion perf | Should the surface react to presence? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-012-literal-vs-generated-imagery.md | wargame | web imagery brand | Literal imagery or generated fields? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-013-kit-escape-and-enforcement.md | wargame | web tooling testing | Where does a design law live so it actually holds? | 2027-07 |
| archive/v1/doctrine/web-design/wargames/WG-WEB-014-media-in-longform.md | wargame | web media layout content | Is a media block a citation or a monument? | 2027-07 |
| archive/v1/GUIDE.md | guide | eos | The all-in-one guide to the EOS, the Venture A genesis and the development lifecycle | 2027-01 |
| archive/v1/kernel/SCALE_MATRIX.md | kernel | eos | The exact seed file list per scale S, M and L, plus trigger add-ons, machine-checked |  |
| archive/v1/org/CADENCE.md | org | eos | The EOS heartbeat, what recurs, how often, and when each last ran |  |
| archive/v1/org/QUEUE.md | org | eos | The ordered build queue for the EOS, phases B to F and the release |  |
| archive/v1/org/STATE.md | org | eos | Live state of the EOS itself, the active session claim and the Resume Packet |  |
| archive/v1/START.md | root | eos | Bootstrap for every session, read order per entry mode and the ground rules |  |
| archive/v1/VISION.md | root | eos | The north star, what the EOS is for and the invariants that hold as it grows |  |
| benchmark/drills/agentic-development.md | example | eos | Cold-agent acceptance drill for the agentic development pack, topology selection under pressure |  |
| benchmark/drills/api-integration.md | example | eos | Single-run cold-agent acceptance drill for the API and integration pack, with deterministic machine-checkable criteria. |  |
| benchmark/drills/architecture.md | example | eos | Single-run cold-agent acceptance drill for the architecture pack, with deterministic machine-checkable criteria |  |
| benchmark/drills/coding.md | example | eos | Cold-agent acceptance drill for the coding pack, pin then change an undocumented parser |  |
| benchmark/drills/delivery-testing.md | example | eos | Cold-agent acceptance drill for the delivery, testing and quality pack, checking double choice, contract verification and flake handling |  |
| benchmark/drills/devops-reliability.md | example | eos | Single-run cold-agent acceptance drill for the devops-reliability pack, with deterministic machine-checkable criteria. |  |
| benchmark/drills/security-privacy.md | example | eos | Proposed cold-agent acceptance drill for the security, privacy and safety pack |  |
| benchmark/drills/ui-ux.md | example | eos | Cold-agent acceptance drill for the ui-ux pack, two philosophies, one behaviour core, machine-checked |  |
| benchmark/fixtures/app-api/README.md | example | eos testing | Energy quote JSON API fixture with planted defects for benchmark tasks |  |
| benchmark/fixtures/app-static/README.md | example | eos testing | Static brochure site fixture with three planted defects for the agent benchmark |  |
| benchmark/fixtures/briefs/BRIEF-M-fieldkit.md | example | eos testing | Canned drill brief, a field-survey web app for one contractor firm, scripted operator answers |  |
| benchmark/fixtures/eos-mini/AGENTS.md | root | eos | Router for the eos-mini fixture, a tiny EOS-style repo used by benchmark tasks |  |
| benchmark/fixtures/eos-mini/CLAUDE.md | root | eos | Router for the eos-mini fixture, a tiny EOS-style repo used by benchmark tasks |  |
| benchmark/fixtures/eos-mini/doctrine/mini/DOCTRINE.md | doctrine | web | Settled doctrine for the mini module, page weight and image delivery |  |
| benchmark/fixtures/eos-mini/doctrine/mini/guidance/IMAGES.md | doctrine | web content | Page-level guidance on serving images for the mini module |  |
| benchmark/fixtures/eos-mini/doctrine/mini/README.md | doctrine | web | Map of the mini doctrine module, one page of guidance and two wargames |  |
| benchmark/fixtures/eos-mini/doctrine/mini/wargames/WG-MINI-001-page-weight.md | wargame | web | How heavy may a page be before the build must push back? | 2027-08 |
| benchmark/fixtures/eos-mini/doctrine/mini/wargames/WG-MINI-002-image-formats.md | wargame | web content | Which formats and sizes do we serve images in? | 2027-08 |
| benchmark/fixtures/eos-mini/doctrine/WARGAME_INDEX.md | index | eos wargame | Derived index of every wargame, the surface inception walks |  |
| benchmark/fixtures/eos-mini/GOVERNANCE.md | governance | eos | The law of eos-mini, front-matter schema excerpt, tag vocabulary and the supersession rule |  |
| benchmark/fixtures/eos-mini/INDEX.md | index | eos | Derived index of every file, one row each, grep the tag column |  |
| benchmark/fixtures/eos-mini/org/STATE.md | org | eos | Org state for eos-mini, which session is active and where work stands |  |
| benchmark/fixtures/seed-v1-M/AGENTS.md | template | eos | FieldKit agent entry point, the M-scale router into the org files |  |
| benchmark/fixtures/seed-v1-M/CLAUDE.md | template | eos | FieldKit agent entry point, the M-scale router into the org files |  |
| benchmark/fixtures/seed-v1-M/docs/COMPILE_REPORT.md | template | eos | FieldKit compile report, the seed's ancestry proof and sign-off record |  |
| benchmark/fixtures/seed-v1-M/docs/EOS_FEEDBACK.md | template | eos | FieldKit feedback file, the one channel back to the EOS, harvested monthly |  |
| benchmark/fixtures/seed-v1-M/docs/LOCKBOOK.md | template | eos | FieldKit lock-book, the M-scale rulings and contracts with the EOS |  |
| benchmark/fixtures/seed-v1-M/docs/VENTURE_BRIEF.md | template | eos | FieldKit venture brief, a field-survey web app for one contractor firm, the business truth |  |
| benchmark/fixtures/seed-v1-M/OPERATORS_GUIDE.md | template | eos | FieldKit operators guide, the owner's manual and M-scale launcher library |  |
| benchmark/fixtures/seed-v1-M/org/CADENCE.md | template | eos | FieldKit recurring sessions, the heartbeat schedule and the rules that keep it honest |  |
| benchmark/fixtures/seed-v1-M/org/CONSTITUTION.md | template | eos | The FieldKit constitution, product doctrine and the protected organisational law |  |
| benchmark/fixtures/seed-v1-M/org/OPERATING_MODEL.md | template | eos | The FieldKit operating model, work types, risk tiers and gates, knowledge, cadences, humans |  |
| benchmark/fixtures/seed-v1-M/org/QUESTIONS.md | template | eos | FieldKit human decision queue, open questions for the operator and the folding rule |  |
| benchmark/fixtures/seed-v1-M/org/QUEUE.md | template | eos | FieldKit queue, the single ordered work file, rows per the templates contract |  |
| benchmark/fixtures/seed-v1-M/org/roles/PLAN.md | template | eos | FieldKit PLAN charter, decides what and why, encodes work a cold session can run unaided |  |
| benchmark/fixtures/seed-v1-M/org/roles/VERIFY.md | template | eos | FieldKit VERIFY charter, independent review and audit, findings not fixes, evidence not vibes |  |
| benchmark/fixtures/seed-v1-M/org/roles/WORK.md | template | eos | FieldKit WORK charter, changes things under an order, small batches, immaculate paper trail |  |
| benchmark/fixtures/seed-v1-M/org/START.md | template | eos | FieldKit worker bootstrap, the read order per role, ground rules and the close-out ritual |  |
| benchmark/fixtures/seed-v1-M/org/STATE.md | template | eos | FieldKit live state, the session claim line, live sections and the Resume Packet |  |
| benchmark/fixtures/seed-v1-M/org/TEMPLATES.md | template | eos | FieldKit canonical artefact formats, front-matter contracts for queue rows, decisions and logs |  |
| benchmark/fixtures/seed-v1-S/AGENTS.md | template | eos | Herbfield Lane agent entry point, the S-scale router into the venture files |  |
| benchmark/fixtures/seed-v1-S/CLAUDE.md | template | eos | Herbfield Lane agent entry point, the S-scale router into the venture files |  |
| benchmark/fixtures/seed-v1-S/docs/COMPILE_REPORT.md | template | eos | Herbfield Lane compile report, the seed's ancestry proof and sign-off record |  |
| benchmark/fixtures/seed-v1-S/docs/EOS_FEEDBACK.md | template | eos | Herbfield Lane feedback file, the one channel back to the EOS, harvested monthly |  |
| benchmark/fixtures/seed-v1-S/docs/LOCKBOOK.md | template | eos | Herbfield Lane lock-book, the S-scale rulings and contracts with the EOS |  |
| benchmark/fixtures/seed-v1-S/docs/VENTURE_BRIEF.md | template | eos | Herbfield Lane venture brief, a sole-trader joinery brochure site, the business truth |  |
| benchmark/fixtures/seed-v1-S/docs/WORKLOG.md | template | eos | Herbfield Lane worklog, the S-scale single running log and open-items list |  |
| benchmark/fixtures/seed-v1-S/OPERATORS_GUIDE.md | template | eos | Herbfield Lane operators guide, the sole trader's manual and S-scale launcher library |  |
| benchmark/fixtures/seed-v2-ORG/AGENTS.md | template | eos | FieldKit agent entry point, the ORG-scale router into the organisation files |  |
| benchmark/fixtures/seed-v2-ORG/CLAUDE.md | template | eos | FieldKit agent entry point, the ORG-scale router into the organisation files |  |
| benchmark/fixtures/seed-v2-ORG/docs/COMPILE_REPORT.md | template | eos | FieldKit compile report, the seed's ancestry proof and sign-off record |  |
| benchmark/fixtures/seed-v2-ORG/docs/EOS_FEEDBACK.md | template | eos | FieldKit feedback file, the one channel back to the EOS, harvested monthly |  |
| benchmark/fixtures/seed-v2-ORG/docs/LOCKBOOK.md | template | eos | FieldKit lock-book, the ORG-scale rulings and contracts with the EOS |  |
| benchmark/fixtures/seed-v2-ORG/docs/VENTURE_BRIEF.md | template | eos | FieldKit venture brief, a field-survey web app for one contractor firm, the business truth |  |
| benchmark/fixtures/seed-v2-ORG/OPERATORS_GUIDE.md | template | eos | FieldKit operators guide, the human's manual and the ORG-scale launcher library |  |
| benchmark/fixtures/seed-v2-ORG/org/CONSTITUTION.md | template | eos | The FieldKit constitution, Part I product doctrine, Parts II and III the protected law |  |
| benchmark/fixtures/seed-v2-ORG/org/PLAYBOOKS.md | template | eos | FieldKit playbooks, per-mode procedures plus hardening, incident, upkeep and retro |  |
| benchmark/fixtures/seed-v2-ORG/org/QUESTIONS.md | template | eos | FieldKit human decision queue, open questions for the operator and the folding rule |  |
| benchmark/fixtures/seed-v2-ORG/org/roles/EXECUTOR.md | template | eos | FieldKit EXECUTOR charter, the default owner who plans, implements, tests and documents |  |
| benchmark/fixtures/seed-v2-ORG/org/roles/ORACLE.md | template | eos | FieldKit ORACLE charter, independent gate-test author for high-assurance work |  |
| benchmark/fixtures/seed-v2-ORG/org/roles/REVIEWER.md | template | eos | FieldKit REVIEWER charter, acceptance judgement, sampled review and bounded repair |  |
| benchmark/fixtures/seed-v2-ORG/org/START.md | template | eos | FieldKit session boot, per-mode budgets, ground rules, close only when exceptional |  |
| benchmark/fixtures/seed-v2-ORG/org/TEMPLATES.md | template | eos | FieldKit canonical artefact shapes, task records, spikes, ADRs, questions, incidents |  |
| benchmark/fixtures/seed-v2-ORG/org/TESTING.md | template | eos | FieldKit adaptive testing law, timing by change class, the test map, quality signals |  |
| benchmark/fixtures/seed-v2-S/AGENTS.md | template | eos | Herbfield Lane agent entry point, the S-scale router into the venture files |  |
| benchmark/fixtures/seed-v2-S/CLAUDE.md | template | eos | Herbfield Lane agent entry point, the S-scale router into the venture files |  |
| benchmark/fixtures/seed-v2-S/docs/COMPILE_REPORT.md | template | eos | Herbfield Lane compile report, the seed's ancestry proof and sign-off record |  |
| benchmark/fixtures/seed-v2-S/docs/EOS_FEEDBACK.md | template | eos | Herbfield Lane feedback file, the one channel back to the EOS, harvested monthly |  |
| benchmark/fixtures/seed-v2-S/docs/LOCKBOOK.md | template | eos | Herbfield Lane lock-book, the S-scale rulings and contracts with the EOS |  |
| benchmark/fixtures/seed-v2-S/docs/TASKS.md | template | eos | Herbfield Lane task list, the S-scale work surface, open items, questions and log |  |
| benchmark/fixtures/seed-v2-S/docs/VENTURE_BRIEF.md | template | eos | Herbfield Lane venture brief, a sole-trader joinery brochure site, the business truth |  |
| benchmark/fixtures/seed-v2-S/OPERATORS_GUIDE.md | template | eos | Herbfield Lane operators guide, the sole trader's manual and S-scale launcher library |  |
| benchmark/holdout/app-api/README.md | example | eos testing | Holdout tests for the app-api fixture, scored after tasks, never shown to agents |  |
| benchmark/PROTOCOL.md | example | eos testing | Frozen benchmark protocol for the EOS v1 versus v2 comparison, session counts, gates, custody and budget |  |
| benchmark/README.md | example | eos testing | How to run and score one benchmark session, the run_meta.json contract, and the honesty rules |  |
| CHANGELOG.md | governance | eos | One entry per release tag, sectioned by area |  |
| CLAUDE.md | root | eos | The v2 router, entry modes, policy-routed mode entry and the never-list |  |
| estate/ESTATE_MAP.md | registry | eos | The estate narrative, how the repos relate, which are governed and what the seams between them are | 2026-11 |
| examples/venture-a-seed.md | example | eos | Worked example, the Venture A reseed, the first L-scale compile from the kernel |  |
| examples/pattertech-website.md | example | web brand | Worked example, the PatterTech website redesign v1 to v4 |  |
| GOVERNANCE.md | governance | eos | The law of the EOS, the graded change path, precedence, promotion, the protected set, ids, budgets |  |
| inception/briefs/BRIEF-S-brochure.md | kernel | eos | Canned drill brief, a sole-trader joinery brochure site, scripted operator answers |  |
| inception/COMPILE.md | kernel | eos | The seed compiler's rules, prune, fill, distil, report, and the never-list |  |
| inception/INCEPTION.md | kernel | eos | The Session 0 master playbook, phases A to E, from idea to signed seed |  |
| inception/INTERVIEW.md | kernel | eos | The intake protocol, question set and the three mandatory challenge steps |  |
| inception/README.md | kernel | eos | The Session 0 system, what it is and what lands here in Phase E |  |
| inception/WALK_ORDER.md | kernel | eos wargame | How to compile the venture's wargame walk from the index, filter by triggers, canonical order |  |
| inception/wargames/WG-EOS-001-venture-scale.md | wargame | eos wargame | What scale of organisational machinery does this venture compile, S, M or L? | 2027-07 |
| inception/wargames/WG-EOS-002-repo-shape.md | wargame | eos wargame infra | One repo, several, or a corner of an existing one? | 2027-07 |
| kernel/GUARD_SPEC.md | kernel | eos | The action-time guard, ten guarded classes, four verdicts, non-waivable floors, fail closed |  |
| kernel/METADATA_SPEC.md | kernel | eos | The eight metadata axes, per-kind required minima, derived defaults and compatibility rules |  |
| kernel/POLICY_SPEC.md | kernel | eos | The risk model law, the semantic factor table, tier routing, exceptions and recomputation |  |
| kernel/README.md | kernel | eos | The kernel in v2, the law files, the compile contract and the current staging state |  |
| kernel/SCALE_MATRIX.md | kernel | eos | The v2 seed law, the S and ORG file lists, first-use directories, trigger add-ons |  |
| kernel/SEED_RUBRIC.md | kernel | eos | The pass gate for a compiled seed, auto items keyed to v2 checker ids, human items headed by cold-start |  |
| kernel/templates/AGENTS.tpl.md | template | eos | Venture router template, the policy-routed v2 entry, compiled output capped at 40 lines |  |
| kernel/templates/COMPILE_REPORT.tpl.md | template | eos | Compile report template, the seed's ancestry proof and the rubric sign-off record |  |
| kernel/templates/EOS_FEEDBACK.tpl.md | template | eos | Venture feedback file template, the one channel back to the EOS, harvested monthly |  |
| kernel/templates/LOCKBOOK.tpl.md | template | eos | Venture lock-book template, the machine rulings header and the module contract sections |  |
| kernel/templates/OPERATORS_GUIDE.tpl.md | template | eos | Venture operators guide template, the human's manual, v2 launcher library per scale |  |
| kernel/templates/org/CONSTITUTION.tpl.md | template | eos | Venture constitution template, Part I product slot, Parts II and III the protected v2 law |  |
| kernel/templates/org/PLAYBOOKS.tpl.md | template | eos | Venture playbook template, per-mode procedures plus hardening, incident, upkeep and retro |  |
| kernel/templates/org/QUESTIONS.tpl.md | template | eos | Questions template, the human decision queue and its folding rule |  |
| kernel/templates/org/roles/EXECUTOR.tpl.md | template | eos | EXECUTOR charter template, the default owner who plans, implements, tests and documents |  |
| kernel/templates/org/roles/ORACLE.tpl.md | template | eos | ORACLE charter template, independent gate-test author for high-assurance work |  |
| kernel/templates/org/roles/REVIEWER.tpl.md | template | eos | REVIEWER charter template, acceptance judgement, sampled review and bounded repair |  |
| kernel/templates/org/START.tpl.md | template | eos | Venture boot template, per-mode budgets, ground rules, close only when exceptional |  |
| kernel/templates/org/TEMPLATES.tpl.md | template | eos | Canonical artefact shapes template, task records, spikes, ADRs, questions, incidents |  |
| kernel/templates/org/TESTING.tpl.md | template | eos | Adaptive testing law template, timing by change class, the test map, quality signals |  |
| kernel/templates/TASKS.tpl.md | template | eos | S-scale task list template, the single hand-kept work surface at the smallest scale |  |
| kernel/templates/VENTURE_BRIEF.tpl.md | template | eos | Venture brief template, the business truth the interview produces, challenge steps recorded |  |
| OPERATORS_GUIDE.md | guide | eos | Daniel's manual for running the EOS, launchers, approval duties, the guard, cadences and what to do when something looks wrong | 2027-03 |
| org/CADENCE.md | org | eos | Pointer, the EOS heartbeat is machine state in org/cadence.json |  |
| org/decisions/ADR-0001-eos-v1-architecture.md | decision | eos | The founding decision, PatterTech EOS v1.0 architecture and the argument for it |  |
| org/decisions/ADR-0002-eos-v2-adaptive-agentic-development.md | decision | eos | EOS v2 architecture, adaptive agentic development, accepted with eight binding clarifications |  |
| org/deviations.md | org | eos | Append-only implementation-deviation log for the EOS v2 build, per ADR-0002 |  |
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
| org/logs/2026-07/S-0012.md | org | eos | Session S-0012, item R1, the FastAPI and full-stack profiles extracted from WiseWattage |  |
| org/logs/2026-07/S-0013.md | org | eos | Session S-0013, Phase F item F1, the architecture module populated |  |
| org/logs/2026-07/S-0014.md | org | eos | Session S-0014, Phase F item F2, the delivery module populated |  |
| org/logs/2026-07/S-0015.md | org | eos | Session S-0015, Phase F item F3, the devops module populated, Phase F complete |  |
| org/logs/2026-07/S-0016.md | org | eos | Session S-0016, item E3, the S-scale ergonomics from the drill findings |  |
| org/logs/2026-07/S-0017.md | org | eos | Session S-0017, item E4, four web decision rules sharpened for non-house brands |  |
| org/logs/2026-07/S-0018.md | org | eos | Session S-0018, REL, v1.0.0 tagged locally, manual close handed to Daniel |  |
| org/logs/2026-07/S-0019.md | org | eos | Session S-0019, the D1 gate closed, G1 and G2 queued, Genesis commissioned |  |
| org/logs/2026-07/S-0020.md | org | eos | Session S-0020, the all-in-one field guide GUIDE.md authored and registered |  |
| org/PLAYBOOKS.md | org | eos | The EOS-side playbooks, PB-E01 to PB-E10, one v2 procedure each |  |
| org/QUEUE.md | org | eos | Pointer, the queue is now per-task records in org/tasks with a derived TASKS view |  |
| org/STATE.md | org | eos | Derived state view of claims, operator flags, cadence and machine facts |  |
| org/TASKS.md | org | eos | Derived task table, one row per record under org/tasks/ |  |
| packs/agentic-development/CHECKS.md | guide | eos arch delivery | What a reviewer or checker can verify about agent workflow design, split into executable today and judgement | 2027-10 |
| packs/agentic-development/exemplars/EX-AGENT-001-logging-migration.md | example | eos arch tooling | Worked topology decision record for a coupled logging migration across one service, and why fan-out was refused |  |
| packs/agentic-development/guides/GD-AGENT-001-topology-selection.md | guide | eos arch tooling | Which of the ten agent topologies does this work need, and what pressure justifies promoting past a single agent? | 2027-03 |
| packs/agentic-development/guides/GD-AGENT-002-context-engineering.md | guide | eos arch tooling | How does context reach an agent, and what happens when the window runs out? | 2027-06 |
| packs/agentic-development/guides/GD-AGENT-003-spawn-a-subagent.md | guide | eos arch tooling | Should this work be a subagent at all, and if so as a tool, a handoff or a peer worker? | 2027-06 |
| packs/agentic-development/guides/GD-AGENT-004-verification-oracle.md | guide | eos delivery tooling | What holds the truth that checks an agent's work, and what do you do when nothing does? | 2027-06 |
| packs/agentic-development/PACK.md | guide | eos arch tooling | Which agent topology to run, the invariants that bind every one of them, and how to bound, verify and trace a run | 2027-03 |
| packs/agentic-development/refs/DECISION_RECORD_SHAPE.md | guide | eos arch tooling | The six-section shape of a topology decision record, and what each section must contain | 2027-10 |
| packs/agentic-development/refs/INVARIANTS_AND_BOUNDS.md | guide | eos arch tooling | How to bound a run, trace it, resume it safely, and where the estate's policy and guard take over | 2027-06 |
| packs/agentic-development/refs/TOPOLOGY_CARD.md | guide | eos arch tooling | The ten topologies by canonical name, the pressure that licenses each, and the evidence behind it | 2027-03 |
| packs/agentic-development/research/DRILL_PROPOSAL.md | example | eos | Cold-agent acceptance drill for the agentic development pack, topology selection under pressure |  |
| packs/agentic-development/research/NOTES.md | example | eos | Research synthesis for the agentic development and orchestration pack, topologies, context, tools, checkpoints, guardrails |  |
| packs/api-integration/CHECKS.md | guide | delivery ci testing | What a reviewer or checker can verify about API and integration work, split into what runs today and what needs judgement | 2028-02 |
| packs/api-integration/exemplars/invoices-api-change.md | example | arch money security | A worked change to a live invoices API and its payment webhook, applying the pack end to end from activation to merge |  |
| packs/api-integration/exemplars/stripe-versioning.md | example | arch money delivery | Stripe's pinned-date versioning read as an exemplar, what it actually costs, and the conditions under which copying it is right |  |
| packs/api-integration/guides/GD-API-001-contract-authoring.md | guide | arch tooling ci | Who writes the contract and when: by hand, in a definition language, generated from the handlers, or not at all? | 2027-11 |
| packs/api-integration/guides/GD-API-002-versioning-and-breaking-change.md | guide | arch ci delivery | How is a boundary allowed to change: add only, declared tier plus gate, explicit version parameter, or pinned date with transformers? | 2027-04 |
| packs/api-integration/guides/GD-API-003-webhook-trust.md | guide | security money arch | How is an inbound webhook trusted: bare-body HMAC, a signed triple, RFC 9421 message signatures, or an asymmetric or provider-native scheme? | 2028-01 |
| packs/api-integration/guides/GD-API-004-boundary-shape.md | guide | arch state realtime | What shape does a boundary take: REST over OpenAPI, typed RPC, an event stream, or GraphQL? | 2027-06 |
| packs/api-integration/guides/GD-API-005-collection-traversal.md | guide | arch perf data | How does a consumer walk a collection: offset paging, opaque cursors, visible keyset, or a hybrid with an estimated total? | 2027-09 |
| packs/api-integration/PACK.md | guide | arch security money | Binding requirements, defaults and decision guides for API contracts, webhooks, event payloads and integration change | 2027-12 |
| packs/api-integration/refs/breaking-change-catalogue.md | example | arch ci delivery | What counts as a breaking change, the compatibility tiers and modes available, and how the gate is wired |  |
| packs/api-integration/refs/error-and-limits.md | example | arch content | The error envelope, rate limit advertisement and deprecation signalling a boundary carries, with the contested parts marked |  |
| packs/api-integration/refs/idempotency-parameters.md | example | money state | The four decisions an idempotency header does not make, and how they are settled on money-touching paths |  |
| packs/api-integration/refs/webhook-verification.md | example | security money | The verification order, tolerance, rotation and replay controls a webhook receiver needs, with the provider variance that defeats a single implementation |  |
| packs/api-integration/research/DRILL_PROPOSAL.md | example | eos | Single-run cold-agent acceptance drill for the API and integration pack, with deterministic machine-checkable criteria. |  |
| packs/api-integration/research/NOTES.md | example | eos | Decision-relevant synthesis for the API and integration pack, covering contract style, versioning philosophy, webhook security, idempotency and pagination, with the disagreements between mature estates left visible. |  |
| packs/architecture/CHECKS.md | example | arch ci tooling | What a reviewer or checker can verify about architecture work, split into what is executable today and what stays a judgement call |  |
| packs/architecture/exemplars/billing-catalogue-boundary.md | example | arch tooling ci | The pack applied end to end to a two-module Python repo where billing may read the catalogue and the catalogue must never know about billing |  |
| packs/architecture/guides/GD-ARCH-001-deployment-shape.md | guide | arch infra | One deployable, several deployables, or contract-shaped seams inside one process | 2027-03 |
| packs/architecture/guides/WG-ARCH-001-boundary-enforcement.md | guide | arch tooling ci | Where module boundaries live, whether convention, a machine contract, the directory tree, or a runtime call graph | 2026-12 |
| packs/architecture/guides/WG-ARCH-007-vendor-seams.md | guide | arch security money | How deep a vendor is allowed into the codebase, whether SDK throughout, an owned adapter, the raw protocol, or a generated client | 2027-01 |
| packs/architecture/guides/WG-ARCH-008-database-topology.md | guide | arch data infra | Where data rests, whether one shared database, private tables with distinct credentials, one store per deployable, or a records core with a separate readings store | 2027-06 |
| packs/architecture/PACK.md | guide | arch data infra tooling ci | Architecture pack for boundaries declared and machine-checked, decisions recorded as ADRs, and one deployable with one database until measured evidence says otherwise | 2027-02 |
| packs/architecture/refs/architecture-description.md | example | arch content | The MADR heading set, the C4 levels worth authoring, the arc42 sections worth borrowing, and the ISO 42010 vocabulary behind them |  |
| packs/architecture/refs/boundary-tooling.md | example | arch tooling ci | Contract shapes, config skeletons and known blind spots for import-linter, dependency-cruiser and ArchUnit, plus how each is wired into a build |  |
| packs/architecture/refs/evidence-map.md | example | arch content | Which evidence row supports which requirement, what population it observed, and where its licence limits reuse to paraphrase |  |
| packs/architecture/research/DRILL_PROPOSAL.md | example | eos | Single-run cold-agent acceptance drill for the architecture pack, with deterministic machine-checkable criteria |  |
| packs/architecture/research/NOTES.md | example | eos | What the evidence supports for the architecture pack, three contrasting philosophies with fit conditions, and the binding versus default versus preference split |  |
| packs/coding/CHECKS.md | guide | delivery ci tooling | What a reviewer or a checker can verify about coding work, split into executable today and judgement | 2027-05 |
| packs/coding/exemplars/EX-COD-001-webhook-silent-failure.md | example | delivery testing | The coding pack applied end to end to a webhook receiver that swallows a signature failure and returns success |  |
| packs/coding/guides/GD-COD-001-oracle-strategy.md | guide | testing delivery wargame | Where does the oracle for this change come from, test-first, characterisation, contract or downstream gate? | 2027-05 |
| packs/coding/guides/GD-COD-002-review-gate.md | guide | delivery ci wargame | Who reviews a change and how hard, from machine gate only to independent human review at every merge | 2027-02 |
| packs/coding/guides/GD-COD-003-failure-mode-contract.md | guide | arch delivery wargame | How do callers learn a call failed, opaque errors, one sentinel, a declared taxonomy or typed results? | 2028-02 |
| packs/coding/guides/GD-COD-004-pin-then-change.md | guide | testing delivery wargame | How do you change code nobody can specify, read carefully, pin behaviour, reconstruct a spec or rewrite behind a contract? | 2027-10 |
| packs/coding/guides/GD-COD-005-repo-shape.md | guide | arch delivery wargame | One repository or several, and how the trunk flows through whichever you pick | 2027-08 |
| packs/coding/PACK.md | playbook | eos delivery testing | How code is written and accepted in a venture repo, oracles, pinning, error paths and the merge gate |  |
| packs/coding/refs/ERROR_PATH.md | foundation | delivery testing | The error-path reference, what counts as handled, how failures are declared, and the checks that catch a swallow | 2028-02 |
| packs/coding/refs/ORACLES.md | foundation | testing delivery | Which oracle each change type needs, what counts as one, and the commit order that proves it came first | 2027-05 |
| packs/coding/refs/REVIEW_GATE.md | foundation | delivery ci | What the machine gate must contain, how findings are split, and how a human reads a diff when one does | 2027-02 |
| packs/coding/research/DRILL_PROPOSAL.md | example | eos | Cold-agent acceptance drill for the coding pack, pin then change an undocumented parser |  |
| packs/coding/research/NOTES.md | example | eos | Research synthesis for the coding pack, four construction philosophies, review at scale, and what should bind |  |
| packs/delivery-testing/CHECKS.md | guide | delivery testing ci | What a reviewer or a checker can verify about delivery and testing work, and which checks run today | 2027-08 |
| packs/delivery-testing/exemplars/EX-DEL-001-drifted-fake-and-a-lying-suite.md | example | delivery testing ci | A worked run of the pack: a rounding defect, a drifted fake and a clock-dependent test, fixed in order |  |
| packs/delivery-testing/guides/WG-DEL-005-test-doubles.md | guide | delivery testing arch | Which double stands in for this port: real, container, verified fake, or mock? | 2027-08 |
| packs/delivery-testing/guides/WG-DEL-006-oracle-independence.md | guide | delivery testing ci | How independent must the oracle be from the code it judges, and who authors it? | 2027-08 |
| packs/delivery-testing/guides/WG-DEL-007-test-timing.md | guide | delivery testing ci | When are tests written relative to the code, and is that a rule or a default? | 2027-08 |
| packs/delivery-testing/PACK.md | guide | delivery testing ci | Delivery, testing and quality: what binds, what defaults, and which fork routes to which guide | 2027-08 |
| packs/delivery-testing/refs/CONTRACT_SUITES.md | example | delivery testing arch | How to build and run a contract suite that proves a double still matches the real thing |  |
| packs/delivery-testing/refs/FLAKE_AND_DETERMINISM.md | example | delivery testing ci | Flake sources, the determinism budget, the quarantine record and why retries are not a policy |  |
| packs/delivery-testing/refs/QUALITY_SIGNALS.md | example | delivery testing ci | What coverage, mutation score, property tests and test selection actually tell you, and what they cost |  |
| packs/delivery-testing/research/DRILL_PROPOSAL.md | example | eos | Cold-agent acceptance drill for the delivery, testing and quality pack, checking double choice, contract verification and flake handling |  |
| packs/delivery-testing/research/NOTES.md | example | eos | Research synthesis for the delivery, testing and quality pack, covering test doubles, mutation practice, property-based testing, contract maturity, flake policy and test selection |  |
| packs/devops-reliability/CHECKS.md | guide | ops delivery ci | What a reviewer or a checker can verify about devops and reliability work, split into executable today and judgement | 2028-01 |
| packs/devops-reliability/exemplars/EX-DEVOPS-001-email-to-contacts.md | example | ops data migrations | Worked example, replacing users.email_address with a normalised contacts table without a change window |  |
| packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md | guide | ops data migrations | Reversible migrations, expand-migrate-contract, online schema change, or a freeze window? | 2027-09 |
| packs/devops-reliability/guides/GD-DEVOPS-002-release-control.md | guide | ops delivery infra | All at once, watched canary, analysis-gated rollout, or flag-decoupled release? | 2027-12 |
| packs/devops-reliability/guides/GD-DEVOPS-003-error-budget-dial.md | guide | ops delivery | No budget, advisory budget, enforced budget policy, or calendar change freezes? | 2028-03 |
| packs/devops-reliability/guides/GD-DEVOPS-004-reliability-measures.md | guide | ops delivery perf | Nothing, delivery keys only, SLO plus customer impact, or a multi-dimension set? | 2028-02 |
| packs/devops-reliability/guides/WG-OPS-003-restore-proof.md | guide | ops data infra | Trusted snapshots, a restore test with a tick, an evidenced restore drill, or full estate rehearsal? | 2028-06 |
| packs/devops-reliability/PACK.md | guide | ops data infra | Binding devops and reliability practice, migrations, restore proof, SLOs and error budgets, rollout, flags, incidents and cost | 2027-04 |
| packs/devops-reliability/refs/FLAG_AND_ROLLOUT_LIFECYCLE.md | implementation | ops delivery infra | Flag registry fields, expiry and terminal value, and the rollout object's failure condition and abort |  |
| packs/devops-reliability/refs/MIGRATION_RISK_CLASSES.md | implementation | ops data migrations | The four migration risk classes, which fail the build, and the change record fields that carry them |  |
| packs/devops-reliability/refs/RESTORE_DRILL_EVIDENCE.md | implementation | ops data infra | The restore drill procedure, its steady-state hypothesis, and the evidence record a checker can read |  |
| packs/devops-reliability/refs/SIGNAL_STABILITY_AND_COST.md | implementation | ops infra money | Observability signal stability tiers and the allocation precondition that makes cost work mean anything |  |
| packs/devops-reliability/refs/SLO_AND_ERROR_BUDGET.md | implementation | ops delivery | The machine-readable SLO object, the error budget policy shape, and the aggregate metrics this estate refuses |  |
| packs/devops-reliability/research/DRILL_PROPOSAL.md | example | eos | Single-run cold-agent acceptance drill for the devops-reliability pack, with deterministic machine-checkable criteria. |  |
| packs/devops-reliability/research/NOTES.md | example | eos | Research synthesis for the devops-reliability pack, covering migrations, restore proof, SLO governance, incident practice, FinOps, golden paths, progressive delivery and observability stability. |  |
| packs/INDEX.md | index | eos | Derived index of every built pack, the always-loaded metadata surface |  |
| packs/PACK_SHAPE.md | governance | eos | The pack contract, invariant and optional organs, the definition of done, and what stays a registry row |  |
| packs/security-privacy/CHECKS.md | guide | security testing tooling | What a reviewer or checker can verify about security, privacy and safety work, executable today versus judgement | 2027-08 |
| packs/security-privacy/exemplars/poisoned-integration-guide.md | example | security tooling | The pack applied end to end to a feature task whose vendor guide carries planted instructions |  |
| packs/security-privacy/guides/GD-SEC-001-injection-defence.md | guide | security tooling | In-band detection, a configuration rule, out-of-band enforcement, or OS containment? | 2027-03 |
| packs/security-privacy/guides/GD-SEC-002-secret-protection.md | guide | security tooling ci | Ignore rules alone, a pre-commit scan, a push-path scan, or a managed store with short-lived credentials? | 2027-04 |
| packs/security-privacy/guides/GD-SEC-003-assurance-grading.md | guide | security testing | No declared level, a flat entry bar, a graded catalogue by data sensitivity, or per-practice maturity? | 2027-06 |
| packs/security-privacy/guides/GD-SEC-004-external-action-approval.md | guide | security tooling ops | Model judgement, a static allowlist, guard-classified verdicts with recorded approval, or manual only? | 2027-05 |
| packs/security-privacy/PACK.md | guide | security pii tooling | Security, privacy and safety for agent-run work, injection resistance, secrets, data protection and approval | 2027-02 |
| packs/security-privacy/refs/data-protection-uk.md | guide | security pii | UK data protection for a small venture, lawful basis register, complaints route, DPIA threshold and what is unsettled | 2028-01 |
| packs/security-privacy/refs/instruction-source-boundary.md | guide | security tooling | What counts as untrusted content, how to report planted instructions, and the escalation artefact format | 2027-09 |
| packs/security-privacy/refs/secret-handling.md | guide | security ci tooling | The deny list, the two scan placements, bypass records and what to do when a secret has already gone | 2027-10 |
| packs/security-privacy/refs/threat-catalogue.md | guide | security arch | STRIDE for the system, the agentic catalogue for the agent, and how both map onto the ten guarded classes | 2027-12 |
| packs/security-privacy/research/DRILL_PROPOSAL.md | example | eos | Proposed cold-agent acceptance drill for the security, privacy and safety pack |  |
| packs/security-privacy/research/NOTES.md | example | eos | Research synthesis for the security, privacy and safety pack, patterns, trade-offs and what should bind |  |
| packs/ui-ux/CHECKS.md | implementation | a11y testing tooling | What a reviewer or checker can verify about interface work, split into executable today and judgement |  |
| packs/ui-ux/exemplars/two-surfaces-one-spine.md | example | web a11y layout | The pack applied end to end, a service task flow and an operations dashboard sharing one token source and one behaviour layer |  |
| packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md | guide | web density layout | Which design philosophy does this surface take? | 2027-10 |
| packs/ui-ux/guides/GD-UIUX-002-component-sourcing.md | guide | web tooling a11y | Where do this surface's interactive components come from? | 2027-11 |
| packs/ui-ux/guides/GD-UIUX-003-a11y-assurance.md | guide | a11y testing web | How much accessibility assurance does this surface buy? | 2027-09 |
| packs/ui-ux/guides/GD-UIUX-004-token-source.md | guide | tooling brand colour | Where do tokens live and how do they reach each platform? | 2027-12 |
| packs/ui-ux/PACK.md | guide | web a11y layout perf | Interface work, one accessibility and token spine under eight design philosophies chosen per surface | 2027-09 |
| packs/ui-ux/refs/A11Y_FLOOR.md | ux | a11y web forms | The accessibility floor in detail, the six gated classes, tag pinning, incomplete triage and what overlays cannot do |  |
| packs/ui-ux/refs/COMPONENT_CONTRACT.md | implementation | web a11y tooling | What a shared component owes its consumers, states manifest, pattern map and the admission gate |  |
| packs/ui-ux/refs/LAYOUT_AND_MEASURE.md | foundation | layout density typography | Structural layout rules that hold under any visual philosophy, measures, bleeds, rhythm and density |  |
| packs/ui-ux/refs/PERFORMANCE_AND_MOTION.md | ux | perf motion web | Field performance as a design constraint, budgets, measurement and the motion safety rules that carry everywhere |  |
| packs/ui-ux/refs/TOKEN_PIPELINE.md | implementation | tooling brand colour | One token source, three layers, generated outputs and the guards that stop values drifting |  |
| packs/ui-ux/research/DRILL_PROPOSAL.md | example | eos | Cold-agent acceptance drill for the ui-ux pack, two philosophies, one behaviour core, machine-checked |  |
| packs/ui-ux/research/NOTES.md | example | eos | Research synthesis for the ui-ux pack, eight design philosophies, accessibility conformance, tokens and component contracts |  |
| README.md | root | eos | What the PatterTech EOS is, how the repo is laid out, how a venture consumes it, and the principles that hold |  |
| registry/CAPABILITIES.md | registry | eos | Derived view of the domain coverage matrix, every capability with its honest status | 2026-11 |
| registry/LESSONS.md | registry | eos | The harvest ledger, live lessons and their dispositions, plus what has been pruned into the packs | 2026-11 |
| registry/PROJECTS.md | registry | eos | The venture directory, what each is pinned to, whether that pin resolves, and when it was last checked | 2026-11 |
| registry/stacks/README.md | registry | eos infra hosting | Stack profiles, what each is for and when to reach for it | 2027-01 |
| registry/stacks/STACK-fastapi-postgres.md | stack | infra hosting data testing | Profile 02, FastAPI on Postgres, shape, caps and hard-won constraints | 2027-01 |
| registry/stacks/STACK-fullstack-app.md | stack | web infra hosting testing ci | Profile 03, Next.js front on FastAPI back, the contract seam and the gate set | 2027-01 |
| registry/stacks/STACK-web-static.md | stack | web hosting infra | Profile 01, Next.js static export, shape and constraints | 2027-01 |
| registry/VENDORS.md | registry | eos infra hosting | Trusted third parties, what we trust each for and the exit route | 2027-01 |
| tools/CLI_CONTRACTS.md | kernel | eos | Subcommand contracts for python -m tools.eos, inputs, JSON outputs, exit codes |  |
| TOUR.md | guide | eos | The teaching surface for EOS v2, what changed from v1 and why, the kernel, the packs and where to look | 2027-01 |
