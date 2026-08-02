"""HTTP layer: routes, JSON helpers, auth plumbing."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    import jsonlogx as logx
except ImportError:
    from app import loglite as logx

from app import auth, quotes

# One connection is shared across handler threads; this lock serialises it.
DB_LOCK = threading.Lock()

VALID_TARIFFS = {"STD", "ECO7", "FIX12"}
VALID_CUSTOMER_TYPES = {"domestic", "business"}
VALID_PROMOS = {"SAVE10", "GREEN5", "NEW"}


class QuoteAPIHandler(BaseHTTPRequestHandler):
    conn = None  # bound by create_server

    # -- plumbing -----------------------------------------------------------

    def log_message(self, format, *args):
        logx.log("http", client=self.client_address[0], line=format % args)

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
        except (TypeError, ValueError):
            return None
        if length <= 0:
            return None
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            return None
        if not isinstance(data, dict):
            return None
        return data

    def _claims(self):
        header = self.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return None
        return auth.check_token(header[len("Bearer "):].strip())

    # -- routes -------------------------------------------------------------

    def do_POST(self):
        if self.path == "/login":
            self._post_login()
        elif self.path == "/quotes":
            self._post_quotes()
        else:
            self._send_json(404, {"error": "not found"})

    def do_GET(self):
        if self.path == "/quotes":
            self._get_quotes()
        elif self.path == "/admin/reports":
            self._get_admin_reports()
        else:
            self._send_json(404, {"error": "not found"})

    def _post_login(self):
        data = self._read_json()
        if data is None or "email" not in data or "password" not in data:
            self._send_json(400, {"error": "email and password required"})
            return
        with DB_LOCK:
            token = auth.issue_token(self.conn, data["email"], data["password"])
        if token is None:
            self._send_json(401, {"error": "invalid credentials"})
            return
        self._send_json(200, {"token": token})

    def _get_quotes(self):
        claims = self._claims()
        if claims is None:
            self._send_json(401, {"error": "authentication required"})
            return
        with DB_LOCK:
            rows = quotes.list_quotes(self.conn, claims["user_id"])
        self._send_json(200, {"quotes": rows})

    def _post_quotes(self):
        claims = self._claims()
        if claims is None:
            self._send_json(401, {"error": "authentication required"})
            return
        data = self._read_json()
        if data is None:
            self._send_json(400, {"error": "JSON body required"})
            return
        kwh = data.get("kwh")
        tariff_code = data.get("tariff_code")
        customer_type = data.get("customer_type")
        promo = data.get("promo")
        if not isinstance(kwh, int) or isinstance(kwh, bool) or kwh < 0:
            self._send_json(400, {"error": "kwh must be a non-negative integer"})
            return
        if tariff_code not in VALID_TARIFFS:
            self._send_json(400, {"error": "unknown tariff_code"})
            return
        if customer_type not in VALID_CUSTOMER_TYPES:
            self._send_json(400, {"error": "unknown customer_type"})
            return
        if promo is not None and promo not in VALID_PROMOS:
            self._send_json(400, {"error": "unknown promo"})
            return
        with DB_LOCK:
            quote = quotes.create_quote(
                self.conn, claims["user_id"], kwh, tariff_code, customer_type, promo
            )
        self._send_json(201, {"quote": quote})

    def _get_admin_reports(self):
        claims = self._claims()
        if claims is None:
            self._send_json(401, {"error": "authentication required"})
            return
        with DB_LOCK:
            data = quotes.report(self.conn)
        self._send_json(200, {"report": data})


def create_server(conn, host, port):
    """Build a ThreadingHTTPServer with the connection bound to the handler."""
    handler = type("BoundQuoteAPIHandler", (QuoteAPIHandler,), {"conn": conn})
    return ThreadingHTTPServer((host, port), handler)
