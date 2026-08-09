"""tinytmpl: braces in, string out, nothing else."""

import re

__version__ = "1.4.0"

_SLOT = re.compile(r"\{\{\s*(\w+)\s*\}\}")


def render(template, **values):
    """Replace every {{ name }} with the matching value."""

    def swap(match):
        key = match.group(1)
        if key not in values:
            raise KeyError(key)
        return str(values[key])

    return _SLOT.sub(swap, template)
