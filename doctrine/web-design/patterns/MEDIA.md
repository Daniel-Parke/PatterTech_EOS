# Media

Doctrine 11: media earns its weight. Media is a cited reference, not a
spectacle.

## Figures and images

- Every image that ships has: a web-sized variant, intrinsic width/height,
  `loading="lazy"` (below the fold), `decoding="async"`, and a real alt text.
- Figures sit in a quiet frame on the first surface step with an annotated
  caption (plate number where the piece numbers its figures).
- Source-of-truth exports (print PNGs, social cards) never ship to a page.
  A small script (see WG-008) generates committed web variants (webp + jpg
  fallback at 1-2 sizes); pages consume them via `<picture>`/srcset through a
  helper so call sites stay one-liners.

## Carousels

One card at a time: a single readable portrait card, grouped prev/next
arrows, dot indicators, an "n / total" mono counter, keyboard and swipe, no
autoplay, reduced-motion aware, tap to zoom. Never a row of tiny cards. In
long reads a carousel sits on an interlude band.

## Video

Embeds are facades: a poster card with a play control that only loads the
player (privacy-respecting domain where available) on click. A video is a
compact card in the reading column, never a full-width slab. Self-hosted
loops belong to signature visuals only and follow the motion budget.

## Audio

Small inline speaker buttons (pronunciations, clips): lazy `preload="none"`,
a clear label, visible playing state.

## Documents

PDFs and decks are artifacts and get Panels with a mono badge (edition, page
count), a title, one line of body and a quiet download button.
