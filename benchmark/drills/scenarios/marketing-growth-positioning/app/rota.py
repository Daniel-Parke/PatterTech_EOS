"""Who is in, when, and who is covering.

Practitioner hours, leave and locum cover in one grid. Leave wins over
regular hours; cover wins over leave.
"""

import datetime as dt


def working(practitioner, day):
    """Minutes the practitioner is available on this day."""
    if any(l["from"] <= day <= l["to"] for l in practitioner["leave"]):
        return []
    return practitioner["hours"].get(day.weekday(), [])


def grid(practitioners, cover, start, days=7):
    out = {}
    for offset in range(days):
        day = start + dt.timedelta(days=offset)
        rows = []
        for person in practitioners:
            slots = working(person, day)
            standing_in = [c for c in cover
                           if c["for_id"] == person["id"] and c["on"] == day]
            if standing_in and not slots:
                rows.append({"who": standing_in[0]["locum_name"],
                             "covering": person["name"],
                             "slots": standing_in[0]["hours"]})
            elif slots:
                rows.append({"who": person["name"], "covering": None,
                             "slots": slots})
        out[day] = rows
    return out
