import unittest
from job_unit_scheduler import JobUnitScheduler

class TestWhiteBoxSymbolicExecution(unittest.TestCase):

    #Symbolic path: job_id <= 0
    def test_symbolic_invalid_job_id(self):
        scheduler = JobUnitScheduler()
        result = scheduler.view_job(-1)
        self.assertIsNone(result)

    #Symbolic path: job_id > 0 AND  job_id not in jobs
    def test_symbolic_non_existing_job(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("job1","Desc","2025-12-12")
        result = scheduler.view_job(5)
        self.assertIsNone(result)

    #Symbolic path: job_id > 0 AND job_id exists
    def test_symbolic_existing_job(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("job1","Desc","2025-12-12")
        result = scheduler.view_job(1)
        self.assertIsNotNone(result)