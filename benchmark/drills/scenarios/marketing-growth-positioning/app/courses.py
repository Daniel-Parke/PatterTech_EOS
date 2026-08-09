"""A course of treatment booked as one object.

Six weekly sessions are one thing. Moving week three moves week three;
moving the course moves all of it and steps over closures.
"""

import datetime as dt

WEEK = dt.timedelta(days=7)


def plan(first_session, weeks, closures=()):
    """Dates for a course, skipping days the practice is shut."""
    dates, when = [], first_session
    while len(dates) < weeks:
        while when.date() in closures:
            when += dt.timedelta(days=1)
        dates.append(when)
        when += WEEK
    return dates


def shift(course, delta, closures=()):
    """Move every remaining session and keep the weekly rhythm."""
    moved = []
    for session in course["sessions"]:
        if session["state"] != "booked":
            moved.append(session)
            continue
        when = session["starts_at"] + delta
        while when.date() in closures:
            when += dt.timedelta(days=1)
        moved.append({**session, "starts_at": when})
    return {**course, "sessions": moved}


def remaining(course):
    return sum(1 for s in course["sessions"] if s["state"] == "booked")
