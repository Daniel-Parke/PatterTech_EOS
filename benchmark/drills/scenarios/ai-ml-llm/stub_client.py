"""Offline stand-in for the hosted support-classifier endpoint.

The real client posts the prompt and the ticket over HTTPS. This one
does the same job locally: it scores a few keyword features and mixes
in a value derived from the digest of the prompt, so editing the prompt
moves the answers the way the hosted model would, while the tests stay
offline and repeatable. Same call signature, no network, no key.

`complete()` returns the label the endpoint picked and the confidence
it reported for it.
"""

import hashlib
import math

LABELS = ("billing", "bug", "account", "feature")

# Builds the endpoint serves. "latest" is an alias the vendor points at
# whichever build is current, so it moves without warning.
BUILDS = ("support-classifier-20260115",)
ALIASES = {"support-classifier-latest": "support-classifier-20260115"}

FEATURES = {
    "billing": (
        "invoice", "refund", "charged", "charge", "payment", "paid",
        "card", "billed", "billing", "receipt", "subscription", "vat",
        "direct debit", "renewal", "plan", "price", "statement",
        "paying", "discount", "pro rata", "currency", "gbp", "money",
        "finance", "extra cost", "add-on", "up front", "quarter",
    ),
    "bug": (
        "error", "crash", "broken", "fails", "failing", "exception",
        "stack trace", "500", "timeout", "freezes", "blank page",
        "does not load", "wrong", "stopped working", "spinner",
        "does not match", "twice", "loses", "overflow", "one behind",
        "nothing happens", "disappeared", "hides", "zero byte",
        "never resets", "empty", "useless", "not appearing",
    ),
    "account": (
        "log in", "login", "password", "sign in", "signed in", "signed up",
        "locked out", "two factor", "seat", "seats", "email address",
        "permissions", "admin", "invite", "sso", "workspace", "profile",
        "access", "guests", "read only", "owner", "ownership",
        "directory", "colleagues", "verification", "domain", "my data",
        "team list", "restrict",
    ),
    "feature": (
        "would be nice", "please add", "support for", "feature request",
        "wish", "could you add", "roadmap", "any plans", "ability to",
        "option to", "would help", "would be useful", "would save",
        "we need a way", "is it possible", "would stop", "would remove",
        "would close", "would use", "would be enough", "a way to",
        "templates", "undo", "custom fields", "integration",
        "reordered", "automatically", "comes up every",
    ),
}

_BIAS_WEIGHT = 0.80
_WOBBLE_WEIGHT = 1.60


def resolve(model):
    """Return the build a model identifier points at."""
    build = ALIASES.get(model, model)
    if build not in BUILDS:
        raise ValueError("unknown model: %s" % model)
    return build


def _unit(*parts):
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / float(1 << 64)


def complete(model, prompt, ticket_text):
    """Ask the endpoint to route one ticket.

    Returns {"label": str, "confidence": float}, the confidence being
    the endpoint's separation between its first and second choice.
    """
    build = resolve(model)
    prompt_digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    text = ticket_text.lower()

    scores = {}
    for label in LABELS:
        hits = sum(1.0 for word in FEATURES[label] if word in text)
        bias = _unit(prompt_digest, label) - 0.5
        wobble = _unit(prompt_digest, build, label, text) - 0.5
        scores[label] = hits + _BIAS_WEIGHT * bias + _WOBBLE_WEIGHT * wobble

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    margin = ranked[0][1] - ranked[1][1]
    return {
        "label": ranked[0][0],
        "confidence": round(1.0 / (1.0 + math.exp(-3.0 * margin)), 4),
    }
