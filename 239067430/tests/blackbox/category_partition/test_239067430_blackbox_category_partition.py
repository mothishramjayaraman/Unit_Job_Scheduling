import unittest
from job_unit_scheduler import JobUnitScheduler

class TestBlackBoxCategoryPartition(unittest.TestCase):

        #Category: valid existing job id
        def test_view_job_valid_existing(self):
            scheduler = JobUnitScheduler()
            scheduler.add_job("Job1","Desc","2025-12-12")
            job = scheduler.view_job(1)
            self.assertIsNotNone(job)

        #Category: valid but non-existing job id
        def test_view_job_valid_non_existing(self):
            scheduler = JobUnitScheduler()
            scheduler.add_job("Job1","Desc","2025-12-12")
            job = scheduler.view_job(99)
            self.assertIsNone(job)

