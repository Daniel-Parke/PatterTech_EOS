#!/usr/bin/env python3
"""Criterion 10: the price lookup uses the public interface only.

The drill specifies a harness-supplied forbidden contract for this,
rather than trusting whatever the agent wrote: the agent could satisfy
its own contract by never writing one that bites. So the grader adds a
contract of its own, forbidding billing from reaching any private
catalogue module, and requires the run to stay green under it.

Adding a contract is done on a copy. Where import-linter is missing the
criterion is left unsettled rather than failed, but the source-level
read still runs first, because a billing module importing
`catalogue.internal` is a fail this grader can prove without any tool.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, emit, imports_of,  # noqa: E402
                     lint_available, read, run_lint, scratch_dir)

CID = "c10"

HARNESS_CONTRACT = """
[importlinter:contract:drill-c10-public-interface-only]
name = Harness: billing reaches the catalogue only through its public interface
type = forbidden
source_modules =
    billing
forbidden_modules =
    catalogue.internal
"""


def billing_modules(scratch):
    root = Path(scratch) / "billing"
    if not root.is_dir():
        return []
    return sorted(p for p in root.rglob("*.py") if p.name != "__init__.py")


def main():
    scratch = scratch_dir()
    modules = billing_modules(scratch)
    if not modules:
        emit(CID, FAIL, "no billing module in the delivered tree")

    # A private import is decidable from the source alone.
    reaches_catalogue = []
    for path in modules:
        rel = path.relative_to(scratch).as_posix()
        for name in imports_of(read(path)):
            if name.startswith("catalogue.internal") or name == \
                    "catalogue.internal":
                emit(CID, FAIL,
                     "%s imports %s, a private catalogue module, rather than "
                     "the declared public interface" % (rel, name))
            if name == "catalogue" or name.startswith("catalogue."):
                reaches_catalogue.append((rel, name))

    if not reaches_catalogue:
        emit(CID, FAIL,
             "no billing module imports the catalogue at all, so the price "
             "lookup the prompt asked for was not delivered")

    if not lint_available():
        emit(CID, UNSETTLED,
             "billing reaches the catalogue only via %s by a source read, but "
             "import-linter is not installed here, so the harness contract "
             "was not run"
             % ", ".join(sorted({n for _, n in reaches_catalogue})))

    work = Path(tempfile.mkdtemp(prefix="drill-arch-c10-"))
    try:
        copy = work / "tree"
        shutil.copytree(scratch, copy)
        config = copy / ".importlinter"
        if not config.is_file():
            for name in ("setup.cfg", "tox.ini"):
                if (copy / name).is_file():
                    config = copy / name
                    break
        existing = read(config) if config.is_file() else ""
        if "[importlinter]" not in existing:
            existing = ("[importlinter]\nroot_packages =\n    billing\n"
                        "    catalogue\n    shared\n") + existing
        config.write_text(existing.rstrip("\n") + "\n" + HARNESS_CONTRACT,
                          encoding="utf-8")

        code, output = run_lint(copy)
        if code is None:
            emit(CID, FAIL,
                 "could not run lint-imports with the harness contract: %s"
                 % output.strip()[:300])
        if code == 0:
            emit(CID, PASS,
                 "the harness contract forbidding billing to reach "
                 "catalogue.internal holds; billing uses %s"
                 % ", ".join(sorted({n for _, n in reaches_catalogue})))
        emit(CID, FAIL,
             "the harness contract fails (exit %d): billing reaches a "
             "private catalogue module. %s"
             % (code, " ".join(output.split())[:250]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
