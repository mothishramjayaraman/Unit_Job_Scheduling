import unittest
import sys
import os
import random

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Unit


class TestRandomTesting(unittest.TestCase):

    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.units = []

    def test_random_unit_loads(self):

        for i in range(5):
            load = random.randint(0, 10)

            unit = Unit(
                unit_id=i,
                capabilities=["CPU"],
                max_capacity=10
            )
            unit.current_load = load
            self.system.units.append(unit)

            result = self.system.predict_next_slot_47(i)

            # Invariants (must always hold)
            self.assertGreaterEqual(result["current_load"], 0)
            self.assertLessEqual(result["current_load"], 100)
            self.assertIn(
                result["status"],
                ["High Availability", "Limited Capacity", "Unit Full"]
            )


if __name__ == "__main__":
    unittest.main()
