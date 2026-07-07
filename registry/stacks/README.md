---
summary: Stack profiles, what each is for and when to reach for it
type: registry
tags: [eos, infra, hosting]
status: active
review_by: 2027-01
---

# Stack profiles

A stack profile is dated fact: a proven combination of frontend,
backend, testing and hosting with its constraints and gotchas. Profiles
are chosen at Session 0 (the lock-book records which), cited by
doctrine, and carry `review_by` dates because platforms move.

| Profile | For | Status |
| --- | --- | --- |
| `STACK-web-static.md` | Marketing and content sites, no server state | Active (proven: PatterTech_Website) |
| `STACK-fastapi-postgres.md` | APIs and services with a database | Phase A follow-up (extract from WiseWattage) |
| `STACK-fullstack-app.md` | Product apps, Next.js front + FastAPI back | Phase A follow-up (extract from WiseWattage) |
