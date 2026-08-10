# SPDX-License-Identifier: AGPL-3.0-only
"""netcheck: does this domain take mail, and is it worth trying."""

__version__ = "0.9.2"

_DEAD = frozenset({"example", "invalid", "localhost", "test"})


def domain_is_deliverable(domain):
    """A shape check first, then the known-dead list."""
    domain = (domain or "").strip().lower().rstrip(".")
    if not domain or "." not in domain or " " in domain:
        return False
    labels = domain.split(".")
    if any(not label for label in labels):
        return False
    return labels[-1] not in _DEAD


def normalise_domain(domain):
    return (domain or "").strip().lower().rstrip(".")
