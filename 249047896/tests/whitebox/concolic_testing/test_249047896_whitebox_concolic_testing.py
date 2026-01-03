import unittest
from job_unit_scheduler import JobUnitScheduler

class TestConcolicStyle(unittest.TestCase):
    def test_concolic_style_us56_remove_unit(self):
        s = JobUnitScheduler()
        s.add_unit(10, ["Legacy"])
        s.add_unit(11, ["Modern"])
        ok1 = s.us56_remove_unit(10)
        self.assertTrue(ok1)
        ok2 = s.us56_remove_unit(10)
        self.assertFalse(ok2)
        ok3 = s.us56_remove_unit(11)
        self.assertTrue(ok3)

    def test_concolic_style_us59_toggle_logging(self):
        s = JobUnitScheduler()
        self.assertFalse(s.us59_toggle_logging(1, True))
        job = s.add_job("J1", "D1", "2025-12-12")
        self.assertEqual(job.id, 1)
        self.assertTrue(s.us59_toggle_logging(1, True))
        self.assertTrue(job.detailed_logging)

if __name__ == "__main__":
    unittest.main()
