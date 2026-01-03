import unittest
from job_unit_scheduler import JobUnitScheduler

class TestCategoryPartition(unittest.TestCase):

    def test_remove_existing_unit(self):
        s = JobUnitScheduler()
        s.add_unit(1, ["GPU"])
        self.assertTrue(s.us56_remove_unit(1))

    def test_remove_non_existing_unit(self):
        s = JobUnitScheduler()
        self.assertFalse(s.us56_remove_unit(99))

if __name__ == "__main__":
    unittest.main()
