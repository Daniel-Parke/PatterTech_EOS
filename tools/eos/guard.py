"""Action-time guard: layer 2 of risk control.

kernel/GUARD_SPEC.md is the law this module implements, verbatim in
semantics: ten guarded classes, four verdicts, non-waivable floors,
unknown-action conservatism and mechanical fail-closed behaviour per
kernel/schemas/guard-action.schema.json.

evaluate(action, policy, adapter_validated) returns one document valid
under guard-action.schema.json.

The host enforcement adapter is loaded, not believed. A policy that
says guard.validated is true proves nothing on its own: this module
reads the mapping file the policy names, checks that it carries a
bypass-suite validation record whose cases all passed, and derives
validation from that. A missing, malformed or failing mapping fails
closed; so does a policy whose guard.validated is anything other than
explicitly true, absent included. And a guarded class the suite never
demonstrated as enforced stays manual-only even under a validated
adapter. See kernel/adapters/README.md.

The action descriptor is a dict. Recognised keys:

- action_class: one of the ten classes, when the caller knows it.
- payload_summary: what the action would do (required in the output).
- command: a shell command line to classify mechanically.
- script_content: content the command would execute (makefiles,
  scripts), scanned with the same rules, so indirection does not evade
  classification.
- tool: tool name for non-shell actions.
- mapped_verdict: the adapter mapping's ruling for a recognised action
  (allow or require-approval). Honoured only under a validated adapter
  and never past a floor.
- Flags: targets_production, emits_secret, new_destination,
  accepts_legal_terms, declared_irreversible.

Classification is deliberately conservative: an unknown shell command
can reach every guarded class through the shell, so it classifies as
guarded and rules manual-only. The guard never guesses an allow.
"""

from __future__ import annotations

import json
import re
import shlex
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

GUARDED_CLASSES = (
    "external-write",
    "deployment",
    "deletion",
    "destructive-git",
    "dependency-install",
    "production-data",
    "secrets",
    "pii-egress",
    "money-movement",
    "irreversible",
)

VERDICTS = ("allow", "require-approval", "manual-only", "deny")

# Nested shell and interpreter wrappers whose payload is re-classified.
_WRAPPER_RE = re.compile(
    r"(?i)^(?:bash|sh|zsh|dash)\s+-l?c\s+(?P<inner>.+)$"
    r"|^powershell(?:\.exe)?\s+(?:-\w+\s+)*-c(?:ommand)?\s+(?P<inner2>.+)$"
    r"|^pwsh\s+(?:-\w+\s+)*-c(?:ommand)?\s+(?P<inner3>.+)$"
    r"|^cmd(?:\.exe)?\s+/c\s+(?P<inner4>.+)$"
    r"|^python[0-9.]*\s+-c\s+(?P<inner5>.+)$"
    r"|^(?:env\s+|nohup\s+|timeout\s+\d+\s+)(?P<inner6>.+)$"
)

