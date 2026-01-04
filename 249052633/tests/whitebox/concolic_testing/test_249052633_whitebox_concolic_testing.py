import unittest
import time

from job_unit_scheduler import JobUnitScheduler


class TestConcolicJobTimeout(unittest.TestCase):
    """
    White-box Testing – Concolic Testing
    User Story #69: Job Timeout Handling
    """

    def test_concolic_job_timeout(self):
        scheduler = JobUnitScheduler()
        job = scheduler.add_job("Job", "ok")

        # Concrete execution: start job with 1-second timeout
        scheduler.start_job(job.id, 1)

        # Concrete delay to satisfy symbolic condition (current_time > start_time + timeout)
        time.sleep(2)

        # Execute function under test
        timed_out = scheduler.check_job_timeouts()

        # Assert symbolic path outcome
        self.assertEqual(len(timed_out), 1)


if __name__ == "__main__":
    unittest.main()
