import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestUS50SymbolicExecution(unittest.TestCase):


    def setUp(self):
        self.scheduler = JobUnitScheduler()

    def _make_job(self, name="J"):
        return self.scheduler.add_job(
            name, "desc", deadline=datetime.now() + timedelta(days=1)
        )

    def test_constraints_all_true_job_cancelled(self):

        timeout = 10
        job = self._make_job("AllTrue")
        job.status = "In Progress"
        job.start_time = datetime.now() - timedelta(seconds=timeout + 5)

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 1)
        self.assertTrue(job.status.startswith("Cancelled"))

    def test_constraint_status_false_not_cancelled(self):

        timeout = 10
        job = self._make_job("StatusFalse")
        job.status = "Done"
        job.start_time = datetime.now() - timedelta(seconds=timeout + 100)

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 0)
        self.assertEqual(job.status, "Done")

    def test_constraint_start_time_none_not_cancelled(self):

        timeout = 10
        job = self._make_job("NoStartTime")
        job.status = "In Progress"
        job.start_time = None

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 0)
        self.assertEqual(job.status, "In Progress")

    def test_constraint_elapsed_not_greater_not_cancelled(self):

        timeout = 10
        job = self._make_job("ElapsedNotGreater")
        job.status = "In Progress"
        job.start_time = datetime.now() - timedelta(seconds=timeout - 0.2)

        stalled = self.scheduler.auto_cancel_stalled_jobs_50(timeout_seconds=timeout)

        self.assertEqual(len(stalled), 0)
        self.assertEqual(job.status, "In Progress")


if __name__ == "__main__":
    unittest.main(verbosity=2)
