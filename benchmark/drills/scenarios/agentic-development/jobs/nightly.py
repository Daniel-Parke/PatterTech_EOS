"""Run one night's extraction over the exported transcripts.

Serial, one process, no resume. It was a stopgap and it never got past
being one. Usage:

    python jobs/nightly.py 2026-08-03
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract import extract_complaint  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS = ROOT / "transcripts"
STATE = ROOT / "state" / "complaints.jsonl"


def transcripts_for(night):
    folder = TRANSCRIPTS / night
    if not folder.is_dir():
        raise SystemExit("no transcripts for %s" % night)
    return sorted(folder.glob("*.txt"))


def main(argv):
    if len(argv) != 2:
        raise SystemExit(__doc__)
    night = argv[1]
    paths = transcripts_for(night)
    print("%d transcripts for %s" % (len(paths), night))

    STATE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE, "a", encoding="utf-8") as out:
        for i, path in enumerate(paths, 1):
            ticket = path.stem
            text = path.read_text(encoding="utf-8")
            record = extract_complaint(ticket, text, night)
            out.write(json.dumps(record, sort_keys=True) + "\n")
            out.flush()
            print("  %2d/%d %s" % (i, len(paths), ticket))

    print("wrote %s" % STATE)
    print("now validate, then write the week's report by hand")


if __name__ == "__main__":
    main(sys.argv)
