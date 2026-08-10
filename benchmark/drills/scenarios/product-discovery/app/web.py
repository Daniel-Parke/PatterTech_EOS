"""The routes. Thin: everything real lives in counts.py and items.py."""

from flask import Flask, jsonify, request

from .counts import Count, CountClosed, summarise
from .items import Catalogue

app = Flask(__name__)

CATALOGUE = Catalogue()
COUNTS = {}


@app.get("/items")
def list_items():
    term = request.args.get("q", "")
    found = CATALOGUE.search(term) if term else CATALOGUE.live()
    return jsonify([{"item_id": i.item_id, "name": i.name, "unit": i.unit}
                    for i in found])


@app.post("/counts")
def open_count():
    body = request.get_json(silent=True) or {}
    count = Count(count_id=body["count_id"], site=body["site"],
                  area=body["area"], opened_by=body["opened_by"])
    COUNTS[count.count_id] = count
    return jsonify({"count_id": count.count_id})


@app.post("/counts/<count_id>/lines")
def enter_line(count_id):
    count = COUNTS.get(count_id)
    if count is None:
        return jsonify({"error": "no such count"}), 404
    body = request.get_json(silent=True) or {}
    try:
        count.enter(body["item_id"], float(body["quantity"]),
                    body.get("unit", "each"), body.get("entered_by", ""))
    except CountClosed:
        return jsonify({"error": "count is closed"}), 409
    return jsonify({"lines": count.total_lines()})


@app.post("/counts/<count_id>/close")
def close_count(count_id):
    count = COUNTS.get(count_id)
    if count is None:
        return jsonify({"error": "no such count"}), 404
    count.close()
    return jsonify({"count_id": count_id,
                    "value": summarise(count, CATALOGUE)})
