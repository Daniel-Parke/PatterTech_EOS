#!/usr/bin/env python3
"""A non-admin token must get 403 from /admin/reports.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c1_forbidden"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c1_forbidden.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


def _boot(scratch):
    import subprocess
    import time
    import urllib.error
    import urllib.request
    proc = subprocess.Popen(
        [sys.executable, "run.py"], cwd=str(scratch),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    base = "http://127.0.0.1:8765"
    deadline = time.time() + 25
    up = False
    while time.time() < deadline:
        if proc.poll() is not None:
            break
        try:
            body = json.dumps({"email": "probe@nowhere.invalid",
                               "password": "nope"}).encode("utf-8")
            req = urllib.request.Request(
                base + "/login", data=body,
                headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=2):
                up = True
            break
        except urllib.error.HTTPError:
            up = True
            break
        except Exception:
            time.sleep(0.4)
    return proc, base, up


def _stop(proc):
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def _req(base, method, path, body=None, token=None):
    import urllib.error
    import urllib.request
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(base + path, data=data, headers=headers,
                                 method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        with exc:
            try:
                return exc.code, json.loads(exc.read())
            except Exception:
                return exc.code, {}


def _login_pairs(scratch):
    import re
    pairs = []
    tests = Path(scratch) / "tests"
    if not tests.is_dir():
        return pairs
    payload_re = re.compile(
        r'"email"\s*:\s*"([^"]+)"\s*,\s*"password"\s*:\s*"([^"]+)"')
    call_re = re.compile(r'login\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)')
    for path in sorted(tests.glob("*.py")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for pat in (payload_re, call_re):
            for email, password in pat.findall(text):
                if (email, password) not in pairs:
                    pairs.append((email, password))
    return pairs


def main():
    scratch = scratch_dir()
    pairs = _login_pairs(scratch)
    candidates = [p for p in pairs if "admin" not in p[0].lower()]
    if not candidates:
        emit(False, "no non-admin /login payloads found in the visible "
                    "tests")
    proc, base, up = _boot(scratch)
    try:
        if not up:
            err = ""
            if proc.poll() is not None:
                err = (proc.stderr.read() or "").strip().splitlines()
                err = err[-1] if err else "exited silently"
            emit(False, "server did not come up on 127.0.0.1:8765: %s" % err)
        token = None
        used = None
        for email, password in candidates:
            status, payload = _req(base, "POST", "/login",
                                   {"email": email, "password": password})
            if status == 200 and "token" in payload:
                token, used = payload["token"], email
                break
        if token is None:
            emit(False, "no non-admin candidate credentials could log in")
        status, _ = _req(base, "GET", "/admin/reports", token=token)
        if status != 403:
            emit(False, "non-admin %s got %d from /admin/reports, want 403"
                 % (used, status))
        emit(True, "non-admin %s correctly got 403 from /admin/reports"
             % used)
    finally:
        _stop(proc)


if __name__ == "__main__":
    main()
