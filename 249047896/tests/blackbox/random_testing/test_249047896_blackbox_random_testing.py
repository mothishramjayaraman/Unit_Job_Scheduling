import unittest
import random
from job_unit_scheduler import JobUnitScheduler

class TestRandom(unittest.TestCase):

    def test_random_priority_labels(self):
        s = JobUnitScheduler()
        for _ in range(10):
            level = random.randint(1, 5)
            self.assertTrue(s.us6_set_priority_label(level, "Random"))

if __name__ == "__main__":
    unittest.main()
