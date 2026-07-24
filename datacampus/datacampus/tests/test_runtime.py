import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from datacampus import importers, runtime, store


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.old_store = store.DEFAULT_STORE
        store.DEFAULT_STORE = self.tmp.name

    def tearDown(self):
        store.DEFAULT_STORE = self.old_store
        try:
            os.unlink(self.tmp.name)
        except FileNotFoundError:
            pass

    def test_create_student_and_cohort(self):
        student = runtime.create_student("Pilot Student")
        cohort = runtime.create_cohort("Pilot Cohort", [student.student_id])
        self.assertTrue(student.student_id.startswith("student_"))
        self.assertEqual(cohort.student_ids, [student.student_id])

    def test_assignment_sandbox_submission_review(self):
        student = runtime.create_student("Pilot Student")
        cohort = runtime.create_cohort("Pilot Cohort", [student.student_id])
        assignment = runtime.create_assignment(cohort.cohort_id, "prompt_injection_basics")
        sandbox = runtime.create_sandbox_vault(assignment.assignment_id)
        transition = runtime.transition_sandbox(sandbox.sandbox_id, "active", "student started lab")
        submission = runtime.submit_evidence(
            assignment.assignment_id,
            student.student_id,
            {"defense_mapping": "complete"},
            sandbox_id=sandbox.sandbox_id,
        )
        review = runtime.review_submission(
            submission.submission_id,
            reviewer="instructor",
            status="needs_context",
            notes="missing source labels",
        )

        self.assertEqual(transition["state"], "active")
        self.assertEqual(submission.sandbox_id, sandbox.sandbox_id)
        self.assertEqual(review.status, "needs_context")

    def test_import_and_assign_manifest(self):
        cohort = runtime.create_cohort("Pilot Cohort")
        manifest_path = os.path.join(
            os.path.dirname(ROOT),
            "Artificial-Criminal",
            "labs",
            "prompt_injection_basics.json",
        )

        result = importers.assign_manifest_file(manifest_path, cohort.cohort_id)
        self.assertEqual(result["lab"].lab_id, "prompt_injection_basics")
        self.assertEqual(result["assignment"].cohort_id, cohort.cohort_id)
        self.assertTrue(result["assignment"].review_required)


if __name__ == "__main__":
    unittest.main()
