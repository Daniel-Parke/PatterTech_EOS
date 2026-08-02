---
summary: Which formats and sizes do we serve images in?
type: wargame
tags: [web, content]
status: active
review_by: 2027-08
---

# WG-MINI-002: Which formats and sizes for images?

## The question

Do pages serve one fixed-size JPEG, or responsive variants in modern
formats?

## It depends on

- The device spread: phone screens dominate and pay the most for
  oversized images.
- The build budget: variants cost a generation step at build time.
- The gallery's role: where photographs sell the work, quality per
  kilobyte decides.

## Options

### A. One JPEG at a fixed width
Simplest build. Phones download desktop weight, and the page-weight
budget in WG-MINI-001 is routinely spent on pixels nobody sees.

### B. Responsive AVIF or WebP variants with a JPEG fallback
A srcset of two or three widths per image, AVIF or WebP first, JPEG
fallback for old browsers. Costs one build step and roughly halves
image weight on phones.

## Decision rule

Choose B whenever a build step exists or can be added for less than a
day's work. A alone no longer survives the page-weight budget.

## Ruling

B. Serve responsive AVIF or WebP variants with a JPEG fallback, two or
three widths per image. Argued at module birth and re-argued when the
page-weight numbers came in; the ruling held both times. Page-level
guidance must follow this ruling.
