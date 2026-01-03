import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestUS44PathCoverage(unittest.TestCase):

    def setUp(self):
        self.scheduler = JobUnitScheduler()
        self.scheduler.add_unit(1, ["CPU"])

    def _make_job(self):
        return self.scheduler.add_job(
            "RetryJob", "desc", deadline=datetime.now() + timedelta(days=1)
        )

    def test_path_a_fail_until_permanent_failure(self):

        job = self._make_job()

        for _ in range(job.max_retries):
            msg = self.scheduler.us44_fail_and_retry_job(job.id, error_msg="boom")

            self.assertIn("retry", msg.lower())

        final_msg = self.scheduler.us44_fail_and_retry_job(job.id, error_msg="boom-again")
        self.assertIn("maximum retries", final_msg.lower())

        status = self.scheduler.view_job(job.id).status
        self.assertTrue(status.lower().startswith("failed"))

    def test_path_c_invalid_job_id(self):

        msg = self.scheduler.us44_fail_and_retry_job(999, error_msg="no job")
        self.assertIn("not found", msg.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)


import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestUS50PathCoverage(unittest.TestCase):


    def setUp(self):
        self.scheduler = JobUnitScheduler()

    def _make_job(self, name):
        return self.scheduler.add_job(name, "desc", deadline=datetime.now() + timedelta(days=1))

    def test_path_a_in_progress_timeout_exceeded_cancelled(self):
        timeout = 10

        job = self._make_job("A")
        job.status = "In Progress"
        job.start_time = datetime.now() - timedelta(seconds=timeout + 5)

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 1)
        self.assertTrue(stalled[0].status.startswith("Cancelled"))
        self.assertTrue(job.status.startswith("Cancelled"))

    def test_path_b_in_progress_not_exceeded_not_cancelled(self):
        timeout = 10

        job = self._make_job("B")
        job.status = "In Progress"
        job.start_time = datetime.now() - timedelta(seconds=timeout - 1)

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 0)
        self.assertEqual(job.status, "In Progress")

    def test_path_c_not_in_progress_ignored(self):
        timeout = 10

        job = self._make_job("C")
        job.status = "Done"
        job.start_time = datetime.now() - timedelta(seconds=timeout + 100)

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 0)
        self.assertEqual(job.status, "Done")

    def test_path_d_in_progress_missing_start_time_ignored(self):
        timeout = 10

        job = self._make_job("D")
        job.status = "In Progress"
        job.start_time = None

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 0)
        self.assertEqual(job.status, "In Progress")


if __name__ == "__main__":
    unittest.main(verbosity=2)

