import unittest
from job_unit_scheduler import JobUnitScheduler

class TestBlackBoxEquivalencePartition(unittest.TestCase):

    #Equivalence Class: Valid existing job ID
    def test_view_job_valid_equivalence(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("Job1","Desc","2025-12-12")
        job = scheduler.view_job(1)
        self.assertIsNotNone(job)

    #Equivalence Class: Invalid non-existing job ID
    def test_view_job_invalid_equivalence(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("Job1","Desc","2025-12-12")
        job = scheduler.view_job(99)
        self.assertIsNone(job)