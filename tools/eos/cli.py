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


class CannotRun(Exception):
    """An input the caller named is absent or will not parse.

    main() prints the message and returns 2. Exit 2 is a promise to a
    caller: 1 means the command ran and found something, 2 means it
    never ran. Raising this rather than letting json or a helper throw
    is how the message gets to say which input it was reading.
    """


def _read_json(path, what):
    """Parse a JSON input, naming which one when it will not parse.

    json's own message, "Expecting value: line 1 column 1 (char 0)",
    does not say which of a command's inputs it was reading. A file
    that is not there raises FileNotFoundError, whose message already
    names the path, and main() maps that to the same exit code.

    Every input read this way is a JSON object, so a document that
    parses to something else is malformed for this purpose; without the
    check it reaches the reader as a list and fails there instead.
    """
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CannotRun(f"{what} {path} is not JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise CannotRun(f"{what} {path} is not a JSON object")
    return data


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
        # Finding.to_dict is the documented machine shape. Building it
        # here as well is how the two spellings come to differ.
        print(json.dumps([f.to_dict() for f in findings], indent=1))
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
        # a run that could not happen rather than a seed that failed.
        # seed.cannot_run names those two findings beside the code that
        # emits them, so the exit code follows the finding rather than a
        # phrase in its message.
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
        declared = _read_json(args.facts, "the declared facts file")
    elif args.task:
        rec = REPO / "org" / "tasks" / f"{args.task}.json"
        if not rec.exists():
            print(f"error: no task record {rec}", file=sys.stderr)
            return 2
        record = _read_json(rec, "task record")
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
    # The factor id is protected-set-contact, spelled exactly as
    # router.FACTOR_TABLE spells it. Exit 3 is the only enforcement of
    # the protected set the tooling has, and a near-miss here would
    # switch it off silently.
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

    # guard.evaluate reads action_class and payload_summary, so the flag
    # form builds that shape rather than a shorthand of its own.
    action = {"action_class": args.action_class,
              "payload_summary": args.payload or ""}
    if args.input:
        action = _read_json(args.input, "the action file")
        if args.tool:
            action.setdefault("tool", args.tool)
    policy = None
    policy_path = REPO / "org" / "policy.json"
    if policy_path.exists():
        policy = _read_json(policy_path, "the policy")
    try:
        verdict = evaluate(action, policy, adapter_validated=args.adapter_validated)
    except ValueError as exc:
        # Exit 2, not 1: a caller reads 1 as "blocked" and 2 as "I could
        # not judge this", and the difference decides whether a human is
        # asked to look.
        print(f"error: guard cannot evaluate this action: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(verdict, indent=1))
    return 0 if verdict.get("verdict") == "allow" else 1


def cmd_activate(args):
    from .contextgen import activation_from_facts, facts_from_brief

    predicates = list(args.predicate or [])
    if args.brief:
        path = Path(args.brief)
        if not path.is_file():
            print(f"error: no brief at {path}", file=sys.stderr)
            return 2
        found = facts_from_brief(path.read_text(encoding="utf-8"))
        if not found:
            print(f"error: {path} declares no venture facts. The block is "
                  f"```facts in kernel/templates/VENTURE_BRIEF.tpl.md, and "
                  f"an empty one is a brief that was compiled before the "
                  f"block existed or never filled it", file=sys.stderr)
            return 2
        predicates += found
    if args.facts:
        doc = _read_json(Path(args.facts), "the facts file")
        if isinstance(doc, dict):
            doc = doc.get("predicates") or doc.get("applies_when") or []
        if not isinstance(doc, list):
            print("error: the facts file must hold a list of predicates, or "
                  "an object with a predicates key", file=sys.stderr)
            return 2
        predicates += [str(p) for p in doc]
    if not predicates:
        print("error: no predicates given; use --facts or --predicate",
              file=sys.stderr)
        return 2

    result = activation_from_facts(REPO, predicates)
    print(json.dumps(result, indent=1))

    for row in result["activated"]:
        print("activate {pack}: {why}".format(
            pack=row["pack"], why=", ".join(row["matched_predicates"])),
            file=sys.stderr)
    print("%d pack(s) activate, %d do not"
          % (len(result["activated"]), len(result["not_activated"])),
          file=sys.stderr)
    if result["unknown_predicates"]:
        # A misspelled fact matches nothing and reads exactly like a fact
        # that is simply false, so the pack it should have loaded stays
        # out and the seed ships without the ruling. That is the
        # expensive direction, so it exits non-zero rather than warning.
        for p in result["unknown_predicates"]:
            print("error: no pack declares %s, so it activates nothing" % p,
                  file=sys.stderr)
        return 1
    return 0


def cmd_context(args):
    from .contextgen import build_packet

    # The record carries the declared predicates, and predicates are the
    # real pack activation gate, so a packet built without them leaves
    # every predicate unresolved.
    predicates = []
    if args.task:
        rec = REPO / "org" / "tasks" / f"{args.task}.json"
        if not rec.exists():
            print(f"error: no task record {rec}", file=sys.stderr)
            return 2
        record = _read_json(rec, "task record")
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
    goes in the contract is the operator's to approve, not a tool's to guess.
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
        # The refusal shape CLI_CONTRACTS.md documents, on stdout so a
        # caller can parse it, with exit 1.
        print(json.dumps(refusal.payload, indent=1))
        return 1


def _cmd_task(args, taskops):
    session = getattr(args, "session", None)
    if args.op == "new":
        # Routing is paid once, here: create_task rules the tier from
        # the declared facts and stores it on the record, so the caller
        # sees the ruling without a second command and later sessions
        # read it off the record.
        record = _read_json(args.record, "the record file")
        path = taskops.create_task(REPO, record, session=session)
        tier = record.get("tier_ruled")
        reasons = record.get("reasons") or []
        print(json.dumps({"created": str(path), "tier_ruled": tier,
                          "reasons": reasons}, indent=1))
        declared = (record.get("declared") or {}).get("side_effects") or []
        if reasons:
            print(f"ruled {tier}, from these factors:", file=sys.stderr)
            for r in reasons:
                print("  {factor} floor {tier_floor} ({source}): {evidence}"
                      .format(**r), file=sys.stderr)
        elif declared:
            print(f"ruled {tier}: {len(declared)} side effect(s) declared and "
                  f"no factor active", file=sys.stderr)
        else:
            # The distinction this draws is the one the ruling turns on.
            # Routing here reads declarations and no diff, so a record
            # declaring nothing rules from an empty fact set. Calling
            # that "a clean R0", as this did, reads as though the
            # thirteen factors looked at the work and found nothing. On
            # 21 of the first 25 records they had nothing to look at.
            print(f"ruled {tier} from an empty fact set: no side effect was "
                  f"declared and no diff is read here, so no factor could "
                  f"fire. This is the absence of evidence, not evidence of "
                  f"low risk.", file=sys.stderr)
        proposed = record.get("tier_proposed")
        if proposed and tier and proposed > tier:
            print(f"note: you proposed {proposed} and the declared facts rule "
                  f"{tier}. The ruling stands, and the gap is worth a look: "
                  f"if {proposed} was right, the facts behind it are not on "
                  f"this record.", file=sys.stderr)
        print("routed once, at record creation: read the ruling off the "
              "record rather than routing again. The merge gate recomputes "
              "against the actual diff and only ever raises it. Nothing runs "
              "that gate for you: it is `python -m tools.eos route --task "
              "{id} --diff RANGE` in the merge playbook.".format(
                  id=record.get("id", "T-####")),
              file=sys.stderr)
        return 0
    if args.op == "show":
        rec = REPO / "org" / "tasks" / f"{args.id}.json"
        if not rec.exists():
            print(f"error: no task record {rec}", file=sys.stderr)
            return 2
        print(rec.read_text(encoding="utf-8"))
        return 0
    if args.op == "update":
        try:
            patch = json.loads(args.patch)
        except json.JSONDecodeError as exc:
            # The patch arrives on the command line rather than in a
            # file, so there is no path to name; say which argument.
            raise CannotRun(f"--patch is not JSON: {exc}") from exc
        taskops.update_task(REPO, args.id, patch, session=session)
        return 0
    if args.op == "claims-verify":
        claims_doc = _read_json(REPO / "org" / "claims.json", "the claim set")
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
        state = _read_json(args.state, "the migration state")
        # The state document cannot name its own seed: the schema at
        # kernel/schemas/migration-state.schema.json fixes the key set
        # and has no seed_root in it. So apply is told which seed to
        # work on, and refuses to guess.
        if not args.seed:
            print("error: migrate apply needs --seed as well as --state; "
                  "the migration state does not record which seed it "
                  "planned", file=sys.stderr)
            return 2
        seed_root = Path(args.seed).resolve()
        # Path containment, not a string prefix. A prefix test lets any
        # sibling whose name merely extends this one through:
        # PatterTech_EOS_backup next to PatterTech_EOS passed it. With
        # --no-dry-run apply rewrites the lock-book header and every
        # file under org/roles/, so the thing the guard exists to stop
        # is a destructive write into a neighbouring repository, and a
        # plausible backup name defeated it.
        if not seed_root.is_relative_to(Path(REPO).resolve()):
            print("error: apply runs on fixture seeds inside this repo, and "
                  "only in this build", file=sys.stderr)
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
        # harness.py is the frozen script that knows what a variant is;
        # runner.py takes a fixture, which is a different argument.
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
    # Constrained, because the filter is a plain prefix match: any
    # other value selected no checks at all and reported a clean tree,
    # so a typo read as a pass. A test holds this list against the
    # registered check ids. The seed D-series is not in that registry
    # and runs only under --seed.
    c.add_argument("--series", choices=["B", "E", "F", "S"],
                   help="run one series by its check-id prefix")
    c.add_argument("--strict-semantic", action="store_true",
                   help="force the S-series to error severity. Error is "
                        "already the default, so this only overrides "
                        "--relax-semantic on a command line carrying both.")
    c.add_argument("--relax-semantic", action="store_true",
                   help="drop the S-series to warnings, for a caller who wants "
                        "the work list rather than the gate.")
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

    a = sub.add_parser(
        "activate",
        description="Which packs a venture's declared facts activate, and "
                    "which they do not. Session 0 has no diff, so this is "
                    "the half of pack activation `context` cannot compute.")
    a.add_argument("--brief", help="a venture brief, whose ```facts block "
                                   "carries the declared venture facts")
    a.add_argument("--facts", help="JSON file holding a list of predicates, "
                                   "or an object with a predicates key")
    a.add_argument("--predicate", action="append", default=[],
                   help="a declared predicate, repeatable")
    a.set_defaults(fn=cmd_activate)

    st = sub.add_parser(
        "study",
        description="Scaffold a lens contract for the Study workflow "
                    "(PB-E11) into a directory. It copies the kernel "
                    "template and fills nothing: the lens is the operator's to "
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
    # Dry run is the default, so --dry-run is accepted and changes
    # nothing; --no-dry-run is the switch that lets apply write.
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
    except (CannotRun, FileNotFoundError, RuntimeError, ValueError) as exc:
        # A run that could not happen, which is exit 2: a file the
        # caller named is not there, a --diff ref git cannot resolve
        # (RuntimeError out of gitfacts.output), a record the schema
        # rejects or a patch that is not JSON (ValueError, which
        # JSONDecodeError is). Uncaught, each of these printed a
        # traceback and exited 1, and 1 is the code for findings, so a
        # caller read a broken invocation as a failing check. A missing
        # jsonschema is not one of these; every import of it is guarded
        # at the point of use and degrades to an error-severity finding
        # instead.
        print(f"error: {exc}", file=sys.stderr)
        return 2
