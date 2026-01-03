import unittest
from job_unit_scheduler import JobUnitScheduler

class TestBoundaryValueUS58(unittest.TestCase):

    def test_priority_label_lower_boundary(self):
        s = JobUnitScheduler()
        self.assertTrue(s.us6_set_priority_label(1, "Emergency"))
        self.assertFalse(s.us6_set_priority_label(0, "Invalid"))

    def test_priority_label_upper_boundary(self):
        s = JobUnitScheduler()
        self.assertTrue(s.us6_set_priority_label(5, "Back"))
        self.assertFalse(s.us6_set_priority_label(6, "Invalid"))


class TestBoundaryValueUS60(unittest.TestCase):

    def test_default_deadline_zero_invalid(self):
        s = JobUnitScheduler()
        self.assertFalse(s.us60_set_default_deadline(0))


if __name__ == "__main__":
    unittest.main()
