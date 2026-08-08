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
        cannot = [f for f in found if f.check_id in ("D001", "D003")
                  and "cannot run" in f.message.lower()]
        if cannot:
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

    packet = build_packet(REPO, base_ref=args.diff)
    lines = packet if isinstance(packet, str) else json.dumps(packet, indent=1)
    text = lines if isinstance(lines, str) else str(lines)
    out = text.splitlines()[:300]
    print("\n".join(out))
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

    if args.op == "run":
        run_args = ["materialise", "--fixture", args.variant or "",
                    "--dest", args.dest or ""]
        if args.task:
            run_args += ["--task", args.task]
        return benchcli.runner(REPO, [a for a in run_args if a != ""])
    if args.op == "score":
        return benchcli.score(REPO, [
            "--task", args.task, "--scratch", args.scratch,
            "--transcript", args.transcript, "--variant", args.variant,
            "--run-id", args.run_id])
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


def main(argv=None):
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
    b.add_argument("op", choices=["run", "score"])
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

    args = ap.parse_args(argv)
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
