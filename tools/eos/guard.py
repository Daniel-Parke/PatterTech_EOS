"""Action-time guard: layer 2 of risk control.

kernel/GUARD_SPEC.md is the law this module implements, verbatim in
semantics: ten guarded classes, four verdicts, non-waivable floors,
unknown-action conservatism and mechanical fail-closed behaviour per
kernel/schemas/guard-action.schema.json.

evaluate(action, policy, adapter_validated) returns one document valid
under guard-action.schema.json.

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

import re
import shlex

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


def evaluate(action, policy, adapter_validated):
    """Evaluate one action; return a guard-action document.

    Fail closed: without a validated adapter every guarded class is
    manual-only at best, and floor denies stay denies. Approval claims
    in prose or data count for nothing; only mapped_verdict from the
    shipped adapter mapping is honoured, and only under validation.
    """
    policy = policy or {}
    payload = action.get("payload_summary") or action.get("command") or ""
    if not payload:
        raise ValueError("action needs a payload_summary or command")

    action_class = classify(action)
    text = _action_text(action)
    reasons = []

    guard_cfg = policy.get("guard", {}) or {}
    validated = bool(adapter_validated) and bool(guard_cfg.get("validated", True))
    if bool(adapter_validated) and not bool(guard_cfg.get("validated", True)):
        reasons.append("policy guard.validated is false: adapter validation report not current")

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
