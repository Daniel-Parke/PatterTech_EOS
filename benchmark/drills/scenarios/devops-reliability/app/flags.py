"""Feature flags, read from config/flags.json.

Deliberately dumb: the file is read on every call so that flipping a
flag does not need a restart.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAGS_FILE = ROOT / "config" / "flags.json"


def _load():
    try:
        doc = json.loads(FLAGS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    flags = doc.get("flags")
    return flags if isinstance(flags, dict) else {}


def enabled(name, default=False):
    entry = _load().get(name)
    if not isinstance(entry, dict):
        return default
    return bool(entry.get("enabled", default))
