import unittest
from job_unit_scheduler import JobUnitScheduler

class TestSymbolicExecutionStyle(unittest.TestCase):
    def test_symbolic_like_inputs_us60(self):
        s = JobUnitScheduler()
        # inputs chosen to satisfy / violate the condition hours > 0
        for hours, expected in [(1, True), (48, True), (0, False), (-1, False)]:
            with self.subTest(hours=hours):
                ok = s.us60_set_default_deadline(hours)
                self.assertEqual(ok, expected)

    def test_symbolic_like_inputs_us58(self):
        s = JobUnitScheduler()
        # inputs chosen around boundary of valid range 1..5
        for level, expected in [(1, True), (5, True), (0, False), (6, False)]:
            with self.subTest(level=level):
                ok = s.us6_set_priority_label(level, "X")
                self.assertEqual(ok, expected)

if __name__ == "__main__":
    unittest.main()
