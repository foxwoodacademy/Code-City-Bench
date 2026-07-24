"""Datacampus runtime operations."""

from .ids import make_id
from .models import Assignment, Cohort, LabRecord, Review, SandboxVault, Student, Submission
from .store import append_record, read_records

PROHIBITED_ACTIONS = [
    "real_world_targeting",
    "unauthorized_scanning",
    "credential_theft",
    "malware",
    "persistence",
    "exfiltration",
]


def initialize_campus():
    """Create an initialization record."""
    return append_record("campus.initialized", {"status": "ready"})


def create_student(name, metadata=None):
    """Create a student record."""
    student = Student(
        student_id=make_id("student", name),
        name=name,
        metadata=metadata or {},
    )
    append_record("student.created", student)
    return student


def create_cohort(name, student_ids=None, metadata=None):
    """Create a cohort record."""
    cohort = Cohort(
        cohort_id=make_id("cohort", name),
        name=name,
        student_ids=student_ids or [],
        metadata=metadata or {},
    )
    append_record("cohort.created", cohort)
    return cohort


def create_assignment(cohort_id, lab_id, source_project="Artificial-Criminal", review_required=True):
    """Create a lab assignment."""
    assignment = Assignment(
        assignment_id=make_id("assignment", cohort_id, lab_id),
        cohort_id=cohort_id,
        lab_id=lab_id,
        source_project=source_project,
        review_required=review_required,
    )
    append_record("assignment.created", assignment)
    return assignment


def import_lab_manifest(manifest, source_project="Artificial-Criminal"):
    """Import a lab manifest into datacampus curriculum records."""
    lab_id = manifest["lab_id"]
    boundary = manifest.get("safety_boundary", {})
    review_required = bool(boundary.get("review_required"))
    lab = LabRecord(
        lab_id=lab_id,
        source_project=source_project,
        title=manifest.get("title", lab_id),
        domain=manifest.get("domain", "unknown"),
        review_required=review_required,
        manifest=manifest,
    )
    append_record("lab.imported", lab)
    return lab


def assign_imported_lab(cohort_id, manifest, source_project="Artificial-Criminal"):
    """Import a manifest and create an assignment for a cohort."""
    lab = import_lab_manifest(manifest, source_project=source_project)
    assignment = create_assignment(
        cohort_id=cohort_id,
        lab_id=lab.lab_id,
        source_project=source_project,
        review_required=lab.review_required,
    )
    return {
        "lab": lab,
        "assignment": assignment,
    }


def create_sandbox_vault(assignment_id, allowed_actions=None, metadata=None):
    """Create a sandbox holding tank record."""
    vault = SandboxVault(
        sandbox_id=make_id("sandbox", assignment_id),
        assignment_id=assignment_id,
        state="created",
        allowed_actions=allowed_actions or ["fixture_read", "mock_simulation", "evidence_submit"],
        prohibited_actions=PROHIBITED_ACTIONS,
        metadata=metadata or {},
    )
    append_record("sandbox.created", vault)
    return vault


def transition_sandbox(sandbox_id, state, reason):
    """Record a sandbox lifecycle transition."""
    record = {
        "sandbox_id": sandbox_id,
        "state": state,
        "reason": reason,
    }
    append_record("sandbox.transitioned", record)
    return record


def submit_evidence(assignment_id, student_id, evidence, sandbox_id=None):
    """Record a student submission."""
    submission = Submission(
        submission_id=make_id("submission", assignment_id, student_id, len(read_records())),
        assignment_id=assignment_id,
        student_id=student_id,
        evidence=evidence,
        sandbox_id=sandbox_id,
    )
    append_record("submission.created", submission)
    return submission


def review_submission(submission_id, reviewer, status, notes=""):
    """Record an instructor review."""
    review = Review(
        review_id=make_id("review", submission_id, reviewer, status),
        submission_id=submission_id,
        reviewer=reviewer,
        status=status,
        notes=notes,
    )
    append_record("review.created", review)
    return review
