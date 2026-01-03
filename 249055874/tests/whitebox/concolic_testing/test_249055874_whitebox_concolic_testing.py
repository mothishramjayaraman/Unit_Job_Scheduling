import unittest
from job_unit_scheduler import JobUnitScheduler


class TestUS47ConcolicTesting(unittest.TestCase):


    def setUp(self):
        self.scheduler = JobUnitScheduler()
        self.scheduler.add_unit(1, ["CPU", "GPU"])  # max_capacity defaults to 100

    def test_branch_invalid_unit_returns_error(self):

        result = self.scheduler.predict_next_slot_47(999)
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("Error: Unit not found"))

    def test_concolic_hit_all_status_branches(self):

        cases = [
            (0.0, True, "High Availability"),
            (69.9, True, "High Availability"),
            (70.0, True, "Limited Capacity"),
            (99.9, True, "Limited Capacity"),
            (100.0, False, "Unit Full"),
            (120.0, False, "Unit Full"),
        ]

        for load, expected_available, expected_status in cases:
            with self.subTest(current_load=load):
                self.scheduler.units[0].current_load = load
                result = self.scheduler.predict_next_slot_47(1)

                self.assertIsInstance(result, dict)
                self.assertEqual(result["unit_id"], 1)
                self.assertEqual(result["available_now"], expected_available)
                self.assertEqual(result["status"], expected_status)
                self.assertAlmostEqual(result["current_load"], load, places=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
