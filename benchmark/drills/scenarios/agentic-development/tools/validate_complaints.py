"""Check a complaints file against schemas/complaint.schema.json.

    python tools/validate_complaints.py state/complaints.jsonl

Exit 0 when every record is valid, 1 with the offending line and the
reason otherwise. Deliberately a small subset of JSON Schema: the
subset the complaint shape actually uses, so the job has no
dependencies to install on the ops box.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schemas" / "complaint.schema.json"

TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "number": (int, float),
}


def check(value, schema, where):
    want = schema.get("type")
    if want and not isinstance(value, TYPES[want]):
        return ["%s: expected %s, found %s" % (where, want, type(value).__name__)]
    if want == "object":
        return check_object(value, schema, where)
    if want == "array":
        return check_array(value, schema, where)
    return check_scalar(value, schema, where)


def check_object(value, schema, where):
    problems = []
    for key in schema.get("required", []):
        if key not in value:
            problems.append("%s: missing %s" % (where, key))
    properties = schema.get("properties", {})
    if schema.get("additionalProperties") is False:
        for key in value:
            if key not in properties:
                problems.append("%s: unexpected key %s" % (where, key))
    for key, sub in properties.items():
        if key in value:
            problems += check(value[key], sub, "%s.%s" % (where, key))
    return problems


def check_array(value, schema, where):
    problems = []
    minimum = schema.get("minItems")
    if minimum is not None and len(value) < minimum:
        problems.append("%s: needs at least %d item(s)" % (where, minimum))
    items = schema.get("items")
    if items:
        for i, item in enumerate(value):
            problems += check(item, items, "%s[%d]" % (where, i))
    return problems


def check_scalar(value, schema, where):
    problems = []
    if "enum" in schema and value not in schema["enum"]:
        problems.append("%s: %r is not one of %s"
                        % (where, value, ", ".join(map(str, schema["enum"]))))
    if "pattern" in schema and not re.match(schema["pattern"], str(value)):
        problems.append("%s: %r does not match %s"
                        % (where, value, schema["pattern"]))
    if "minLength" in schema and len(str(value)) < schema["minLength"]:
        problems.append("%s: shorter than %d characters"
                        % (where, schema["minLength"]))
    if "maxLength" in schema and len(str(value)) > schema["maxLength"]:
        problems.append("%s: longer than %d characters"
                        % (where, schema["maxLength"]))
    return problems


def main(argv):
    if len(argv) != 2:
        raise SystemExit(__doc__)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    target = Path(argv[1])
    bad = 0
    seen = 0
    for n, line in enumerate(target.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        seen += 1
        try:
            record = json.loads(line)
        except ValueError as exc:
            print("line %d: not JSON: %s" % (n, exc))
            bad += 1
            continue
        for problem in check(record, schema, "line %d" % n):
            print(problem)
            bad += 1
    print("%d record(s) read, %d problem(s)" % (seen, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
