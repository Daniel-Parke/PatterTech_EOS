#!/usr/bin/env python3
"""Criterion 7: a TEST verdict declares its stopping rule and its sample.

Only bites on TEST. A record that decided BUILD or KILL is not running
an experiment and has nothing to pre-declare, so it passes here and says
which verdict let it through, rather than passing silently.

On TEST the record must carry `- stopping rule: …` and `- sample: <n>`,
and the sample may not exceed the weekly active users in the frozen
`metrics.json`. A sample larger than the population is the clearest sign
the record was written without reading the numbers, and this product has
few enough users that most experiments cannot be powered at all.

The sample line is matched strictly, digits and nothing else, because
that is the frozen grammar. `- sample: 340 users` fails. The stopping
rule is matched on the folded line, so a rule wrapped at seventy-two
columns still counts.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, METRICS, PASS, RECORD, clip, decision_of,  # noqa: E402
                     emit, logical_lines, record_text, scratch_dir,
                     weekly_active_users)

CID = "c7"

STOPPING = re.compile(r"^-\s*stopping rule:\s*(.+)$", re.I)
SAMPLE = re.compile(r"^-\s*sample:\s*([0-9]+)$", re.I)


def main():
    scratch = scratch_dir()
    text = record_text(CID, scratch)

    verdict = decision_of(text)
    if verdict is None:
        emit(CID, FAIL,
             "%s reaches no verdict in the fixed grammar, so whether the "
             "TEST lines are owed cannot be settled; criterion 1 is where "
             "that is reported" % RECORD)
    if verdict != "TEST":
        emit(CID, PASS,
             "the verdict is %s, not TEST, so the stopping rule and sample "
             "lines are not owed" % verdict)

    lines = [line.strip() for line in logical_lines(text)]
    rule = next((m for m in (STOPPING.match(line) for line in lines) if m),
                None)
    if rule is None or not rule.group(1).strip():
        emit(CID, FAIL,
             "the verdict is TEST and %s carries no `- stopping rule: …` "
             "line, so nothing was fixed before the data arrives" % RECORD)

    sample = next((m for m in (SAMPLE.match(line) for line in lines) if m),
                  None)
    if sample is None:
        loose = [line for line in lines
                 if re.match(r"^-\s*sample:", line, re.I)]
        emit(CID, FAIL,
             "the verdict is TEST and %s carries no `- sample: <integer>` "
             "line; %s"
             % (RECORD,
                "the closest is %s" % clip(loose[0], 100) if loose
                else "there is no sample line at all"))

    population = weekly_active_users(CID)
    size = int(sample.group(1))
    if size > population:
        emit(CID, FAIL,
             "the sample is %d against %d %s in the frozen %s, so the test "
             "is declared over more users than exist"
             % (size, population, "weekly active users", METRICS))

    emit(CID, PASS,
         "TEST with a stopping rule (%s) and a sample of %d, inside the %d "
         "weekly active users the fixture records"
         % (clip(rule.group(1), 80), size, population))


if __name__ == "__main__":
    main()
