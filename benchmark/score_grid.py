"""Score a whole prepared grid: map transcripts, run criteria, append rows.

Stdlib only. `score.py` scores one session and is frozen; this drives
it across every run in a grid without touching it.

    python benchmark/score_grid.py --grid DIR --transcripts DIR \
        [--variant-suffix ""] [--dry-run]

Every run in the grid's plan.json is matched to its session transcript
by the run id the session prompt carries, scored through score.py, and
appended to benchmark/results/ledger.json as one row. A run whose
transcript cannot be found is reported and skipped rather than scored
from a partial tree, because a row with no session behind it is worse
than a missing row.

Rows carry the variant from the plan, so the arm a row belongs to comes
from the prepared tree rather than from a label typed at scoring time.
That was the hole: `--variant` used to be free text that nothing
upstream consumed.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

BENCH = Path(__file__).resolve().parent
REPO = BENCH.parent


def load_plan(grid):
    path = Path(grid) / "plan.json"
    if not path.is_file():
        sys.exit("error: no plan.json in %s; run `harness.py grid` first"
                 % grid)
    return json.loads(path.read_text(encoding="utf-8"))


def map_transcripts(transcripts, run_ids):
    """run_id -> transcript path, matched on the id in the session prompt."""
    tdir = Path(transcripts)
    if not tdir.is_dir():
        sys.exit("error: transcript directory not found: %s" % tdir)
    found = {}
    for path in sorted(tdir.glob("agent-*.jsonl")):
        head = path.read_text(encoding="utf-8", errors="replace")[:20000]
        # Longest first: G-v1-T01-doc-fix-t1 must not match inside
        # G-v1-T01-doc-fix-t10 if a grid ever runs to ten trials.
        for run_id in sorted(run_ids, key=len, reverse=True):
            if run_id in head and run_id not in found:
                found[run_id] = path
                break
    return found


def score_one(task_dir, scratch, transcript, variant, run_id, notes):
    cmd = [sys.executable, str(BENCH / "score.py"),
           "--task", str(task_dir), "--scratch", str(scratch),
           "--transcript", str(transcript), "--variant", variant,
           "--run-id", run_id, "--notes", notes]
    return subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--grid", required=True)
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--notes", default="")
    # The ledger already holds rows labelled v1 and v2 from the
    # 2026-08-03 batch, whose variant mechanism was never encoded and
    # cannot be reproduced. Pooling those with a fresh grid would
    # average two measurements that are not the same measurement, so a
    # new batch takes its own labels and the old rows stay where they
    # are as history. gates.py already selects arms by label.
    ap.add_argument("--variant-suffix", default="",
                    help="appended to each row's variant, e.g. -2026-08-08")
    # A transcript file exists for every agent the runner launched,
    # including ones that never ran: a session killed by a rate limit
    # still leaves a file with the opening turn in it. Scoring those
    # would put rows in the ledger for sessions that did no work, which
    # is the one thing worse than a missing row. Pass the ids that
    # actually returned a result.
    ap.add_argument("--completed",
                    help="JSON file holding the list of run ids that "
                         "genuinely finished; others are skipped")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    allowed = None
    if args.completed:
        allowed = set(json.loads(
            Path(args.completed).read_text(encoding="utf-8")))

    plan = load_plan(args.grid)
    runs = plan["runs"]
    ids = [r["run_id"] for r in runs]
    found = map_transcripts(args.transcripts, ids)

    if allowed is not None:
        found = {k: v for k, v in found.items() if k in allowed}
    missing = [i for i in ids if i not in found]
    scored, failed = [], []

    for run in runs:
        rid = run["run_id"]
        if rid not in found:
            continue
        if args.dry_run:
            scored.append(rid)
            continue
        proc = score_one(run["task_dir"], run["scratch"], found[rid],
                         run["variant"] + args.variant_suffix, rid,
                         args.notes)
        if proc.returncode != 0:
            failed.append({"run_id": rid,
                           "why": (proc.stderr or proc.stdout).strip()[:200]})
        else:
            scored.append(rid)

    report = {
        "planned": len(runs),
        "transcripts_matched": len(found),
        "scored": len(scored),
        "missing_transcript": missing,
        "failed": failed,
    }
    print(json.dumps(report, indent=1))
    return 1 if (missing or failed) else 0


if __name__ == "__main__":
    sys.exit(main())
