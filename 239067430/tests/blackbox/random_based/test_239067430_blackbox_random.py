"""
Black-box Testing - Random Based Testing

Testing Technique:
This test file applies Random-Based Black-box Testing, as introduced in the lecture sessions.
Test inputs are generated randomly without any knowledge of the internal implementation of the system.

Functions Tested:
- add_job()
- view_job()

Expected Behaviour:
-The system should successfully create jobs when valid random inputs are provided.
-The system should safely handle invalid job identifiers and return None when a job does not exist.
"""
import unittest
import random
from job_unit_scheduler import JobUnitScheduler

class TestRandomJob(unittest.TestCase):
    def test_random_job_creation(self):
        s = JobUnitScheduler()
        for _ in range(10):
            name = f"Job{random.randint(1,100)}"
            job = s.add_job(name, "Random", "2025-12-12")
            self.assertEqual(job.name, name)
            self.assertEqual(job.description, "Random")

    def test_random_invalid_job_ids(self):
        s = JobUnitScheduler()
        s.add_job("Job1", "Description1", "2025-12-12")
        self.assertIsNone(s.view_job(999))

#if __name__ == "__main__":
 #   unittest.main()