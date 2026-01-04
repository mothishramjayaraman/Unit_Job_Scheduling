import unittest
import sys
import os
from datetime import datetime, timedelta

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Unit, Job



class TestBlackBoxBoundaryValue(unittest.TestCase):


    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.units = []
        self.system.jobs = []

    # ---------------- US47: Predict Next Available Unit Slot ----------------

    def test_us47_zero_load_boundary(self):
        unit = Unit(unit_id=1, capabilities=["CPU"], max_capacity=10)
        unit.current_load = 0
        self.system.units.append(unit)

        result = self.system.predict_next_slot_47(1)
        self.assertEqual(result["status"], "High Availability")

    def test_us47_exact_70_percent_boundary(self):
        unit = Unit(unit_id=2, capabilities=["CPU"], max_capacity=10)
        unit.current_load = 7
        self.system.units.append(unit)

        result = self.system.predict_next_slot_47(2)
        self.assertEqual(result["status"], "Limited Capacity")

    def test_us47_full_capacity_boundary(self):
        unit = Unit(unit_id=3, capabilities=["CPU"], max_capacity=10)
        unit.current_load = 10
        self.system.units.append(unit)

        result = self.system.predict_next_slot_47(3)
        self.assertFalse(result["available_now"])
        self.assertEqual(result["status"], "Unit Full")

    def test_us47_invalid_unit(self):
        result = self.system.predict_next_slot_47(999)
        self.assertIn("Error", result)

    # ---------------- US50: Auto-Cancel Stalled Jobs ----------------

    def test_us50_just_over_timeout_boundary(self):
        job = Job(
            job_id=1,
            name="Test Job",
            description="Timeout test",
            deadline=datetime.now() + timedelta(days=1),
            priority=3
        )

        job.status = "In Progress"
        job.start_time = datetime.now() - timedelta(seconds=301)

        self.system.jobs.append(job)

        cancelled = self.system.auto_cancel_stalled_jobs_50(300)
        self.assertIn(job, cancelled)
        self.assertEqual(job.status, "Cancelled (Stalled)")


if __name__ == "__main__":
    unittest.main()
