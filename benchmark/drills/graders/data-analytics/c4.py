#!/usr/bin/env python3
"""Criterion 4: the analytics layer holds no direct identifiers.

The drill's third named failure condition is source columns copied
forward without anyone asking what the analytics layer is allowed to
hold. So this reads the columns of the tables the pipeline actually
produces, not the SQL that produces them: a model that reads
`user_email` in order to hash it is doing the right thing, and a grader
grepping the source for the word would mark it wrong.

The pipeline is run on a copy with the seeded batch dropped, so a
correct gate does not stop the tables being built and the criterion
still has something to look at. Files already committed under a
warehouse or models directory are read too, in case the delivery ships
its output rather than generating it.

`raw/` is out of scope by definition. That is the export; the criterion
is about what the analytics layer carries downstream of it.
"""

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, columns_of, copy_tree,  # noqa: E402
                     drop_seeded_batch, emit, find_pipeline,
                     looks_like_missing_dependency, output_data_files,
                     parquet_column_scan, rel, run_pipeline, scratch_dir)

CID = "c4"

FORBIDDEN = re.compile(r"(?i)email|full_name|postcode")
# A hash or a surrogate key. `user_id` on its own is not either: it is
# the source identifier carried forward under the same name.
SURROGATE = re.compile(
    r"(?i)(^|_)(hash|hashed|sk|key|pseudonym|pseudonymous|anon|"
    r"anonymised|anonymized|surrogate|sid)(_|$)|"
    r"(?i)_(hash|key|sk|hk)$|(?i)^(user|customer|person|visitor)_(key|sk|hash)")


def main():
    scratch = scratch_dir()
    argv, description = find_pipeline(scratch)

    work, copy = copy_tree(scratch, "drill-data-c4-")
    try:
        if argv is not None:
            drop_seeded_batch(copy)
            code, output = run_pipeline(copy, argv)
            if code not in (0, None) and looks_like_missing_dependency(output):
                emit(CID, UNSETTLED,
                     "`%s` cannot start here (%s), so no tables were built "
                     "to inspect. That is a gap in this environment, not a "
                     "finding against the delivered tree."
                     % (description, " ".join(output.split())[:160]))

        tables = output_data_files(copy)
        if not tables:
            emit(CID, FAIL,
                 "no analytics table in the delivered tree: nothing outside "
                 "raw/ was shipped or produced, so there is no analytics "
                 "layer to inspect")

        opaque, inspected, offences, surrogates = [], [], [], []
        for path in tables:
            relative = rel(copy, path)
            columns = columns_of(path)
            if columns is None:
                if path.suffix.lower() == ".parquet":
                    blob = parquet_column_scan(path)
                    hit = FORBIDDEN.search(blob)
                    if hit:
                        offences.append("%s (parquet, byte scan) contains %r"
                                        % (relative, hit.group(0)))
                    inspected.append(relative + " (byte scan)")
                else:
                    opaque.append(relative)
                continue
            inspected.append(relative)
            bad = [c for c in columns if FORBIDDEN.search(c)]
            if bad:
                offences.append("%s carries %s" % (relative, ", ".join(bad)))
            surrogates.extend(c for c in columns if SURROGATE.search(c))

        if offences:
            emit(CID, FAIL,
                 "a delivered table carries a direct identifier: %s"
                 % "; ".join(offences[:4]))
        if not inspected:
            emit(CID, UNSETTLED,
                 "every delivered table is in a format this grader cannot "
                 "read (%s), so the criterion was not settled here"
                 % ", ".join(opaque[:4]))
        if not surrogates:
            emit(CID, FAIL,
                 "no direct identifier survives in %s, but no hashed or "
                 "surrogate identifier appears either; the analytics layer "
                 "has to be joinable on something that is not the source "
                 "identifier" % ", ".join(inspected[:4]))

        emit(CID, PASS,
             "%d delivered table(s) inspected, none carries a column matching "
             "email, full_name or postcode; the identifier is %s"
             % (len(inspected), ", ".join(sorted(set(surrogates))[:3])))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
