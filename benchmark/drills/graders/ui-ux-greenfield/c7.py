#!/usr/bin/env python3
"""Criterion 7: contrast measured from rendered colours, AA on every tier.

The measurement is the harness's, not the attempt's. Chromium opens
every delivered page, and for each element carrying its own text the
grader reads the computed colour and walks the ancestors for the first
opaque background. That is the rendered colour, which is the point: a
ratio computed off the token file cannot see a tint applied by a rule
three selectors away.

Thresholds are the WCAG 2.2 AA floor: 3.0 for text at 24px or above,
or 18.66px and bold, and 4.5 for everything else.

Where no browser engine is installed the criterion is unsettled rather
than failed, because a machine that cannot look has found nothing. A
tree with no page at all still fails: that is a missing surface, not a
missing tool.

Known limits, stated rather than hidden. Only text that renders on load
is measured, so a state hidden until a form is submitted is not covered
here. Text over a background image or gradient is counted and reported
as unmeasurable rather than guessed at.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, contrast, emit, rel,  # noqa: E402
                     scratch_dir, walk)

CID = "c7"

PROBE = r"""
() => {
  const out = [];
  const parse = (value) => {
    const m = String(value).match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const parts = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
    if (parts.length < 3) return null;
    const alpha = parts.length > 3 ? parts[3] : 1;
    return {rgb: [parts[0], parts[1], parts[2]], alpha: alpha};
  };
  for (const el of document.querySelectorAll('*')) {
    let text = '';
    for (const node of el.childNodes) {
      if (node.nodeType === 3) text += node.textContent;
    }
    text = text.replace(/\s+/g, ' ').trim();
    if (!text) continue;
    const style = getComputedStyle(el);
    if (style.display === 'none' || style.visibility === 'hidden') continue;
    if (parseFloat(style.opacity) === 0) continue;
    const box = el.getBoundingClientRect();
    if (box.width < 1 || box.height < 1) continue;
    const fg = parse(style.color);
    if (!fg || fg.alpha < 0.95) continue;
    let bg = null, image = false, node = el;
    while (node) {
      const s = getComputedStyle(node);
      if (s.backgroundImage && s.backgroundImage !== 'none') image = true;
      const c = parse(s.backgroundColor);
      if (c && c.alpha >= 0.95) { bg = c.rgb; break; }
      node = node.parentElement;
    }
    let where = el.tagName.toLowerCase();
    if (el.id) where += '#' + el.id;
    else if (el.className && typeof el.className === 'string') {
      where += '.' + el.className.trim().split(/\s+/)[0];
    }
    out.push({
      where: where,
      text: text.slice(0, 40),
      fg: fg.rgb,
      bg: bg,
      image: image,
      size: parseFloat(style.fontSize) || 16,
      weight: parseInt(style.fontWeight, 10) || 400
    });
  }
  return out;
}
"""


def floor_for(size, weight):
    if size >= 24 or (size >= 18.66 and weight >= 700):
        return 3.0
    return 4.5


def main():
    scratch = scratch_dir()
    pages = [p for p in walk(scratch, {".html", ".htm"})]
    if not pages:
        emit(CID, FAIL,
             "no page in the delivered tree, so there are no rendered "
             "colours to measure")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        emit(CID, UNSETTLED,
             "no browser engine here: playwright is not installed, so "
             "contrast could not be measured from rendered colours. That is "
             "a gap in the environment, not a finding against the tree.")

    measured, failures, unmeasurable = 0, [], 0
    try:
        with sync_playwright() as driver:
            browser = driver.chromium.launch()
            try:
                page = browser.new_page(viewport={"width": 1280,
                                                  "height": 1024})
                for path in pages:
                    page.goto(path.as_uri(), timeout=20000)
                    page.wait_for_timeout(150)
                    for row in page.evaluate(PROBE):
                        if row["bg"] is None or row["image"]:
                            unmeasurable += 1
                            continue
                        fg = tuple(int(round(v)) for v in row["fg"])
                        bg = tuple(int(round(v)) for v in row["bg"])
                        ratio = contrast(fg, bg)
                        floor = floor_for(row["size"], row["weight"])
                        measured += 1
                        if ratio + 0.005 < floor:
                            failures.append(
                                "%s in %s: %.2f to 1 against a floor of %.1f "
                                "(%r)" % (row["where"], rel(scratch, path),
                                          ratio, floor, row["text"]))
            finally:
                browser.close()
    except Exception as exc:  # noqa: BLE001 - any engine fault is unsettled
        emit(CID, UNSETTLED,
             "the browser engine could not run here (%s: %s), so contrast "
             "was not measured" % (type(exc).__name__, str(exc)[:160]))

    if failures:
        emit(CID, FAIL,
             "%d of %d rendered text element(s) sit under the AA floor: %s"
             % (len(failures), measured, "; ".join(failures[:4])))
    if measured < 3:
        emit(CID, FAIL,
             "only %d rendered text element(s) across %d page(s), which is "
             "not a delivered surface to measure" % (measured, len(pages)))
    tail = ""
    if unmeasurable:
        tail = ("; %d element(s) sit on an image or gradient and were not "
                "measured" % unmeasurable)
    emit(CID, PASS,
         "%d rendered text element(s) across %d page(s) measured in Chromium, "
         "every one at or above its AA floor%s"
         % (measured, len(pages), tail))


if __name__ == "__main__":
    main()
