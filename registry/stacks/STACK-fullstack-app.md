---
summary: Profile 03, Next.js front on FastAPI back, the contract seam and the gate set
type: stack
tags: [web, infra, hosting, testing, ci]
status: active
review: 2027-01
---

# Stack profile 03: Full-stack app (Next.js + FastAPI + Postgres)

The default stack for product apps: profile 02 underneath, a Next.js
front on top, one typed seam between them. Reference implementation:
Venture B; Venture A builds on it per its ADR-0002 (AWS variant).

## Shape

- Monorepo (WG-EOS-002 default): pnpm workspaces for the JS side
  (version pinned via `packageManager`), uv for Python, surfaces as
  top-level dirs (`api/`, `app/`, `website/`, `packages/`).
- Frontend: Next.js App Router, React 19, TypeScript strict, Tailwind
  v4 tokens in `@theme`. The marketing site is profile 01 inside the
  same repo (separate deployable, same design language).
- **The contract seam, non-negotiable**: OpenAPI generated from the
  FastAPI app offline and deterministically, committed, and compiled
  into a types package plus a typed fetch client that always checks
  `response.ok` and throws a typed error. A CI drift test fails when
  the committed schema lags the live app. A failed mutation must never
  masquerade as success.
- Testing: the profile 02 Python gates, plus Vitest for JS units,
  Playwright end-to-end against a real local stack, axe accessibility
  checks at zero violations, and pixel-exact visual regression (Lost
  Pixel or equivalent) in a pinned container with committed baselines.
- CI jobs: python, node, ui-visual, docker-build, security (advisory);
  merge gates per branch, end-to-end blocking on `main`.
- Hosting: API and workers as containers (Railway or AWS App Runner
  per the venture's ADR); app and website on the static or edge host
  the venture rules; secrets only ever on the server-side host.

## Constraints to design around

- Generated artefacts (types, schemas) are committed with a drift
  check or they rot silently; hand-maintained seams are forbidden.
- Ratchets beat big-bang strictness: mypy allowlist, coverage floors,
  breakpoint and design-token gates that only tighten.
- Every external dependency needs a synthetic or offline mode for CI
  (weather, email, payments); determinism is what makes the e2e gate
  blocking rather than flaky.
- Pin the VRT renderer in a container or fonts diverge across
  machines; pixel-exact only works containerised.
- Playwright in CI uses the runner's preinstalled Chrome
  (`PLAYWRIGHT_CHANNEL=chrome`); the CDN download stalls chronically.
- Windows dev: resolve pnpm via `shutil.which` for subprocesses, call
  Next via `node ./node_modules/next`, and dockerignore
  `**/node_modules` or symlinks break Docker builds.
- Vocabulary: the API's nouns match the product's nouns; a renamed
  domain concept is a migration, not a UI alias (Venture B ADR-004
  learned this the expensive way).

## When not to use this profile

No app, just content: profile 01. Service without a front: profile 02.
Multi-tenant platform machinery or heavy realtime: rule it through
`packs/architecture/` first; this profile assumes one product team and
request-response shapes.
