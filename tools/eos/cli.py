"""Command-line dispatch for python -m tools.eos.

Contract: tools/CLI_CONTRACTS.md. Exit codes: 0 clean or warnings only,
1 findings (errors, refusals, blocking verdicts, failed criteria),
2 cannot run, 3 protected-touch-unacknowledged.
"""

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent


def _ctx(args):
    from .repo import RepoModel

    today = _dt.date.today()
    model = RepoModel.load(REPO, today=today)
    return {
        "model": model,
        "root": REPO,
        "today": today,
        "offline": getattr(args, "offline", False),
        "strict_semantic": getattr(args, "strict_semantic", False),
        "relax_semantic": getattr(args, "relax_semantic", False),
    }


def _emit(findings, as_json):
    errors = [f for f in findings if f.severity == "error"]
    if as_json:
        print(json.dumps(
            [{"check": f.check_id, "path": f.path, "message": f.message,
              "severity": f.severity} for f in findings], indent=1))
    else:
        for f in findings:
            stream = sys.stderr
            tag = "ERROR" if f.severity == "error" else "warn "
            print(f"{tag} {f.check_id} {f.path}: {f.message}", file=stream)
        print(f"{len(errors)} errors, {len(findings) - len(errors)} warnings",
              file=sys.stderr)
    return 1 if errors else 0


def cmd_check(args):
    from .checks import run_all
    from .checks import seed as seed_checks
    from .checks import structural

    if args.repo and args.seed:
        print("error: --repo and --seed are different runs; pass one",
              file=sys.stderr)
        return 2
    ctx = _ctx(args)
    if args.write_index:
        findings = structural.write_indexes(ctx)
        return _emit(findings, args.json)
    if args.seed:
        findings = seed_checks.run_seed(Path(args.seed), ctx)
        found = list(findings)
        # A seed path that does not exist, or a missing scale matrix, is
        # a run that could not happen, not a seed that failed. The test
        # here used to look for the words "cannot run" in the message
        # and neither message says them, so this branch never once ran
        # and both cases exited 1. seed.cannot_run names them at source.
        if seed_checks.cannot_run(found):
            _emit(found, args.json)
            return 2
        return _emit(found, args.json)
    findings = run_all(ctx, series=args.series)
    return _emit(findings, args.json)


def cmd_route(args):
    from . import taskops
    from .router import TIERS, derive_signals, route

    rank = {t: i for i, t in enumerate(TIERS)}
    declared = {}
    stored_tier = None
    if args.facts:
        declared = json.loads(Path(args.facts).read_text(encoding="utf-8"))
    elif args.task:
        rec = REPO / "org" / "tasks" / f"{args.task}.json"
        if not rec.exists():
            print(f"error: no task record {rec}", file=sys.stderr)
            return 2
        record = json.loads(rec.read_text(encoding="utf-8"))
        # The record's declared block is the fact set; the ruling stored
        # on it at creation is the floor this recomputation may raise
        # and never lower.
        declared = record.get("declared") or {}
        stored_tier = record.get("tier_ruled")
    policy = taskops.load_policy(REPO)
    derived = {}
    if args.diff:
        derived = derive_signals(REPO, args.diff, declared, policy=policy)
    result = route(declared, derived, policy=policy)
    if stored_tier in rank and rank[stored_tier] > rank.get(result["tier"], 0):
        print(f"gate recomputation resolves upward only: holding "
              f"{args.task} at the ruling stored on the record, "
              f"{stored_tier}", file=sys.stderr)
        result["tier"] = stored_tier
    print(json.dumps(result, indent=1))
    # The router's factor id is protected-set-contact (router.py
    # FACTOR_TABLE). This filtered for "protected-set", which never
    # matched, so the only return 3 in the codebase was unreachable and
    # the enforcement AGENTS.md, POLICY_SPEC.md and CLI_CONTRACTS.md all
    # describe never ran once.
    protected = [r for r in result.get("reasons", [])
                 if r.get("factor") == "protected-set-contact"]
    if protected and not args.adr:
        for reason in protected:
            print(f"protected-set touch without --adr authorisation: "
                  f"{reason.get('evidence', 'no evidence recorded')}",
                  file=sys.stderr)
        return 3
    if args.diff and result.get("discrepancies"):
        return 1
    return 0


