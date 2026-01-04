import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestSymbolicPriorityPaths(unittest.TestCase):
    """
    White-box Testing – Symbolic Execution
    User Story #19: Priority Escalation Based on Deadlines
    """

    def test_symbolic_priority_paths(self):
        scheduler = JobUnitScheduler()

        j1 = scheduler.add_job(
            "J1",
            "ok",
            datetime.now() + timedelta(hours=10)
        )

        j2 = scheduler.add_job(
            "J2",
            "ok",
            datetime.now() + timedelta(hours=40)
        )

        j3 = scheduler.add_job(
            "J3",
            "ok",
            datetime.now() + timedelta(days=4)
        )

        scheduler.us19_auto_escalate_job_priority()

        # Symbolic path: deadline < 24 hours
        self.assertEqual(j1.priority, 1)

        # Symbolic path: 24 ≤ deadline < 48 hours
        self.assertEqual(j2.priority, 2)

        # Symbolic path: deadline ≥ 48 hours
        self.assertEqual(j3.priority, 5)


if __name__ == "__main__":
    unittest.main()
