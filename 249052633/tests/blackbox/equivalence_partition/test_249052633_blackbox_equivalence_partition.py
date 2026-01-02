import unittest
import os
import tempfile
from job_unit_scheduler import JobUnitScheduler


class TestJobTagEquivalenceClasses(unittest.TestCase):
    """
    Black-box Testing – Equivalence Partition
    User Story #20: Tag Jobs With Categories
    """

    def test_job_tag_equivalence_classes(self):
        scheduler = JobUnitScheduler()
        job = scheduler.add_job("Job", "ok")

        # Valid equivalence class
        result_valid = scheduler.add_jobtag(job.id, "system")
        self.assertIn("added", result_valid.lower())

        # Invalid equivalence class
        result_invalid = scheduler.add_jobtag(job.id, "wrongtag")
        self.assertEqual(result_invalid, "Wrong tag")


class TestUS15ExportMetricsEquivalence(unittest.TestCase):
    """
    Black-box Testing – Equivalence Partition
    User Story #15: Export Job Metrics
    """

    def test_us15_export_job_metrics_equivalence(self):
        scheduler = JobUnitScheduler()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, "metrics.csv")

            # Equivalence class 1: no jobs
            result1 = scheduler.export_job_metrics(output_file)
            self.assertIn("exported", result1.lower())
            self.assertTrue(os.path.exists(output_file))

            # Equivalence class 2: job with execution data
            job = scheduler.add_job("Job1", "ok")
            scheduler.complete_job(job.id)

            result2 = scheduler.export_job_metrics(output_file)
            self.assertTrue(os.path.exists(output_file))


if __name__ == "__main__":
    unittest.main()
