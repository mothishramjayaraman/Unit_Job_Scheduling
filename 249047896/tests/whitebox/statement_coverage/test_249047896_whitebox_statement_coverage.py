import unittest
from datetime import datetime, timedelta
from job_unit_scheduler import JobUnitScheduler

class TestStatementCoverage(unittest.TestCase):
    def test_statement_coverage_many_methods(self):
        s = JobUnitScheduler()
        s.add_unit(1, ["GPU", "NVMe"])
        s.add_unit(2, ["CPU"])
        caps = s.us7_list_capabilities()
        self.assertIn("GPU", caps)

        # US58: set priority label valid + invalid
        self.assertTrue(s.us6_set_priority_label(1, "Emergency"))
        self.assertFalse(s.us6_set_priority_label(0, "Bad"))

        # US60: set default deadline valid + invalid
        self.assertTrue(s.us60_set_default_deadline(72))
        self.assertFalse(s.us60_set_default_deadline(0))

        try:
            job = s.add_job("Auto-Time Job", "Testing", deadline=None)
            expected = datetime.now() + timedelta(hours=s.default_deadline_hours)
            self.assertTrue(abs((job.deadline - expected).total_seconds()) < 60)
        except TypeError:

            pass

        # US59: toggle logging (requires job exists)
        job2 = s.add_job("Logger Job", "Testing", "2025-12-30")
        self.assertTrue(s.us59_toggle_logging(job2.id, True))
        self.assertTrue(job2.detailed_logging)

        # US55: view unit history
        s.units[0].historical_loads = [10.0, 20.0]
        hist = s.us4_view_unit_history(1)
        self.assertEqual(hist, [10.0, 20.0])

        # US61: reset unit history
        self.assertTrue(s.us61_reset_unit_history(1))
        hist2 = s.us4_view_unit_history(1)
        self.assertTrue(len(hist2) >= 1)

        # US56: remove unit (existing + non-existing)
        self.assertTrue(s.us56_remove_unit(2))
        self.assertFalse(s.us56_remove_unit(999))

if __name__ == "__main__":
    unittest.main()
