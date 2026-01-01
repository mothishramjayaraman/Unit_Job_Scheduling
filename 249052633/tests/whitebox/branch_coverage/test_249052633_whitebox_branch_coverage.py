import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestPriorityEscalationBranches(unittest.TestCase):
    """
    White-box Testing – Branch Coverage
    User Story #19: Auto-Escalate Job Priority
    """

    def test_priority_escalation_branches(self):
        scheduler = JobUnitScheduler()

        urgent = scheduler.add_job(
            "Urgent",
            "ok",
            datetime.now() + timedelta(hours=10)
        )

        normal = scheduler.add_job(
            "Normal",
            "ok",
            datetime.now() + timedelta(days=5)
        )

        scheduler.us19_auto_escalate_job_priority()

        # Escalation branch
        self.assertEqual(urgent.priority, 1)

        # No-escalation branch
        self.assertEqual(normal.priority, 5)


class TestUS42RetryBranchPaths(unittest.TestCase):
    """
    White-box Testing – Branch / Path Coverage
    User Story #42: Job Retry Limit
    """

    def test_us42_retry_branch_paths(self):
        scheduler = JobUnitScheduler()
        job = scheduler.add_job("RetryJob", "ok")

        # Path 1: retry count < max
        scheduler.mark_job_failed(job.id, "fail1")
        self.assertEqual(job.status, "RETRYING")

        # Path 2: retry count == max
        scheduler.mark_job_failed(job.id, "fail2")
        scheduler.mark_job_failed(job.id, "fail3")
        self.assertEqual(job.status, "FAILED_PERMANENTLY")


if __name__ == "__main__":
    unittest.main()