# Ordered (class, pattern) rules over the flattened action text. First
# match wins within a severity ordering applied by _classify_text.
_TEXT_RULES = [
    ("money-movement", re.compile(r"(?i)\b(stripe\s+(charge|transfer|payout)|wire\s+transfer|send\s+funds|paypal\s+payout)\b")),
    ("secrets", re.compile(r"(?i)(\.env\b|secretsmanager|vault\s+(read|kv)|BEGIN (RSA |EC )?PRIVATE KEY|id_rsa|\bAWS_SECRET|\bprintenv\b.*(SECRET|TOKEN|KEY))")),
    ("destructive-git", re.compile(r"(?i)git\s+push\s+[^|;&]*(--force(-with-lease)?|\s-f\b)|git\s+push\s+\S+\s+:\S+|git\s+push\s+--delete|git\s+branch\s+-D\b|git\s+tag\s+-d\b|git\s+(filter-branch|filter-repo)\b|git\s+reset\s+--hard\s+\S+.*&&.*push|git\s+rebase\b.*&&.*push")),
    ("destructive-git", re.compile(r"(?i)(\.git/hooks/|\.claude/settings|hooks?\.(json|ya?ml)\b|pre-commit\b.*(>|>>|sed\s+-i|tee\b)|(>|>>|sed\s+-i|tee\b).*\.git/hooks)")),
    ("deletion", re.compile(r"(?i)\brm\s+(-\w*\s+)*(/|~|\.\.)|\bdel\s+/s\b|DROP\s+DATABASE|aws\s+s3\s+rb|gsutil\s+rm|kubectl\s+delete\b")),
    ("production-data", re.compile(r"(?i)\b(prod(uction)?[-_.]?(db|database|data)\b|psql\s+\S*prod|--env[= ]prod)")),
    ("deployment", re.compile(r"(?i)\b(kubectl\s+(apply|rollout)|terraform\s+apply|docker\s+push|gcloud\s+(app|run)\s+deploy|aws\s+.*deploy|helm\s+(install|upgrade)|fly\s+deploy|vercel\s+(deploy|--prod))\b")),
    ("dependency-install", re.compile(r"(?i)\b(npm\s+(install|ci|i\b|add)|npm\s+run\s+(pre|post)?install|yarn\s+(add|install)|pnpm\s+(add|install)|pip[0-9.]*\s+(install|wheel|download)|python\s+setup\.py\s+(install|develop|build)|pip\s+.*--no-binary|postinstall|preinstall|build\s+hooks?|cargo\s+install|gem\s+install|apt(-get)?\s+install|brew\s+install)")),
    ("pii-egress", re.compile(r"(?i)\b(ssn|passport_number|date_of_birth|national_insurance)\b.*(curl|wget|http|post|upload)|\b(curl|wget|http|post|upload)\b.*\b(ssn|passport_number|date_of_birth|national_insurance)\b")),
    ("external-write", re.compile(r"(?i)\b(curl|wget|Invoke-WebRequest|iwr\b|Invoke-RestMethod|http\s+(post|put|delete)|git\s+push\b|git\s+remote\s+add|ssh\s|scp\s|rsync\s+\S+:|sendmail|mail\s+-s|twilio|slack\s+api|gh\s+(pr|release|issue)\s+create|npm\s+publish|twine\s+upload|subprocess\.(run|Popen|call)|os\.system|requests\.(post|put|delete)|urllib)")),
]

_LEGAL_RE = re.compile(r"(?i)(accept.*(terms|licen[cs]e|agreement|eula)|--accept-licen[cs]e|agree.*terms)")
_MAIN_FORCE_RE = re.compile(r"(?i)git\s+push\s+[^|;&]*(--force(-with-lease)?|\s-f\b)[^|;&]*\b(main|master)\b|git\s+push\s+\S+\s+:(main|master)\b|git\s+push\s+--delete\s+\S+\s+(main|master)\b")
_SECRET_EMIT_RE = re.compile(r"(?i)(cat|echo|printf|curl|wget|post|upload|tee)\b.*(\.env\b|PRIVATE KEY|id_rsa|SECRET|TOKEN|API[_-]?KEY)")

_CLASS_SEVERITY = {c: i for i, c in enumerate([
    "money-movement", "secrets", "destructive-git", "deletion",
    "production-data", "pii-egress", "deployment", "dependency-install",
    "external-write", "irreversible",
])}


def _unwrap(command):
    """Peel nested shell and interpreter wrappers, collecting layers."""
    layers = [command.strip()]
    seen = 0
    current = command.strip()
    while seen < 8:
        m = _WRAPPER_RE.match(current)
        if not m:
            break
        inner = next(g for g in m.groups() if g)
        inner = inner.strip()
        if inner[:1] in ("'", '"') and inner[-1:] == inner[:1]:
            inner = inner[1:-1]
        else:
            try:
                parts = shlex.split(inner)
                inner = " ".join(parts) if parts else inner
            except ValueError:
                pass
        layers.append(inner)
        current = inner
        seen += 1
    return layers


def _action_text(action):
    pieces = []
    command = action.get("command") or ""
    if command:
        pieces.extend(_unwrap(command))
    if action.get("script_content"):
        pieces.append(str(action["script_content"]))
    if action.get("payload_summary"):
        pieces.append(str(action["payload_summary"]))
    return "\n".join(pieces)


