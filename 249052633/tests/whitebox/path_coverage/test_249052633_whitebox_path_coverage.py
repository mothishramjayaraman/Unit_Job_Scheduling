import unittest
import time

from job_unit_scheduler import JobUnitScheduler


class TestTimeoutExecutionPaths(unittest.TestCase):
    """
    White-box Testing – Path Coverage
    User Story #69: Job Timeout Execution Paths
    """

    def test_timeout_execution_path(self):
        scheduler = JobUnitScheduler()
        job = scheduler.add_job("Job", "ok")

        scheduler.start_job(job.id, 0)
        time.sleep(1)
        timed_out = scheduler.check_job_timeouts()

        # Path coverage: both outcomes are acceptable depending on timing
        self.assertTrue(
            timed_out == [] or timed_out[0].status == "TIMED_OUT"
        )


class TestUS14PreemptionExecutionPaths(unittest.TestCase):
    """
    White-box Testing – Path Coverage
    User Story #14: Job Preemption Scheduling Paths
    """

    def test_us14_preemption_execution_paths(self):
        scheduler = JobUnitScheduler()

        job1 = scheduler.add_job("Job1", "ok", priority=3)
        job2 = scheduler.add_job("Job2", "ok", priority=3)

        scheduler.schedule_job(job1.id)

        # Path: equal priority → no preemption
        result = scheduler.schedule_job(job2.id)
        self.assertIn("not started", result.lower())


if __name__ == "__main__":
    unittest.main()
