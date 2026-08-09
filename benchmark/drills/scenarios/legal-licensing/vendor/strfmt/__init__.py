"""strfmt: the string tidying bits everybody writes twice."""

__version__ = "1.0.4"

_PAIRS = (('"', '"'), ("'", "'"))


def unquote(value):
    """Strip one matched pair of quotes, if there is one."""
    for opener, closer in _PAIRS:
        if len(value) >= 2 and value.startswith(opener) \
                and value.endswith(closer):
            return value[1:-1]
    return value


def humanise(count, singular, plural=None):
    plural = plural or singular + "s"
    return "%d %s" % (count, singular if count == 1 else plural)
