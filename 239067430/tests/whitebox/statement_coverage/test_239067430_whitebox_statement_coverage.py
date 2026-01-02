import unittest
from job_unit_scheduler import JobUnitScheduler

class TestWhiteBoxStatementCoverage(unittest.TestCase):

    """
    White-box testing: Statement Coverage
    Function under test: view_job(job_id)
    """
    def test_view_job_all_statement_executed(self):
        scheduler = JobUnitScheduler()

        #Statement 1: add a job so internal list is not empty
        scheduler.add_job("Job1", "Desc","2025-12-12")

        #Statement 2: job_id <=0 condition (execute return None)
        result_invalid = scheduler.view_job(0)
        self.assertIsNone(result_invalid)

        #Statement 3: job_id not in jobs condition
        result_non_existing = scheduler.view_job(99)
        self.assertIsNone(result_non_existing)

        #Statement 4: valid job_id returns job object
        result_valid = scheduler.view_job(1)
        self.assertIsNotNone(result_valid)
