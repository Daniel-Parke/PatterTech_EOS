"""Build the warehouse tables from the raw nightly exports.

Straight copy for now: read the export, write it back out under
`warehouse/` so the dashboards have something to point at. Nobody has
had time to model it properly.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
WAREHOUSE = ROOT / "warehouse"


def load(name):
    with open(RAW / name, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def write(name, fields, rows):
    WAREHOUSE.mkdir(exist_ok=True)
    with open(WAREHOUSE / name, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields,
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    fields, rows = load("events.csv")
    write("events.csv", fields, rows)
    print("events: %d rows" % len(rows))

    fields, rows = load("experiment.csv")
    write("experiment.csv", fields, rows)
    print("experiment: %d rows" % len(rows))


if __name__ == "__main__":
    main()
