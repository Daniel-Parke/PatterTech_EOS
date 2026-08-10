"""Waiting list backfill.

When a slot is released, everyone on the list who could take it is
texted in urgency order and the first to accept gets it. The slot is
held for nobody in the meantime: a held slot that nobody claims is the
thing practices were doing by hand and hated.
"""

URGENCY_ORDER = ("post-op", "acute", "routine", "review")


def candidates(entries, slot):
    """Waiting list entries that could take this slot."""
    out = [e for e in entries
           if e["practitioner_id"] in (None, slot["practitioner_id"])
           and slot["starts_at"].weekday() in e["available_days"]
           and e["appointment_type"] == slot["appointment_type"]]
    return sorted(out, key=lambda e: (URGENCY_ORDER.index(e["urgency"]),
                                      e["waiting_since"]))


def offer(entries, slot, send_text):
    """Text every candidate. First accept wins; there is no queue."""
    offered = []
    for entry in candidates(entries, slot):
        send_text(entry["mobile"], _wording(entry, slot))
        offered.append(entry["id"])
    return offered


def accept(slot, entry_id):
    if slot["state"] != "open":
        return False, "taken"
    slot["state"] = "booked"
    slot["booked_for"] = entry_id
    return True, "booked"


def _wording(entry, slot):
    return ("%s, we have %s free with %s. Reply YES to take it."
            % (entry["first_name"],
               slot["starts_at"].strftime("%a %-d %b at %H:%M"),
               slot["practitioner_name"]))
