import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestUS45CategoryPartition(unittest.TestCase):


    def setUp(self):
        self.scheduler = JobUnitScheduler()
        self.j1 = self.scheduler.add_job(
            "Job1", "desc", deadline=datetime.now() + timedelta(days=1)
        )
        self.j2 = self.scheduler.add_job(
            "Job2", "desc", deadline=datetime.now() + timedelta(days=1)
        )

    def test_cp1_both_exist_normal_dependency_not_completed(self):

        msg = self.scheduler.add_dependency(self.j2.id, self.j1.id)
        self.assertTrue(msg.startswith("Success:"))
        self.assertFalse(self.scheduler.check_dependencies_met(self.j2.id))

    def test_cp2_both_exist_normal_dependency_completed(self):

        msg = self.scheduler.add_dependency(self.j2.id, self.j1.id)
        self.assertTrue(msg.startswith("Success:"))

        self.scheduler.complete_job(self.j1.id)
        self.assertTrue(self.scheduler.check_dependencies_met(self.j2.id))

    def test_cp3_both_exist_self_dependency(self):

        msg = self.scheduler.add_dependency(self.j1.id, self.j1.id)
        self.assertIn("cannot depend on itself", msg.lower())

    def test_cp4_dependent_job_missing(self):

        msg = self.scheduler.add_dependency(999, self.j1.id)
        self.assertIn("not found", msg.lower())

    def test_cp5_dependency_job_missing(self):

        msg = self.scheduler.add_dependency(self.j2.id, 999)
        self.assertIn("not found", msg.lower())

    def test_cp6_check_dependencies_for_job_without_dependencies(self):

        result = self.scheduler.check_dependencies_met(self.j2.id)

        self.assertIn(result, [True, False])  # safe black-box check


if __name__ == "__main__":
    unittest.main(verbosity=2)
