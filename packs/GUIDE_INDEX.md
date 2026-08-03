---
summary: Derived index of every decision guide and archived wargame
type: index
tags: [eos, wargame]
derived: true
---

# GUIDE_INDEX

Derived file. Edit guide front-matter, then run
`python -m tools.eos check --write-index`.

| id | question | module | tags | status | review_by |
| --- | --- | --- | --- | --- |  --- |
| WG-ARCH-001 | Where do module boundaries live: convention, machine contract, or the directory tree? | architecture | arch tooling | archived | 2027-07 |
| WG-ARCH-002 | ORM, query builder, or raw SQL behind repositories? | architecture | arch data | archived | 2027-07 |
| WG-ARCH-003 | Derived values: always computed, cached, or stored as immutable snapshots? | architecture | arch data state | archived | 2027-07 |
| WG-ARCH-004 | Background jobs: in-process, a durable database queue, or an external broker? | architecture | arch state infra | archived | 2027-07 |
| WG-ARCH-005 | How do frontend and backend share types: by hand, generated with a drift gate, or one language? | architecture | arch ci tooling | archived | 2027-07 |
| WG-ARCH-006 | What proves a change changed nothing: green tests, pinned behaviour, or byte-stable output? | architecture | arch testing ci | archived | 2027-07 |
| WG-ARCH-007 | Vendor integration: their SDK everywhere, an owned adapter, or the raw protocol? | architecture | arch infra security | archived | 2027-07 |
| WG-ARCH-008 | One shared database, one per service, or a records core with a separate high-volume store? | architecture | arch data infra | archived | 2027-07 |
| WG-DEL-001 | What coverage floor, per surface, and how does it move? | delivery | delivery testing ci | archived | 2027-07 |
| WG-DEL-002 | How much end-to-end, and which branch does it block? | delivery | delivery testing ci | archived | 2027-07 |
| WG-DEL-003 | Visual regression: nothing, component states, or full pages? | delivery | delivery testing web | archived | 2027-07 |
| WG-DEL-004 | When a test flakes: retry, quarantine, or root-cause now? | delivery | delivery testing ci | archived | 2027-07 |
| WG-OPS-001 | Managed PaaS, a cloud estate under contract, or self-hosting? | devops | ops hosting infra | archived | 2027-07 |
| WG-OPS-002 | Everything in containers, platform-native builds, or a mixed fleet? | devops | ops infra hosting | archived | 2027-07 |
| WG-OPS-003 | Trusted snapshots, scheduled restore tests, or full disaster rehearsal? | devops | ops data infra | archived | 2027-07 |
| WG-OPS-004 | How is spend governed: unwatched, budget-gated, or hard-capped? | devops | ops infra money | archived | 2027-07 |
| WG-VOX-001 | Which register does this surface speak in? | voice | voice content brand | archived | 2027-07 |
| WG-WEB-001 | Dark, light, or dual register? | web-design | web colour brand | archived | 2027-07 |
| WG-WEB-002 | Which vocabulary does this page speak? | web-design | web nav content | archived | 2027-07 |
| WG-WEB-003 | Card, ledger, plaque, table or prose? | web-design | web layout density | archived | 2027-07 |
| WG-WEB-004 | How much may this project move? | web-design | web motion | archived | 2027-07 |
| WG-WEB-005 | How much light does this project carry? | web-design | web colour motion brand | archived | 2027-07 |
| WG-WEB-006 | How dense, for whom? | web-design | web density content | archived | 2027-07 |
| WG-WEB-007 | Static export or a server? | web-design | web hosting infra state | archived | 2027-07 |
| WG-WEB-008 | How do images get to the page? | web-design | web media perf | archived | 2027-07 |
| WG-WEB-009 | One brand or a family of accents? | web-design | web brand colour | archived | 2027-07 |
| WG-WEB-010 | How to pick the type trio? | web-design | web typography brand | archived | 2027-07 |
| WG-WEB-011 | Should the surface react to presence? | web-design | web motion perf | archived | 2027-07 |
| WG-WEB-012 | Literal imagery or generated fields? | web-design | web imagery brand | archived | 2027-07 |
| WG-WEB-013 | Where does a design law live so it actually holds? | web-design | web tooling testing | archived | 2027-07 |
| WG-WEB-014 | Is a media block a citation or a monument? | web-design | web media layout content | archived | 2027-07 |
| WG-MINI-001 | How heavy may a page be before the build must push back? | mini | web | active | 2027-08 |
| WG-MINI-002 | Which formats and sizes do we serve images in? | mini | web content | active | 2027-08 |
| WG-EOS-001 | What scale of organisational machinery does this venture compile, S, M or L? | inception | eos wargame | active | 2027-07 |
| WG-EOS-002 | One repo, several, or a corner of an existing one? | inception | eos wargame infra | active | 2027-07 |
