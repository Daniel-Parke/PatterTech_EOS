---
summary: Crawler directives, sitemaps and structured data as release-gated artefacts, and the folk levers the index operator says are inert
kind: fact
scope: estate
sources: [EV-0022]
volatility: fast
review: on-change-of:Google-structured-data-guidelines-revision
type: implementation
tags: [seo, content, ci]
---

# Discovery surface

Reference for PACK.md D6, D7 and D8. Three artefacts decide whether a
published page can be found, and all three belong in the release
pipeline rather than in a console.

## Crawler directives

The protocol is advisory. It is explicitly not a substitute for content
security, so a disallowed path is a hint to well-behaved crawlers and an
index of interesting places to everyone else (FRAG-MKTG-06). Never put
a secret path in it.

The operational failure semantics are what make it release-gated:

- A 5xx response on the file means a conforming crawler must assume
  complete disallow. A botched deploy is therefore a self-inflicted
  deindexing incident.
- Cached rules should not be used beyond twenty four hours, so the blast
  radius of a bad file is about a day of crawling.
- The file is under 500 KiB.
- The protocol governs crawling, not indexing. A disallowed URL can
  still surface from external links.

The gate: a test asserts the production profile carries no blanket
disallow, and a staging fixture that does carry one fails the same test.
A check that cannot fail is not a check.

## Sitemaps

Every published page appears exactly once. Every listed URL returns 200.
No listed URL is disallowed by the crawler directives, which is the
contradiction that quietly wastes a crawl budget. The three assertions
are one script.

## Structured data

The rule is short: markup describes what a reader can see, the crawler
is not blocked from the page, and the vocabulary is the versioned one at
EV-0022 (FRAG-MKTG-03). Every markup property carrying user-facing text
has a matching string in the rendered page, and a script asserts zero
orphan properties.

The penalty for breach is loss of rich-result eligibility rather than a
ranking hit. That bounded blast radius plus a testable rule is why
PACK.md makes this a default with a machine check behind it rather than
a matter of taste.

## The inert levers

The operator of the index names these as unused or near worthless, so
spending effort on them is ceremony (FRAG-MKTG-01):

- The keywords meta tag. Unused.
- Word-count targets. No such target exists.
- Heading order as a ranking input. Irrelevant.
- Keywords in the domain or the URL. Near worthless.
- E-E-A-T as a ranking factor. Explicitly not one.

What the operator claims to weigh is content people find useful,
crawlability, and discovery through links. Treat that list as what it
is: one vendor describing its own closed system with no external
verification and no published weights. It settles what is not worth
doing far better than it settles what is.

## AI surfaces

The same operator states there are no additional requirements and no
special optimisation for its AI answer surfaces, and specifically that
no new machine-readable file or markup is needed (FRAG-MKTG-05).
Eligibility is ordinary indexing plus snippet eligibility. That denial
is self-interested and covers its own surfaces only, and a live
counter-practice exists with no measurement behind it, so the pack
records the disagreement and adopts neither side. What it forbids is an
agent inventing a workstream here on the strength of vendor-adjacent
noise.
