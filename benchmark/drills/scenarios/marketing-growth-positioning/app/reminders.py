"""SMS reminders, and the replies that come back.

The schedule is per appointment type because a first assessment and a
five minute review do not need the same nagging.
"""

import datetime as dt

DEFAULT_SCHEDULE = {
    "assessment": (dt.timedelta(days=2), dt.timedelta(hours=3)),
    "follow-up": (dt.timedelta(days=1),),
    "course": (dt.timedelta(days=1),),
    "review": (dt.timedelta(hours=4),),
}

REPLY_WORDS = {
    "yes": "confirmed",
    "y": "confirmed",
    "c": "cancelled",
    "cancel": "cancelled",
    "stop": "opted-out",
}


def due(appointment, now, schedule=None):
    schedule = schedule or DEFAULT_SCHEDULE
    offsets = schedule.get(appointment["type"], (dt.timedelta(days=1),))
    sent = set(appointment.get("reminders_sent", ()))
    for offset in offsets:
        when = appointment["starts_at"] - offset
        if offset in sent or now < when:
            continue
        return offset, when
    return None, None


def classify_reply(body):
    """What the patient meant. Anything else goes to the practice inbox."""
    return REPLY_WORDS.get(body.strip().lower(), "unread")
