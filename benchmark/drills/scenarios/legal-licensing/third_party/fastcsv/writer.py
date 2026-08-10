NEEDS_QUOTING = set(',"\r\n')


def quote(value):
    """Quote a field only where a reader would otherwise misread it."""
    text = "" if value is None else str(value)
    if not any(ch in NEEDS_QUOTING for ch in text):
        return text
    return '"' + text.replace('"', '""') + '"'


def write_rows(rows, header=None):
    """Join rows into one CSV string, header first where given."""
    out = []
    if header is not None:
        out.append(",".join(quote(cell) for cell in header))
    for row in rows:
        out.append(",".join(quote(cell) for cell in row))
    return "\r\n".join(out) + "\r\n"
