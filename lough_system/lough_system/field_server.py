"""
field_server.py — Field HTTP Bridge
Exposes field_bridge over HTTP so Code City and other clients can read/write.
Flask only — no Rust-compiled deps, works on Android/Termux.
"""

import sys
import os
sys.path.insert(0, '/data/data/com.termux/files/home/lough_system')

from flask import Flask, request, jsonify
from flask_cors import CORS
import domain_bridge
import field_bridge
import event_registry

app = Flask(__name__)
CORS(app)

API_TOKEN = os.getenv("LOUGH_API_TOKEN")
ALLOW_REMOTE = os.getenv("LOUGH_ALLOW_REMOTE", "0") == "1"
LOCAL_ADDRS = {"127.0.0.1", "::1", "localhost"}


def _authorized_request():
    if API_TOKEN:
        supplied = request.headers.get("X-Lough-Token") or request.args.get("token")
        return supplied == API_TOKEN
    if ALLOW_REMOTE:
        return True
    return request.remote_addr in LOCAL_ADDRS


@app.before_request
def enforce_access_policy():
    if _authorized_request():
        return None
    return jsonify({
        "error": "Unauthorized",
        "detail": "Set LOUGH_API_TOKEN and send X-Lough-Token, or keep requests local."
    }), 401

@app.after_request
def log_usage(response):
    """Logs all requests as system.usage events."""
    try:
        field_bridge.emit(
            event_type="system.usage",
            location="field_server",
            source="field_server",
            payload={
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "remote_addr": request.remote_addr,
            }
        )
    except Exception as e:
        print(f"[META-ERROR] Failed to log usage: {e}")
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    """Catches all unhandled exceptions and emits system.error events."""
    try:
        field_bridge.emit(
            event_type="system.error",
            location="field_server",
            source="field_server",
            payload={
                "error": type(e).__name__,
                "message": str(e),
                "path": request.path,
                "method": request.method
            }
        )
    except Exception as meta_e:
        print(f"[META-ERROR] Failed to log error: {meta_e}")

    return jsonify({
        "error": "Internal Server Error",
        "detail": str(e)
    }), 500

@app.route("/emit", methods=["POST"])
def emit_event():
    d = request.get_json(force=True)
    field_bridge.emit(
        event_type = d.get("event_type", "unknown"),
        intensity  = float(d.get("intensity", 1.0)),
        location   = d.get("location", "system"),
        payload    = d.get("payload", {}),
        source     = d.get("source", "unknown"),
        relation_id = d.get("relation_id", None),
        confidence = d.get("confidence", None),
        provenance = d.get("provenance", None),
        review_status = d.get("review_status", None),
        created_by = d.get("created_by", None),
    )
    return jsonify({"status": "emitted"})


@app.route("/poll", methods=["GET"])
def poll_events():
    events = field_bridge.poll(
        since        = request.args.get("since", None, type=float),
        source_layer = request.args.get("source_layer", None),
        event_type   = request.args.get("event_type", None),
        limit        = request.args.get("limit", 50, type=int),
        relation_id  = request.args.get("relation_id", None, type=int),
    )
    return jsonify(events)


@app.route("/registry", methods=["GET"])
def registry():
    return jsonify(event_registry.all_namespaces())


@app.route("/review", methods=["GET"])
def list_review_queue():
    review_status = request.args.get("review_status", "review_required")
    relation_id = request.args.get("relation_id", None, type=int)
    limit = request.args.get("limit", 50, type=int)
    return jsonify(field_bridge.review_queue(
        review_status=review_status,
        relation_id=relation_id,
        limit=limit,
    ))


@app.route("/review/<int:event_id>", methods=["POST"])
def update_review(event_id):
    data = request.get_json(force=True)
    review_status = data.get("review_status")
    reviewed_by = data.get("reviewed_by")
    if not review_status:
        return jsonify({"error": "Bad Request", "detail": "review_status is required."}), 400
    if not reviewed_by:
        return jsonify({"error": "Bad Request", "detail": "reviewed_by is required."}), 400

    event = field_bridge.update_review_status(
        event_id=event_id,
        review_status=review_status,
        reviewed_by=reviewed_by,
        review_note=data.get("review_note", None),
    )
    if event is None:
        return jsonify({"error": "Not Found", "detail": "Event not found."}), 404
    return jsonify({"status": "updated", "event": event})


@app.route("/clients", methods=["GET"])
def list_clients():
    limit = request.args.get("limit", 100, type=int)
    return jsonify(field_bridge.list_entities(entity_type="client", limit=limit))


@app.route("/clients", methods=["POST"])
def create_client():
    data = request.get_json(force=True)
    name = data.get("name")
    if not name:
        return jsonify({"error": "Bad Request", "detail": "Client name is required."}), 400

    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        return jsonify({"error": "Bad Request", "detail": "metadata must be an object."}), 400

    client_id = field_bridge.create_entity("client", name, metadata)
    client = field_bridge.get_entity(client_id)
    field_bridge.emit(
        event_type=event_registry.SYSTEM_NAMESPACE["client"],
        location="client.onboarding",
        source="field_server",
        relation_id=client_id,
        payload={"client_id": client_id, "name": name, "metadata": metadata},
        provenance={"method": "POST /clients"},
        created_by=data.get("created_by", "field_server"),
    )
    return jsonify({"status": "created", "client": client}), 201


@app.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    client = field_bridge.get_entity(client_id)
    if client is None or client["entity_type"] != "client":
        return jsonify({"error": "Not Found", "detail": "Client not found."}), 404
    return jsonify(client)


@app.route("/clients/<int:client_id>/emit", methods=["POST"])
def emit_client_event(client_id):
    client = field_bridge.get_entity(client_id)
    if client is None or client["entity_type"] != "client":
        return jsonify({"error": "Not Found", "detail": "Client not found."}), 404

    data = request.get_json(force=True)
    if data.get("domain") and data.get("event_key"):
        domain_bridge.emit_domain_event(
            domain=data["domain"],
            event_key=data["event_key"],
            intensity=float(data.get("intensity", 1.0)),
            location=data.get("location", f"client.{client_id}"),
            payload=data.get("payload", {}),
            source=data.get("source", "client_api"),
            relation_id=client_id,
            confidence=data.get("confidence", None),
            provenance=data.get("provenance", {"method": "POST /clients/<id>/emit"}),
            review_status=data.get("review_status", None),
            created_by=data.get("created_by", None),
        )
    else:
        field_bridge.emit(
            event_type=data.get("event_type", "unknown"),
            intensity=float(data.get("intensity", 1.0)),
            location=data.get("location", f"client.{client_id}"),
            payload=data.get("payload", {}),
            source=data.get("source", "client_api"),
            relation_id=client_id,
            confidence=data.get("confidence", None),
            provenance=data.get("provenance", {"method": "POST /clients/<id>/emit"}),
            review_status=data.get("review_status", None),
            created_by=data.get("created_by", None),
        )
    return jsonify({"status": "emitted", "client_id": client_id})


if __name__ == "__main__":
    print("[FIELD SERVER] Running on http://0.0.0.0:7070")
    app.run(host="0.0.0.0", port=7070)
