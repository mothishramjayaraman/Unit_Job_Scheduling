import unittest
from job_unit_scheduler import JobUnitScheduler

class TestWhiteBoxConcolicTesting(unittest.TestCase):

    #Path 1: job_id <= 0 (symbolic condition: job_id <= 0)
    def test_view_job_invalid_id(self):
        scheduler = JobUnitScheduler()
        result = scheduler.view_job(0)
        self.assertIsNone(result)

    #Path 2: job_id > 0 but job does not exist
    def test_view_job_non_existing(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("job1","Desc","2025-12-12")
        result = scheduler.view_job(99)
        self.assertIsNone(result)

    #Path 3: job_id > 0 and job exists
    def test_view_job_existing(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("job1","Desc","2025-12-12")
        result = scheduler.view_job(1)
        self.assertIsNotNone(result)