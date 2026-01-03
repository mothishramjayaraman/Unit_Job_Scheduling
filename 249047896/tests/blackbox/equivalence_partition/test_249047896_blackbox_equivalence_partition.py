import unittest
from job_unit_scheduler import JobUnitScheduler

class TestEquivalencePartition(unittest.TestCase):

    def test_valid_priority_levels(self):
        s = JobUnitScheduler()
        self.assertTrue(s.us6_set_priority_label(2, "Urgent"))
        self.assertTrue(s.us6_set_priority_label(4, "Low"))

    def test_invalid_priority_levels(self):
        s = JobUnitScheduler()
        self.assertFalse(s.us6_set_priority_label(-1, "Bad"))
        self.assertFalse(s.us6_set_priority_label(10, "Bad"))

if __name__ == "__main__":
    unittest.main()
