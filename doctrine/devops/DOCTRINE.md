---
summary: The six binding devops rules, migrations, parity, secrets, runbooks, restores, cost
type: doctrine
tags: [ops]
---

# Devops doctrine

Binding on every venture that deploys, stores data or spends money on
infrastructure. The wargames beneath carry the arguments; the stack
profiles carry the versioned facts.

1. **Migrations are forward-only, idempotent, advisory-locked, applied
   before app start, and fail closed.** A failed migration fails the
   deploy; nobody edits an applied migration; corrections are new
   migrations. Schema docs move in the same change (the WORK charter
   holds the author to it).

2. **Local parity is law.** The whole platform stands up locally with
   one command: services, database, storage, mail, migrations, seed
   data, health checks. What passes locally is what ships; a venture
   whose production cannot be rehearsed on a laptop is operating on
   faith (WG-OPS-002 keeps the artefacts honest).

3. **Secrets never touch the repo or the client.** Server-side secret
   managers only; frontend hosts hold nothing sensitive; CI reaches
   the cloud through short-lived identity (OIDC), never long-lived
   keys. A secret that leaks into git history is rotated, not deleted.

4. **Console-clicking is forbidden.** Every infrastructure action
   lands as a runbook from day one and as infrastructure-as-code as
   soon as the estate justifies it. State that exists only in a web
   console is state the organisation does not have.

5. **A backup is proven by its restore.** From the first production
   deploy, the restore test runs on cadence with recorded evidence
   (WG-OPS-003); regulated data links the evidence from its registry
   row. Recovery objectives are written before they are needed.

6. **Cost is a design input.** The budget line lives in the state
   file, spend is logged per session, paid tiers wait for the named
   approver, and tier cliffs shape architecture rather than invoices
   (WG-OPS-004). Unattended fleets get hard caps where the platform
   offers them.
