"""Import external lab manifests into datacampus."""

import json
from pathlib import Path

from .runtime import assign_imported_lab, import_lab_manifest


def load_manifest(path):
    """Load a manifest JSON file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def import_manifest_file(path, source_project="Artificial-Criminal"):
    """Import one manifest file."""
    return import_lab_manifest(load_manifest(path), source_project=source_project)


def assign_manifest_file(path, cohort_id, source_project="Artificial-Criminal"):
    """Import one manifest file and assign it to a cohort."""
    return assign_imported_lab(
        cohort_id=cohort_id,
        manifest=load_manifest(path),
        source_project=source_project,
    )
