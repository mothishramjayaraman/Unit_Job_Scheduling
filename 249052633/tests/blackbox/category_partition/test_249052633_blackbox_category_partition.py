import unittest
from job_unit_scheduler import JobUnitScheduler


class TestJobHandlingCategories(unittest.TestCase):
    """
    Black-box Testing – Category Partition
    User Story #69: Automatic Job Handling
    """

    def test_job_handling_categories(self):
        scheduler = JobUnitScheduler()
        job = scheduler.add_job("Job", "ok")

        # Category 1: job not running
        result1 = scheduler.start_job(job.id, 5)
        self.assertIn("started", result1.lower())

        # Category 2: job already running
        result2 = scheduler.start_job(job.id, 5)
        self.assertIn("already running", result2.lower())


class TestUS14PreemptionCategories(unittest.TestCase):
    """
    Black-box Testing – Category Partition
    User Story #14: Job Preemption Rules
    """

    def test_us14_preemption_categories(self):
        scheduler = JobUnitScheduler()

        low = scheduler.add_job("Low", "ok", priority=5)
        high = scheduler.add_job("High", "ok", priority=1)

        # Category 1: no running job
        result1 = scheduler.schedule_job(low.id)
        self.assertIn("started", result1.lower())

        # Category 2: preemption occurs
        result2 = scheduler.schedule_job(high.id)
        self.assertIn("preempted", result2.lower())


if __name__ == "__main__":
    unittest.main()
