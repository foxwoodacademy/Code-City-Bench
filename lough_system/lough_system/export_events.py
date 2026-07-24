"""
export_events.py
Export recent Lough events as JSON Lines for backup and review.
"""

import argparse
import json
import sys

import field_bridge


def main():
    parser = argparse.ArgumentParser(description="Export Lough events as JSON Lines.")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--event-type", default=None)
    parser.add_argument("--source-layer", default=None)
    parser.add_argument("--relation-id", type=int, default=None)
    args = parser.parse_args()

    events = field_bridge.poll(
        event_type=args.event_type,
        source_layer=args.source_layer,
        relation_id=args.relation_id,
        limit=args.limit,
    )
    for event in reversed(events):
        sys.stdout.write(json.dumps(event, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
