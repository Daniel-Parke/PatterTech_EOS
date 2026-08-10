"""Task router: layer 1 of risk control.

kernel/POLICY_SPEC.md is the law this module implements. The factor
table below mirrors its 13-row table as data; if the spec and this
table ever disagree, the spec wins and this file is the bug.

Two entry points:

- derive_signals(root, base_ref, declared) inspects the actual git diff
  and returns mechanical derived signals (detector id to evidence).
- route(declared, derived, policy) unions declared facts with derived
  signals and rules the minimum tier consistent with the active
  factors, with machine-readable reasons per task-record.schema.json.

Paths and diff size are signals that instantiate semantic factors. No
rule here maps a path alone to a tier. Detection is mechanical, never
interpretive: text inside data files is data, and instructions found in
data activate no factor.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

TIERS = ("R0", "R1", "R2", "R3")
_TIER_RANK = {t: i for i, t in enumerate(TIERS)}

# Declarable side effects, from task-record.schema.json.
DECLARABLE = {
    "sends-external",
    "writes-production-data",
    "migrates-schema",
    "touches-auth",
    "handles-pii",
    "financial-impact",
    "irreversible-action",
    "rollback-cost",
}

# The 13-row factor table, mirroring kernel/POLICY_SPEC.md (the law).
# sources are declared side-effect names, derived detector ids, or path
# classes (paths:protected, paths:sensitive).
FACTOR_TABLE = [
    {"id": "protected-set-contact", "tier_floor": "R3", "denies_express": False,
     "sources": ["paths:protected"]},
    {"id": "irreversible-action", "tier_floor": "R3", "denies_express": False,
     "sources": ["irreversible-action", "no-rollback"]},
    {"id": "destructive-migration", "tier_floor": "R3", "denies_express": False,
     "sources": ["ddl-drop", "destructive-dml"]},
    {"id": "key-material", "tier_floor": "R3", "denies_express": False,
     "sources": ["secret-pattern"]},
    {"id": "data-deletion", "tier_floor": "R3", "denies_express": False,
     "sources": ["data-deletion"]},
    {"id": "auth-surface", "tier_floor": "R2", "denies_express": False,
     "sources": ["touches-auth", "paths:auth"]},
    {"id": "money", "tier_floor": "R2", "denies_express": False,
     "sources": ["financial-impact", "paths:payment"]},
    {"id": "schema-change", "tier_floor": "R2", "denies_express": False,
     "sources": ["migrates-schema", "ddl-change", "migration-path"]},
    {"id": "public-contract", "tier_floor": "R2", "denies_express": False,
     "sources": ["public-api-delta"]},
    # Dependency manifests that gain install hooks are executable
    # supply-chain surface, so the install-script detector feeds this
    # factor alongside CI config and stateful infrastructure files.
    {"id": "ci-stateful-infra", "tier_floor": "R2", "denies_express": False,
     "sources": ["ci-config", "infra-state", "install-script"]},
    {"id": "pii-handling", "tier_floor": "R2", "denies_express": False,
     "sources": ["handles-pii", "pii-fields"]},
    # Denies R0 only: raises nothing by itself, so the effective floor
    # once active is Standard (R1).
    {"id": "boundary-contact", "tier_floor": "R1", "denies_express": True,
     "sources": ["sends-external", "egress"]},
    {"id": "size-threshold", "tier_floor": "R1", "denies_express": True,
     "sources": ["diff-size"]},
]

DEFAULT_EXPRESS = {"max_diff_lines": 200, "max_files": 10}

_DEP_MANIFESTS = ("package.json", "pyproject.toml", "setup.py")
_AUTH_NAMES = {
    "auth", "authn", "authz", "authentication", "authorization",
    "authorisation", "oauth", "login", "sso",
}
_PAYMENT_NAMES = {
    "billing", "payment", "payments", "checkout", "stripe", "invoice",
    "invoices", "payout", "payouts",
}
_CI_MARKERS = (
    ".github/workflows/", ".gitlab-ci.yml", "jenkinsfile",
    "azure-pipelines", ".circleci/", "dockerfile", "docker-compose",
    ".tf", "ansible/",
)
_PUBLIC_API_MARKERS = ("api/", "public/", "openapi", ".d.ts")

_SECRET_RE = re.compile(
    r"(?i)(?:\b(?:api[_-]?key|secret|token|password|passwd)\b\s*[:=])"
    r"|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"
)
_DDL_RE = re.compile(r"(?i)\b(?:CREATE|ALTER)\s+(?:TABLE|INDEX|VIEW|SCHEMA|TYPE)\b")
_DDL_DROP_RE = re.compile(r"(?i)\b(?:DROP\s+(?:TABLE|COLUMN|INDEX|SCHEMA|VIEW)|TRUNCATE\s+TABLE|TRUNCATE\b)")
_DML_DESTRUCTIVE_RE = re.compile(r"(?i)\b(?:DELETE\s+FROM|UPDATE\s+\w+\s+SET)\b")
_DROP_DATABASE_RE = re.compile(r"(?i)\bDROP\s+DATABASE\b")
_INSTALL_SCRIPT_RE = re.compile(r'"(?:preinstall|postinstall|install|prepare|prepublish)"\s*:')
_PII_RE = re.compile(r"(?i)\b(?:ssn|social_security|national_insurance|date_of_birth|passport_number)\b")


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), proc.stderr.strip()))
    return proc.stdout


def _is_sqlish(path):
    parts = path.lower().split("/")
    return path.lower().endswith(".sql") or any(
        p in ("migrations", "migration") for p in parts
    )


def _name_parts(path):
    parts = path.lower().split("/")
    stem = Path(parts[-1]).stem
    return set(parts[:-1]) | {stem}


def _glob_match(path, patterns):
    import fnmatch
    for pat in patterns:
        if fnmatch.fnmatch(path, pat):
            return pat
        if pat.endswith("/") and path.startswith(pat):
            return pat
    return None


def derive_signals(root, base_ref, declared, *, policy=None):
    """Inspect the diff against base_ref and return derived signals.

    Returns a dict with meta keys (changed_paths, deleted_paths,
    diff_lines, diff_files) and a 'signals' dict of detector id to
    evidence string. Read-only towards the repository.
    """
    root = Path(root)
    policy = policy or {}
    signals = {}

    numstat = _git(root, "diff", "--numstat", base_ref)
    diff_lines = 0
    changed_paths = []
    for line in numstat.splitlines():
        cols = line.split("\t")
        if len(cols) < 3:
            continue
        add, dele, path = cols[0], cols[1], cols[-1]
        path = path.replace("\\", "/")
        changed_paths.append(path)
        if add.isdigit():
            diff_lines += int(add)
        if dele.isdigit():
            diff_lines += int(dele)

    name_status = _git(root, "diff", "--name-status", base_ref)
    deleted_paths = []
    for line in name_status.splitlines():
        cols = line.split("\t")
        if not cols:
            continue
        status = cols[0]
        if status.startswith("D") and len(cols) > 1:
            deleted_paths.append(cols[1].replace("\\", "/"))
        if status.startswith("R") and len(cols) > 2:
            old = cols[1].replace("\\", "/")
            if old not in changed_paths:
                changed_paths.append(old)

    diff_text = _git(root, "diff", base_ref)
    added_lines = [l[1:] for l in diff_text.splitlines()
                   if l.startswith("+") and not l.startswith("+++")]
    added_text = "\n".join(added_lines)

    path_patterns = (policy.get("risk", {}) or {}).get("path_patterns", {})
    for cls in ("protected", "sensitive"):
        pats = path_patterns.get(cls, [])
        for path in changed_paths:
            hit = _glob_match(path, pats)
            if hit:
                signals["paths:" + cls] = "%s matches %s pattern %s" % (path, cls, hit)
                break

    dep_deltas = []
    for path in changed_paths:
        low = path.lower()
        base = low.rsplit("/", 1)[-1]
        if base in _DEP_MANIFESTS or base.startswith("requirements") and base.endswith(".txt") or low.endswith(".lock"):
            dep_deltas.append(path)
        if any(m in low or low.endswith(m.rstrip("/")) for m in _CI_MARKERS):
            signals.setdefault("ci-config", "CI or infra file touched: %s" % path)
        if any(m in low for m in _PUBLIC_API_MARKERS):
            signals.setdefault("public-api-delta", "public API surface touched: %s" % path)
        names = _name_parts(path)
        if names & _AUTH_NAMES:
            signals.setdefault("paths:auth", "auth surface path touched: %s" % path)
        if names & _PAYMENT_NAMES:
            signals.setdefault("paths:payment", "payment or billing path touched: %s" % path)
        if low.endswith(".env") or "/.env" in low or low == ".env":
            signals.setdefault("secret-pattern", "environment secrets file touched: %s" % path)
    if dep_deltas:
        signals["dependency-manifest-delta"] = "dependency manifest changed: %s" % ", ".join(dep_deltas)

    # DDL and DML detection runs only over sql and migration content:
    # mechanical keyword scan of added lines, no interpretation of prose.
    sql_added = []
    for path in changed_paths:
        if _is_sqlish(path):
            signals.setdefault("migration-path", "migration path touched: %s" % path)
    if any(_is_sqlish(p) for p in changed_paths):
        sql_added = added_lines
    sql_text = "\n".join(sql_added)
    if sql_text:
        if _DDL_DROP_RE.search(sql_text):
            signals["ddl-drop"] = "destructive DDL in diff: %s" % _DDL_DROP_RE.search(sql_text).group(0)
        if _DML_DESTRUCTIVE_RE.search(sql_text):
            signals["destructive-dml"] = "destructive DML in diff: %s" % _DML_DESTRUCTIVE_RE.search(sql_text).group(0)
        if _DDL_RE.search(sql_text):
            signals["ddl-change"] = "DDL in diff: %s" % _DDL_RE.search(sql_text).group(0)
    if _DROP_DATABASE_RE.search(added_text):
        signals["data-deletion"] = "DROP DATABASE in diff"

    if _SECRET_RE.search(added_text):
        signals.setdefault("secret-pattern", "secret-like pattern in added lines: %s"
                           % _SECRET_RE.search(added_text).group(0)[:40])

    if dep_deltas and _INSTALL_SCRIPT_RE.search(added_text):
        signals["install-script"] = ("dependency manifest gains an install hook: %s"
                                     % _INSTALL_SCRIPT_RE.search(added_text).group(0))

    if _PII_RE.search(added_text):
        signals["pii-fields"] = "personal-data field in added lines: %s" % _PII_RE.search(added_text).group(0)

    return {
        "changed_paths": changed_paths,
        "deleted_paths": deleted_paths,
        "diff_lines": diff_lines,
        "diff_files": len(changed_paths),
        "signals": signals,
    }


def route(declared, derived, policy=None):
    """Rule the minimum tier consistent with the active factors.

    declared: {'capabilities': [...], 'side_effects': [...]} per the
    task record. derived: the derive_signals result (or a bare
    {'signals': ...} dict). Returns {'tier', 'reasons', 'discrepancies'}
    where reasons rows follow task-record.schema.json and discrepancies
    lists factors the derived signals exposed but the declaration
    missed. Deterministic given the same inputs and policy version.
    """
    policy = policy or {}
    declared = declared or {}
    side_effects = set(declared.get("side_effects", []))
    signals = dict((derived or {}).get("signals", {}))

    express = dict(DEFAULT_EXPRESS)
    express.update(policy.get("express", {}) or {})
    diff_lines = (derived or {}).get("diff_lines", 0)
    diff_files = (derived or {}).get("diff_files", 0)
    if diff_lines > express["max_diff_lines"] or diff_files > express["max_files"]:
        signals["diff-size"] = ("diff size %d lines across %d files exceeds express limits %d/%d"
                               % (diff_lines, diff_files,
                                  express["max_diff_lines"], express["max_files"]))

    reasons = []
    discrepancies = []
    floor = "R0"
    denies_express = False

    for factor in FACTOR_TABLE:
        declared_hits = [s for s in factor["sources"] if s in side_effects]
        derived_hits = [s for s in factor["sources"] if s in signals]
        if not declared_hits and not derived_hits:
            continue
        if declared_hits:
            reasons.append({
                "factor": factor["id"],
                "tier_floor": factor["tier_floor"],
                "source": "declared",
                "evidence": "declared side effect: %s" % ", ".join(declared_hits),
            })
        for hit in derived_hits:
            row = {
                "factor": factor["id"],
                "tier_floor": factor["tier_floor"],
                "source": "derived",
                "evidence": signals[hit],
            }
            # A derived activation of a factor with a declarable source
            # that was not declared is a gate-time discrepancy.
            declarable = set(factor["sources"]) & DECLARABLE
            if declarable and not declared_hits:
                row["discrepancy"] = True
                if factor["id"] not in discrepancies:
                    discrepancies.append(factor["id"])
            reasons.append(row)
        if _TIER_RANK[factor["tier_floor"]] > _TIER_RANK[floor]:
            if not factor["denies_express"]:
                floor = factor["tier_floor"]
        if factor["denies_express"]:
            denies_express = True

    if denies_express and floor == "R0":
        floor = "R1"

    return {"tier": floor, "reasons": reasons, "discrepancies": discrepancies}
