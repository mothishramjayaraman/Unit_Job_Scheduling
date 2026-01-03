import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestUS45EquivalencePartition(unittest.TestCase):

    def setUp(self):
        self.scheduler = JobUnitScheduler()
        self.j1 = self.scheduler.add_job(
            "Job1", "desc", deadline=datetime.now() + timedelta(days=1)
        )
        self.j2 = self.scheduler.add_job(
            "Job2", "desc", deadline=datetime.now() + timedelta(days=1)
        )

    def test_ep1_add_valid_dependency_success(self):

        msg = self.scheduler.add_dependency(self.j2.id, self.j1.id)
        self.assertTrue(msg.startswith("Success:"))

    def test_ep2_dependency_not_completed_dependencies_not_met(self):

        self.scheduler.add_dependency(self.j2.id, self.j1.id)
        self.assertFalse(self.scheduler.check_dependencies_met(self.j2.id))



    def test_ep3_self_dependency_error(self):

        msg = self.scheduler.add_dependency(self.j1.id, self.j1.id)
        self.assertIn("cannot depend on itself", msg)

    def test_ep4_job_not_found_error(self):

        msg = self.scheduler.add_dependency(999, self.j1.id)
        self.assertIn("not found", msg)


if __name__ == "__main__":
    unittest.main(verbosity=2)



import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestUS46EquivalencePartition(unittest.TestCase):


    def setUp(self):
            self.scheduler = JobUnitScheduler()
            self.scheduler.add_unit(1, ["CPU", "GPU"])
            self.scheduler.add_unit(2, ["CPU"])

    def test_ep1_valid_unit_no_logs_returns_empty_list(self):

            logs = self.scheduler.get_unit_error_logs(1)
            self.assertEqual(logs, [])



    def test_ep2_valid_unit_with_logs_returns_list_with_error(self):

        job = self.scheduler.add_job(
            "JobErr", "desc", deadline=None, required_capacity=10.0, priority=3
        )

        self.scheduler.us43_validate_and_assign(job.id, 1)
        self.scheduler.us44_fail_and_retry_job(job.id, error_msg="Boom")

        logs = self.scheduler.get_unit_error_logs(1)

        self.assertIsInstance(logs, list)
        self.assertTrue(any("Boom" in line for line in logs))


if __name__ == "__main__":
        unittest.main(verbosity=2)

