"""The day sheet.

CSV for whoever wants it in a spreadsheet, and a plain text version for
the printer by the kettle.
"""

import csv
import io

COLUMNS = ("time", "patient", "practitioner", "room", "type", "notes_flag")


def day_sheet_csv(bookings):
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(COLUMNS)
    for booking in sorted(bookings, key=lambda b: b["starts_at"]):
        writer.writerow([
            booking["starts_at"].strftime("%H:%M"),
            booking["patient_name"],
            booking["practitioner_name"],
            booking["room_name"],
            booking["appointment_type"],
            "first visit" if booking.get("first_visit") else "",
        ])
    return buffer.getvalue()


def day_sheet_text(bookings):
    lines = []
    for booking in sorted(bookings, key=lambda b: b["starts_at"]):
        lines.append("%s  %-22s %-16s %s"
                     % (booking["starts_at"].strftime("%H:%M"),
                        booking["patient_name"],
                        booking["practitioner_name"],
                        booking["room_name"]))
    return "\n".join(lines)
