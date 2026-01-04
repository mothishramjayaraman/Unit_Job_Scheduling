import unittest
import sys
import os
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Unit


class TestCategoryPartition(unittest.TestCase):

    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.units = []

    def test_low_load_category(self):

        unit = Unit(unit_id=1, capabilities=["CPU"], max_capacity=10)
        unit.current_load = 3
        self.system.units.append(unit)

        result = self.system.predict_next_slot_47(1)
        self.assertEqual(result["status"], "High Availability")

    def test_high_load_category(self):

        unit = Unit(unit_id=2, capabilities=["CPU"], max_capacity=10)
        unit.current_load = 9
        self.system.units.append(unit)

        result = self.system.predict_next_slot_47(2)
        self.assertEqual(result["status"], "Limited Capacity")


if __name__ == "__main__":
    unittest.main()



import unittest
import sys
import os
from datetime import datetime, timedelta

# ------------------------------------------------------------
# PATH FIX
# ------------------------------------------------------------
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Job


class TestUS50BlackBox(unittest.TestCase):
    """
    Black-box tests for US50: Auto-Cancel Stalled Jobs
    Category Partitioning based on job runtime state
    """

    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.jobs = []

    def test_job_exceeds_timeout_is_cancelled(self):
        job = Job(
            job_id=1,
            name="Stalled Job",
            description="Should be cancelled",
            deadline=datetime.now()
        )
        job.status = "In Progress"
        job.start_time = datetime.now() - timedelta(seconds=400)

        self.system.jobs.append(job)

        cancelled = self.system.auto_cancel_stalled_jobs_50(300)
        self.assertIn(job, cancelled)
        self.assertEqual(job.status, "Cancelled (Stalled)")

    def test_job_within_timeout_not_cancelled(self):
        job = Job(
            job_id=2,
            name="Active Job",
            description="Should continue",
            deadline=datetime.now()
        )
        job.status = "In Progress"
        job.start_time = datetime.now() - timedelta(seconds=100)

        self.system.jobs.append(job)

        cancelled = self.system.auto_cancel_stalled_jobs_50(300)
        self.assertNotIn(job, cancelled)
        self.assertEqual(job.status, "In Progress")


if __name__ == "__main__":
    unittest.main()
