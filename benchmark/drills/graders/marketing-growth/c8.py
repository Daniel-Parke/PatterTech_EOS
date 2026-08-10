#!/usr/bin/env python3
"""Criterion 8: every contact carries a basis, a time and a source.

The stored records are read directly, and the validator is then driven
with two synthetic records built from a delivered one:

- soft opt-in with the prior transaction reference removed, which the
  criterion says must fail validation;
- a basis outside the enum, which is how a closed enum is proved closed.
  An open enum accepts legitimate interests for everything, which is the
  failure this criterion exists to catch.

The validator must still exit 0 on the delivered file, or the two
refusals prove nothing.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, all_files, contact_files, emit,  # noqa: E402
                     find_script, load_records, read, run, scratch_dir,
                     work_copy)

CID = "c8"

BASIS_KEYS = ("lawful_basis", "lawfulbasis", "basis", "legal_basis",
              "consent_basis")
TIME_KEYS = ("captured_at", "consented_at", "opted_in_at", "collected_at",
             "created_at", "added_at", "timestamp", "captured", "added",
             "date", "when")
SOURCE_KEYS = ("source", "collection_source", "captured_via", "origin",
               "captured_from", "capture_source")
TRANSACTION_KEYS = ("transaction_ref", "transaction_reference", "transaction",
                    "order_ref", "order_reference", "order_id",
                    "prior_transaction", "purchase_ref", "sale_ref")

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?)?")
SOFT = re.compile(r"soft[-_ ]?opt[-_ ]?in", re.I)

OUTSIDE = "legitimate_interests"


def value_for(record, keys):
    for key in record:
        if str(key).strip().lower() in keys:
            value = record[key]
            if value not in (None, "", [], {}):
                return str(key), value
    return None, None


def soft_token(scratch, records):
    """The spelling this tree uses for soft opt-in."""
    for record in records:
        _, value = value_for(record, BASIS_KEYS)
        if isinstance(value, str) and SOFT.match(value.strip()):
            return value.strip()
    counts = {}
    for path in all_files(scratch):
        if path.suffix.lower() not in (".py", ".json", ".md", ".txt", ".js"):
            continue
        for hit in SOFT.findall(read(path)):
            counts[hit] = counts.get(hit, 0) + 1
    if counts:
        return sorted(counts.items(), key=lambda kv: -kv[1])[0][0]
    return "soft_opt_in"


def dump_like(source, records):
    """One record file in the shape the delivered one uses."""
    text = read(source)
    try:
        doc = json.loads(text)
    except ValueError:
        return "\n".join(json.dumps(r) for r in records) + "\n"
    if isinstance(doc, dict):
        for key in ("contacts", "records", "subscribers", "rows"):
            if isinstance(doc.get(key), list):
                return json.dumps({**doc, key: records}, indent=2) + "\n"
    return json.dumps(records, indent=2) + "\n"


def main():
    scratch = scratch_dir()
    stores = contact_files(scratch)
    if not stores:
        emit(CID, FAIL, "no contact store found in the tree")
    store = stores[0]
    rel_store = store.relative_to(scratch).as_posix()

    records = load_records(store)
    if not records:
        emit(CID, FAIL, "%s holds no contact records this grader can read"
                        % rel_store)

    faults = []
    for i, record in enumerate(records):
        who = record.get("address") or record.get("email") or "record %d" % i
        basis_key, basis = value_for(record, BASIS_KEYS)
        time_key, when = value_for(record, TIME_KEYS)
        source_key, source = value_for(record, SOURCE_KEYS)
        if not basis:
            faults.append("%s carries no lawful basis" % who)
        elif basis.strip().lower().replace(" ", "_").startswith("legitimate"):
            faults.append("%s claims %s, which is not a basis for marketing "
                          "mail to an individual" % (who, basis))
        if not when:
            faults.append("%s carries no capture timestamp" % who)
        elif not ISO.match(str(when).strip()):
            faults.append("%s has %s=%r, which is not a timestamp"
                          % (who, time_key, when))
        if not source:
            faults.append("%s carries no collection source" % who)
    if faults:
        emit(CID, FAIL, "%d record fault(s) in %s: %s"
                        % (len(faults), rel_store, "; ".join(faults[:5])))

    script = find_script(scratch, "validate_contacts", keyword="contact")
    if script is None:
        emit(CID, FAIL, "the records look right but no contact validator "
                        "exists, so nothing rejects a bad one")
    rel_script = script.relative_to(scratch).as_posix()

    good = dict(records[0])
    basis_key, _ = value_for(good, BASIS_KEYS)
    basis_key = basis_key or "lawful_basis"

    soft = dict(good)
    soft[basis_key] = soft_token(scratch, records)
    for key in list(soft):
        if str(key).strip().lower() in TRANSACTION_KEYS:
            del soft[key]

    open_enum = dict(good)
    open_enum[basis_key] = OUTSIDE

    with work_copy(scratch) as tree:
        code, out = run(tree / rel_script, [rel_store], tree)
        if code is None:
            emit(CID, FAIL, "%s would not run: %s" % (rel_script, out[:200]))
        if code != 0:
            emit(CID, FAIL,
                 "%s rejects the delivered store %s (exit %d), so its "
                 "refusals below would prove nothing: %s"
                 % (rel_script, rel_store, code,
                    out.strip()[-160:] or "no output"))

        checks = [
            ("soft opt-in with no transaction reference", soft),
            ("a basis outside the enum (%s)" % OUTSIDE, open_enum),
        ]
        accepted = []
        for label, record in checks:
            probe = tree / ("_probe" + store.suffix)
            probe.write_text(dump_like(store, [record]), encoding="utf-8")
            code, out = run(tree / rel_script, [probe.name], tree)
            if code == 0:
                accepted.append(label)
            probe.unlink()
        if accepted:
            emit(CID, FAIL, "%s accepts %s"
                            % (rel_script, " and ".join(accepted)))

    emit(CID, PASS,
         "%d record(s) in %s each carry a basis, a timestamp and a source, "
         "and %s refuses both a soft opt-in with no transaction reference "
         "and a basis outside the enum"
         % (len(records), rel_store, rel_script))


if __name__ == "__main__":
    main()
