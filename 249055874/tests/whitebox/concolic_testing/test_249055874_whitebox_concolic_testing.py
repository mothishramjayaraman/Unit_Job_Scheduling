import unittest
import sys
import os
from datetime import datetime, timedelta

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Job


class TestConcolicTesting(unittest.TestCase):


    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.jobs = []

    def test_concolic_timeout_path(self):
        timeout = 300
        elapsed = 400  # concrete value satisfying symbolic condition

        job = Job(
            job_id=1,
            name="Concolic Job",
            description="Timeout concolic test",
            deadline=datetime.now()
        )
        job.status = "In Progress"
        job.start_time = datetime.now() - timedelta(seconds=elapsed)

        self.system.jobs.append(job)

        cancelled = self.system.auto_cancel_stalled_jobs_50(timeout)

        self.assertIn(job, cancelled)
        self.assertEqual(job.status, "Cancelled (Stalled)")


if __name__ == "__main__":
    unittest.main()
