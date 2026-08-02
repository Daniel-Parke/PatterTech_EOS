---
summary: Page-level guidance on serving images for the mini module
type: doctrine
tags: [web, content]
---

# Serving images

Guidance for pages in this module.

Serve every image as JPEG at a fixed 1200px width; responsive variants
are not worth the build cost.

Lazy-load anything below the first viewport and give every image an
explicit width and height so the page does not shift while loading.
Alt text is written for the reader, not the crawler.
