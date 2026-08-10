#!/usr/bin/env python3
"""Criterion 9: no new commercial or hosted-service dependency.

What a script can settle: whether anything was added at all, and
whether what was added is on a list of names that are plainly a paid or
hosted service. What a script cannot settle from a name alone, offline,
is whether some package nobody listed here bills you or phones home.
Guessing that would be inventing a verdict, so an addition this grader
does not recognise is reported as unsettled and lands as manual for a
human to judge. The names it does recognise are named in the reason
either way, so the human starts from a short list rather than a diff.

Sources read: `pyproject.toml` in every form it carries dependencies,
`requirements*.txt`, and the CI workflows, both the actions they use
and anything a `pip install` line names.
"""

import fnmatch
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, PRISTINE, UNSETTLED, emit, read,  # noqa: E402
                     relative, scratch_dir)

CID = "c9"

COMMERCIAL = {
    # observability and error tracking sold as a service
    "sentry-sdk", "sentry", "datadog", "datadog-api-client", "ddtrace",
    "newrelic", "new-relic", "bugsnag", "rollbar", "honeycomb-beeline",
    "libhoney", "elastic-apm", "splunk-sdk", "logdna", "loggly",
    # feature flags, experimentation, session replay
    "launchdarkly-server-sdk", "launchdarkly", "split-io", "optimizely-sdk",
    "statsig", "fullstory", "logrocket",
    # hosted test and quality services
    "browserstack", "browserstack-local", "saucelabs", "sauceclient",
    "lambdatest", "crossbrowsertesting", "percy", "percy-python-selenium",
    "applitools", "applitools-eyes", "mabl", "testim", "ghostinspector",
    "blazemeter", "gremlin", "testrail-api", "pytest-testrail",
    "qase-pytest", "xray-pytest", "codecov", "coveralls", "sonarcloud",
    "sonarqube-api", "snyk", "pactflow", "pact-broker", "smartbear",
    "runscope", "postman",
    # commercial APIs a test suite has no business acquiring
    "stripe", "braintree", "adyen", "twilio", "sendgrid", "mailgun",
    "auth0", "okta-sdk-python", "algolia", "pusher", "pubnub",
    # hosted CI actions
    "codecov/codecov-action", "percy/exec-action",
    "browserstack/github-actions", "datadog/agent-github-action",
    "saucelabs/sauce-connect-action",
    "snyk/actions", "sonarsource/sonarcloud-github-action",
}

OPEN_SOURCE = {
    "pytest", "pytest-cov", "pytest-mock", "pytest-timeout", "pytest-xdist",
    "pytest-randomly", "pytest-subtests", "pytest-repeat", "pytest-asyncio",
    "pytest-freezegun", "pytest-freezer", "pytest-recording", "pytest-vcr",
    "pytest-rerunfailures", "flaky", "coverage", "freezegun", "time-machine",
    "hypothesis", "responses", "respx", "requests-mock", "vcrpy", "httpx",
    "requests", "urllib3", "jsonschema", "pydantic", "python-dateutil",
    "faker", "syrupy", "schemathesis", "pact-python", "mypy", "ruff",
    "flake8", "black", "isort", "tox", "nox", "pre-commit", "setuptools",
    "wheel", "build", "packaging", "typing-extensions", "pyyaml",
    "importlib-metadata", "tomli",
    "actions/checkout", "actions/setup-python", "actions/cache",
    "actions/upload-artifact", "actions/download-artifact",
}

SPLIT = re.compile(r"[<>=!~;\[\s,]")
USES = re.compile(r"^\s*-?\s*uses:\s*([^\s@]+)", re.M)
PIP = re.compile(r"pip install\s+(.+)", re.I)


def normalise(raw):
    name = SPLIT.split(str(raw).strip().strip("'\""), 1)[0]
    name = name.strip().lower()
    if "/" in name:
        return name
    return re.sub(r"[-_.]+", "-", name)


def from_pyproject(path):
    names = set()
    if not path.is_file():
        return names
    try:
        import tomllib
    except ImportError:
        for line in read(path).splitlines():
            match = re.match(r"\s*[\"']([A-Za-z0-9_.\-]+)", line)
            if match:
                names.add(normalise(match.group(1)))
        return names
    try:
        with open(path, "rb") as handle:
            doc = tomllib.load(handle)
    except (OSError, ValueError):
        return names

    def eat(value):
        if isinstance(value, str):
            names.add(normalise(value))
        elif isinstance(value, list):
            for item in value:
                eat(item)
        elif isinstance(value, dict):
            for key, item in value.items():
                names.add(normalise(key))
                if isinstance(item, (list, dict)):
                    eat(item)

    project = doc.get("project", {})
    eat(project.get("dependencies", []))
    eat(project.get("optional-dependencies", {}))
    eat(doc.get("dependency-groups", {}))
    eat(doc.get("build-system", {}).get("requires", []))
    poetry = doc.get("tool", {}).get("poetry", {})
    eat(poetry.get("dependencies", {}))
    eat(poetry.get("group", {}))
    names.discard("")
    return names


def from_requirements(tree):
    names = set()
    for path in Path(tree).rglob("requirements*.txt"):
        for line in read(path).splitlines():
            line = line.strip()
            if not line or line.startswith(("#", "-r", "--")):
                continue
            names.add(normalise(line))
    names.discard("")
    return names


def from_ci(tree):
    names = set()
    for path in Path(tree).rglob("*"):
        if not path.is_file() or path.suffix not in (".yml", ".yaml"):
            continue
        rel = relative(tree, path)
        if not (fnmatch.fnmatch(rel, ".github/workflows/*") or
                "ci" in path.name or "pre-commit" in path.name):
            continue
        text = read(path)
        for match in USES.finditer(text):
            names.add(normalise(match.group(1)))
        for match in PIP.finditer(text):
            for word in match.group(1).split():
                if word.startswith("-") or word in (".", "-e"):
                    continue
                names.add(normalise(word))
    names.discard("")
    return names


def declared(tree):
    return (from_pyproject(Path(tree) / "pyproject.toml")
            | from_requirements(tree) | from_ci(tree))


def main():
    scratch = scratch_dir()
    before = declared(PRISTINE)
    after = declared(scratch)
    added = sorted(after - before)

    if not added:
        emit(CID, PASS,
             "no dependency was added to pyproject.toml, requirements or the "
             "CI workflows")

    paid = [name for name in added if name in COMMERCIAL]
    if paid:
        emit(CID, FAIL,
             "new commercial or hosted-service dependency: %s"
             % ", ".join(paid))

    unknown = [name for name in added if name not in OPEN_SOURCE]
    if unknown:
        emit(CID, UNSETTLED,
             "added %s, none of which is on this grader's list of paid or "
             "hosted services, and none of which it can classify from the "
             "name alone. Whether these are commercial is a judgement for a "
             "human, so the criterion is left unsettled rather than guessed."
             % ", ".join(unknown))

    emit(CID, PASS,
         "added %s, all of which are open source packages with no hosted "
         "service behind them" % ", ".join(added))


if __name__ == "__main__":
    main()
