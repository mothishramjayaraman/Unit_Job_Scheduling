# test_specification.py
# Black-Box (Specification-Based) Testing
# Techniques: Equivalence Partitioning (EP) + Boundary Value Analysis (BVA)

import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestSpecificationBasedBlackBox(unittest.TestCase):

    def setUp(self):
        self.scheduler = JobUnitScheduler()

    def _add_job_safe(self, **kwargs):

        try:
            result = self.scheduler.add_job(**kwargs)
            if isinstance(result, str):
                return None, result
            return result, None
        except Exception as e:
            return None, str(e)

    def _assert_error_contains(self, error_msg, expected):
        self.assertIsNotNone(error_msg, "Expected an error message but got None.")
        self.assertIn(expected, error_msg)


    def test_add_job_valid_equivalence_partition(self):

        job, err = self._add_job_safe(
            name="Job A",
            description="Short description",
            deadline=None
        )
        self.assertIsNone(err)
        self.assertIsNotNone(job)

        if hasattr(job, "name"):
            self.assertEqual(job.name, "Job A")

    def test_add_job_empty_name_is_accepted_in_current_spec(self):

        job, err = self._add_job_safe(
            name="",
            description="Desc",
            deadline=None
        )
        self.assertIsNone(err)
        self.assertIsNotNone(job)

    def test_add_job_invalid_description_too_long_partition(self):

        long_desc = "x" * 101
        job, err = self._add_job_safe(
            name="Job B",
            description=long_desc,
            deadline=None
        )
        self.assertIsNone(job)
        self._assert_error_contains(err, "Description too long")


    def test_add_job_boundary_description_exact_100(self):

        desc_100 = "x" * 100
        job, err = self._add_job_safe(
            name="Job C",
            description=desc_100,
            deadline=None
        )
        self.assertIsNone(err)
        self.assertIsNotNone(job)


    def test_view_job_boundary_zero_id(self):

        self.assertIsNone(self.scheduler.view_job(0))

    def test_view_job_boundary_negative_id(self):

        self.assertIsNone(self.scheduler.view_job(-1))

    def test_view_job_valid_existing_id(self):

        job, err = self._add_job_safe(
            name="Job D",
            description="Desc",
            deadline=None
        )
        self.assertIsNone(err)
        self.assertIsNotNone(job)
        self.assertTrue(hasattr(job, "id"))

        fetched = self.scheduler.view_job(job.id)
        self.assertIsNotNone(fetched)
        if hasattr(fetched, "id"):
            self.assertEqual(fetched.id, job.id)

    def test_view_job_invalid_nonexistent_id_partition(self):

        self.assertIsNone(self.scheduler.view_job(999999))


    def test_add_jobtag_valid_tag_equivalence_partition(self):

        job, err = self._add_job_safe(
            name="Job E",
            description="Desc",
            deadline=None
        )
        self.assertIsNone(err)
        self.assertIsNotNone(job)

        result = self.scheduler.add_jobtag(job.id, "system")
        self.assertIsInstance(result, str)
        self.assertIn("system", result.lower())
        self.assertTrue("add" in result.lower() or "success" in result.lower())

    def test_add_jobtag_invalid_tag_equivalence_partition(self):

        job, err = self._add_job_safe(
            name="Job F",
            description="Desc",
            deadline=None
        )
        self.assertIsNone(err)
        self.assertIsNotNone(job)

        result = self.scheduler.add_jobtag(job.id, "not_a_valid_tag")
        self.assertIsInstance(result, str)
        self.assertIn("wrong tag", result.lower())

    def test_add_jobtag_duplicate_tag(self):

        job, err = self._add_job_safe(
            name="Job G",
            description="Desc",
            deadline=None
        )
        self.assertIsNone(err)
        self.assertIsNotNone(job)

        self.scheduler.add_jobtag(job.id, "system")
        result = self.scheduler.add_jobtag(job.id, "system")
        self.assertIsInstance(result, str)
        self.assertIn("already", result.lower())


    def test_add_job_deadline_none_uses_default_if_supported(self):

        job, err = self._add_job_safe(
            name="Job H",
            description="Desc",
            deadline=None
        )
        self.assertIsNone(err)
        self.assertIsNotNone(job)

        if hasattr(job, "deadline") and hasattr(self.scheduler, "default_deadline_hours"):
            now = datetime.now()
            expected = now + timedelta(hours=self.scheduler.default_deadline_hours)
            self.assertTrue(
                abs((job.deadline - expected).total_seconds()) < 7200
            )


if __name__ == "_main_":
    unittest.main(verbosity=2)