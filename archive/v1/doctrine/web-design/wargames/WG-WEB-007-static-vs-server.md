---
summary: Static export or a server?
type: wargame
tags: [web, hosting, infra, state]
status: archived
review_by: 2027-07
---

# WG-WEB-007: Static export or a server?

## The question

Does the site ship as a fully static export, or does it need server
rendering, ISR or an API layer?

## It depends on

- Auth, personalisation or user-generated state anywhere on the roadmap's
  first year.
- Forms: mailto and third-party form endpoints keep a site static; server
  handling does not.
- Content update cadence: git-committed Markdown suits weekly; a
  non-technical editor or hourly updates suit a CMS + ISR.
- Traffic shape: static is immune to bad requests and free-tier friendly.
- Team: a static export has no runtime to operate.

## Options

### A. Static export (profile 01)
Everything prerendered at build. Cheapest, fastest, most reliable; images
must be pre-optimised; headers live in host config; no runtime logic.

### B. Hybrid (SSG + ISR/serverless islands)
Static by default with regenerating pages or the odd function. Buys CMS
freshness and form handling; costs platform coupling and a runtime to watch.

### C. Server-rendered app
For actual applications (auth, dashboards). A different module of this
framework once it exists; do not drag a marketing site here for one form.

## Decision rule

Start at A. Move to B only when a named requirement (editor without git,
sub-daily content, server-handled forms) forces it, and keep the static
surfaces static. C means you are building an app; treat the marketing site
and the app as separate deployables speaking the same design language.

## Default

A. Static export.

## Worked rulings

- **PatterTech Website (2026-07)**: A. No auth, no forms (contact is
  mailto), content is git-authored Markdown plus bespoke routes. The
  constraint set (pre-generated image variants, host-config headers,
  static params for dynamic routes) is documented in
  implementation/STACK_next-static.md.
