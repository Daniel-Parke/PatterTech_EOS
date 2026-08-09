#!/usr/bin/env python3
"""Criterion 10: the repricing trigger runs, and names a cost cause.

The harness raises the allocated unit cost by fifteen per cent in the
scenario's own cost export, then runs whatever repricing script the
agent committed. Three things have to be true: the script exists, it
exits zero, and it emits a new price with a stated cause of type cost.

The rise is injected into the data rather than passed as an argument.
Inventing a command line the agent was never told about would test
whether it guessed the harness, and the trigger is supposed to be
watching the cost file.

Everything happens on a copy, so a grader that dies midway cannot leave
the delivered tree holding a fabricated cost history.

The drill logs one failure here separately: a rise emitted with a cause
of demand means the dual entitlement rule did not survive the pack. This
grader names that case rather than folding it into a generic fail.

Where the script is not Python and no interpreter for it exists on this
machine, the criterion is unsettled rather than failed.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (COSTS, COST_COMPONENT_COLUMNS, DECISION,  # noqa: E402
                     FAIL, PASS, PRICING, UNIT_COST_COLUMN, UNSETTLED, emit,
                     number, read, rows_of, scratch_dir)

CID = "c10"

RISE = 1.15
MONTHS_INJECTED = 3
TIMEOUT_S = 300

NAME = re.compile(r"repric|re-pric|price[_\-]?(?:change|update|review|check)|"
                  r"(?:change|update|review|check)[_\-]?price", re.I)
SEARCH_DIRS = (PRICING, ".", "scripts", "bin", "tools")

CAUSE_KEYS = ("cause_type", "cause-type", "causeType", "cause_types")
PRICE_KEYS = ("to", "new_price", "new_headline_price", "headline_price",
              "price", "to_price")

PROSE = re.compile(r"cause[^\n]{0,60}?\bcost\b|\bcost\b[^\n]{0,30}?cause",
                   re.I)
MONEY = re.compile(r"(?<![\d.])(\d+(?:\.\d{1,2})?)(?![\d])")


# ------------------------------------------------------------- finding it


def find_script(scratch):
    seen, found = set(), []
    for where in SEARCH_DIRS:
        base = scratch / where
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*")):
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            if path.suffix.lower() in (".json", ".csv", ".md", ".txt"):
                continue
            if NAME.search(path.stem):
                found.append(path)
    return found


def interpreter(path):
    """(argv prefix, why it cannot run here)."""
    suffix = path.suffix.lower()
    if suffix in (".py", ""):
        head = read(path)[:200]
        if suffix == "" and not head.startswith("#!"):
            return None, "%s has no extension and no shebang" % path.name
        if suffix == "" and "python" not in head.split("\n", 1)[0]:
            return None, ("%s is a script for %s"
                          % (path.name, head.split("\n", 1)[0][2:].strip()))
        return [sys.executable, str(path)], None
    if suffix in (".sh", ".bash"):
        shell = shutil.which("bash") or shutil.which("sh")
        if not shell:
            return None, "no bash or sh on this machine"
        return [shell, str(path)], None
    if suffix == ".ps1":
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            return None, "no PowerShell on this machine"
        return [shell, "-File", str(path)], None
    return None, "no interpreter is known here for a %s file" % suffix


# ------------------------------------------------------------- injecting


def inject_rise(copy):
    """Append months at a fifteen per cent higher unit cost."""
    path = copy / COSTS
    if not path.is_file():
        return None, ("%s is not in the delivered tree; the harness raises "
                      "the cost in that file, so the injection has nowhere "
                      "to land" % COSTS)
    rows = rows_of(path)
    if not rows:
        return None, "%s is empty or will not parse as CSV" % COSTS
    fields = list(rows[0].keys())
    if UNIT_COST_COLUMN not in fields:
        return None, ("%s no longer has a %s column, so a unit cost rise "
                      "cannot be injected into it"
                      % (COSTS, UNIT_COST_COLUMN))

    last = rows[-1]
    base = number(last.get(UNIT_COST_COLUMN))
    if base is None or base <= 0:
        return None, "the last %s in %s is %r" % (UNIT_COST_COLUMN, COSTS,
                                                  last.get(UNIT_COST_COLUMN))

    month = str(last.get("month", "")).strip()
    match = re.match(r"^(\d{4})-(\d{2})$", month)
    year, index = (int(match.group(1)), int(match.group(2))) if match \
        else (None, None)

    added = []
    for step in range(1, MONTHS_INJECTED + 1):
        row = dict(last)
        if year is not None:
            total = (year * 12 + index - 1) + step
            row["month"] = "%04d-%02d" % (total // 12, total % 12 + 1)
        row[UNIT_COST_COLUMN] = "%.2f" % (base * RISE)
        for column in COST_COMPONENT_COLUMNS:
            value = number(last.get(column))
            if value is not None:
                row[column] = "%.2f" % (value * RISE)
        added.append(row)

    import csv
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows + added:
            writer.writerow({k: row.get(k, "") for k in fields})
    return base * RISE, None


# -------------------------------------------------------- reading it back


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            for found in walk(value):
                yield found
    elif isinstance(node, list):
        for value in node:
            for found in walk(value):
                yield found


def cause_of(record):
    for key in CAUSE_KEYS:
        if key in record:
            value = record[key]
            if isinstance(value, list):
                return [str(v).strip().lower() for v in value]
            return [str(value).strip().lower()]
    return []


def price_of(record):
    for key in PRICE_KEYS:
        value = record.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
    return None


def stdout_records(stdout):
    out = []
    for line in [stdout] + stdout.splitlines():
        line = line.strip()
        if not line.startswith(("{", "[")):
            continue
        try:
            out.extend(walk(json.loads(line)))
        except ValueError:
            continue
    return [r for r in out if cause_of(r)]


def file_records(tree):
    out = []
    pricing = Path(tree) / PRICING
    if pricing.is_dir():
        for path in sorted(pricing.rglob("*.json")):
            try:
                out.extend(walk(json.loads(
                    path.read_text(encoding="utf-8"))))
            except (OSError, ValueError):
                continue
    return [r for r in out if cause_of(r)]


def fingerprint(record):
    return json.dumps(record, sort_keys=True, default=str)


def emissions(scratch, copy, stdout):
    """Price-change shaped records this run produced, and only this run.

    A record already sitting in the delivered tree before the injection
    is not something the trigger emitted. Without this the criterion
    would pass on a decision record that was hand-written with a cost
    caused change in it and a script that does nothing.
    """
    already = {fingerprint(r) for r in file_records(scratch)}
    fresh = [r for r in file_records(copy)
             if fingerprint(r) not in already]
    return stdout_records(stdout) + fresh


def old_price(scratch):
    path = scratch / DECISION
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    value = doc.get("headline_price")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None


# -------------------------------------------------------------------- run


def main():
    scratch = scratch_dir()
    scripts = find_script(scratch)
    if not scripts:
        emit(CID, FAIL,
             "no repricing script in the delivered tree; looked for a file "
             "named for repricing under %s"
             % ", ".join("%s/" % d for d in SEARCH_DIRS))
    script = scripts[0]
    argv, why = interpreter(script)
    if argv is None:
        emit(CID, UNSETTLED,
             "the repricing script is %s and %s, so the trigger was not run"
             % (script.relative_to(scratch).as_posix(), why))

    before = old_price(scratch)

    work = Path(tempfile.mkdtemp(prefix="drill-bmp-c10-"))
    try:
        copy = work / "tree"
        shutil.copytree(scratch, copy)
        in_copy = copy / script.relative_to(scratch)
        argv = [str(in_copy) if a == str(script) else a for a in argv]

        raised, problem = inject_rise(copy)
        if problem:
            emit(CID, FAIL, problem)

        env = dict(os.environ)
        env["PYTHONPATH"] = str(copy) + os.pathsep + env.get("PYTHONPATH", "")
        try:
            proc = subprocess.run(argv, cwd=str(copy), capture_output=True,
                                  text=True, encoding="utf-8",
                                  errors="replace", timeout=TIMEOUT_S,
                                  env=env)
        except OSError as exc:
            emit(CID, UNSETTLED,
                 "the repricing script %s could not be started here: %s"
                 % (script.name, exc))
        except subprocess.TimeoutExpired:
            emit(CID, FAIL,
                 "the repricing script %s did not finish within %ds"
                 % (script.name, TIMEOUT_S))

        output = (proc.stdout or "") + "\n" + (proc.stderr or "")
        if proc.returncode != 0:
            emit(CID, FAIL,
                 "%s exits %d after the unit cost was raised to %.2f: %s"
                 % (script.name, proc.returncode, raised,
                    " ".join(output.split())[:250]))

        records = emissions(scratch, copy, proc.stdout or "")
        demand = [r for r in records
                  if any("demand" in c for c in cause_of(r))]
        if demand:
            emit(CID, FAIL,
                 "%s emits a price change with a cause of demand (%s); the "
                 "two allowed causes are cost and value, and a demand-framed "
                 "rise is the pattern the fairness evidence refuses"
                 % (script.name,
                    json.dumps(demand[0], default=str)[:160]))

        for record in records:
            if not any(c == "cost" for c in cause_of(record)):
                continue
            new = price_of(record)
            if new is None:
                continue
            if before is not None and abs(new - before) < 1e-9:
                continue
            emit(CID, PASS,
                 "%s exits 0 with the unit cost raised to %.2f and emits a "
                 "new price of %s with a cause of type cost"
                 % (script.name, raised, new))

        # Prose fallback: the criterion asks for a price and a cause, not
        # for a particular file format.
        if PROSE.search(output):
            numbers = [float(n) for n in MONEY.findall(output)]
            moved = [n for n in numbers
                     if before is None or abs(n - before) > 1e-9]
            if moved:
                emit(CID, PASS,
                     "%s exits 0 with the unit cost raised to %.2f and its "
                     "output states a cost cause alongside a new price: %r"
                     % (script.name, raised,
                        " ".join(output.split())[:140]))

        if records:
            emit(CID, FAIL,
                 "%s exits 0 but no emitted record pairs a new price with a "
                 "cause of type cost; found %s"
                 % (script.name,
                    "; ".join(json.dumps(r, default=str)[:90]
                              for r in records[:3])))
        emit(CID, FAIL,
             "%s exits 0 after the unit cost rose to %.2f but emits no new "
             "price with a stated cause: %s"
             % (script.name, raised, " ".join(output.split())[:200]
                or "no output at all"))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
