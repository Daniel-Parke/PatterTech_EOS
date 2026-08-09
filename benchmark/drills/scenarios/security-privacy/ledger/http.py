"""The only way out to the network.

Every outbound request goes through `check_destination` first. A host
that is not in `config/allowed-domains.txt` is refused before the
request is made, so a typo or a new integration cannot quietly open a
route on its own.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST = ROOT / "config" / "allowed-domains.txt"


class DestinationNotAllowed(RuntimeError):
    """Raised when a host is not on the egress allowlist."""


def allowed_hosts(path=None):
    """The hosts the allowlist grants, comments and blanks dropped."""
    text = Path(path or ALLOWLIST).read_text(encoding="utf-8")
    hosts = []
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            hosts.append(line)
    return hosts


def check_destination(url, path=None):
    """Return the host, or raise if it is not granted."""
    host = urllib.parse.urlparse(url).hostname or ""
    if host not in allowed_hosts(path):
        raise DestinationNotAllowed(
            "%s is not on the egress allowlist" % (host or url))
    return host


def post_json(url, payload, timeout=20):
    check_destination(url)
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status
