#!/usr/bin/env python3
"""Criterion 5: A against B is paired, and the verdict holds.

Two halves, both settled as the frozen spec words them. The first is a
field naming the pairing. The second is that the verdict on 0.71
against 0.74 is not "B is better": either no significant difference, or
a statement that this sample cannot resolve the gap.

The second half is a read of wording, and this grader reads it with a
vocabulary rather than with judgement. A verdict phrased outside that
vocabulary would be marked fail here even if a human would accept it,
so the reason always quotes the string it judged, and an empty verdict
is reported as an absent verdict rather than as a wrong one.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, find_keys, flat_text,  # noqa: E402
                     json_strings, norm_key, read, require_report,
                     scratch_dir, walk, walk_json)

CID = "c5"

PAIRING = re.compile(
    r"paired|pairing|mcnemar|matched[_ ]pair|discordant|same[_ ]items|"
    r"item[_ ]level|per[_ ]item", re.I)

INCONCLUSIVE = re.compile(
    r"no significant|not significant|non[- ]significant|insignificant|"
    r"cannot resolve|can not resolve|can't resolve|cannot be resolved|"
    r"does not resolve|inconclusive|no difference|no measurable difference|"
    r"indistinguishable|underpowered|not enough evidence|"
    r"insufficient evidence|too small to|no evidence|not distinguishable|"
    r"cannot tell|cannot separate|does not separate|within noise|"
    r"keep (?:prompt |variant )?a", re.I)

B_BETTER = re.compile(
    r"(?:prompt |variant )?b\b[^.]{0,40}\b(?:is |are |looks |performs )?"
    r"(?:better|superior|wins|stronger|preferred|improves)|"
    r"(?:adopt|switch to|move to|prefer|choose|accept|ship)\s+"
    r"(?:prompt |variant )?b\b", re.I)

VERDICT_KEY = re.compile(
    r"verdict|conclusion|decision|recommendation|outcome|interpretation|"
    r"finding|significan|accept|reject|call", re.I)

NAMES_B = re.compile(r"prompt[_ -]?b\b|variant[_ -]?b\b|[\"']b[\"']", re.I)


def documents(scratch, run):
    """The eval report, plus any other JSON report sitting in the tree."""
    docs = [(run.rel, run.report)]
    for path in walk(scratch, {".json"}):
        try:
            doc = json.loads(read(path))
        except ValueError:
            continue
        if isinstance(doc, dict):
            docs.append((path.relative_to(scratch).as_posix(), doc))
    return docs


def main():
    scratch = scratch_dir()
    run = require_report(CID, scratch)
    docs = documents(scratch, run)

    pairing = None
    named_b = False
    verdicts = []
    for where, doc in docs:
        if NAMES_B.search(flat_text(doc)):
            named_b = True
        for path, key, value in walk_json(doc):
            if pairing is None and PAIRING.search(str(key)):
                pairing = (where, path, key)
            if pairing is None and isinstance(value, str) \
                    and PAIRING.search(value):
                pairing = (where, path, value[:60])
            if VERDICT_KEY.search(norm_key(key)) and isinstance(value, str) \
                    and value.strip():
                verdicts.append((where, path, value.strip()))
        if pairing is None:
            for text in json_strings(doc):
                if PAIRING.search(text):
                    pairing = (where, "$", text[:60])
                    break

    if not named_b:
        emit(CID, FAIL,
             "no report names the second prompt variant, so no A against B "
             "comparison was recorded at all")
    if pairing is None:
        emit(CID, FAIL,
             "no field names the pairing: nothing in the reports says the "
             "two variants were scored over the same items, so the "
             "comparison could be two independent runs")
    if not verdicts:
        emit(CID, FAIL,
             "%s pairs the comparison (%s) but states no verdict on it, so "
             "the reader is left to compare two accuracies unaided"
             % (pairing[0], pairing[2]))

    settled = [v for v in verdicts if INCONCLUSIVE.search(v[2])]
    claims_b = [v for v in verdicts
                if B_BETTER.search(v[2]) and not INCONCLUSIVE.search(v[2])]

    if claims_b:
        emit(CID, FAIL,
             "the verdict calls it for B: %s says %r. On 85 and 89 of the "
             "same 120 items that gap is not resolvable"
             % (claims_b[0][1], claims_b[0][2][:160]))
    if not settled:
        emit(CID, FAIL,
             "the verdict neither says the difference is insignificant nor "
             "that the sample cannot resolve it: %s says %r"
             % (verdicts[0][1], verdicts[0][2][:160]))

    emit(CID, PASS,
         "paired at %s, and the verdict is %r"
         % (pairing[2], settled[0][2][:160]))


if __name__ == "__main__":
    main()
