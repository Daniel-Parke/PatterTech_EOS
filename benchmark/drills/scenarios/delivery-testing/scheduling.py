"""When unpaid invoice reminders go out.

Reminders are sent in quarter hour windows so the mail provider is not
hit with one burst per invoice.
"""

from datetime import datetime, timedelta

WINDOW_MINUTES = 15
MAX_ATTEMPTS = 5


def next_window(now=None):
    """The start of the next quarter hour sending window."""
    now = now or datetime.now()
    top_of_hour = now.replace(minute=0, second=0, microsecond=0)
    minutes = (now.minute // WINDOW_MINUTES + 1) * WINDOW_MINUTES
    return top_of_hour + timedelta(minutes=minutes)


def retry_delay_seconds(attempt, now=None):
    """Seconds to wait before retrying a failed send.

    Doubles per attempt, with a sub second jitter taken from the clock
    so that a batch of reminders does not retry in lockstep.
    """
    if not 1 <= attempt <= MAX_ATTEMPTS:
        raise ValueError("attempt must be between 1 and %d" % MAX_ATTEMPTS)
    now = now or datetime.now()
    jitter = now.microsecond / 1_000_000
    return 2 ** attempt + jitter
