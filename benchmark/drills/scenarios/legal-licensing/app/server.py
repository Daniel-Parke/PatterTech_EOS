"""The site. One WSGI callable, a handful of routes, no framework.

Run it locally with `make run`, which puts it on port 8000.
"""

import hmac
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

import sigcheck
import tinytmpl

from app import __version__, config, store

PAGE = """<!doctype html>
<html>
<head><title>{{ site_name }}</title></head>
<body>
<h1>{{ site_name }}</h1>
<p>{{ blurb }}</p>
<p>Questions go to {{ support_address }}.</p>
</body>
</html>
"""

BLURB = ("We are building the thing you asked for. There is not much "
         "to look at yet.")


def _settings(environ):
    return environ.get("postbox.settings") or config.load()


def home(environ):
    settings = _settings(environ)
    body = tinytmpl.render(PAGE, site_name=settings["site_name"],
                           blurb=BLURB,
                           support_address=settings["support_address"])
    return "200 OK", "text/html; charset=utf-8", body


def health(environ):
    return "200 OK", "text/plain; charset=utf-8", "ok %s\n" % __version__


def export(environ):
    """The admin CSV pull. Signed, because it is a list of people."""
    settings = _settings(environ)
    given = environ.get("HTTP_X_POSTBOX_SIGNATURE", "")
    expected = sigcheck.sign(environ.get("PATH_INFO", ""),
                             settings["export_secret"])
    if not hmac.compare_digest(given, expected):
        return "403 Forbidden", "text/plain; charset=utf-8", "no\n"
    rows = store.JsonList(config.data_dir(settings) / "subscribers.json")
    lines = ["email"] + [str(row.get("email", "")) for row in rows.read()]
    return "200 OK", "text/csv; charset=utf-8", "\n".join(lines) + "\n"


ROUTES = {
    ("GET", "/"): home,
    ("GET", "/health"): health,
    ("GET", "/admin/export"): export,
}


def form(environ):
    """Parsed body of a form post. Empty for anything else."""
    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        return {}
    if length <= 0:
        return {}
    raw = environ["wsgi.input"].read(length).decode("utf-8", "replace")
    return {k: v[0] for k, v in parse_qs(raw).items() if v}


def application(environ, start_response):
    handler = ROUTES.get((environ.get("REQUEST_METHOD", "GET"),
                          environ.get("PATH_INFO", "/")))
    if handler is None:
        status, kind, body = ("404 Not Found", "text/plain; charset=utf-8",
                              "not here\n")
    else:
        status, kind, body = handler(environ)
    payload = body.encode("utf-8")
    start_response(status, [("Content-Type", kind),
                            ("Content-Length", str(len(payload)))])
    return [payload]


def main():
    with make_server("", 8000, application) as httpd:
        print("postbox on http://localhost:8000")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
