#!/usr/bin/env python3
"""Criterion 4: CI runs a migration linter, and the linter bites.

Finding a step whose name contains "lint" proves nothing, so this
grader takes the command CI actually invokes and drives it against
three seeded migrations in a copy of the tree:

    destructive              a DROP COLUMN            must exit non-zero
    backwards-incompatible   a NOT NULL with no default  must exit non-zero
    ordinary                 a nullable ADD COLUMN    must exit zero

The third is what stops `exit 1` from passing as a linter. The seeded
files are graded against the fixture's own migrations rather than the
delivered ones, so a linter cannot be satisfied by an allow-list aimed
at the agent's own contract migration.

Where the command names a tool this machine does not have, the
criterion is left unsettled rather than failed: nothing was looked at.
"""

import re
import shlex
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, copy_tree, emit,  # noqa: E402
                     migration_files, read, require_baseline, run,
                     scratch_dir)

CID = "c4"

CI_FILES = (".github/workflows", ".gitlab-ci.yml", ".circleci/config.yml",
            "azure-pipelines.yml", "Jenkinsfile", ".pre-commit-config.yaml",
            ".pre-commit-config.yml", "bitbucket-pipelines.yml")

LINTER_HINT = re.compile(
    r"(?i)(lint|squawk|atlas\s+migrate|migration[-_ ]?check|"
    r"check[-_ ]?migration|schema[-_ ]?diff|sqlfluff)")

RUN_KEY = re.compile(r"^(\s*)(?:-\s*)?(?:run|entry|command|script)\s*:\s*(.*)$")
LIST_ITEM = re.compile(r"^\s*-\s+(\S.*)$")

SHELL_METACHARS = set("$`&|;<>()")

BAD_DESTRUCTIVE = (
    "-- 0900\nALTER TABLE users DROP COLUMN email_address;\n")
BAD_INCOMPATIBLE = (
    "-- 0900\nALTER TABLE users ADD COLUMN nickname TEXT NOT NULL;\n")
GOOD = (
    "-- 0900\nALTER TABLE users ADD COLUMN nickname TEXT;\n")

INJECTED = "0900_seeded_by_the_check.sql"


def ci_files(scratch):
    found = []
    for name in CI_FILES:
        path = scratch / name
        if path.is_dir():
            found.extend(sorted(p for p in path.rglob("*")
                                if p.suffix.lower() in (".yml", ".yaml")))
        elif path.is_file():
            found.append(path)
    return found


def commands(text):
    """Every shell command the CI file appears to run."""
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        match = RUN_KEY.match(line)
        if not match:
            continue
        indent, value = len(match.group(1)), match.group(2).strip()
        if value in ("|", ">", "|-", ">-", ""):
            for follow in lines[i + 1:]:
                if not follow.strip():
                    continue
                level = len(follow) - len(follow.lstrip(" "))
                if level <= indent:
                    break
                item = LIST_ITEM.match(follow)
                out.append((item.group(1) if item else follow.strip()))
        else:
            out.append(value.strip("\"'"))
    return [c for c in out if c]


def argv_for(command, scratch):
    """(argv, problem). argv is None when the command cannot be driven."""
    if set(command) & SHELL_METACHARS:
        return None, ("the command %r needs a shell to run, so it was not "
                      "driven here" % command)
    try:
        parts = shlex.split(command, posix=True)
    except ValueError:
        return None, "the command %r does not split into arguments" % command
    if not parts:
        return None, "empty command"
    head = parts[0]
    if head in ("python", "python3", "py"):
        return [sys.executable] + parts[1:], None
    if head.endswith(".py"):
        return [sys.executable] + parts, None
    if head in ("sh", "bash"):
        if not shutil.which(head):
            return None, "%s is not available on this machine" % head
        return parts, None
    if head.endswith(".sh"):
        if not shutil.which("sh"):
            return None, "sh is not available on this machine"
        return ["sh"] + parts, None
    if (scratch / head).is_file():
        return None, ("%s is not an executable this grader knows how to "
                      "start" % head)
    if not shutil.which(head):
        return None, "%s is not installed on this machine" % head
    return parts, None


def local_target(command, scratch):
    """A script inside the repo that the command names, if any."""
    for token in re.findall(r"[\w./\\-]+\.(?:py|sh)", command):
        if (scratch / token).is_file():
            return token
    return None


def stage(copy, baseline, content):
    folder = copy / "migrations"
    if folder.is_dir():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    for path in migration_files(baseline):
        shutil.copy2(path, folder / path.name)
    readme = baseline / "migrations" / "README.md"
    if readme.is_file():
        shutil.copy2(readme, folder / "README.md")
    if content is not None:
        (folder / INJECTED).write_text(content, encoding="utf-8")


def main():
    scratch = scratch_dir()
    baseline = require_baseline(CID)

    files = ci_files(scratch)
    if not files:
        emit(CID, FAIL, "no CI configuration in the tree")

    candidates = []
    for path in files:
        for command in commands(read(path)):
            if LINTER_HINT.search(command):
                candidates.append((path.relative_to(scratch).as_posix(),
                                   command))
    if not candidates:
        emit(CID, FAIL,
             "no step in %s runs anything that looks like a migration "
             "linter" % ", ".join(p.relative_to(scratch).as_posix()
                                  for p in files))

    problems = []
    for where, command in candidates:
        target = local_target(command, scratch)
        argv, problem = argv_for(command, scratch)
        if argv is None:
            if target is None and re.search(r"[\w./\\-]+\.(?:py|sh)", command):
                problems.append("%s runs %r but that script is not in the "
                                "repository" % (where, command))
            else:
                problems.append(problem)
            continue

        work, copy = copy_tree(scratch, "drill-devops-c4-")
        try:
            results = {}
            for label, content in (("destructive", BAD_DESTRUCTIVE),
                                   ("backwards-incompatible",
                                    BAD_INCOMPATIBLE),
                                   ("ordinary", GOOD)):
                stage(copy, baseline, content)
                code, output = run(argv, copy)
                results[label] = (code, " ".join(output.split())[:200])
            if any(code is None for code, _ in results.values()):
                broken = [lab for lab, (code, _) in results.items()
                          if code is None]
                emit(CID, UNSETTLED,
                     "%s runs %r, which would not start here (%s), so the "
                     "linter was not exercised"
                     % (where, command, results[broken[0]][1]))
            bad_pass = [lab for lab in ("destructive",
                                        "backwards-incompatible")
                        if results[lab][0] == 0]
            if bad_pass:
                emit(CID, FAIL,
                     "%s runs %r, but it exits 0 on a seeded %s migration"
                     % (where, command, " and ".join(bad_pass)))
            if results["ordinary"][0] != 0:
                emit(CID, FAIL,
                     "%s runs %r, and it also rejects an ordinary nullable "
                     "ADD COLUMN (exit %s: %s), so a non-zero exit says "
                     "nothing about the finding"
                     % (where, command, results["ordinary"][0],
                        results["ordinary"][1]))
            emit(CID, PASS,
                 "%s runs %r: exit %s on a seeded DROP COLUMN, exit %s on a "
                 "seeded NOT NULL without default, exit 0 on an ordinary "
                 "additive migration"
                 % (where, command, results["destructive"][0],
                    results["backwards-incompatible"][0]))
        finally:
            shutil.rmtree(work, ignore_errors=True)

    emit(CID, UNSETTLED if all("not installed" in p or "not available" in p
                               or "needs a shell" in p for p in problems)
         else FAIL,
         "found %d linter-shaped CI step(s) but none could be exercised: %s"
         % (len(candidates), "; ".join(problems[:3])))


if __name__ == "__main__":
    main()
