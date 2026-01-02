import unittest
from job_unit_scheduler import JobUnitScheduler

class TestWhiteBoxPathCoverage(unittest.TestCase):

    #Path 1: job_id <= 0 -> return None
    def test_path_invalid_job_id(self):
        scheduler = JobUnitScheduler()
        result = scheduler.view_job(0)
        self.assertIsNone(result)

    #Path 2: job_id > 0 but job does not exist -> return None
    def test_path_valid_job_id(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("job1","Desc","2025-12-12")
        result = scheduler.view_job(99)
        self.assertIsNone(result)

    #Path 3: job_id > 0 and job exists -> return job
    def test_path_valid_existing_job(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("job1","Desc","2025-12-12")
        result = scheduler.view_job(1)
        self.assertIsNotNone(result)
