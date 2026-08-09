#!/usr/bin/env python3
"""Criterion 4: a Polish catalogue drops in and works, with no src change.

The spec adds a locale file carrying the four Polish plural categories
and asks for the right form at n of 1, 2, 5 and 22 with nothing under
`src/` touched. Rendering that needs the app running, which these
graders cannot do offline, so this one settles the structure the claim
rests on and says as much.

Four things have to hold, and each of them is a way the fixture's
design would break the claim:

1. the count is carried by a message that selects the form inside
   itself, so a translator can supply `few` and `many` at all;
2. the category for a number comes from the locale, through
   `Intl.PluralRules` or a formatter that uses it, not from a
   comparison written for English;
3. no source file fixes the set of categories to the English two, and
   nothing branches on a count of one;
4. the catalogue loader finds files by pattern rather than by name, so
   the `locales/pl.json` this grader writes into a throwaway copy is
   picked up without an edit under `src/`.

The four Polish categories are checked against the file the grader
injects, not against anything the tree supplies, so a tree cannot pass
by shipping Polish itself.
"""

import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, app_files, base_catalogue,  # noqa: E402
                     copy_tree, emit, plural_messages, read, rel,
                     scratch_dir, strip_comments, string_literals)

CID = "c4"

# The CLDR categories for Polish, all four. n of 1 is one, 2 and 22 are
# few, 5 is many, and other carries the rest.
POLISH_MESSAGE = ("{count, plural, one {# rzecz} few {# rzeczy} "
                  "many {# rzeczy} other {# rzeczy}}")

DYNAMIC = (
    (re.compile(r"import\.meta\.glob\s*(?:<[^<>]*>\s*)?\("),
     "import.meta.glob"),
    (re.compile(r"(?<![\w.$])import\s*\(\s*[`$]"), "dynamic import()"),
    (re.compile(r"(?<![\w.$])import\s*\(\s*[A-Za-z_$]"), "dynamic import()"),
    (re.compile(r"require\s*\(\s*[`$A-Za-z_$]"), "dynamic require()"),
    (re.compile(r"require\.context\s*\("), "require.context"),
    (re.compile(r"readdir(Sync)?\s*\("), "a directory read"),
    (re.compile(r"fetch\s*\(\s*[`$]"), "a fetch by pattern"),
    (re.compile(r"i18next-(http|fs|resources-to)-backend"),
     "an i18next backend"),
)

AWARE = (
    (re.compile(r"Intl\.PluralRules"), "Intl.PluralRules"),
    (re.compile(r"@formatjs/"), "@formatjs"),
    (re.compile(r"intl-messageformat"), "intl-messageformat"),
    (re.compile(r"@?messageformat"), "messageformat"),
    (re.compile(r"react-intl"), "react-intl"),
    (re.compile(r"@lingui/"), "lingui"),
    (re.compile(r"@fluent/"), "fluent"),
    (re.compile(r"i18next-icu"), "i18next-icu"),
)

CLOSED_SET = re.compile(
    r"\[\s*['\"]one['\"]\s*,\s*['\"]other['\"]\s*\]|"
    r"\{\s*one\s*:[^{};]{0,60}?,\s*other\s*:")
COUNT_BRANCH = re.compile(r"[=!<>]==?\s*1\s*\)?\s*\?")


def pattern_regex(literal):
    """A glob or template literal as a regex over a path tail."""
    body = literal.replace("\\", "/")
    body = re.sub(r"\$\{[^{}]*\}", "*", body)
    body = re.sub(r"^(\./|\.\./)+", "", body)
    parts = [re.escape(p) for p in re.split(r"\*\*/?|\*", body)]
    glob = ".*".join(parts)
    return re.compile(glob + "$")


def main():
    scratch = scratch_dir()
    code, path, base = base_catalogue(scratch)
    if base is None:
        emit(CID, FAIL, "no message catalogue found")

    plurals = plural_messages(base)
    if not plurals:
        emit(CID, FAIL,
             "no message in %s selects a plural form inside itself, so a "
             "Polish catalogue has nowhere to put few and many"
             % rel(scratch, path))

    files = app_files(scratch)
    sources = {rel(scratch, f): strip_comments(read(f)) for f in files}
    blob = "\n".join(sources.values())
    manifest = read(Path(scratch) / "package.json")

    aware = [name for rx, name in AWARE
             if rx.search(blob) or rx.search(manifest)]
    if not aware:
        emit(CID, FAIL,
             "nothing under the application source asks the locale which "
             "plural category a number falls in; no Intl.PluralRules and no "
             "formatter that uses it, so few and many can never be chosen")

    closed = []
    for name, text in sorted(sources.items()):
        flat = re.sub(r"\s+", " ", text)
        if CLOSED_SET.search(flat):
            closed.append("%s fixes the categories to one and other" % name)
        if COUNT_BRANCH.search(flat):
            closed.append("%s branches on a count of one" % name)
    if closed:
        emit(CID, FAIL,
             "%d source file(s) decide the form in English: %s"
             % (len(closed), "; ".join(closed[:3])))

    # The loader must find a catalogue this grader writes, by pattern.
    dest, tree = copy_tree(scratch)
    try:
        home = Path(tree) / Path(path).relative_to(scratch).parent
        target = home / "pl.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        message = sorted(plurals)[0]
        payload = dict(base)
        payload[message] = POLISH_MESSAGE
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                          encoding="utf-8")
        injected = target.relative_to(tree).as_posix()

        found = None
        mechanism = None
        for rx, name in DYNAMIC:
            if not rx.search(blob) and not rx.search(manifest):
                continue
            mechanism = name
            for text in sources.values():
                for _, literal in string_literals(text):
                    if not ("*" in literal or "$" in literal or
                            literal.rstrip("/").endswith(
                                Path(path).parent.name)):
                        continue
                    if pattern_regex(literal).search(injected):
                        found = literal
                        break
                for match in re.finditer(r"`([^`]*)`", text):
                    if pattern_regex(match.group(1)).search(injected):
                        found = match.group(1)
                        break
                if found:
                    break
            if found:
                break
        if mechanism is None:
            emit(CID, FAIL,
                 "the catalogue loader names its files one by one; adding "
                 "%s would need an edit under src/, which the criterion "
                 "forbids" % injected)
        if found is None:
            emit(CID, FAIL,
                 "%s is used but no pattern in the source matches %s, so the "
                 "injected catalogue would not be found"
                 % (mechanism, injected))

        static = []
        for name, text in sorted(sources.items()):
            for match in re.finditer(
                    r"import\s+\w+\s+from\s+['\"]([^'\"]+\.json)['\"]", text):
                stem = Path(match.group(1)).stem.lower()
                if stem not in (code.lower(), "package"):
                    static.append("%s imports %s by name"
                                  % (name, match.group(1)))
        if static:
            emit(CID, FAIL,
                 "%d per-locale import(s) under the source: %s. Every new "
                 "language would need the same edit"
                 % (len(static), "; ".join(static[:3])))
    finally:
        shutil.rmtree(str(dest), ignore_errors=True)

    emit(CID, PASS,
         "%s carries the count with in-message selection, %s chooses the "
         "category from the locale, and the pattern %r matches the injected "
         "%s, so no file under src/ names a language. The four Polish forms "
         "were checked structurally, not rendered"
         % (sorted(plurals)[0], ", ".join(aware), found, injected))


if __name__ == "__main__":
    main()
