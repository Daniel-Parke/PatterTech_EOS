---
summary: How do images get to the page?
type: wargame
tags: [web, media, perf]
status: active
review_by: 2027-07
---

# WG-WEB-008: How do images get to the page?

## The question

How are page images produced, optimised and served, especially when the
source of truth is a print-quality export pipeline?

## It depends on

- Whether the host can optimise at request time (a static export cannot).
- Whether a separate pipeline (print/social exports) owns the originals.
- Asset count and churn: a dozen stable cards vs thousands of user uploads.

## Options

### A. Committed pre-generated variants (with static export)
A repo script (sharp) with an explicit input allowlist writes webp + jpg
fallback at one or two sizes into a `web/` folder; variants are committed so
CI stays hermetic; pages consume them via `<picture>`/srcset through a small
helper. Originals stay byte-identical for the export pipeline.

### B. Host/runtime optimisation
`next/image` or a CDN transformer. Right when there is a server (WG-WEB-007 B/C)
or high asset churn; couples you to the platform.

### C. Hand-exported one-offs
Fine for a favicon; a process smell for anything recurring.

## Decision rule

Static export -> A, always with: an explicit allowlist (never touch
unrelated exports), idempotent runs with a `--force` flag, a printed size
table, and a stated per-file budget the script warns on. Server present and
assets churn -> B. Either way: intrinsic dimensions, lazy loading, and no
page ever references a print-quality original.

## Default

A, for the static-first profile.

## Worked rulings

- **PatterTech Website (2026-07)**: A. Twenty carousel cards at ~1.7MB each
  (2160x2700 print PNGs, shown at 448px) plus a 1.08MB og:image were being
  served raw: ~34MB of potential page media. `scripts/optimize-media.mjs`
  now emits 540/1080 webp + 1080 jpg fallback + a 34KB OG jpg (58 variants,
  2.6MB committed). Measured article image transfer after a full scroll:
  0.33MB. A `socialCard()` helper keeps call sites to one line.
