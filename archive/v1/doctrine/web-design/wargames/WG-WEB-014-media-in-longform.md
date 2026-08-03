---
summary: Is a media block a citation or a monument?
type: wargame
tags: [web, media, layout, content]
status: archived
review_by: 2027-07
---

# WG-WEB-014: Is a media block a citation or a monument?

## The question

When a long read carries media (a video, a carousel of cards, a gallery),
does it sit in the reading column as a cited figure, or does it take a
full-width band the way an interlude does?

## It depends on

- What the piece treats the media as. Cited evidence reads at the measure;
  spectacle competes with the argument it is supposed to serve.
- Whether the block is content (a video, your own cards) or pacing (a tonal
  band with nothing wider than a sentence on it).
- Whether the layout guarantees that a bleed means the same width in every
  wrapper (see foundations/LAYOUT_AND_GRID.md). If it does not, a full-bleed
  media block renders at whatever width its wrapper happens to be.

## Options

### A. Citation: media in the reading column
A compact card or figure at the reading or wide measure. A video is a card
that opens the player in the overlay on demand; a carousel is a figure with a
caption. The argument stays in charge.

### B. Monument: media on a full-width band
The interlude treatment applied to content. It reads as spectacle, invites
the widest surface on the page to carry someone else's pixels, and inherits
the wrapper's width unless the grid caps it.

## Decision rule

Media is a citation. Bands are reserved for the piece's own monuments: a
marquee quote, a tonal step between chapters. If a block contains an image,
a video or an iframe, it does not get a band.

## Default

A, without exception found so far.

## Worked rulings

- **PatterTech Website (2026-07)**: a chapter carousel shipped as B by
  accident and rendered at three different widths on one page. Rebuilt as A:
  the carousel is a reading-column figure, the video is a cited card opening
  into the fullscreen overlay, and the bands stayed with the quote and
  interlude monuments. Recorded alongside it: a production CSP that blocks
  third-party frames by default must carve out `frame-src` for the one embed
  the site sanctions, or the citation dies silently on deploy.