def classify(action):
    """Classify an action descriptor into a guarded class, or None.

    None means the action shows no contact with any guarded class and
    no shell command at all. Any shell command that matches nothing
    still classifies as external-write, because a shell can reach the
    network and the guard never guesses an allow.
    """
    explicit = action.get("action_class")
    if explicit is not None:
        if explicit not in GUARDED_CLASSES:
            raise ValueError("unknown action class: %r" % (explicit,))
        return explicit
    text = _action_text(action)
    if action.get("declared_irreversible"):
        return "irreversible"
    hits = set()
    for cls, pattern in _TEXT_RULES:
        if pattern.search(text):
            hits.add(cls)
    if action.get("emits_secret"):
        hits.add("secrets")
    if action.get("targets_production"):
        hits.add("production-data")
    if hits:
        return min(hits, key=lambda c: _CLASS_SEVERITY[c])
    if action.get("command"):
        # Unrecognised shell command: guarded by construction.
        return "external-write"
    return None


# --- host enforcement adapter -----------------------------------------

# Strictness order for capping. A verdict may only ever move right.
_VERDICT_STRICTNESS = {"allow": 0, "require-approval": 1,
                       "manual-only": 2, "deny": 3}


def _stricter(a, b):
    return a if _VERDICT_STRICTNESS[a] >= _VERDICT_STRICTNESS[b] else b


def load_adapter(policy, root=None):
    """Read the mapping file named by policy.guard.mapping_ref.

    Returns (mapping, reason). mapping is None when the policy names no
    mapping, when the file is absent, or when it does not parse. The
    reason says which, so the fail-closed ruling can explain itself.
    """
    guard_cfg = ((policy or {}).get("guard") or {})
    ref = guard_cfg.get("mapping_ref")
    if not ref:
        return None, "policy names no adapter mapping (guard.mapping_ref)"
    path = Path(root or REPO_ROOT) / str(ref).replace("\\", "/")
    if not path.is_file():
        return None, "adapter mapping file absent: %s" % ref
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return None, "adapter mapping unreadable: %s (%s)" % (ref, exc)
    if not isinstance(doc, dict):
        return None, "adapter mapping is not an object: %s" % ref
    return doc, "adapter mapping loaded: %s" % ref


def adapter_state(policy, root=None):
    """Derive the adapter's real state from the mapping on disk.

    validated is true only when the policy names a mapping, the mapping
    file exists, it carries a validation record with at least one
    bypass-suite case and no case that failed, and the policy's own
    guard.validated is explicitly true. The policy can withdraw
    validation; it can never grant it.

    Absent means withdrawn, which is what
    kernel/schemas/policy.schema.json has always said the key means and
    what the D008 seed check has always read it as. This module read an
    absent key as "not withdrawn", so one word had three readings across
    the schema, the guard and the seed check. Fail closed is the
    safety-preserving one, so it is the one all three now hold.

    covered holds the classes the suite actually demonstrated as
    enforced. Every other guarded class stays manual-only, per
    kernel/GUARD_SPEC.md, however the mapping rules it.
    """
    guard_cfg = ((policy or {}).get("guard") or {})
    reasons = []
    mapping, reason = load_adapter(policy, root)
    reasons.append(reason)
    if mapping is None:
        return {"validated": False, "covered": frozenset(), "mapping": None,
                "verdicts": {}, "reasons": reasons}

    validation = mapping.get("validation") or {}
    cases = validation.get("cases") or []
    failed = [c.get("id", "?") for c in cases
              if isinstance(c, dict) and c.get("result") != "pass"]
    validated = True
    if not cases:
        validated = False
        reasons.append("adapter mapping carries no bypass-suite cases")
    elif failed:
        validated = False
        reasons.append("bypass-suite cases failed: %s" % ", ".join(failed))
    if guard_cfg.get("validated") is not True:
        validated = False
        reasons.append(
            "policy guard.validated is %s, not true: validation withdrawn"
            % ("absent" if "validated" not in guard_cfg
               else repr(guard_cfg.get("validated"))))

    classes = mapping.get("classes") or {}
    verdicts = {}
    for name, entry in classes.items():
        if name in GUARDED_CLASSES and isinstance(entry, dict):
            verdict = entry.get("verdict", "manual-only")
            verdicts[name] = verdict if verdict in VERDICTS else "manual-only"
    recorded = set(validation.get("covered_classes") or [])
    covered = frozenset(
        name for name in recorded
        if name in GUARDED_CLASSES
        and (classes.get(name) or {}).get("covered") is True)
    if not validated:
        covered = frozenset()
    uncovered = sorted(set(GUARDED_CLASSES) - covered)
    if validated and uncovered:
        reasons.append("classes the suite did not demonstrate as enforced "
                       "stay manual-only: %s" % ", ".join(uncovered))
    return {"validated": validated, "covered": covered, "mapping": mapping,
            "verdicts": verdicts, "reasons": reasons}


