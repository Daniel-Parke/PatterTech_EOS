#!/usr/bin/env python3
"""Criterion 9: nothing was added beyond the standard library.

Two reads, because a declaration and a use can disagree.

The manifest read collects every requirement the tree declares, from
pyproject, any requirements file, setup.cfg and Pipfile, and allows
only what the fixture already pinned to run its own suite. A rule
engine or a state machine library shows up here.

The source read looks at what `booking/` actually imports and allows
only standard library modules and the package itself, which catches the
same library brought in without being declared.

Four statuses do not warrant an engine, so this is the criterion that
separates knowing a tool from knowing when it is not needed yet.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, booking_modules,  # noqa: E402
                     emit, imports_of, read, require_implementation,
                     scratch_dir)

CID = "c9"

# What the fixture already pinned so that its own suite could run.
HARNESS_PINS = {"pytest", "setuptools", "wheel", "pip", "python"}

REQUIREMENTS = ("requirements.txt", "requirements-dev.txt",
                "requirements_dev.txt", "requirements-test.txt",
                "dev-requirements.txt", "test-requirements.txt")

NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*")
INSTALL_REQUIRES = re.compile(
    r"install_requires\s*=\s*\[(.*?)\]", re.S)
QUOTED = re.compile(r"""['"]([^'"]+)['"]""")


def canonical(raw):
    """PEP 503 style: case and separators do not distinguish a project."""
    match = NAME.match(str(raw).strip())
    if not match:
        return None
    return re.sub(r"[-_.]+", "-", match.group(0)).lower()


def from_requirement_lines(text):
    found = set()
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith("-") or line.startswith("."):
            continue
        name = canonical(line)
        if name:
            found.add(name)
    return found


def from_pyproject(path):
    """Every declared requirement in a pyproject, or None if it will not parse."""
    try:
        import tomllib
    except ImportError:
        return None
    try:
        with open(path, "rb") as handle:
            doc = tomllib.load(handle)
    except (OSError, ValueError):
        return None

    raw = []
    project = doc.get("project") or {}
    raw.extend(project.get("dependencies") or [])
    for group in (project.get("optional-dependencies") or {}).values():
        raw.extend(group or [])
    for group in (doc.get("dependency-groups") or {}).values():
        raw.extend([g for g in (group or []) if isinstance(g, str)])
    raw.extend((doc.get("build-system") or {}).get("requires") or [])
    poetry = ((doc.get("tool") or {}).get("poetry") or {})
    raw.extend(list((poetry.get("dependencies") or {}).keys()))
    for group in (poetry.get("group") or {}).values():
        raw.extend(list((group.get("dependencies") or {}).keys()))

    found = set()
    for item in raw:
        name = canonical(item)
        if name:
            found.add(name)
    return found


def declared(scratch):
    """Returns (names, files_read, unparsed_pyproject)."""
    names, files, unparsed = set(), [], False

    pyproject = scratch / "pyproject.toml"
    if pyproject.is_file():
        got = from_pyproject(pyproject)
        if got is None:
            unparsed = True
        else:
            names |= got
            files.append("pyproject.toml")

    for name in REQUIREMENTS:
        path = scratch / name
        if path.is_file():
            names |= from_requirement_lines(read(path))
            files.append(name)

    setup_cfg = scratch / "setup.cfg"
    if setup_cfg.is_file():
        text = read(setup_cfg)
        match = re.search(r"install_requires\s*=\s*(.*?)(?=^\S|\Z)",
                          text, re.S | re.M)
        if match:
            names |= from_requirement_lines(match.group(1))
            files.append("setup.cfg")

    setup_py = scratch / "setup.py"
    if setup_py.is_file():
        for block in INSTALL_REQUIRES.findall(read(setup_py)):
            for item in QUOTED.findall(block):
                got = canonical(item)
                if got:
                    names.add(got)
        files.append("setup.py")

    pipfile = scratch / "Pipfile"
    if pipfile.is_file():
        section = None
        for line in read(pipfile).splitlines():
            stripped = line.strip()
            if stripped.startswith("["):
                section = stripped.strip("[]").lower()
                continue
            if section in ("packages", "dev-packages") and "=" in stripped:
                got = canonical(stripped.split("=", 1)[0])
                if got:
                    names.add(got)
        files.append("Pipfile")

    return names, files, unparsed


def main():
    scratch = scratch_dir()
    require_implementation(CID, scratch)

    names, files, unparsed = declared(scratch)
    if unparsed and not files:
        emit(CID, UNSETTLED,
             "pyproject.toml is the only manifest here and this interpreter "
             "has no tomllib to read it with, so the declared dependencies "
             "were never seen")
    if not files:
        emit(CID, FAIL,
             "no dependency manifest in the delivered tree; the one the "
             "project shipped is gone, so nothing states what it runs on")

    added = sorted(names - HARNESS_PINS)
    if added:
        emit(CID, FAIL,
             "%s declare%s %s beyond the standard library and the pins the "
             "suite already needed: %s"
             % (", ".join(files), "" if len(files) > 1 else "s",
                "a dependency" if len(added) == 1 else "%d dependencies"
                % len(added), ", ".join(added)))

    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    if not stdlib:
        emit(CID, UNSETTLED,
             "this interpreter does not publish sys.stdlib_module_names, so "
             "what booking/ imports could not be classified")

    outside = []
    for path in booking_modules(scratch):
        rel = path.relative_to(scratch).as_posix()
        for module in sorted(imports_of(read(path))):
            if module in stdlib or module == "booking":
                continue
            outside.append("%s imports %s" % (rel, module))
    if outside:
        emit(CID, FAIL,
             "the manifest is clean but the code is not: %s. An undeclared "
             "library is still a dependency" % "; ".join(outside[:5]))

    emit(CID, PASS,
         "%s declare%s nothing beyond %s, and booking/ imports only the "
         "standard library"
         % (", ".join(files), "" if len(files) > 1 else "s",
            ", ".join(sorted(names)) or "an empty dependency list"))


if __name__ == "__main__":
    main()
