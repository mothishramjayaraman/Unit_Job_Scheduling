"""
Black-Box Testing: Specification-Based Testing

Testing Technique:
This test file applies specification-Based Black-Box Testing, as covered in the lecture sessions.
Test cases are derived directly from the functional requirements and user stories of the system.

Functions Tested:
- add_job()
- list_jobs()

Expected Behaviour:
- add_job() Should create a job when valid inputs are provided.
- list_jobs() should return all previously created jobs.
"""
import unittest
from job_unit_scheduler import JobUnitScheduler

class TestJobSchedulerSpec(unittest.TestCase):

    def test_add_job(self):
        scheduler = JobUnitScheduler()
        job = scheduler.add_job("Demo for job", "Description", "2025-12-12")
        self.assertEqual(job.name,"Demo for job")

    def test_list_jobs(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("Job1", "Description1", "2025-12-12")
        jobs = scheduler.list_jobs()
        self.assertEqual(len(jobs), 1)


#if __name__ == '__main__':
 #   unittest.main()