def hook_surface(action):
    """What a host PreToolUse hook can actually read from a tool call.

    The hook sees the tool name and the tool input. It does not see the
    contents of files the command will later read, so script_content is
    dropped here even when the caller supplied it. Running the bypass
    cases against this reduced surface is what makes the validation
    record honest: it measures the adapter, not the test fixture.
    """
    surface = {"tool": action.get("tool") or ("Bash" if action.get("command")
                                              else None)}
    for key in ("command", "action_class", "declared_irreversible",
                "targets_production", "emits_secret", "new_destination",
                "accepts_legal_terms"):
        if action.get(key) is not None:
            surface[key] = action[key]
    return {k: v for k, v in surface.items() if v is not None}


def run_bypass_suite(mapping, cases):
    """Run the bypass contract cases against a mapping, offline.

    Each case is a (action_descriptor, expected_class) pair. A case
    passes when the mapping routes that tool through a hook event, the
    guard classifies the hook surface into a guarded class, and the
    mapping's ruling for that class is not allow. Anything else is a
    fail, and a class with no passing case is uncovered.
    """
    matchers = set((mapping or {}).get("hook_matchers") or [])
    classes = (mapping or {}).get("classes") or {}
    results = []
    for index, (action, expected_class) in enumerate(cases, start=1):
        surface = hook_surface(action)
        tool = surface.get("tool") or "Bash"
        try:
            seen = classify(surface)
        except ValueError:
            seen = None
        entry = classes.get(seen) or {}
        verdict = entry.get("verdict", "manual-only")
        hooked = tool in matchers
        blocked = (seen in GUARDED_CLASSES
                   and verdict in ("require-approval", "manual-only", "deny"))
        text = _action_text(surface)
        named = any(p.search(text) for _, p in _TEXT_RULES)
        results.append({
            "id": "B%02d" % index,
            "tool": tool,
            "surface": surface.get("command", surface.get("action_class", "")),
            "expected_class": expected_class,
            "classified": seen or "none",
            "by": "named-rule" if named else "unrecognised-command fallback",
            "mapping_verdict": verdict,
            "hook_fires": hooked,
            "result": "pass" if (hooked and blocked) else "fail",
        })
    return results


def suite_coverage(results):
    """Classes the suite demonstrated as enforced, sorted."""
    return sorted({r["classified"] for r in results if r["result"] == "pass"})


def _floor(action, action_class, text):
    """Return (floor_hit, floor_verdict) or (None, None)."""
    if action_class == "money-movement":
        return "money-movement", "manual-only"
    if _MAIN_FORCE_RE.search(text):
        return "force-push-or-delete-main", "deny"
    if action_class == "secrets" and (
            action.get("emits_secret") or _SECRET_EMIT_RE.search(text)):
        return "secret-emission", "deny"
    if action.get("targets_production") and (
            action_class in ("deletion", "production-data")
            and (action_class == "deletion" or action.get("deletes_data")
                 or re.search(r"(?i)\b(delete|drop|truncate|rm)\b", text))):
        return "production-data-deletion", "manual-only"
    if action_class == "external-write" and action.get("new_destination"):
        return "new-external-destination", "manual-only"
    if action.get("accepts_legal_terms") or _LEGAL_RE.search(text):
        return "legal-terms", "manual-only"
    return None, None


