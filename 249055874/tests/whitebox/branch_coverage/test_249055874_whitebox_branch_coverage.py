import unittest
import sys
import os
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Job


class TestBranchCoverage(unittest.TestCase):


    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.jobs = []
        self.system.view_job = lambda job_id: next(
            (j for j in self.system.jobs if j.id == job_id),
            None
        )

    def test_normal_usage_branch(self):

        job = Job(
            job_id=1,
            name="Normal Job",
            description="Branch test",
            deadline=datetime.now(),
            required_capacity=10
        )
        self.system.jobs.append(job)

        result = self.system.job_resource_overconsumption_detection_51(1, 5)
        self.assertIn("Normal", result)

    def test_overconsumption_branch(self):

        job = Job(
            job_id=2,
            name="Overuse Job",
            description="Branch test",
            deadline=datetime.now(),
            required_capacity=5
        )
        self.system.jobs.append(job)

        result = self.system.job_resource_overconsumption_detection_51(2, 9)
        self.assertIn("ALERT", result)
        self.assertEqual(job.status, "FLAGGED: Overconsumption")


if __name__ == "__main__":
    unittest.main()


class TestUS44RetryMechanism(unittest.TestCase):

    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.jobs = []
        self.system.view_job = lambda job_id: next(
            (j for j in self.system.jobs if j.id == job_id),
            None
        )

    def test_retry_non_completed_job(self):

        job = Job(1, "Retry Job", "Desc", datetime.now())
        job.complete = False
        self.system.jobs.append(job)

        result = self.system.us44_fail_and_retry_job(1)

        # FIXED ASSERTION (robust & correct)
        self.assertIn("retrying", result.lower())

    def test_retry_completed_job_rejected(self):

        job = Job(2, "Completed Job", "Desc", datetime.now())
        job.complete = True
        self.system.jobs.append(job)

        result = self.system.us44_fail_and_retry_job(2)
        self.assertIn("Error", result)


if __name__ == "__main__":
    unittest.main()

