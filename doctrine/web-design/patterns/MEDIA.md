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
long reads a carousel is a cited figure in the reading column with a caption;
media never sits on an interlude band and never bleeds full (WG-014; this
sentence used to say the opposite, and the PatterTech chapter-six carousel
shipped at three widths on one page because of it).

## Video

Embeds are facades: a poster card with a play control that only loads the
player (privacy-respecting domain where available) on click. A video is a
compact card in the reading column, never a full-width slab, and the player
opens in the site's fullscreen overlay rather than expanding in place.
Closing the overlay unmounts the player, which stops the audio. Two hard
lessons behind that (2026-07): a grid child with auto margins gives up
stretch and shrinks to fit, so a box whose only child is absolutely
positioned collapses to a border shell while its audio plays; and a
protection-grade CSP (`default-src 'self'`) silently blocks every
third-party frame in production unless `frame-src` carves out the sanctioned
embed domain. Self-hosted loops belong to signature visuals only and follow
the motion budget.

## Audio

Small inline speaker buttons (pronunciations, clips): lazy `preload="none"`,
a clear label, visible playing state.

## Documents

PDFs and decks are artifacts and get Panels with a mono badge (edition, page
count), a title, one line of body and a quiet download button.
