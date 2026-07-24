"""Datacampus data models."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Student:
    student_id: str
    name: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Cohort:
    cohort_id: str
    name: str
    student_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Assignment:
    assignment_id: str
    cohort_id: str
    lab_id: str
    source_project: str
    review_required: bool = True


@dataclass(frozen=True)
class Submission:
    submission_id: str
    assignment_id: str
    student_id: str
    evidence: dict[str, Any]
    sandbox_id: str | None = None


@dataclass(frozen=True)
class Review:
    review_id: str
    submission_id: str
    reviewer: str
    status: str
    notes: str = ""


@dataclass(frozen=True)
class SandboxVault:
    sandbox_id: str
    assignment_id: str
    state: str
    allowed_actions: list[str]
    prohibited_actions: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LabRecord:
    lab_id: str
    source_project: str
    title: str
    domain: str
    review_required: bool
    manifest: dict[str, Any]
