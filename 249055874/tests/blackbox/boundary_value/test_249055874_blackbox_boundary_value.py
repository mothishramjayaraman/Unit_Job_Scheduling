import unittest
from job_unit_scheduler import JobUnitScheduler


class TestUS43BoundaryValue(unittest.TestCase):


    def setUp(self):
        self.scheduler = JobUnitScheduler()
        self.scheduler.add_unit(1, ["CPU", "GPU"])

    def test_capacity_exact_boundary_accept(self):


        self.scheduler.units[0].current_load = 70.0

        job = self.scheduler.add_job(
            "JobExact", "desc", deadline=None,
            required_capacity=30.0, priority=3
        )

        result = self.scheduler.us43_validate_and_assign(job.id, 1)

        self.assertTrue(result.startswith("Success"))
        self.assertEqual(self.scheduler.view_job(job.id).status, "In Progress")

    def test_capacity_just_below_boundary_accept(self):
        self.scheduler.units[0].current_load = 70.0

        job = self.scheduler.add_job(
            "JobBelow", "desc", deadline=None,
            required_capacity=29.9, priority=3
        )

        result = self.scheduler.us43_validate_and_assign(job.id, 1)

        self.assertTrue(result.startswith("Success"))

    def test_capacity_just_above_boundary_reject(self):
        self.scheduler.units[0].current_load = 70.0

        job = self.scheduler.add_job(
            "JobAbove", "desc", deadline=None,
            required_capacity=30.1, priority=3
        )

        result = self.scheduler.us43_validate_and_assign(job.id, 1)

        self.assertTrue(result.startswith("Rejected"))



import unittest
from datetime import datetime, timedelta
from job_unit_scheduler import JobUnitScheduler


class TestUS44BoundaryValue(unittest.TestCase):

    def setUp(self):
        self.scheduler = JobUnitScheduler()
        self.scheduler.add_unit(1, ["CPU"])
        self.job = self.scheduler.add_job(
            "RetryJob", "desc", deadline=datetime.now() + timedelta(days=1)
        )

    def test_retry_just_below_max(self):

        for _ in range(self.job.max_retries - 1):
            msg = self.scheduler.us44_fail_and_retry_job(self.job.id)

        self.assertIn("Automatically retrying", msg)

    def test_retry_at_max_boundary(self):

        for _ in range(self.job.max_retries):
            self.scheduler.us44_fail_and_retry_job(self.job.id)

        msg = self.scheduler.us44_fail_and_retry_job(self.job.id)
        self.assertIn("Maximum retries", msg)
        self.assertTrue(
            self.scheduler.view_job(self.job.id).status.startswith("Failed")
        )


import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestUS50BoundaryValue(unittest.TestCase):

    def setUp(self):
        self.scheduler = JobUnitScheduler()
        # Add at least one unit (not strictly required for US50, but keeps system realistic)
        self.scheduler.add_unit(1, ["CPU", "GPU"])

    def _make_in_progress_job(self):
        job = self.scheduler.add_job(
            "StallJob", "desc", deadline=datetime.now() + timedelta(days=1)
        )
        job.status = "In Progress"
        return job

    def test_us50_just_below_timeout_not_cancelled(self):

        timeout = 10

        job = self._make_in_progress_job()
        job.start_time = datetime.now() - timedelta(seconds=timeout - 0.5)

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 0)
        self.assertEqual(job.status, "In Progress")

    def test_us50_exact_timeout_not_cancelled(self):

        timeout = 10

        job = self._make_in_progress_job()
        # "as close as possible" to exact boundary but safe from drifting above
        job.start_time = datetime.now() - timedelta(seconds=timeout - 0.05)

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 0)
        self.assertEqual(job.status, "In Progress")

    def test_us50_just_above_timeout_cancelled(self):

        timeout = 10

        job = self._make_in_progress_job()
        # clearly above timeout
        job.start_time = datetime.now() - timedelta(seconds=timeout + 1.0)

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 1)
        self.assertTrue(stalled[0].status.startswith("Cancelled"))
        self.assertTrue(job.status.startswith("Cancelled"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

    import unittest
    from datetime import datetime, timedelta

    from job_unit_scheduler import JobUnitScheduler