def cmd_guard(args):
    from .guard import evaluate

    # guard.evaluate takes action_class and payload_summary; the flag form
    # must build that shape, not a shorthand the evaluator cannot read.
    action = {"action_class": args.action_class,
              "payload_summary": args.payload or ""}
    if args.input:
        action = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if args.tool:
            action.setdefault("tool", args.tool)
    policy = None
    policy_path = REPO / "org" / "policy.json"
    if policy_path.exists():
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    try:
        verdict = evaluate(action, policy, adapter_validated=args.adapter_validated)
    except ValueError as exc:
        # CLI_CONTRACTS promises exit 2 when evaluation cannot run. This
        # raised an uncaught ValueError and exited 1, which a caller
        # reads as "blocked" rather than "I could not judge this".
        print(f"error: guard cannot evaluate this action: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(verdict, indent=1))
    return 0 if verdict.get("verdict") == "allow" else 1


def cmd_context(args):
    from .contextgen import build_packet

    # --task was parsed and discarded. The record is where a task's
    # declared predicates live, and predicates are the real activation
    # gate, so ignoring it threw away the only input that can settle one.
    predicates = []
    if args.task:
        rec = REPO / "org" / "tasks" / f"{args.task}.json"
        if not rec.exists():
            print(f"error: no task record {rec}", file=sys.stderr)
            return 2
        record = json.loads(rec.read_text(encoding="utf-8"))
        predicates = list(record.get("applies_when") or [])
    packet = build_packet(REPO, base_ref=args.diff,
                          declared_predicates=predicates)
    out = json.dumps(packet, indent=1).splitlines()
    if len(out) > 300:
        # Truncation is lossy, so say so rather than cutting silently.
        out = out[:300] + [f"... truncated at 300 lines of "
                           f"{len(json.dumps(packet, indent=1).splitlines())}"]
    print("\n".join(out))
    return 0


LENS_TEMPLATE = "kernel/templates/LENS.tpl.md"


def cmd_study(args):
    """Scaffold a lens contract from the kernel template.

    The Study workflow (PB-E11) writes the lens contract before it reads
    the source: what is being studied, at what version, how it was
    lawfully acquired, what is in the lens and what is deliberately out.
    This command only puts the skeleton where the study session can fill
    it. It reads nothing else, fetches nothing and fills no slot: what
    goes in the contract is Daniel's to approve, not a tool's to guess.
    """
    import re

    template = REPO / LENS_TEMPLATE
    if not template.is_file():
        print(f"error: no lens template at {LENS_TEMPLATE}", file=sys.stderr)
        return 2
    out_dir = Path(args.out)
    name = (args.name or "").strip()
    target = out_dir / (f"LENS-{name}.md" if name else "LENS.md")
    if target.exists():
        print(f"refused: {target} already exists; a lens contract is the "
              f"record that makes a study defensible and is never "
              f"overwritten", file=sys.stderr)
        return 1
    text = template.read_text(encoding="utf-8")
    # The scaffold is a working file, not a template: leaving
    # template: true on it would exempt it from the slot check that
    # exists to catch a contract shipped unfilled.
    text = re.sub(r"^template:\s*true\s*$\n?", "", text, flags=re.M)
    out_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    slots = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", text)))
    print(json.dumps({"created": str(target), "template": LENS_TEMPLATE,
                      "slots": slots}, indent=1))
    return 0


def cmd_task(args):
    from . import taskops

    try:
        return _cmd_task(args, taskops)
    except taskops.ClaimRefused as refusal:
        # The documented shape, on stdout so a caller can parse it, with
        # exit 1. Nothing emitted this before: the control was described
        # in three files and implemented in none.
        print(json.dumps(refusal.payload, indent=1))
        return 1


def _cmd_task(args, taskops):
    session = getattr(args, "session", None)
    if args.op == "new":
        # Routing is paid once, here: create_task rules the tier from
        # the declared facts and stores it on the record, so the caller
        # sees the ruling without a second command and later sessions
        # read it off the record.
        record = json.loads(Path(args.record).read_text(encoding="utf-8"))
        path = taskops.create_task(REPO, record, session=session)
        tier = record.get("tier_ruled")
        reasons = record.get("reasons") or []
        print(json.dumps({"created": str(path), "tier_ruled": tier,
                          "reasons": reasons}, indent=1))
        if reasons:
            print(f"ruled {tier}, from these factors:", file=sys.stderr)
            for r in reasons:
                print("  {factor} floor {tier_floor} ({source}): {evidence}"
                      .format(**r), file=sys.stderr)
        else:
            print(f"ruled {tier}, no factor active, a clean {tier}",
                  file=sys.stderr)
        print("routed once, at record creation: read the ruling off the "
              "record rather than routing again. The merge gate recomputes "
              "against the actual diff and only ever raises it.",
              file=sys.stderr)
        return 0
    if args.op == "show":
        rec = REPO / "org" / "tasks" / f"{args.id}.json"
        if not rec.exists():
            return 2
        print(rec.read_text(encoding="utf-8"))
        return 0
    if args.op == "update":
        patch = json.loads(args.patch)
        taskops.update_task(REPO, args.id, patch, session=session)
        return 0
    if args.op == "claims-verify":
        claims_doc = json.loads(
            (REPO / "org" / "claims.json").read_text(encoding="utf-8"))
        diff_paths = args.paths or []
        findings = taskops.verify_claims(REPO, claims_doc, args.lane,
                                         diff_paths)
        bad = [f for f in findings if getattr(f, "severity", "error") == "error"]
        for f in findings:
            print(f"{f.check_id} {f.path}: {f.message}", file=sys.stderr)
        return 1 if bad else 0
    if args.op == "views":
        findings = taskops.render_views(REPO)
        bad = [f for f in findings if getattr(f, "severity", "error") == "error"]
        for f in findings:
            print(f"{f.check_id} {f.path}: {f.message}", file=sys.stderr)
        print(json.dumps({"regenerated": ["org/TASKS.md", "org/STATE.md"]}))
        return 1 if bad else 0
    print(f"error: unknown task op {args.op}", file=sys.stderr)
    return 2


def cmd_migrate(args):
    from . import migrate

    if args.op == "plan":
        state = migrate.plan(Path(args.seed))
        print(json.dumps(state, indent=1))
        return 0
    if args.op == "apply":
        state = json.loads(Path(args.state).read_text(encoding="utf-8"))
        seed_root = Path(state.get("seed_root", args.seed or ""))
        if not str(seed_root).replace("\\", "/").startswith(
                str(REPO).replace("\\", "/")):
            print("error: apply runs on fixture seeds inside this repo only "
                  "this build", file=sys.stderr)
            return 2
        result = migrate.apply(seed_root, state, dry_run=args.dry_run)
        print(json.dumps(result, indent=1))
        blocked = [s for s in result.get("state", result).get("steps", [])
                   if s.get("status") == "blocked"]
        return 1 if blocked else 0
    return 2


def cmd_benchmark(args):
    from . import benchcli

    if args.op == "prepare":
        # This used to pass --variant into runner.py's --fixture slot, so
        # every invocation died with "fixture not found: .../fixtures/v2".
        # No fixture is named v1 or v2, so the documented command had
        # never once run. It now drives harness.py, which is the thing
        # that actually knows what a variant is.
        missing = [n for n in ("task", "variant", "dest", "run_id")
                   if not getattr(args, n, None)]
        if missing:
            print("benchmark prepare needs --%s"
                  % ", --".join(m.replace("_", "-") for m in missing),
                  file=sys.stderr)
            return 2
        proc = benchcli.harness(REPO, [
            "prepare", "--task", args.task, "--variant", args.variant,
            "--run-id", args.run_id, "--dest", args.dest])
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        return proc.returncode
    if args.op == "score":
        proc = benchcli.score(REPO, [
            "--task", args.task, "--scratch", args.scratch,
            "--transcript", args.transcript, "--variant", args.variant,
            "--run-id", args.run_id])
        # This returned the CompletedProcess itself where an int exit
        # code was expected, so the shell saw a truthy object and the
        # scorer's output never reached the caller.
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        return proc.returncode
    return 2


def cmd_drills(args):
    from . import benchcli

    action = "run" if (args.pack or args.all) else "list"
    payload, code = benchcli.drills(
        REPO, action, pack=args.pack, scratch=args.scratch,
        record=args.record, attempt=args.attempt)
    print(json.dumps(payload, indent=1))
    for f in benchcli.drill_findings(payload):
        tag = "ERROR" if f.severity == "error" else "warn "
        print(f"{tag} {f.check_id} {f.path}: {f.message}", file=sys.stderr)
    return code


def build_parser():
    """The whole argparse tree, in one place.

    Split out of main so a test can read the command set and hold it
    against tools/CLI_CONTRACTS.md, which is the law this file
    implements. A command the contract does not mention is a command
    nobody agreed to.
    """
    ap = argparse.ArgumentParser(prog="python -m tools.eos")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check")
    c.add_argument("--repo", action="store_true")
    c.add_argument("--seed")
    c.add_argument("--write-index", action="store_true")
    c.add_argument("--json", action="store_true")
    c.add_argument("--series")
    c.add_argument("--strict-semantic", action="store_true",
                   help="force the S-series to error severity. It is already "
                        "the default; this pins it against a future relaxation.")
    c.add_argument("--relax-semantic", action="store_true",
                   help="drop the S-series to warnings, for a caller who wants "
                        "the work list rather than the gate. The module "
                        "docstring promised this flag and it did not exist.")
    c.add_argument("--offline", action="store_true")
    c.set_defaults(fn=cmd_check)

    r = sub.add_parser(
        "route",
        description="Rule a tier from declared facts, optionally against a "
                    "diff. Ordinary task routing is already paid once at "
                    "record creation, where task new stores tier_ruled and "
                    "the reasons on the record; this command is for "
                    "gate-time recomputation with --diff and for routing a "
                    "facts file before any record exists.")
    r.add_argument("--task")
    r.add_argument("--facts")
    r.add_argument("--diff")
    r.add_argument("--adr")
    r.set_defaults(fn=cmd_route)

    g = sub.add_parser("guard")
    gsub = g.add_subparsers(dest="gop", required=True)
    ge = gsub.add_parser("eval")
    ge.add_argument("--class", dest="action_class")
    ge.add_argument("--payload")
    ge.add_argument("--tool")
    ge.add_argument("--input")
    ge.add_argument("--adapter-validated", action="store_true")
    ge.set_defaults(fn=cmd_guard)

    x = sub.add_parser("context")
    x.add_argument("--task")
    x.add_argument("--diff")
    x.set_defaults(fn=cmd_context)

    st = sub.add_parser(
        "study",
        description="Scaffold a lens contract for the Study workflow "
                    "(PB-E11) into a directory. It copies the kernel "
                    "template and fills nothing: the lens is Daniel's to "
                    "approve before the source is read.")
    st.add_argument("--out", required=True,
                    help="directory to write the contract into; created if "
                         "it does not exist")
    st.add_argument("--name",
                    help="the four-digit id, giving LENS-NNNN.md instead of LENS.md, "
                         "so two studies can share a directory")
    st.set_defaults(fn=cmd_study)

    t = sub.add_parser(
        "task",
        description="Task record and claim ops per tools/CLI_CONTRACTS.md. "
                    "The new op routes the record as it creates it and "
                    "prints the ruled tier and reasons, so no session needs "
                    "a second routing command. The views op regenerates the "
                    "derived views org/TASKS.md and org/STATE.md from the "
                    "canonical records; derived views belong to the "
                    "integrator and are never lane-claimed or hand-edited.")
    t.add_argument(
        "op", choices=["new", "show", "update", "claims-verify", "views"],
        help="new routes the record and stores the ruling on it; views "
             "regenerates the derived views (integrator-only op)")
    t.add_argument("--id")
    t.add_argument("--record")
    t.add_argument("--patch")
    t.add_argument("--lane")
    t.add_argument("--paths", nargs="*")
    t.add_argument("--session",
                   help="the writing session's id; falls back to EOS_SESSION_ID "
                        "then to the record's owner_session. It must be named "
                        "in org/claims.json or the write is refused.")
    t.set_defaults(fn=cmd_task)

    m = sub.add_parser("migrate")
    m.add_argument("op", choices=["plan", "apply"])
    m.add_argument("--seed")
    m.add_argument("--state")
    # store_true with default=True made --dry-run permanently on, with
    # no way to turn it off, so migrate apply could never apply and 273
    # lines of migrate.py had no reachable write path.
    m.add_argument("--dry-run", dest="dry_run", action="store_true", default=True)
    m.add_argument("--no-dry-run", dest="dry_run", action="store_false",
                   help="actually write. Without this, apply reports what it "
                        "would do and changes nothing.")
    m.set_defaults(fn=cmd_migrate)

    b = sub.add_parser("benchmark")
    b.add_argument("op", choices=["prepare", "score"])
    b.add_argument("--task")
    b.add_argument("--dest")
    b.add_argument("--scratch")
    b.add_argument("--transcript")
    b.add_argument("--variant")
    b.add_argument("--run-id")
    b.set_defaults(fn=cmd_benchmark)

    d = sub.add_parser(
        "drills",
        description="Pack acceptance drills. With neither --pack nor --all "
                    "it lists the frozen drills, their hashes and whether "
                    "each was frozen before its pack was authored.")
    d.add_argument("--pack")
    d.add_argument("--all", action="store_true")
    d.add_argument("--scratch",
                   help="scratch root to materialise scenarios into; a "
                        "temporary directory is used and removed otherwise")
    d.add_argument("--attempt",
                   help="grade the tree a cold agent delivered, instead of a "
                        "freshly materialised scenario; needs --pack")
    d.add_argument("--record", action="store_true",
                   help="append the run to benchmark/drills/RESULTS.json")
    d.set_defaults(fn=cmd_drills)
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except ModuleNotFoundError as exc:
        if "jsonschema" in str(exc):
            print("error: jsonschema missing; install with: python -m pip "
                  "install --require-hashes -r tools/requirements.txt",
                  file=sys.stderr)
            return 2
        raise
