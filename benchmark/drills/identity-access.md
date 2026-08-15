---
summary: Single-run cold-agent acceptance drill for identity, authorisation and tenancy, adding a cross-tenant support role to a service whose tenant scoping is inconsistent
type: example
tags: [eos]
---

# Drill: add a cross-tenant role without opening the tenant wall

## Scenario

A cold agent is given the pack and a seeded Python repository holding a
small multi-tenant service. Nothing in the tree tells it which of the
three handlers is right.

- `service/app.py`, holding the route table and the frozen entry point
  `handle(request) -> {"status": int, "body": str}`. A request is a
  plain dict with `route`, `params`, `headers` and `session`. Five
  routes: `GET /invoices`, `GET /invoices/{id}`, `GET /projects`,
  `GET /projects/{id}`, `GET /members`.
- `service/handlers/invoices.py`, which takes the tenant from the
  request header `X-Tenant-Id`.
- `service/handlers/projects.py`, which takes the tenant from the
  session and filters in SQL.
- `service/handlers/members.py`, which applies no tenant filter at all
  and leans on a `WHERE user_id = ?` clause to do it by accident.
- `service/session.py`, a cookie-backed session lookup returning
  `user_id`, `tenant_id` and `role`. The seeded roles are `member` and
  `admin`.
- `service/db.py`, and `service/clock.py` whose `now()` is the only
  clock the service reads. The harness replaces it.
- `migrations/001_init.sql` and `seed/seed.sql`. Two tenants, `t_alpha`
  and `t_beta`. Four users, `u_alpha_member`, `u_alpha_admin`,
  `u_beta_member` and `u_support`. Rows `inv_alpha_1`, `inv_beta_1`,
  `prj_alpha_1`, `prj_beta_1`, `mem_alpha_1`, `mem_beta_1`. Every
  `t_beta` row carries the string `beta-only-marker` in a text column.
- `tests/`, holding two happy-path tests and no isolation test.
- `requirements.txt`, pinning pytest and nothing else.

`TASK.md` asks for one change. Add a `support` role that can read
invoices and projects belonging to any tenant, for a named support
case, and the open case is `case-4417`. Support access must be
attributable and must not be permanent. Four things are frozen and the
task says so: the entry point signature, the five route names, the
seeded identifiers, and two artefacts. A support request names its
target in `params.tenant` and its case in `params.case`. Every read
that crosses a tenant boundary appends one JSON object as a line to
`audit.log` at the tree root. The task also asks for `DECISIONS.md`,
carrying one line that reads `authorisation-model:` followed by one of
role-based, attribute-based or relationship-based, and one line that
reads `credential:` followed by session or token.

The three handlers disagree with each other about where the tenant
comes from, and the task names none of that. One run, no human turns.

## Deterministic pass criteria

Every check must return true. Each is a file existence, exit code or
parse assertion, no judgement.

1. `python -m pytest tests/` exits 0 on the delivered tree.
2. `service.app.handle` imports and keeps its signature. Called as
   `u_alpha_member` for `inv_alpha_1` it returns status 200 with
   `inv_alpha_1` in the body, and called as `u_beta_member` for
   `inv_beta_1` it returns status 200 with `beta-only-marker` in the
   body. A tree that answered by refusing everything fails here.
3. Cross-tenant leakage. For each of the five routes the harness issues
   the request as `u_alpha_member` with every seeded `t_beta`
   identifier substituted into `params` in turn, twenty-five calls in
   all, and asserts no response carries status 200 and no response body
   contains `beta-only-marker`.
4. Prohibition. The tenant never comes from the caller. With the clock
   held fixed, two responses to the identical `u_alpha_member` request,
   one carrying `X-Tenant-Id: t_beta` and one carrying no such header,
   are equal byte for byte on all five routes. An AST walk of every
   module under `service/handlers/` finds no read of a key containing
   `tenant` from `headers`, from `params`, or from a request body.
5. Prohibition. No authorisation decision is left in a handler. An AST
   walk finds no comparison against a role-name string literal in any
   module under `service/handlers/`, and the delivered role names
   appear as string literals in at most one module under `service/`.
   At most, not exactly, so a tree that keeps its roles in the database
   passes.
6. An admin is not a superuser. Every criterion 3 call repeated as
   `u_alpha_admin` returns a status other than 200 and a body without
   `beta-only-marker`.
7. Break-glass works, and only when it is asked for properly. As
   `u_support` with `params.tenant` of `t_beta` and `params.case` of
   `case-4417`, `GET /invoices/{id}` for `inv_beta_1` returns status
   200 with `beta-only-marker`. The same request with `params.tenant`
   omitted, and again with `params.case` omitted, each returns a status
   other than 200 and a body without `beta-only-marker`.
8. Break-glass expires. The harness advances `service.clock.now` by 365
   days, establishes a fresh `u_support` session at that time, changes
   nothing else, and repeats the successful call from criterion 7. It
   returns a status other than 200 and a body without
   `beta-only-marker`.
9. The crossing is attributable. `audit.log` gains exactly one line
   during the successful call from criterion 7, that line parses as one
   JSON object, and `u_support`, `t_beta` and `case-4417` each appear
   among its values.
10. `DECISIONS.md` exists, holds a line matching
    `^authorisation-model: (role-based|attribute-based|relationship-based)$`,
    holds a line matching `^credential: (session|token)$`, and names all
    three of `role-based`, `attribute-based` and `relationship-based`
    somewhere in the file.
11. Prohibition. No route answers without a session. Each of the five
    routes, called with `session` absent and again with a session
    identifier that is not in the store, returns a status other than
    200 and a body containing none of the seeded row identifiers.

## Scoring

Eleven binary checks, pass threshold 11 of 11. Partial credit is
recorded for diagnosis only and is not a pass.

## Boundary

This drill tests who may act, on whose data, and how a deliberate
crossing is bounded and recorded. It deliberately tests none of the
security and privacy pack's four subjects. There is no secret in the
tree to leak, no planted text addressed to the agent, no personal data
beyond opaque user identifiers, and no outbound network call to
approve. A pack that answers this drill by restating injection
resistance or secret scanning has answered a different question.
