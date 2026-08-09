#!/usr/bin/env python3
"""Criterion 10: no averaged duration is reported as a headline number.

Two tests, both over keys and headings under `out/` rather than over
prose:

1. The frozen regex `mean_time|avg_.*_time|MTTR`, applied to each key
   or heading and again to it with spaces turned into underscores, so
   "Mean time to recovery" as a heading is caught as well as
   `mean_time_to_recovery` as a key.
2. Any key or heading that names an average (mean, average, avg) of a
   duration (time, duration, hours, minutes, latency, days, age) and
   carries no percentile label. `p50`, `p90`, `percentile`, `median` and
   `quantile` count as labels; `median` is the fiftieth percentile and
   is labelled as such.

Keeping this to keys and headings is deliberate. A policy sentence that
says which statistic the team refuses to publish, and why, is not a
breach of a criterion about what is reported, and a text-wide search
would fail a tree for naming the thing it avoids.

**On an empty tree.** This criterion is a prohibition. Over a tree where
nothing was produced it is vacuously satisfied, and passing a fatal
criterion because no work was done measures nothing. So when `out/`
carries none of the artefacts the drill asks for, the grader exits 2:
unsettled, never a pass.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (ARTEFACTS, FAIL, PASS, UNSETTLED, emit,  # noqa: E402
                     label_positions, produced_files, read, rel,
                     scratch_dir)

CID = "c10"

FROZEN = re.compile(r"mean_time|avg_.*_time|MTTR", re.I)
AVERAGE = re.compile(r"(?i)\b(mean|average|averages|avg)\b")
DURATION = re.compile(
    r"(?i)\b(time|times|duration|hours?|hrs?|minutes?|mins?|seconds?|secs?|"
    r"latency|days?|age|wait|delay|ttr|tta)\b")
PERCENTILE = re.compile(r"(?i)\bp\d{1,2}\b|percentile|median|quantile")

SEPARATORS = re.compile(r"[^A-Za-z0-9]+")
CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def offending(label):
    # `average_handling_time` has no word boundary after "average": the
    # underscore is a word character. So the second test runs over the
    # label with camel humps and every separator turned into spaces,
    # which reads snake_case, camelCase and prose headings alike.
    words = SEPARATORS.sub(" ", CAMEL.sub(" ", label)).strip()
    if FROZEN.search(label) or FROZEN.search(words.replace(" ", "_")):
        return "matches mean_time|avg_.*_time|MTTR"
    if AVERAGE.search(words) and DURATION.search(words) \
            and not PERCENTILE.search(words):
        return "averages a duration with no percentile label"
    return None


def main():
    scratch = scratch_dir()
    files = produced_files(scratch)
    if not files:
        emit(CID, UNSETTLED,
             "out/ carries none of the artefacts the drill produces (%s), so "
             "there is nothing to check this prohibition against. Vacuously "
             "true is not a pass on a criterion that is fatal, so it is left "
             "unsettled rather than granted." % ", ".join(ARTEFACTS))

    findings, checked = [], 0
    for path in files:
        text = read(path)
        for label, where in label_positions(path, text):
            checked += 1
            why = offending(label)
            if why:
                findings.append("%s: %s %r %s"
                                % (rel(scratch, path), where, label[:50], why))
    if findings:
        emit(CID, FAIL, "; ".join(sorted(set(findings))[:5]))

    emit(CID, PASS,
         "%d keys and headings across %d file(s) under out/ and none reports "
         "an averaged duration: no mean_time, no avg_*_time, no MTTR, and no "
         "unlabelled average of a duration" % (checked, len(files)))


if __name__ == "__main__":
    main()
