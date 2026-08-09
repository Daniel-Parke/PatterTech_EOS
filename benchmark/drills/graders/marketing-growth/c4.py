#!/usr/bin/env python3
"""Criterion 4: every published page has a named owner and a purpose.

Set equality in both directions, because checking one way lets the
manifest rot: a page with no entry fails, and an entry with no page
fails. The keywords meta tag is refused on the same pass, since the
index operator says it is unused and shipping one is ceremony.

What is graded structurally and not by execution: the criterion also
asks for a schema check and a test. This grader validates the manifest
itself against the shape the criterion states, and asserts the tree
carries a schema and a test that name it. It does not run the delivered
test suite, so a test that exists and asserts nothing would satisfy the
second half. That is stated here rather than hidden.
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, all_files, emit, html_pages,  # noqa: E402
                     read, scratch_dir, site_dir)

CID = "c4"

MANIFEST = "content_owners.json"

PLACEHOLDER = {"", "-", "?", "tbd", "todo", "tba", "n/a", "na", "none",
               "unknown", "unassigned", "team", "the team", "marketing",
               "everyone", "nobody", "someone", "owner"}

KEYWORDS_META = re.compile(
    r"<meta[^>]*name\s*=\s*['\"]keywords['\"]", re.I)

OWNER_KEYS = ("owner", "owned_by", "editor", "responsible", "maintainer")
PURPOSE_KEYS = ("purpose", "why", "job", "intent", "summary")
PATH_KEYS = ("page", "path", "file", "url", "location")


def normalise(value):
    """A manifest key or path, spelled the way a page file is."""
    text = str(value or "").strip()
    if not text:
        return None
    if "://" in text:
        text = urlparse(text).path
    text = text.lstrip("./")
    for prefix in ("site/", "/site/", "/"):
        if text.startswith(prefix):
            text = text[len(prefix):]
    if not text or text.endswith("/"):
        text += "index.html"
    if not Path(text).suffix:
        text += ".html"
    return text


def entries_of(doc):
    """(path, record) pairs from either manifest shape."""
    if isinstance(doc, dict):
        for key in ("pages", "content", "entries"):
            if isinstance(doc.get(key), (list, dict)):
                return entries_of(doc[key])
        out = []
        for key, value in doc.items():
            if isinstance(value, dict):
                out.append((normalise(key), value))
            elif isinstance(value, str):
                out.append((normalise(key), {"owner": value}))
        return out
    if isinstance(doc, list):
        out = []
        for item in doc:
            if not isinstance(item, dict):
                continue
            path = next((item[k] for k in PATH_KEYS if item.get(k)), None)
            out.append((normalise(path), item))
        return out
    return []


def first(record, keys):
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def main():
    scratch = scratch_dir()
    root = site_dir(scratch)
    if root is None:
        emit(CID, FAIL, "no site/ directory, so there is no published set to "
                        "own")

    found = [p for p in all_files(scratch)
             if p.name.lower() == MANIFEST]
    if not found:
        emit(CID, FAIL, "no CONTENT_OWNERS.json anywhere in the tree")
    manifest = found[0]
    rel_manifest = manifest.relative_to(scratch).as_posix()
    try:
        doc = json.loads(read(manifest))
    except ValueError as exc:
        emit(CID, FAIL, "%s does not parse: %s" % (rel_manifest, exc))

    entries = entries_of(doc)
    if not entries:
        emit(CID, FAIL, "%s carries no page entries this grader can read; "
                        "expected a list of records or an object keyed by "
                        "page" % rel_manifest)

    bad = []
    for path, record in entries:
        if path is None:
            bad.append("an entry names no page")
            continue
        owner = first(record, OWNER_KEYS)
        purpose = first(record, PURPOSE_KEYS)
        if owner.casefold() in PLACEHOLDER:
            bad.append("%s has no human owner (%r)" % (path, owner))
        if not purpose:
            bad.append("%s has no purpose" % path)
        elif "\n" in purpose or len(purpose) < 8:
            bad.append("%s has no one-line purpose (%r)" % (path, purpose))
    if bad:
        emit(CID, FAIL, "%d manifest problem(s): %s"
                        % (len(bad), "; ".join(bad[:5])))

    pages = {p.relative_to(root).as_posix() for p in html_pages(scratch)}
    named = {p for p, _ in entries}
    unowned = sorted(pages - named)
    ghosts = sorted(named - pages)
    if unowned or ghosts:
        parts = []
        if unowned:
            parts.append("pages with no entry: %s" % ", ".join(unowned))
        if ghosts:
            parts.append("entries with no page: %s" % ", ".join(ghosts))
        emit(CID, FAIL, "the page set and the manifest set differ. %s"
                        % "; ".join(parts))

    tagged = [p.relative_to(scratch).as_posix() for p in html_pages(scratch)
              if KEYWORDS_META.search(read(p))]
    if tagged:
        emit(CID, FAIL, "%d page(s) still carry a keywords meta tag: %s"
                        % (len(tagged), ", ".join(tagged[:5])))

    schema = None
    test = None
    for path in all_files(scratch):
        text = read(path)
        low = text.lower()
        if path.suffix.lower() == ".json" and path != manifest:
            if ("$schema" in text or '"properties"' in text) and \
                    "owner" in low and "purpose" in low:
                schema = path.relative_to(scratch).as_posix()
        rel = path.as_posix().lower()
        if ("test" in rel or "spec" in rel or "check" in rel) and \
                path.suffix.lower() in (".py", ".sh", ".js", ".ts") and \
                "content_owners" in low:
            test = path.relative_to(scratch).as_posix()
    if schema is None:
        emit(CID, FAIL, "%s is valid but no schema file describes it, so "
                        "nothing validates its shape" % rel_manifest)
    if test is None:
        emit(CID, FAIL, "%s is valid but no test names it, so nothing "
                        "asserts the two sets stay identical" % rel_manifest)

    emit(CID, PASS,
         "%s names an owner and a one-line purpose for each of %d page(s), "
         "the sets match both ways, no page carries a keywords meta tag, and "
         "%s and %s stand behind it"
         % (rel_manifest, len(pages), schema, test))


if __name__ == "__main__":
    main()
