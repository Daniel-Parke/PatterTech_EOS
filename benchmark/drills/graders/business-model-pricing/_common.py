"""Shared helpers for the DRILL-BMP-001 graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third is used where the thing
a criterion needs is missing from the machine rather than from the
delivered tree: the pack's schema file for criterion 2, the evidence
ledger for criterion 9, an interpreter for a repricing script that is
not Python for criterion 10. In each of those the honest answer is that
nothing was looked at, and reporting that as a fail invents a finding
against work nobody inspected.

Two things this module deliberately does not do.

It does not carry its own copy of the pricing decision schema. Criterion
2 says "the pack's pricing decision schema", so the grader reads the
pack's file. A second copy here would drift, and the drill would then be
grading a schema no venture ever sees.

It does not guess at the arithmetic behind a criterion. Blended churn,
the naive lifetime value and the cost injection are all computed from
the scenario's own input files, which are fixed inputs of the drill.
"""

import csv
import json
import re
import sys
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

PRICING = "pricing"
INPUTS = "inputs"

# The five artefacts a pricing decision emits, by the name the drill
# uses for each.
DECISION = "pricing/decision.json"
RETENTION = "pricing/retention.csv"
DEFINITIONS = "pricing/definitions.md"
OBLIGATIONS = "pricing/obligations.md"
EVIDENCE = "pricing/evidence.md"

COSTS = "inputs/costs.csv"
COHORTS = "inputs/cohorts.csv"

UNIT_COST_COLUMN = "allocated_unit_cost_gbp"
COST_COMPONENT_COLUMNS = ("hosting_gbp", "support_gbp", "third_party_gbp")


def emit(cid, code, reason):
    print(json.dumps({"id": cid, "pass": code == PASS, "reason": reason}))
    sys.exit(code)


def scratch_dir():
    if len(sys.argv) < 2:
        emit("c0", FAIL, "usage: c<N>.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit("c0", FAIL, "scratch dir not found: %s" % path)
    return path


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def flatten(text):
    return re.sub(r"\s+", " ", text)


def repo_root():
    """The EOS repository this grader ships inside.

    graders/<pack>/_common.py -> graders/<pack> -> graders -> drills ->
    benchmark -> root. The graded tree is somewhere else entirely, which
    is the point: the schema and the evidence ledger belong to the pack
    being tested, not to the agent's delivery.
    """
    return Path(__file__).resolve().parents[4]


# ------------------------------------------------------------- artefacts


def decision_doc(cid, scratch, missing_is=FAIL):
    """Load pricing/decision.json, or emit and exit.

    Every criterion from 2 onwards that reads the decision needs it to
    exist, and criterion 1 is the one that reports its absence. So the
    others say so in their reason and fail rather than pretending to a
    finding of their own.
    """
    path = Path(scratch) / DECISION
    if not path.is_file():
        emit(cid, missing_is,
             "no %s, so this criterion cannot be settled; criterion 1 is "
             "where that is reported" % DECISION)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        emit(cid, missing_is, "%s does not parse: %s" % (DECISION, exc))


def rows_of(path):
    """Every row of a CSV as a dict, or None if it will not read."""
    try:
        with open(path, newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))
    except (OSError, csv.Error, UnicodeError):
        return None


def number(value):
    try:
        return float(str(value).strip().replace(",", ""))
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------- inputs


def cohort_panel(scratch):
    """{cohort_month: {age: accounts}} from the scenario's cohort export."""
    rows = rows_of(Path(scratch) / COHORTS)
    if not rows:
        return None
    panel = {}
    for row in rows:
        month = (row.get("cohort_month") or "").strip()
        age = number(row.get("age_months"))
        count = number(row.get("accounts_retained"))
        if not month or age is None or count is None:
            return None
        panel.setdefault(month, {})[int(age)] = count
    return panel or None


def blended_churn(scratch):
    """Accounts lapsing over accounts exposed, across the whole panel.

    The house definition of blended churn is accounts lapsing in a period
    over accounts active at the start of it, so pooling the panel gives
    the single rate the refused formula would divide by.
    """
    panel = cohort_panel(scratch)
    if not panel:
        return None
    lapsed = exposed = 0.0
    for ages in panel.values():
        for age in sorted(ages):
            if age == 0 or (age - 1) not in ages:
                continue
            lapsed += max(ages[age - 1] - ages[age], 0.0)
            exposed += ages[age - 1]
    if exposed <= 0:
        return None
    return lapsed / exposed


def cost_rows(scratch):
    return rows_of(Path(scratch) / COSTS)


def latest_unit_cost(scratch):
    rows = cost_rows(scratch)
    if not rows:
        return None
    for row in reversed(rows):
        value = number(row.get(UNIT_COST_COLUMN))
        if value is not None:
            return value
    return None


# ---------------------------------------------------------- pack schema


