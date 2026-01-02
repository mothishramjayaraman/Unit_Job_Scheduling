import unittest
from job_unit_scheduler import JobUnitScheduler

class TestWhiteBoxBranchCoverage(unittest.TestCase):

    """
    White-box testing: Branch Coverage
    Function under test: view_job(job_id)
    """
    def test_view_job_branch_coverage(self):
        scheduler = JobUnitScheduler()

        #Branch 1: job_id <=0 -> True
        result_invalid = scheduler.view_job(0)
        self.assertIsNone(result_invalid)

        #Prepare scheduler with one job
        scheduler.add_job("job1","Desc","2025-12-12")

        #Branch 1: job_id <=0 -> False
        #Branch 2: job_id not in jobs ->True
        result_non_existing = scheduler.view_job(99)
        self.assertIsNone(result_non_existing)

        #Branch 2:job_id not in jobs -> False
        result_existing = scheduler.view_job(1)
        self.assertIsNotNone(result_existing)
