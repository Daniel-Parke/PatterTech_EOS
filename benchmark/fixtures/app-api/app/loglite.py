"""Vendored fallback for jsonlogx: JSON lines to stderr, nothing more."""

import json
import sys


def log(event, **fields):
    record = {"event": event}
    record.update(fields)
    print(json.dumps(record, sort_keys=True, default=str), file=sys.stderr)


class _Bound:
    def __init__(self, base):
        self._base = base

    def log(self, event, **fields):
        merged = dict(self._base)
        merged.update(fields)
        log(event, **merged)


def bind(**base):
    """Return a logger with base fields attached to every record."""
    return _Bound(base)
