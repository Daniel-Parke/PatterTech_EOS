"""Check registry: stable check ids mapped to callables.

Every registered callable takes a ctx dict {model, root, today,
offline, strict_semantic} and returns a list[Finding]. The E-series
(structural) is the v1 parity port, the S-series is semantic, the
F-series freshness. Seed checks live in checks.seed as run_seed and
are invoked per seed path, not through this registry.
"""

from __future__ import annotations

from typing import Callable

REGISTRY: dict[str, Callable] = {}


def register(check_id: str):
    def deco(fn):
        REGISTRY[check_id] = fn
        return fn
    return deco


def run_all(ctx: dict, series: str | None = None) -> list:
    """Run every registered check (optionally one series prefix), in id order."""
    findings: list = []
    for check_id in sorted(REGISTRY):
        if series and not check_id.startswith(series):
            continue
        findings.extend(REGISTRY[check_id](ctx))
    return findings


from . import structural  # noqa: E402,F401  (registers E001-E010)
from . import semantic    # noqa: E402,F401  (registers S001-S015)
from . import freshness   # noqa: E402,F401  (registers F001-F004)
from . import freeze      # noqa: E402,F401  (registers B001)
from . import seed        # noqa: E402,F401  (exposes run_seed)
