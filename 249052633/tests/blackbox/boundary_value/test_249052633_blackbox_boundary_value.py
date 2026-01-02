import unittest
from job_unit_scheduler import JobUnitScheduler


class TestBoundaryValueDescription(unittest.TestCase):
    """Black-box: Boundary Value Testing for Job Description Length"""

    def test_description_length_at_upper_boundary(self):
        scheduler = JobUnitScheduler()

        desc_100 = "a" * 100        # upper valid boundary
        desc_101 = "a" * 101        # just above boundary

        self.assertIsNotNone(scheduler.add_job("Job1", desc_100))
        self.assertEqual(
            scheduler.add_job("Job2", desc_101),
            "Description too long! Try to add fewer than 100 characters"
        )


class TestUS42RetryLimit(unittest.TestCase):
    """Black-box: Boundary Value Testing for Job Retry Limit"""

    def test_us42_retry_limit_boundary(self):
        scheduler = JobUnitScheduler()
        job = scheduler.add_job("RetryJob", "ok")

        r1 = scheduler.mark_job_failed(job.id, "err1")
        r2 = scheduler.mark_job_failed(job.id, "err2")
        r3 = scheduler.mark_job_failed(job.id, "err3")

        self.assertIn("retrying", r1.lower())
        self.assertIn("retrying", r2.lower())
        self.assertIn("failed_permanently", r3.lower())

#
# if __name__ == "__main__":
#     unittest.main()
