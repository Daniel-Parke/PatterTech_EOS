# Performance

Budgets are written down and gated, not aspired to.

## Default budgets (tighten per project in the lock-in)

- No single image over ~150KB on the wire.
- A page's total image transfer after a full scroll stays under ~1.5MB; the
  first viewport under ~500KB.
- At most three font families, subset, `display: swap`.
- No third-party scripts beyond analytics; embeds are facades until clicked.
- Client JavaScript earns its place: reveals are CSS + IntersectionObserver,
  not a motion library; a motion library is loaded only for genuinely
  stateful animation.

## Structural choices that keep it fast

- Static-first delivery (WG-007): prerender everything that can be
  prerendered; a static export is impossible to take down with a bad request
  and trivially cacheable.
- Pre-generated, committed image variants (WG-008) rather than runtime
  optimisation when the host cannot resize.
- Intrinsic dimensions on all media (zero layout shift), lazy loading below
  the fold.
- Signature canvas/SVG visuals pause when hidden and cap device pixel ratio.

## Measuring

Measure with a script, in CI or locally, not by feel: drive a headless
browser through a full-page scroll, total the image bytes, flag anything over
budget. Keep the script in the repo and the numbers in the QC gate. Re-run
Lighthouse (or equivalent) after structural changes; record regressions as
bugs.
