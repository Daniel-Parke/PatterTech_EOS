---
summary: Trusted third parties, what we trust each for and the exit route
type: registry
tags: [eos, infra, hosting]
status: active
review_by: 2027-01
---

# VENDORS

The trusted-dependency registry. A vendor earns a row by surviving real
use in the estate. Ventures choosing a vendor off this list record the
argument in their lock-book; a vendor failing us gets its row amended,
not silently dropped.

| Vendor | Trusted for | Proven in | Exit route | Status |
| --- | --- | --- | --- | --- |
| Vercel | Static and Next.js hosting, preview deploys | PatterTech_Website, WiseWattage app | Any static host; Railway for SSR | met |
| Railway | Dockerised APIs, Postgres, cron and worker services | WiseWattage | AWS App Runner (proven shape in AutoWatt ADR-0002) | met |
| AWS eu-west-2 | Full estate when residency or contracts demand it | AutoWatt (ADR-0002, proposed) | n/a, the fallback itself | proposed |
| GitHub | Source, CI (Actions), private repos | Everything | Any git host; CI is YAML, portable with work | met |
| Clerk | Auth when velocity beats self-hosting | WiseWattage (feature-flagged) | Cognito or self-hosted per ADR-0002 §A4 | met |
| Resend | Transactional email | WiseWattage digest | SES | met |
| Sentry | Error signal | WiseWattage | CloudWatch, self-hosted GlitchTip | met |
| Stripe | Billing | WiseWattage (feature-flagged) | None painless; keep billing behind a flag | met |
| Upstash Redis | Cache and rate-limit state, optional | WiseWattage | In-memory fallback exists by design | met |
| Anthropic | The workforce | Everything | Model-agnostic files (AGENTS.md parity) are the hedge | met |

Rules of thumb the rows encode: feature-flag every vendor off by
default, document the exit route at adoption time, and never let a
vendor become load-bearing without a row here.
