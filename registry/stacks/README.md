---
summary: Stack profiles, what each is for and when to reach for it
type: registry
tags: [eos, infra, hosting]
status: active
review: 2027-01
---

# Stack profiles

A stack profile is a dated fact about a tested combination of tools, versions
and interoperability boundaries. It records what ran and where its evidence
stops. It is not timeless Doctrine.

Profiles are selected during Session 0 and recorded in the venture lock-book.
Doctrine and Wargames cite them where a decision turns on a stack fact. Every
profile carries a review date because platforms move. Its `STACK-<slug>`
filename is the profile identity and does not allocate a pack ID namespace.

| Profile | For | Status |
| --- | --- | --- |
| `STACK-web-static.md` | Marketing and content sites, no server state | Active (proven: PatterTech_Website) |
| `STACK-fastapi-postgres.md` | APIs and services with a database | Active (proven: Venture B) |
| `STACK-fullstack-app.md` | Product apps, Next.js front + FastAPI back | Active (proven: Venture B; Venture A builds on it per its ADR-0002) |
| `STACK-local-first-pwa.md` | Local-first browser products with a WASM compute core, data never leaves the machine | Active (proven: Venture C S1) |
| `STACK-data-compute.md` | Local analytical compute across Polars, pandas, NumPy, Numba and DuckDB | Active (tested by the dated compute probe) |