def evaluate(action, policy, adapter_validated=None, *, root=None, state=None):
    """Evaluate one action; return a guard-action document.

    Fail closed: without a validated adapter every guarded class is
    manual-only at best, and floor denies stay denies. Approval claims
    in prose or data count for nothing; only mapped_verdict from the
    shipped adapter mapping is honoured, and only under validation.

    adapter_validated is the caller's assertion that the call arrives
    through the host adapter's own hook. It can only withdraw, never
    grant: the mapping on disk decides whether that adapter is
    validated at all, and a class the bypass suite never demonstrated
    as enforced stays manual-only whatever the mapping rules for it.
    """
    policy = policy or {}
    payload = action.get("payload_summary") or action.get("command") or ""
    if not payload:
        raise ValueError("action needs a payload_summary or command")

    action_class = classify(action)
    text = _action_text(action)
    reasons = []

    if state is None:
        state = adapter_state(policy, root)
    validated = bool(state.get("validated"))
    if adapter_validated is not None and not adapter_validated:
        if validated:
            reasons.append("caller does not assert the host adapter hook: "
                           "treated as no adapter")
        validated = False
    if not validated:
        reasons.extend(r for r in state.get("reasons", [])
                       if not r.startswith("adapter mapping loaded"))

    if action_class is None:
        # Unknown action outside every guarded class: require-approval
        # at minimum. The document records it as external-write, the
        # broadest reachable class, so the ruling stays schema-valid.
        action_class = "external-write"
        verdict = "require-approval" if validated else "manual-only"
        reasons.append("unrecognised action outside the mapped classes: require-approval at minimum")
        if not validated:
            reasons.append("fail closed: no validated host enforcement adapter")
        return _doc(action_class, payload, verdict, reasons, None, validated)

    floor_hit, floor_verdict = _floor(action, action_class, text)
    if floor_hit:
        verdict = floor_verdict
        reasons.append("non-waivable floor %s: %s" % (floor_hit, floor_verdict))
        if not validated and verdict == "manual-only":
            reasons.append("fail closed: no validated host enforcement adapter")
        return _doc(action_class, payload, verdict, reasons, floor_hit, validated)

    if not validated:
        verdict = "manual-only"
        reasons.append("fail closed: no validated host enforcement adapter, guarded class %s is manual-only" % action_class)
        return _doc(action_class, payload, verdict, reasons, None, validated)

    covered = state.get("covered") or frozenset()
    if action_class not in covered:
        verdict = "manual-only"
        reasons.append("the bypass suite did not demonstrate %s as enforced: "
                       "class stays manual-only" % action_class)
        return _doc(action_class, payload, verdict, reasons, None, validated)

    always_human = set((policy.get("approvals", {}) or {}).get("always_human", []))
    mapped = action.get("mapped_verdict")
    if mapped is not None and mapped not in VERDICTS:
        raise ValueError("unknown mapped verdict: %r" % (mapped,))

    if action_class in always_human:
        verdict = "require-approval"
        reasons.append("policy approvals.always_human names %s" % action_class)
    elif mapped in ("allow", "require-approval"):
        verdict = mapped
        reasons.append("adapter mapping rules %s for this recognised action" % mapped)
    elif mapped in ("manual-only", "deny"):
        verdict = mapped
        reasons.append("adapter mapping rules %s" % mapped)
    else:
        # Recognised class, but no mapped ruling for this action:
        # unknown inside a guarded class resolves to manual-only.
        verdict = "manual-only"
        reasons.append("unrecognised action inside guarded class %s resolves to manual-only" % action_class)

    ceiling = (state.get("verdicts") or {}).get(action_class)
    if ceiling in VERDICTS and _stricter(verdict, ceiling) != verdict:
        reasons.append("capped at the mapping's ruling for %s: %s"
                       % (action_class, ceiling))
        verdict = ceiling
    return _doc(action_class, payload, verdict, reasons, None, validated)


def _doc(action_class, payload, verdict, reasons, floor_hit, validated):
    doc = {
        "action_class": action_class,
        "payload_summary": payload,
        "verdict": verdict,
        "reasons": reasons,
        "adapter_validated": validated,
    }
    if floor_hit:
        doc["floor_hit"] = floor_hit
    if not validated and verdict not in ("manual-only", "deny"):
        # Mechanical fail-closed rule from the schema, enforced here so
        # the document can never leave this module invalid.
        doc["verdict"] = "manual-only"
        doc["reasons"] = reasons + ["fail closed: verdict clamped without a validated adapter"]
    return doc
