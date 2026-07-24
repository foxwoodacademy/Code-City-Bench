"""
CSV ingest adapter for Phase 2.

Each CSV row becomes one domain event. The adapter is intentionally small:
it works offline, supports dry runs, and records provenance for every row.
"""

import argparse
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import domain_bridge
import event_registry
import field_bridge


def _coerce_value(value):
    if value is None:
        return None
    text = value.strip()
    if text == "":
        return ""
    for caster in (int, float):
        try:
            return caster(text)
        except ValueError:
            pass
    lowered = text.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return text


def ingest_csv(
    path,
    domain,
    event_key,
    source="csv_ingest",
    location="csv.import",
    relation_id=None,
    dry_run=False,
    created_by=None,
):
    """Import a CSV file into a registered Lough domain."""
    if domain not in event_registry.all_namespaces():
        raise ValueError(f"Unknown domain: {domain}")
    if event_key not in event_registry.get_domain_events(domain):
        raise ValueError(f"Unknown event key for {domain}: {event_key}")

    emitted = 0
    preview = []
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV file must include a header row")

        for row_number, row in enumerate(reader, start=2):
            payload = {
                key: _coerce_value(value)
                for key, value in row.items()
            }
            provenance = {
                "adapter": "csv_ingest",
                "path": path,
                "row_number": row_number,
                "fieldnames": list(reader.fieldnames),
            }
            if dry_run:
                preview.append({
                    "domain": domain,
                    "event_key": event_key,
                    "location": location,
                    "source": source,
                    "relation_id": relation_id,
                    "payload": payload,
                    "provenance": provenance,
                })
                continue

            domain_bridge.emit_domain_event(
                domain=domain,
                event_key=event_key,
                location=location,
                source=source,
                payload=payload,
                relation_id=relation_id,
                provenance=provenance,
                created_by=created_by or source,
            )
            emitted += 1

    if not dry_run:
        field_bridge.emit(
            event_type=event_registry.SYSTEM_NAMESPACE["ingest"],
            location=location,
            source=source,
            relation_id=relation_id,
            payload={
                "adapter": "csv_ingest",
                "path": path,
                "domain": domain,
                "event_key": event_key,
                "rows_emitted": emitted,
            },
            provenance={"adapter": "csv_ingest", "path": path},
            created_by=created_by or source,
        )

    return {
        "dry_run": dry_run,
        "rows": len(preview) if dry_run else emitted,
        "preview": preview,
    }


def main():
    parser = argparse.ArgumentParser(description="Import CSV rows as Lough domain events.")
    parser.add_argument("path")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--event-key", required=True)
    parser.add_argument("--source", default="csv_ingest")
    parser.add_argument("--location", default="csv.import")
    parser.add_argument("--relation-id", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result = ingest_csv(
        path=args.path,
        domain=args.domain,
        event_key=args.event_key,
        source=args.source,
        location=args.location,
        relation_id=args.relation_id,
        dry_run=args.dry_run,
    )
    print(result)


if __name__ == "__main__":
    main()
