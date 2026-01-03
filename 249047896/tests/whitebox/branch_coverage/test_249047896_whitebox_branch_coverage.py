import unittest
from job_unit_scheduler import JobUnitScheduler

class TestBranchCoverage(unittest.TestCase):
    def test_us58_branches_priority_label(self):
        s = JobUnitScheduler()
        self.assertTrue(s.us6_set_priority_label(1, "Emergency"))  # valid branch
        self.assertFalse(s.us6_set_priority_label(6, "Invalid"))   # invalid branch

    def test_us60_branches_default_deadline(self):
        s = JobUnitScheduler()
        self.assertTrue(s.us60_set_default_deadline(24))   # hours > 0 branch
        self.assertFalse(s.us60_set_default_deadline(0))   # else branch
        self.assertFalse(s.us60_set_default_deadline(-5))  # else branch

    def test_us59_branches_toggle_logging(self):
        s = JobUnitScheduler()
        job = s.add_job("J1", "D1", "2025-12-12")
        self.assertTrue(s.us59_toggle_logging(job.id, True))  # job exists branch
        self.assertTrue(job.detailed_logging)

        self.assertFalse(s.us59_toggle_logging(9999, False))  # job not found branch

    def test_us56_branches_remove_unit(self):
        s = JobUnitScheduler()
        s.add_unit(1, ["GPU"])
        self.assertTrue(s.us56_remove_unit(1))     # found branch
        self.assertFalse(s.us56_remove_unit(1))    # not found branch (already removed)

    def test_us55_us61_unit_history_branches(self):
        s = JobUnitScheduler()
        s.add_unit(1, ["CPU"])
        s.units[0].historical_loads = [1.0, 2.0]
        self.assertEqual(s.us4_view_unit_history(1), [1.0, 2.0])
        self.assertEqual(s.us4_view_unit_history(999), [])
        self.assertTrue(s.us61_reset_unit_history(1))
        self.assertFalse(s.us61_reset_unit_history(999))

if __name__ == "__main__":
    unittest.main()
