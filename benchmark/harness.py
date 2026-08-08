"""Run harness: prepare a scored session, map its transcript, score it.

Stdlib only. `runner.py` materialises a fixture and `score.py` scores a
finished session; nothing joined the two, and nothing at all encoded
what makes a run v1 rather than v2. That step lived outside the
repository, so the 172 rows in the ledger cannot be reproduced by a
second party from what is committed here. This module encodes it.

Subcommands:
  plan --tasks A,B --variants v1,v2 --trials N [--seed S]
      Seeded interleaved run plan, one row per session, as JSON.
  prepare --task DIR --variant V --run-id R --dest D
      Materialise the fixture, place the variant's process surface,
      write run.json into the scratch tree, print the task prompt.
  map --transcripts DIR --dest D
      Match each agent transcript under DIR to the run whose run.json
      names it, by the run id the session prompt carries.

The variant surface
-------------------
A benchmark session is an agent doing a piece of work under a process.
The fixture is the work. The variant is the process, and it reaches
the scratch tree one of two ways:

  paired      The fixture is already a seeded venture carrying its own
              EOS, so v1 and v2 are two different fixtures. seed-v1-S
              pairs with seed-v2-S and seed-v1-M with seed-v2-ORG.
  overlaid    The fixture is a bare application with no process files
              at all, so the variant's process surface is copied on
              top of it from benchmark/surfaces/<variant>/.

Which one a task uses is recorded in the run.json this module writes,
so a reader never has to infer it.
"""

import argparse
import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent
REPO = BENCH_DIR.parent
FIXTURES = BENCH_DIR / "fixtures"
SURFACES = BENCH_DIR / "surfaces"

# Fixtures that already carry a process surface, and their counterpart
# under the other variant. A task naming one of these is `paired`.
PAIRED = {
    "seed-v1-S": {"v1": "seed-v1-S", "v2": "seed-v2-S"},
    "seed-v2-S": {"v1": "seed-v1-S", "v2": "seed-v2-S"},
    "seed-v1-M": {"v1": "seed-v1-M", "v2": "seed-v2-ORG"},
    "seed-v2-ORG": {"v1": "seed-v1-M", "v2": "seed-v2-ORG"},
}

# Fixtures that are a process surface in their own right. eos-mini is
# a miniature v1 EOS: it routes through doctrine/WARGAME_INDEX.md and
# runs tools/eos_check.py, both v1 spellings. It has no v2 twin, so a
# task using it is scored on v1 only and says so rather than pretending
# to a comparison it cannot make.
SELF_SURFACED = {"eos-mini": ["v1"]}


def fail(message):
    print("error: %s" % message, file=sys.stderr)
    sys.exit(1)


