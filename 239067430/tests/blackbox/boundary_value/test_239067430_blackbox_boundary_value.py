"""
Black-box testing technique: Boundary Value Analysis
"""
import unittest
from job_unit_scheduler import JobUnitScheduler

class TestBlackBoxBoundaryValue(unittest.TestCase):

    #Minimum valid boundary
    def test_view_job_min_boundary(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("Job1", "Desc","2025-12-12")
        job = scheduler.view_job(1)
        self.assertIsNotNone(job)

    #Below minimum boundary (invalid id)
    def test_view_job_below_min_boundary(self):
        scheduler = JobUnitScheduler()
        job = scheduler.view_job(0)
        self.assertIsNone(job)

    #Above maximum boundary(invalid id)
    def test_view_job_above_max_boundary(self):
        scheduler = JobUnitScheduler()
        scheduler.add_job("Job1", "Desc","2025-12-12")
        job = scheduler.view_job(2)
        self.assertIsNone(job)