---
summary: Derived index of every wargame, the surface inception walks
type: index
tags: [eos, wargame]
derived: true
---

# WARGAME_INDEX

Derived file. Edit wargame front-matter, then run
`python tools/eos_check.py --write-index`.

| id | question | module | tags | status | review_by |
| --- | --- | --- | --- | --- |  --- |
| WG-ARCH-001 | Where do module boundaries live: convention, machine contract, or the directory tree? | architecture | arch tooling | active | 2027-07 |
| WG-ARCH-002 | ORM, query builder, or raw SQL behind repositories? | architecture | arch data | active | 2027-07 |
| WG-ARCH-003 | Derived values: always computed, cached, or stored as immutable snapshots? | architecture | arch data state | active | 2027-07 |
| WG-ARCH-004 | Background jobs: in-process, a durable database queue, or an external broker? | architecture | arch state infra | active | 2027-07 |
| WG-ARCH-005 | How do frontend and backend share types: by hand, generated with a drift gate, or one language? | architecture | arch ci tooling | active | 2027-07 |
| WG-ARCH-006 | What proves a change changed nothing: green tests, pinned behaviour, or byte-stable output? | architecture | arch testing ci | active | 2027-07 |
| WG-ARCH-007 | Vendor integration: their SDK everywhere, an owned adapter, or the raw protocol? | architecture | arch infra security | active | 2027-07 |
| WG-ARCH-008 | One shared database, one per service, or a records core with a separate high-volume store? | architecture | arch data infra | active | 2027-07 |
| WG-DEL-001 | What coverage floor, per surface, and how does it move? | delivery | delivery testing ci | active | 2027-07 |
| WG-DEL-002 | How much end-to-end, and which branch does it block? | delivery | delivery testing ci | active | 2027-07 |
| WG-DEL-003 | Visual regression: nothing, component states, or full pages? | delivery | delivery testing web | active | 2027-07 |
| WG-DEL-004 | When a test flakes: retry, quarantine, or root-cause now? | delivery | delivery testing ci | active | 2027-07 |
| WG-VOX-001 | Which register does this surface speak in? | voice | voice content brand | active | 2027-07 |
| WG-WEB-001 | Dark, light, or dual register? | web-design | web colour brand | active | 2027-07 |
| WG-WEB-002 | Which vocabulary does this page speak? | web-design | web nav content | active | 2027-07 |
| WG-WEB-003 | Card, ledger, plaque, table or prose? | web-design | web layout density | active | 2027-07 |
| WG-WEB-004 | How much may this project move? | web-design | web motion | active | 2027-07 |
| WG-WEB-005 | How much light does this project carry? | web-design | web colour motion brand | active (rewritten 2026-07 after the PatterTech v2 over-correction) | 2027-07 |
| WG-WEB-006 | How dense, for whom? | web-design | web density content | active | 2027-07 |
| WG-WEB-007 | Static export or a server? | web-design | web hosting infra state | active | 2027-07 |
| WG-WEB-008 | How do images get to the page? | web-design | web media perf | active | 2027-07 |
| WG-WEB-009 | One brand or a family of accents? | web-design | web brand colour | active | 2027-07 |
| WG-WEB-010 | How to pick the type trio? | web-design | web typography brand | active | 2027-07 |
| WG-WEB-011 | Should the surface react to presence? | web-design | web motion perf | active | 2027-07 |
| WG-WEB-012 | Literal imagery or generated fields? | web-design | web imagery brand | active | 2027-07 |
| WG-WEB-013 | Where does a design law live so it actually holds? | web-design | web tooling testing | active | 2027-07 |
| WG-WEB-014 | Is a media block a citation or a monument? | web-design | web media layout content | active | 2027-07 |
| WG-EOS-001 | What scale of organisational machinery does this venture compile, S, M or L? | inception | eos wargame | active | 2027-07 |
| WG-EOS-002 | One repo, several, or a corner of an existing one? | inception | eos wargame infra | active | 2027-07 |
