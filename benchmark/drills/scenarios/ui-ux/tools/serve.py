#!/usr/bin/env python3
"""Preview dist/ on http://localhost:8000. Build first."""

import functools
import http.server
import socketserver
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORT = 8000


def main():
    directory = ROOT / "dist"
    if not directory.is_dir():
        print("dist/ is not there yet: run python tools/build.py")
        return 1
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory=str(directory))
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print("serving %s on http://localhost:%d" % (directory, PORT))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
