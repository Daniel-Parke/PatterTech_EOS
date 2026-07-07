# Stack profile 01: Next.js static export

The default stack for marketing, editorial and research sites (ruled by
WG-007). Reference implementation: PatterTech_Website.

## Shape

- Next.js App Router with `output: "export"`: `next build` writes plain
  HTML/CSS/JS; any static host serves it. Cheap, fast, cacheable, impossible
  to take down with a bad request.
- Tailwind v4 with tokens in `@theme` (see TOKENS.md); a raw-value TypeScript
  mirror for code that needs numbers.
- Fonts via `next/font` with `display: swap`.
- Content: filesystem Markdown parsed at build (frontmatter + reading time),
  merged with a typed registry of bespoke pages; one loader, directory-
  parametrised.
- A dev-only `/styleguide` route rendering the whole kit (the acceptance
  surface), excluded from nav, sitemap and indexing.

## Constraints to design around

- No runtime image optimisation: variants are pre-generated and committed
  (WG-008).
- No runtime headers/redirects: set them in the host config (with a strict
  CSP; a static export cannot use nonces, so plan for `unsafe-inline` and
  keep third-party scripts out).
- Dynamic routes need `generateStaticParams()`, and a dynamic route with zero
  entries fails the export: commit it together with its first content file.
- Feature flags do three things when off: hide the nav entry, drop the route
  from the sitemap, `notFound()` the page (accepting the soft-404 with
  noindex).
- SEO is build-time: metadata helper per page, generated sitemap and robots,
  a build-time OG image route, JSON-LD injected in the layout.

## When not to use this profile

Auth, personalisation, forms with server handling, frequently changing data,
or previewable CMS workflows: rule through WG-007 before reaching for a
server.