def load_task(task_dir):
    path = Path(task_dir)
    doc = path / "task.json"
    if not doc.is_file():
        fail("no task.json in %s" % path)
    try:
        return path, json.loads(doc.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail("could not read %s: %s" % (doc, exc))


def resolve_surface(fixture, variant):
    """Return (fixture_to_materialise, how, surface_dir_or_None)."""
    if fixture in PAIRED:
        chosen = PAIRED[fixture].get(variant)
        if chosen is None:
            fail("no %s counterpart for paired fixture %s" % (variant, fixture))
        return chosen, "paired", None
    if fixture in SELF_SURFACED:
        if variant not in SELF_SURFACED[fixture]:
            fail("fixture %s carries only %s; it has no %s counterpart, so a "
                 "%s run of this task would be measuring nothing"
                 % (fixture, "/".join(SELF_SURFACED[fixture]), variant,
                    variant))
        return fixture, "self-surfaced", None
    surface = SURFACES / variant
    if not surface.is_dir():
        fail("no process surface at %s; a bare application fixture cannot be "
             "run under %s without one" % (surface, variant))
    return fixture, "overlaid", surface


def copy_surface(surface, dest, venture):
    """Copy a process surface over a materialised fixture.

    The one substitution is the venture identity, which is the same
    string in both arms, so it cannot move the comparison.
    """
    written = []
    for src in sorted(surface.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(surface)
        target = Path(dest) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8")
        target.write_text(text.replace("{{VENTURE_NAME}}", venture),
                          encoding="utf-8")
        written.append(rel.as_posix())
    return written


BRIEF = """---
summary: {venture} venture brief, the standing description of what this
  repository is for
type: template
tags: [eos]
---

# {venture} · Venture brief

{readme}

## Standing constraints

- The work lives in this repository and nowhere else.
- Keep changes to what the task asks for.
- The tests in this repository are the acceptance surface.
"""

LOCKBOOK = """---
summary: {venture} lock-book, rulings that win on specifics
type: template
tags: [eos]
---

# {venture} · Lock-book

Rulings recorded for this venture. A ruling here wins over general
guidance on the specific it names.

## Rulings

1. (none yet)
"""


def write_venture_content(dest, venture, fixture_readme):
    """Write the brief and lock-book both arms get, identically.

    The process surface has to point somewhere: the v1 and v2 routers
    both open by telling a session to read the lock-book and the brief.
    Neither seed's own brief fits an application fixture, so this is
    generated from the fixture's README and is byte-identical across
    variants, which keeps venture material out of the comparison.
    """
    docs = Path(dest) / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    readme = ""
    if fixture_readme and Path(fixture_readme).is_file():
        raw = Path(fixture_readme).read_text(encoding="utf-8",
                                             errors="replace")
        body = raw.split("---", 2)[-1] if raw.startswith("---") else raw
        readme = "\n".join(body.strip().splitlines()[:20])
    (docs / "VENTURE_BRIEF.md").write_text(
        BRIEF.format(venture=venture, readme=readme or "(no README)"),
        encoding="utf-8")
    (docs / "LOCKBOOK.md").write_text(
        LOCKBOOK.format(venture=venture), encoding="utf-8")
    return ["docs/VENTURE_BRIEF.md", "docs/LOCKBOOK.md"]


def run_git(dest, *args):
    cmd = ["git", "-c", "user.name=eos-benchmark",
           "-c", "user.email=benchmark@pattertech.invalid",
           "-C", str(dest)] + list(args)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        fail("git %s failed in %s: %s"
             % (" ".join(args), dest, proc.stderr.strip()))
    return proc


def cmd_prepare(args):
    task_path, task = load_task(args.task)
    fixture = task.get("fixture")
    if not fixture:
        fail("task %s declares no fixture" % task_path)
    # T10 names its fixture in prose rather than as a directory.
    if not (FIXTURES / fixture).is_dir():
        fail("task %s names fixture %r, which is not a directory under "
             "benchmark/fixtures/. It cannot be materialised automatically."
             % (task_path.name, fixture))

    chosen, how, surface = resolve_surface(fixture, args.variant)
    src = FIXTURES / chosen
    if not src.is_dir():
        fail("fixture not found: %s" % src)

    dest = Path(args.dest)
    if dest.exists() and any(dest.iterdir()):
        fail("destination is not empty: %s" % dest)
    dest.mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(BENCH_DIR))
    import runner
    shutil.copytree(src, dest, ignore=runner.ignore_holdout,
                    dirs_exist_ok=True)

    overlaid = []
    if how == "overlaid":
        venture = chosen.replace("-", " ").title()
        overlaid = copy_surface(surface, dest, venture)
        overlaid += write_venture_content(dest, venture, dest / "README.md")

    run_git(dest, "init")
    run_git(dest, "add", "-A")
    run_git(dest, "commit", "--allow-empty", "-m", "fixture: initial state")

    patch = task_path / "break.patch"
    if patch.is_file():
        run_git(dest, "apply", str(patch.resolve()))

    prompt = task.get("prompt")
    if not prompt:
        fail("task.json in %s has no prompt field" % task_path)

    meta = {
        "run_id": args.run_id,
        "task": task.get("id", task_path.name),
        "variant": args.variant,
        "fixture_declared": fixture,
        "fixture_materialised": chosen,
        "surface": how,
        "surface_files": overlaid,
        "trial": args.trial,
    }
    (dest / "run.json").write_text(json.dumps(meta, indent=1) + "\n",
                                   encoding="utf-8")
    print(json.dumps({"scratch": str(dest), "prompt": prompt, **meta},
                     indent=1))


def cmd_plan(args):
    tasks = sorted(t.strip() for t in args.tasks.split(",") if t.strip())
    variants = [v.strip() for v in args.variants.split(",") if v.strip()]
    rng = random.Random(args.seed)
    plan = []
    for trial in range(1, args.trials + 1):
        for task in tasks:
            arms = list(variants)
            rng.shuffle(arms)
            for variant in arms:
                plan.append({
                    "task": task, "variant": variant, "trial": trial,
                    "run_id": "R-%s-%s-t%d" % (variant, task, trial),
                })
    rng.shuffle(plan)
    print(json.dumps({"seed": args.seed, "trials": args.trials,
                      "runs": plan}, indent=1))


def cmd_map(args):
    """Match transcripts to runs by the run id carried in the prompt.

    A workflow writes one agent-<id>.jsonl per session and names it
    after an internal id, so the only reliable join is the run id in
    the session's own first message.
    """
    tdir = Path(args.transcripts)
    if not tdir.is_dir():
        fail("transcript directory not found: %s" % tdir)
    dest = Path(args.dest)
    wanted = {}
    for run_json in sorted(dest.glob("*/run.json")):
        meta = json.loads(run_json.read_text(encoding="utf-8"))
        wanted[meta["run_id"]] = run_json.parent

    found = {}
    for path in sorted(tdir.glob("agent-*.jsonl")):
        if path.name.endswith(".meta.json"):
            continue
        head = path.read_text(encoding="utf-8", errors="replace")[:20000]
        for run_id in wanted:
            if run_id in head:
                found[run_id] = str(path)
                break

    rows = []
    for run_id, scratch in sorted(wanted.items()):
        rows.append({"run_id": run_id, "scratch": str(scratch),
                     "transcript": found.get(run_id)})
    missing = [r["run_id"] for r in rows if not r["transcript"]]
    print(json.dumps({"runs": rows, "unmatched": missing}, indent=1))
    return 1 if missing else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("prepare")
    p.add_argument("--task", required=True)
    p.add_argument("--variant", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--dest", required=True)
    p.add_argument("--trial", type=int, default=1)
    p.set_defaults(func=cmd_prepare)

    p = sub.add_parser("plan")
    p.add_argument("--tasks", required=True)
    p.add_argument("--variants", required=True)
    p.add_argument("--trials", type=int, default=3)
    p.add_argument("--seed", type=int, default=20260808)
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("map")
    p.add_argument("--transcripts", required=True)
    p.add_argument("--dest", required=True)
    p.set_defaults(func=cmd_map)

    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
