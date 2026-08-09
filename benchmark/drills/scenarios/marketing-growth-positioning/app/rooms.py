"""Rooms and the kit in them.

A booking holds a room and whatever equipment the appointment type
needs. Two bookings cannot hold the same plinth at the same time, which
is the whole reason this module exists.
"""

NEEDS = {
    "assessment": ("couch",),
    "follow-up": ("couch",),
    "course": ("gym-plinth",),
    "review": (),
}


def clashes(bookings, candidate):
    """Bookings that would fight this one over a room or a piece of kit."""
    wanted = {candidate["room_id"], *candidate.get("equipment", ())}
    found = []
    for booking in bookings:
        if booking["id"] == candidate["id"]:
            continue
        if not _overlaps(booking, candidate):
            continue
        held = {booking["room_id"], *booking.get("equipment", ())}
        if wanted & held:
            found.append(booking["id"])
    return found


def allocate(bookings, candidate):
    conflict = clashes(bookings, candidate)
    if conflict:
        return None, conflict
    return {**candidate,
            "equipment": tuple(NEEDS.get(candidate["appointment_type"], ()))
            }, []


def _overlaps(a, b):
    return a["starts_at"] < b["ends_at"] and b["starts_at"] < a["ends_at"]
