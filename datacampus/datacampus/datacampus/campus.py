"""Datacampus command-line interface."""

import argparse
import json
from dataclasses import asdict, is_dataclass

from .importers import assign_manifest_file, import_manifest_file
from .runtime import create_cohort, create_student, initialize_campus
from .store import read_records


def _print(value):
    if is_dataclass(value):
        value = asdict(value)
    print(json.dumps(value, indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description="Datacampus CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init")

    student_parser = subparsers.add_parser("create-student")
    student_parser.add_argument("--name", required=True)

    cohort_parser = subparsers.add_parser("create-cohort")
    cohort_parser.add_argument("--name", required=True)

    import_parser = subparsers.add_parser("import-manifest")
    import_parser.add_argument("path")
    import_parser.add_argument("--source-project", default="Artificial-Criminal")

    assign_parser = subparsers.add_parser("assign-manifest")
    assign_parser.add_argument("path")
    assign_parser.add_argument("--cohort-id", required=True)
    assign_parser.add_argument("--source-project", default="Artificial-Criminal")

    subparsers.add_parser("list-records")
    args = parser.parse_args()

    if args.command == "init":
        _print(initialize_campus())
    elif args.command == "create-student":
        _print(create_student(args.name))
    elif args.command == "create-cohort":
        _print(create_cohort(args.name))
    elif args.command == "import-manifest":
        _print(import_manifest_file(args.path, source_project=args.source_project))
    elif args.command == "assign-manifest":
        _print(assign_manifest_file(
            args.path,
            cohort_id=args.cohort_id,
            source_project=args.source_project,
        ))
    elif args.command == "list-records":
        _print(read_records())


if __name__ == "__main__":
    main()
