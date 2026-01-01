import unittest
import tempfile
import os

from job_unit_scheduler import JobUnitScheduler


class TestClearCompletedJobsStatementCoverage(unittest.TestCase):
    """
    White-box Testing – Statement Coverage
    User Story #18: Clear Completed Jobs
    """

    def test_statement_coverage_clear_completed(self):
        scheduler = JobUnitScheduler()
        job = scheduler.add_job("Job", "ok")

        scheduler.complete_job(job.id)
        scheduler.remove_completed_jobs()

        self.assertEqual(len(scheduler.jobs), 0)


class TestUS15ExportMetricsStatementCoverage(unittest.TestCase):
    """
    White-box Testing – Statement Coverage
    User Story #15: Export Job Metrics
    """

    def test_us15_statement_coverage_export(self):
        scheduler = JobUnitScheduler()

        job = scheduler.add_job("Job1", "ok")
        scheduler.complete_job(job.id)

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "job_metrics.csv")
            scheduler.export_job_metrics(path)

            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
