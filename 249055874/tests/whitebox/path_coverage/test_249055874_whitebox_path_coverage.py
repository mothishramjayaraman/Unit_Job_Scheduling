import unittest
import sys
import os

# ------------------------------------------------------------
# PATH FIX (points to folder containing job_unit_scheduler.py)
# ------------------------------------------------------------
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

# ------------------------------------------------------------
# IMPORT SYSTEM UNDER TEST
# ------------------------------------------------------------
from job_unit_scheduler import JobUnitScheduler, Unit


class TestPathCoverage(unittest.TestCase):
    """
    White-box Path Coverage
    User Story: US47
    """

    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.units = []

    def test_all_execution_paths(self):
        """
        Executes all logical paths of predict_next_slot_47:
        - High Availability
        - Limited Capacity
        - Unit Full
        """
        test_loads = [0, 7, 9, 10]

        for i, load in enumerate(test_loads):
            unit = Unit(
                unit_id=i,
                capabilities=["CPU"],
                max_capacity=10
            )
            unit.current_load = load
            self.system.units.append(unit)

            result = self.system.predict_next_slot_47(i)
            self.assertIn(
                result["status"],
                ["High Availability", "Limited Capacity", "Unit Full"]
            )


if __name__ == "__main__":
    unittest.main()
