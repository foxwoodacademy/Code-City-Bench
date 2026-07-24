"""
field_bridge.py — FEP Event Spine
Connects ~/lough_system/ to /storage/emulated/0/modmind/modmind.db
All layers (physical, informational, computational) write and read here.
"""

import sqlite3
import json
import time
from datetime import datetime
from contextlib import closing
import event_envelope

DB_PATH = "/storage/emulated/0/modmind/modmind.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS field_entities (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type   TEXT    NOT NULL,
    entity_name   TEXT    NOT NULL,
    metadata      TEXT    NOT NULL DEFAULT '{}',
    created_at    REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS field_events (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type    TEXT    NOT NULL,
    intensity     REAL    NOT NULL DEFAULT 1.0,
    location      TEXT    NOT NULL,
    payload       TEXT    NOT NULL DEFAULT '{}',
    source_layer  TEXT    NOT NULL DEFAULT 'unknown',
    timestamp     REAL    NOT NULL,
    relation_id   INTEGER,
    FOREIGN KEY (relation_id) REFERENCES field_entities(id)
);

CREATE TABLE IF NOT EXISTS lough_migrations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    migration     TEXT    NOT NULL UNIQUE,
    applied_at    REAL    NOT NULL
);
"""

INDEX_SCHEMA = """
CREATE INDEX IF NOT EXISTS idx_field_events_type      ON field_events(event_type);
CREATE INDEX IF NOT EXISTS idx_field_events_timestamp ON field_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_field_events_source    ON field_events(source_layer);
CREATE INDEX IF NOT EXISTS idx_field_events_relation  ON field_events(relation_id);
"""


def emit(
    event_type,
    intensity=1.0,
    location="system",
    payload=None,
    source="unknown",
    relation_id=None,
    confidence=None,
    provenance=None,
    review_status=None,
    created_by=None,
):
    """
    Emit a FieldEvent into modmind.db.
    All layers call this — game, accountability, sensors, agents.
    """
    payload = event_envelope.normalize_payload(
        event_type=event_type,
        payload=payload,
        source=source,
        confidence=confidence,
        provenance=provenance,
        review_status=review_status,
        created_by=created_by,
    )
    ts = time.time()
    with closing(_connect()) as conn:
        conn.execute(
            "INSERT INTO field_events (event_type, intensity, location, payload, source_layer, timestamp, relation_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (event_type, float(intensity), location, json.dumps(payload), source, ts, relation_id)
        )
        conn.commit()
    print(f"[FIELD] {datetime.fromtimestamp(ts).strftime('%H:%M:%S')}  "
          f"{source:>16} → {event_type}  "
          f"@ {location}  (intensity={intensity})")


def poll(since=None, source_layer=None, event_type=None, limit=50, relation_id=None):
    """
    Read FieldEvents back out with optional filters.
    Returns list of dicts, newest first.
    """
    query = "SELECT * FROM field_events WHERE 1=1"
    params = []

    if since is not None:
        query += " AND timestamp > ?"
        params.append(since)
    if source_layer is not None:
        query += " AND source_layer = ?"
        params.append(source_layer)
    if event_type is not None:
        query += " AND event_type LIKE ?"
        params.append(f"%{event_type}%")
    if relation_id is not None:
        query += " AND relation_id = ?"
        params.append(relation_id)

    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    with closing(_connect()) as conn:
        rows = conn.execute(query, params).fetchall()

    return [_event_from_row(row) for row in rows]


def get_event(event_id):
    """Return one event by id, or None if it does not exist."""
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT * FROM field_events WHERE id = ?",
            (event_id,)
        ).fetchone()
    if row is None:
        return None
    return _event_from_row(row)


def create_entity(entity_type, entity_name, metadata=None):
    """
    Create a trackable entity in the system.
    Returns the entity_id.
    """
    if metadata is None:
        metadata = {}
    ts = time.time()
    with closing(_connect()) as conn:
        cursor = conn.execute(
            "INSERT INTO field_entities (entity_type, entity_name, metadata, created_at) "
            "VALUES (?, ?, ?, ?)",
            (entity_type, entity_name, json.dumps(metadata), ts)
        )
        conn.commit()
        return cursor.lastrowid


def get_entity(entity_id):
    """Return one entity by id, or None if it does not exist."""
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT * FROM field_entities WHERE id = ?",
            (entity_id,)
        ).fetchone()
    if row is None:
        return None
    return _entity_from_row(row)


def list_entities(entity_type=None, limit=100):
    """Return entities newest first."""
    query = "SELECT * FROM field_entities WHERE 1=1"
    params = []
    if entity_type is not None:
        query += " AND entity_type = ?"
        params.append(entity_type)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    with closing(_connect()) as conn:
        rows = conn.execute(query, params).fetchall()

    return [
        _entity_from_row(row)
        for row in rows
    ]


def review_queue(review_status="review_required", relation_id=None, limit=50):
    """Return recent events matching a `_lough.review_status` value."""
    candidates = poll(relation_id=relation_id, limit=max(limit * 5, limit))
    matches = []
    for event in candidates:
        envelope = event_envelope.envelope_from_event(event)
        if envelope.get("review_status") == review_status:
            matches.append(event)
        if len(matches) >= limit:
            break
    return matches


def update_review_status(event_id, review_status, reviewed_by, review_note=None):
    """Update an event envelope review status and emit an audit event."""
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT * FROM field_events WHERE id = ?",
            (event_id,)
        ).fetchone()
        if row is None:
            return None

        payload = json.loads(row["payload"])
        if not isinstance(payload, dict):
            payload = {"value": payload}
        envelope = payload.get("_lough", {})
        if not isinstance(envelope, dict):
            envelope = {}

        envelope.update({
            "review_status": review_status,
            "reviewed_by": reviewed_by,
            "reviewed_at": time.time(),
        })
        if review_note:
            envelope["review_note"] = review_note
        payload["_lough"] = envelope

        conn.execute(
            "UPDATE field_events SET payload = ? WHERE id = ?",
            (json.dumps(payload), event_id)
        )
        conn.commit()

    emit(
        event_type="system.review.updated",
        location="review.queue",
        source="review_api",
        relation_id=row["relation_id"],
        payload={
            "event_id": event_id,
            "event_type": row["event_type"],
            "review_status": review_status,
            "reviewed_by": reviewed_by,
            "review_note": review_note,
        },
        provenance={"method": "update_review_status"},
        created_by=reviewed_by,
    )
    return get_event(event_id)


def tail(limit=10):
    """Print the most recent events for quick command-line verification."""
    for event in poll(limit=limit):
        print(
            f"[{event['time_str']}] {event['source_layer']:>16} -> "
            f"{event['event_type']:<32} @ {event['location']}"
        )


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _migrate(conn)
    conn.executescript(INDEX_SCHEMA)
    conn.commit()
    return conn


def _migrate(conn):
    """Apply lightweight migrations for databases created by older versions."""
    event_columns = _table_columns(conn, "field_events")
    _record_migration(conn, "0001_initial_schema")
    if "relation_id" not in event_columns:
        conn.execute("ALTER TABLE field_events ADD COLUMN relation_id INTEGER")
        _record_migration(conn, "0002_field_events_relation_id")
    _record_migration(conn, "0003_event_envelope_metadata")


def _table_columns(conn, table_name):
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row["name"] for row in rows}


def _record_migration(conn, migration):
    conn.execute(
        "INSERT OR IGNORE INTO lough_migrations (migration, applied_at) VALUES (?, ?)",
        (migration, time.time())
    )


def _event_from_row(row):
    return {
        "id":           row["id"],
        "event_type":   row["event_type"],
        "intensity":    row["intensity"],
        "location":     row["location"],
        "payload":      json.loads(row["payload"]),
        "source_layer": row["source_layer"],
        "timestamp":    row["timestamp"],
        "relation_id":  row["relation_id"],
        "time_str":     datetime.fromtimestamp(row["timestamp"]).strftime("%H:%M:%S"),
    }


def _entity_from_row(row):
    return {
        "id": row["id"],
        "entity_type": row["entity_type"],
        "entity_name": row["entity_name"],
        "metadata": json.loads(row["metadata"]),
        "created_at": row["created_at"],
        "time_str": datetime.fromtimestamp(row["created_at"]).strftime("%H:%M:%S"),
    }


if __name__ == "__main__":
    print("[FIELD] Initializing bridge to modmind.db...")

    # Boot event — the bridge itself coming online
    emit(
        event_type="field.bridge.online",
        intensity=1.0,
        location="system.bridge",
        payload={"version": "1.0", "db": DB_PATH},
        source="field_bridge"
    )

    # Verify we can read it back
    events = poll(event_type="field.bridge.online", limit=1)
    if events:
        print(f"[FIELD] Bridge verified. Last boot: {events[0]['time_str']}")
    else:
        print("[FIELD] WARNING: emit succeeded but poll returned nothing. Check DB path.")

    print("\n[FIELD] Recent event log:")
    tail(5)
