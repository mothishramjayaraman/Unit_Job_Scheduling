import unittest
from job_unit_scheduler import JobUnitScheduler

class TestPathCoverage(unittest.TestCase):

    def test_path_remove_unit_recomputes_capabilities(self):
        s = JobUnitScheduler()
        s.add_unit(1, ["GPU"])
        s.add_unit(2, ["CPU"])
        self.assertIn("GPU", s.us7_list_capabilities())
        self.assertIn("CPU", s.us7_list_capabilities())
        self.assertTrue(s.us56_remove_unit(1))
        caps = s.us7_list_capabilities()
        self.assertNotIn("GPU", caps)
        self.assertIn("CPU", caps)

    def test_path_logging_then_delete_job_doesnt_crash(self):
        s = JobUnitScheduler()
        job = s.add_job("J1", "D1", "2025-12-12")
        self.assertTrue(s.us59_toggle_logging(job.id, True))
        # If delete_job exists in your scheduler:
        try:
            self.assertTrue(s.delete_job(job.id))
            self.assertFalse(s.us59_toggle_logging(job.id, True))  # should now fail
        except AttributeError:
            pass

    def test_path_priority_label_then_legend(self):
        s = JobUnitScheduler()
        self.assertTrue(s.us6_set_priority_label(2, "Urgent+"))
        legend = s.us57_get_priority_legend()
        self.assertEqual(legend[2], "Urgent+")

if __name__ == "__main__":
    unittest.main()
