#!/usr/bin/env python3
"""Criterion 3: the sitemap matches the site, resolves and is crawlable.

Three assertions in one script, as the pack's reference says. Every page
appears exactly once, every listed URL returns 200, and nothing listed
is shut out by the crawler directives.

The 200 is a real one. The grader serves site/ over localhost with a
plain static host, so a URL that resolves to nothing, or to a directory
with no index, answers 404 the way the live host would.
"""

import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, html_pages, parse_robots,  # noqa: E402
                     path_forms, read, robots_allows, robots_files,
                     scratch_dir, serve, site_dir, sitemap_locs,
                     sitemap_path, status_of, url_path)

CID = "c3"


def main():
    scratch = scratch_dir()
    root = site_dir(scratch)
    if root is None:
        emit(CID, FAIL, "no site/ directory, so there is nothing to list")

    smap = sitemap_path(scratch)
    if smap is None:
        emit(CID, FAIL, "no sitemap.xml under site/")
    locs = sitemap_locs(smap)
    if locs is None:
        emit(CID, FAIL, "%s does not parse as XML"
                        % smap.relative_to(scratch).as_posix())
    if not locs:
        emit(CID, FAIL, "%s lists no URLs"
                        % smap.relative_to(scratch).as_posix())

    listed = [unquote(urlparse(loc).path or "/") for loc in locs]

    pages = html_pages(scratch)
    if not pages:
        emit(CID, FAIL, "site/ carries no pages")

    missing, duplicated = [], []
    for page in pages:
        forms = path_forms(url_path(scratch, page))
        hits = [p for p in listed if p in forms]
        rel = page.relative_to(scratch).as_posix()
        if not hits:
            missing.append(rel)
        elif len(hits) > 1:
            duplicated.append("%s listed %d times" % (rel, len(hits)))
    if missing or duplicated:
        parts = []
        if missing:
            parts.append("not in the sitemap: %s" % ", ".join(missing))
        if duplicated:
            parts.append("; ".join(duplicated))
        emit(CID, FAIL, "%d of %d pages do not appear exactly once. %s"
                        % (len(missing) + len(duplicated), len(pages),
                           " ".join(parts)))

    dead = []
    with serve(root) as base:
        for path in listed:
            code = status_of(base, path)
            if code != 200:
                dead.append("%s -> %s" % (path, code or "no response"))
    if dead:
        emit(CID, FAIL, "%d sitemap URL(s) do not return 200: %s"
                        % (len(dead), "; ".join(dead[:5])))

    live, _ = robots_files(scratch)
    blocked = []
    if live is not None:
        parsed = parse_robots(read(live))
        blocked = [p for p in listed if not robots_allows(parsed, p)]
    if blocked:
        emit(CID, FAIL, "%d sitemap URL(s) are disallowed by robots.txt: %s"
                        % (len(blocked), ", ".join(blocked[:5])))

    emit(CID, PASS,
         "%d page(s) each listed once, %d sitemap URL(s) all returned 200, "
         "and none is disallowed by the crawler directives"
         % (len(pages), len(listed)))


if __name__ == "__main__":
    main()
