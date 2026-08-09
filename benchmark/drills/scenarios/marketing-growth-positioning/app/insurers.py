"""Insurer authorisations, counted down.

Ossa does not submit claims and does not know what anything costs. It
knows how many sessions an insurer authorised and how many are left,
and it says so before the practice books one too many.
"""

WARN_AT = 1


def remaining(authorisation, booked):
    used = sum(1 for b in booked
               if b["authorisation_ref"] == authorisation["ref"]
               and b["state"] in ("booked", "attended"))
    return authorisation["sessions"] - used


def check(authorisation, booked, today):
    left = remaining(authorisation, booked)
    if authorisation["expires_on"] < today:
        return "expired", left
    if left <= 0:
        return "exhausted", left
    if left <= WARN_AT:
        return "last-session", left
    return "ok", left


def banner(state, left, insurer):
    if state == "expired":
        return "Authorisation with %s has expired." % insurer
    if state == "exhausted":
        return "No sessions left on the %s authorisation." % insurer
    if state == "last-session":
        return "Last funded session with %s. Reauthorise or bill the patient." % insurer
    return "%d sessions left with %s." % (left, insurer)
