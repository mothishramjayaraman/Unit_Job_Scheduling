import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Unit


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.units = []

    def test_symbolic_low_load_condition(self):

        x = 6

        unit = Unit(
            unit_id=1,
            capabilities=["CPU"],
            max_capacity=10
        )
        unit.current_load = x
        self.system.units.append(unit)

        result = self.system.predict_next_slot_47(1)
        self.assertEqual(result["status"], "High Availability")


if __name__ == "__main__":
    unittest.main()
