"""duraconf: key = value files that survive being edited by people."""

import strfmt

__version__ = "2.1.0"


def read(path):
    """Parse one config file into a dict of strings."""
    settings = {}
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            settings[key.strip()] = strfmt.unquote(value.strip())
    return settings


def write(path, settings):
    lines = ["%s = %s" % (k, settings[k]) for k in sorted(settings)]
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
