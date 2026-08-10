# Ossa

Scheduling for independent physiotherapy practices. One diary, one set
of slots, everybody looking at the same thing.

Ossa runs the appointment book: who is in, which room they are in, what
they are booked for, and what happens when somebody cancels at eight in
the morning. It does not hold clinical notes and it does not raise
invoices. Practices keep those wherever they already keep them.

Most of the practices on Ossa have between one and eight practitioners
and a front desk that is also somebody's clinical time.

## What it does

- **Waiting list backfill.** A cancelled slot goes out to the waiting
  list by text in urgency order, first accept wins, and the slot closes
  itself. `app/waiting_list.py`
- **SMS reminders.** A reminder schedule per appointment type, with
  replies routed back to the practice inbox rather than to a void.
  `app/reminders.py`
- **Recurring courses.** A six week rehabilitation course is booked as
  one thing, moves as one thing, and steps around bank holidays.
  `app/courses.py`
- **Room and equipment allocation.** A booking holds a room and the kit
  it needs, so the gym plinth cannot be taken twice. `app/rooms.py`
- **Insurer authorisation tracking.** Sessions count down against an
  authorisation and the practice is warned before the last funded one.
  `app/insurers.py`
- **Rota view.** Practitioner hours, leave and locum cover in one grid.
  `app/rota.py`
- **Day sheet export.** The day's list as CSV or as something you can
  pin up. `app/exports.py`

## Layout

- `app/` the application. Each module above is one file.
- `web/` the public site. `web/pricing.html` is the live pricing page.
- `support/tickets/` every ticket we have kept since the rebuild. They
  are written up by whoever picked the phone up.

## Running it

```
python -m venv .venv
.venv/bin/pip install -e .
python -m app
```

There are no tests worth the name yet.
