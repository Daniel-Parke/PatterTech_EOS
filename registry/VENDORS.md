---
summary: Trusted third parties, what we trust each for and the exit route
type: registry
tags: [eos, infra, hosting]
status: active
review: 2027-01
---

# VENDORS

The trusted-dependency registry. A vendor earns `met` by surviving real
use in the estate. Ventures choosing a vendor off this list record the
argument in their lock-book; a vendor failing us gets its row amended,
not silently dropped. A vendor a plan depends on but nothing has run
yet is `proposed`, and its exit route may honestly be unknown.

| Vendor | Trusted for | Proven in | Exit route | Status |
| --- | --- | --- | --- | --- |
| Vercel | Static and Next.js hosting, preview deploys | PatterTech_Website, Venture B app | Any static host; Railway for SSR | met |
| Railway | Dockerised APIs, Postgres, cron and worker services | Venture B | AWS App Runner, a shape already proven in a Venture A ADR | met |
| AWS eu-west-2 | The full estate where residency or contracts demand it | Venture A, as a proposed target | Not applicable, it is the fallback itself | proposed |
| GitHub | Source, CI, private repos | Everything with a remote | Any git host; the CI is YAML and portable with work | met |
| Clerk | Auth when velocity beats self-hosting | Venture B, behind a flag | Cognito or self-hosted, per a Venture A ADR | met |
| Resend | Transactional email | Venture B digest | Amazon SES | met |
| Sentry | Error signal | Venture B | CloudWatch, or self-hosted GlitchTip | met |
| Stripe | Billing | Venture B, behind a flag | None painless. Keep billing behind a flag | met |
| Upstash Redis | Cache and rate-limit state, optional | Venture B | An in-memory fallback exists by design | met |
| Anthropic | The workforce | Everything | Model-agnostic files, the AGENTS and CLAUDE parity rule, are the hedge | met |
| Listmonk | Self-hosted mailing list and campaign sending | Nowhere yet. Planned in Venture J, which is dormant | Any list manager that can import a subscriber table and a consent ledger; the ledger is ours, which is the point | proposed |
| Amazon SES | Outbound sending reputation and relay behind Listmonk | Nowhere yet. Planned in Venture J | Resend, already met for transactional mail. Reputation does not transfer, so a move costs warm-up | proposed |
| Fly.io | EU-West hosting for the data spine, as the alternative to Railway | Nowhere yet. Named in Venture J as "Railway or Fly EU-West" | Railway, which is already met. The two are interchangeable for a Dockerised FastAPI service | proposed |
| Umami | Privacy-preserving web analytics, self-hosted or cloud | Nowhere yet. Planned in Venture J | Unknown. Nothing has been instrumented, so no export path has been tested | proposed |
| Migadu | Mailbox hosting and mailbox security for the domains | Unknown. Named in Venture J as a rented dependency; whether it is in use has not been verified from this repo | Any IMAP host; mail is portable, the domain is what matters | proposed |

Rules of thumb the rows encode: feature-flag every vendor off by
default, write the exit route down at adoption time, and never let a
vendor become load-bearing without a row here. Where the exit route is
unknown, the row says unknown rather than inventing one.

Five rows were added in the v2 build after an audit found live and
planned dependencies with no row at all: Listmonk, Amazon SES, Fly.io,
Umami and Migadu. Every one of the five is named in Venture J, which is
dormant, so none is proven and all say so.
