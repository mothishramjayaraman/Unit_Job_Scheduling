import unittest
from job_unit_scheduler import JobUnitScheduler


class TestUS43BranchCoverage(unittest.TestCase):


    def setUp(self):
        self.scheduler = JobUnitScheduler()
        self.scheduler.add_unit(1, ["CPU", "GPU"])

    def test_branch_job_not_found(self):

        result = self.scheduler.us43_validate_and_assign(999, 1)
        self.assertTrue(result.startswith("Error: Job not found."))

    def test_branch_unit_not_found(self):

        job = self.scheduler.add_job(
            "Job1", "desc", deadline=None, required_capacity=10.0, priority=3
        )

        result = self.scheduler.us43_validate_and_assign(job.id, 999)
        self.assertTrue(result.startswith("Error: Unit not found."))

    def test_branch_rejected_insufficient_capacity(self):

        self.scheduler.units[0].current_load = 95.0

        job = self.scheduler.add_job(
            "Job2", "desc", deadline=None, required_capacity=10.0, priority=3
        )

        result = self.scheduler.us43_validate_and_assign(job.id, 1)
        self.assertTrue(result.startswith("Rejected"))
        self.assertNotEqual(self.scheduler.view_job(job.id).status, "In Progress")

    def test_branch_success_sufficient_capacity(self):

        self.scheduler.units[0].current_load = 40.0

        job = self.scheduler.add_job(
            "Job3", "desc", deadline=None, required_capacity=10.0, priority=3
        )

        before_load = self.scheduler.units[0].current_load
        result = self.scheduler.us43_validate_and_assign(job.id, 1)

        self.assertTrue(result.startswith("Success"))
        self.assertEqual(self.scheduler.view_job(job.id).status, "In Progress")
        self.assertIn("Unit 1", self.scheduler.view_job(job.id).units)
        self.assertEqual(
            self.scheduler.units[0].current_load,
            before_load + 10.0
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)


import unittest

from job_unit_scheduler import JobUnitScheduler


class TestUS51BranchCoverage(unittest.TestCase):


    def setUp(self):
        self.scheduler = JobUnitScheduler()
        self.scheduler.add_unit(1, ["CPU", "NVMe"])

        # Create a job with required_capacity and assign it to Unit 1
        self.job = self.scheduler.add_job(
            "UsageJob", "desc", deadline=None, required_capacity=10.0, priority=3
        )
        self.scheduler.us43_validate_and_assign(self.job.id, 1)

    def test_branch_job_not_found(self):

        msg = self.scheduler.job_resource_overconsumption_detection_51(
            job_id=999, actual_usage=5.0
        )

        self.assertIsInstance(msg, str)
        self.assertTrue(msg.lower().startswith("error"))

    def test_branch_normal_usage(self):

        msg = self.scheduler.job_resource_overconsumption_detection_51(
            job_id=self.job.id, actual_usage=10.0
        )

        self.assertTrue(msg.startswith(" Normal:"))
        self.assertFalse(self.scheduler.view_job(self.job.id).status.startswith("FLAGGED"))

    def test_branch_overconsumption_alert(self):

        msg = self.scheduler.job_resource_overconsumption_detection_51(
            job_id=self.job.id, actual_usage=25.0
        )

        self.assertIn("ALERT", msg)
        self.assertTrue(self.scheduler.view_job(self.job.id).status.startswith("FLAGGED"))

        # White-box check: alert should be written to the unit error logs
        logs = self.scheduler.get_unit_error_logs(1)
        self.assertTrue(any("ALERT #51" in line for line in logs))


if __name__ == "__main__":
    unittest.main(verbosity=2)