SCHEMA_REL = "packs/business-model-pricing/refs/pricing-decision.schema.json"


def pack_schema(cid):
    path = repo_root() / SCHEMA_REL
    if not path.is_file():
        emit(cid, UNSETTLED,
             "the pack's schema is not at %s, so nothing was validated "
             "against it here" % SCHEMA_REL)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        emit(cid, UNSETTLED,
             "the pack's schema at %s does not parse (%s), so nothing was "
             "validated against it" % (SCHEMA_REL, exc))


class Unsupported(Exception):
    """A schema keyword this validator does not implement.

    Raised rather than ignored. A validator that skips what it does not
    understand reports a document as valid that it never checked, which
    is the one failure mode a grader must not have.
    """


_KNOWN = {
    "type", "enum", "const", "required", "properties", "additionalProperties",
    "items", "minItems", "maxItems", "minLength", "maxLength", "minimum",
    "maximum", "exclusiveMinimum", "exclusiveMaximum", "pattern",
    # Annotations, no assertion behaviour.
    "$schema", "$id", "title", "description", "default", "examples",
    "$comment",
}

_TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "null": type(None),
}


def _is_type(value, name):
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    expected = _TYPES.get(name)
    if expected is None:
        raise Unsupported("type %r" % name)
    if expected is not bool and isinstance(value, bool):
        return False
    return isinstance(value, expected)


def validate(doc, schema, where="$"):
    """Return a list of human-readable violations. Draft 2020-12 subset.

    Only the keywords the pack's schema actually uses are implemented.
    Anything else raises Unsupported, and the grader reports the
    criterion as unsettled rather than passing a document it did not
    fully check.
    """
    unknown = set(schema) - _KNOWN
    if unknown:
        raise Unsupported("keyword(s) %s at %s"
                          % (", ".join(sorted(unknown)), where))

    errors = []

    if "type" in schema:
        names = schema["type"]
        names = names if isinstance(names, list) else [names]
        if not any(_is_type(doc, n) for n in names):
            errors.append("%s should be %s, found %s"
                          % (where, " or ".join(names),
                             type(doc).__name__))
            return errors

    if "const" in schema and doc != schema["const"]:
        errors.append("%s should be %r, found %r"
                      % (where, schema["const"], doc))
    if "enum" in schema and doc not in schema["enum"]:
        errors.append("%s should be one of %s, found %r"
                      % (where, ", ".join(repr(v) for v in schema["enum"]),
                         doc))

    if isinstance(doc, str):
        if "minLength" in schema and len(doc) < schema["minLength"]:
            errors.append("%s is shorter than %d characters"
                          % (where, schema["minLength"]))
        if "maxLength" in schema and len(doc) > schema["maxLength"]:
            errors.append("%s is longer than %d characters"
                          % (where, schema["maxLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], doc):
            errors.append("%s does not match %s" % (where, schema["pattern"]))

    if isinstance(doc, (int, float)) and not isinstance(doc, bool):
        if "minimum" in schema and doc < schema["minimum"]:
            errors.append("%s is below %s" % (where, schema["minimum"]))
        if "maximum" in schema and doc > schema["maximum"]:
            errors.append("%s is above %s" % (where, schema["maximum"]))
        if "exclusiveMinimum" in schema and doc <= schema["exclusiveMinimum"]:
            errors.append("%s must be above %s"
                          % (where, schema["exclusiveMinimum"]))
        if "exclusiveMaximum" in schema and doc >= schema["exclusiveMaximum"]:
            errors.append("%s must be below %s"
                          % (where, schema["exclusiveMaximum"]))

    if isinstance(doc, dict):
        for name in schema.get("required", []):
            if name not in doc:
                errors.append("%s is missing required field %r"
                              % (where, name))
        properties = schema.get("properties", {})
        for name, sub in properties.items():
            if name in doc:
                errors.extend(validate(doc[name], sub,
                                       "%s.%s" % (where, name)))
        extra = schema.get("additionalProperties", True)
        if extra is False:
            for name in doc:
                if name not in properties:
                    errors.append("%s carries unexpected field %r"
                                  % (where, name))
        elif isinstance(extra, dict):
            for name, value in doc.items():
                if name not in properties:
                    errors.extend(validate(value, extra,
                                           "%s.%s" % (where, name)))

    if isinstance(doc, list):
        if "minItems" in schema and len(doc) < schema["minItems"]:
            errors.append("%s has %d entries, fewer than the %d required"
                          % (where, len(doc), schema["minItems"]))
        if "maxItems" in schema and len(doc) > schema["maxItems"]:
            errors.append("%s has %d entries, more than the %d allowed"
                          % (where, len(doc), schema["maxItems"]))
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(doc):
                errors.extend(validate(item, item_schema,
                                       "%s[%d]" % (where, i)))

    return errors
