import os
import tempfile
import unittest

from job_unit_scheduler import JobUnitScheduler


class TestUS48StatementCoverage(unittest.TestCase):


    def setUp(self):
        self.scheduler = JobUnitScheduler()
        self.scheduler.add_unit(1, ["CPU", "NVMe"])

    def test_us48_success_creates_and_writes_file(self):

        job = self.scheduler.add_job(
            "JobA", "desc", deadline=None, required_capacity=10.0, priority=3
        )
        self.scheduler.us43_validate_and_assign(job.id, 1)

        with tempfile.TemporaryDirectory() as td:
            old_cwd = os.getcwd()
            try:
                os.chdir(td)

                msg = self.scheduler.export_unit_activity_summary(1)
                self.assertTrue(msg.startswith("Success!"))

                expected_file = os.path.join(td, "Unit_1_Activity_Log.txt")
                self.assertTrue(os.path.exists(expected_file))

                with open(expected_file, "r", encoding="utf-8") as f:
                    content = f.read()

                self.assertIn("UNIT ACTIVITY REPORT", content)
                self.assertIn("Unit ID: 1", content)

            finally:
                os.chdir(old_cwd)

    def test_us48_error_unit_not_found(self):

        msg = self.scheduler.export_unit_activity_summary(999)
        self.assertIsInstance(msg, str)
        self.assertIn("Error", msg)


if __name__ == "__main__":
    unittest.main(verbosity=2)

import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestUS52StatementCoverage(unittest.TestCase):

    def setUp(self):
        self.scheduler = JobUnitScheduler()

    def test_us52_no_completed_jobs_report_structure(self):

        self.scheduler.add_job(
            "J1", "desc", deadline=datetime.now() + timedelta(days=1), priority=1
        )
        self.scheduler.add_job(
            "J2", "desc", deadline=datetime.now() + timedelta(days=1), priority=3
        )
        self.scheduler.add_job(
            "J3", "desc", deadline=datetime.now() + timedelta(days=1), priority=5
        )

        report = self.scheduler.analyze_execution_patterns_52()

        self.assertIsInstance(report, dict)
        self.assertEqual(report["total_jobs"], 3)
        self.assertIn("avg_runtime", report)
        self.assertIn("peak_hours", report)
        self.assertIn("priority_counts", report)
        self.assertEqual(sum(report["priority_counts"].values()), 3)
        self.assertIsInstance(report["avg_runtime"], (int, float))
        self.assertGreaterEqual(report["avg_runtime"], 0)

    def test_us52_some_completed_jobs_executes_runtime_and_peak_hour_logic(self):


        j1 = self.scheduler.add_job(
            "C1", "desc", deadline=datetime.now() + timedelta(days=1), priority=2
        )
        j2 = self.scheduler.add_job(
            "C2", "desc", deadline=datetime.now() + timedelta(days=1), priority=2
        )
        j3 = self.scheduler.add_job(
            "C3", "desc", deadline=datetime.now() + timedelta(days=1), priority=4
        )

        j1.start_time = datetime.now() - timedelta(seconds=30)
        self.scheduler.complete_job(j1.id)

        j2.start_time = datetime.now() - timedelta(seconds=90)
        self.scheduler.complete_job(j2.id)
        report = self.scheduler.analyze_execution_patterns_52()

        self.assertEqual(report["total_jobs"], 3)
        self.assertIsInstance(report["avg_runtime"], (int, float))
        self.assertGreaterEqual(report["avg_runtime"], 0)
        self.assertIsInstance(report["peak_hours"], dict)
        self.assertIsInstance(report["priority_counts"], dict)
        self.assertEqual(sum(report["priority_counts"].values()), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
