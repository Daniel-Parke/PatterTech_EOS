"""Configuration.

Values that are not secret come from a service's env file. Values that
are secret come from the environment, which the runner fills from the
secret store. Nothing here reads the secret store directly, and nothing
here writes a secret anywhere.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"


def load_env(name):
    """Parse `config/<name>.env` into a dict. Non-secret values only."""
    path = CONFIG / ("%s.env" % name)
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def api_key():
    """The tenant key, from the environment. Never from a file here."""
    key = os.environ.get("INVOICE_API_KEY", "")
    if not key:
        raise RuntimeError(
            "INVOICE_API_KEY is not set; the runner loads it from the "
            "secret store before starting the service")
    return key


def timeout_seconds(name="ledger", default=20):
    try:
        return int(load_env(name).get("EXPORT_TIMEOUT_SECONDS", default))
    except (OSError, ValueError):
        return default
