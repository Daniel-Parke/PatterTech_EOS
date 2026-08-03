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
    from .router import derive_signals, route

    declared = {}
    if args.facts:
        declared = json.loads(Path(args.facts).read_text(encoding="utf-8"))
    elif args.task:
        rec = REPO / "org" / "tasks" / f"{args.task}.json"
        if not rec.exists():
            print(f"error: no task record {rec}", file=sys.stderr)
            return 2
        declared = json.loads(rec.read_text(encoding="utf-8"))
    policy = None
    policy_path = REPO / "org" / "policy.json"
    if policy_path.exists():
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    derived = {}
    if args.diff:
        derived = derive_signals(REPO, args.diff, declared, policy=policy)
    result = route(declared, derived, policy=policy)
    print(json.dumps(result, indent=1))
    protected = [r for r in result.get("reasons", [])
                 if r.get("factor") == "protected-set"]
    if protected and not args.adr:
        print("protected-set touch without --adr authorisation",
              file=sys.stderr)
        return 3
    if args.diff and result.get("discrepancies"):
        return 1
    return 0


def cmd_guard(args):
    from .guard import evaluate

    action = {"class": args.action_class, "payload": args.payload or ""}
    if args.input:
        action = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if args.tool:
            action.setdefault("tool", args.tool)
    policy = None
    policy_path = REPO / "org" / "policy.json"
    if policy_path.exists():
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    verdict = evaluate(action, policy, adapter_validated=args.adapter_validated)
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

    if args.op == "new":
        record = json.loads(Path(args.record).read_text(encoding="utf-8"))
        path = taskops.create_task(REPO, record)
        print(json.dumps({"created": str(path)}))
        return 0
    if args.op == "show":
        rec = REPO / "org" / "tasks" / f"{args.id}.json"
        if not rec.exists():
            return 2
        print(rec.read_text(encoding="utf-8"))
        return 0
    if args.op == "update":
        patch = json.loads(args.patch)
        taskops.update_task(REPO, args.id, patch)
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

    return benchcli.drills("list" if not args.pack and not args.all else "run",
                           pack=args.pack)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m tools.eos")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check")
    c.add_argument("--repo", action="store_true")
    c.add_argument("--seed")
    c.add_argument("--write-index", action="store_true")
    c.add_argument("--json", action="store_true")
    c.add_argument("--series")
    c.add_argument("--strict-semantic", action="store_true")
    c.add_argument("--offline", action="store_true")
    c.set_defaults(fn=cmd_check)

    r = sub.add_parser("route")
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

    t = sub.add_parser("task")
    t.add_argument("op", choices=["new", "show", "update", "claims-verify"])
    t.add_argument("--id")
    t.add_argument("--record")
    t.add_argument("--patch")
    t.add_argument("--lane")
    t.add_argument("--paths", nargs="*")
    t.set_defaults(fn=cmd_task)

    m = sub.add_parser("migrate")
    m.add_argument("op", choices=["plan", "apply"])
    m.add_argument("--seed")
    m.add_argument("--state")
    m.add_argument("--dry-run", action="store_true", default=True)
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

    d = sub.add_parser("drills")
    d.add_argument("--pack")
    d.add_argument("--all", action="store_true")
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
