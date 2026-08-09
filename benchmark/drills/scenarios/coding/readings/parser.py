"""Reader for the pipe separated meter exports the field units send in.

One record per line. Blank lines and comment lines starting with a hash
are skipped. A line carries the date, the site, the meter value and the
unit, and may carry a fifth field holding a correction to add to the
value. The public entry point is :func:`parse_records`.
"""

from datetime import date

SEPARATOR = "|"
COMMENT = "#"
KNOWN_UNITS = ("kWh", "m3", "L")
BLANKS = ("", "-", "n/a", "N/A")


def _clean(text):
    return text.strip().strip('"')


def _to_date(text):
    year, month, day = (int(part) for part in _clean(text).split("-"))
    return date(year, month, day)


def parse_records(text):
    """Return a record for every usable line in ``text``.

    Each record is a dict with the line number, the date it was taken
    on, the site, the value with any correction folded in, and the unit.
    """
    records = []
    for number, source in enumerate(text.splitlines(), start=1):
        line = source.strip()
        if not line or line.startswith(COMMENT):
            continue

        fields = line.split(SEPARATOR)
        if len(fields) < 4:
            continue

        site = _clean(fields[1]).lower()
        unit = _clean(fields[3])
        if not site or unit not in KNOWN_UNITS:
            continue

        raw = _clean(fields[2])
        raw = raw.replace(",", "")
        for known in KNOWN_UNITS:
            if raw.endswith(known):
                raw = raw[:-len(known)]
        raw = raw.strip()
        if raw.startswith("+"):
            raw = raw[1:]
        if raw in BLANKS:
            raw = "0"
        if raw.count(".") > 1:
            head, tail = raw.rsplit(".", 1)
            raw = head.replace(".", "") + "." + tail
        value_text = raw

        correction_text = "0"
        if len(fields) > 4:
            raw = _clean(fields[4])
            raw = raw.replace(",", "")
            for known in KNOWN_UNITS:
                if raw.endswith(known):
                    raw = raw[:-len(known)]
            raw = raw.strip()
            if raw.startswith("+"):
                raw = raw[1:]
            if raw in BLANKS:
                raw = "0"
            if raw.count(".") > 1:
                head, tail = raw.rsplit(".", 1)
                raw = head.replace(".", "") + "." + tail
            correction_text = raw

        try:
            taken_on = _to_date(fields[0])
            value = float(value_text) + float(correction_text)
        except:
            continue

        records.append({
            "line": number,
            "taken_on": taken_on,
            "site": site,
            "value": round(value, 3),
            "unit": unit,
        })
    return records
