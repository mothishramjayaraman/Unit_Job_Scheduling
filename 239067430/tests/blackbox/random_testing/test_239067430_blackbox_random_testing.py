import unittest
import random
from job_unit_scheduler import JobUnitScheduler

class TestBlackboxRandomTesting(unittest.TestCase):

    #Random-based testing for view_job
    def test_view_job_random_inputs(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("Job1","Desc","2025-12-12")

        for _ in range(10):
            random_id = random.randint(-10, 50)
            result = scheduler.view_job(random_id)

            #Result should either be a Job object or None
            self.assertTrue(result is None or hasattr(result, "id"))