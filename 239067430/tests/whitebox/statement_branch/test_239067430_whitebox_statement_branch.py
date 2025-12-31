"""
White-Box Testing: Statement and Branch Testing

Test Technique:
This test file applies White-Box Testing using Statement and Branch Coverage,
as introduced in the lectures sessions. Test cases are designed based on the internal control flow of the code.

Function Tested:
- view_job()

Branch Coverage:
- True branch: job exists
- False branch: job does not exist

Expected Behaviour:
- view_job() should return a job object when a valid job ID is provided
- view_job() should return None when an invalid job ID is provided
"""
import unittest
from job_unit_scheduler import JobUnitScheduler

class TestWhitebox(unittest.TestCase):

    def test_view_job_true_branch(self):
        s = JobUnitScheduler()
        s.add_job("Job1", "Description", "2025-12-12")
        job = s.view_job(1)
        self.assertIsNotNone(job)

    def test_view_job_false_branch(self):
        s = JobUnitScheduler()
        self.assertIsNone(s.view_job(999))

    def test_complete_job(self):
        s = JobUnitScheduler()
        job = s.add_job("Job", "Description", "2025-12-12")
        result = s.complete_job(job.id)
        self.assertTrue(result)
        self.assertTrue(job.complete)

    def test_delete_job(self):
        s = JobUnitScheduler()
        job = s.add_job("Job", "Description", "2025-12-12")
        result = s.delete_job(job.id)
        self.assertTrue(result)

    def test_delete_job_invalid_id(self):
        s = JobUnitScheduler()
        result = s.delete_job(999)
        self.assertFalse(result)
