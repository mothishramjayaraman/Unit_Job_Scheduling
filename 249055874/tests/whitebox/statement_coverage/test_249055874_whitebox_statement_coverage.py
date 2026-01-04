import unittest
import sys
import os
from datetime import datetime, timedelta

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Job


class TestStatementCoverage(unittest.TestCase):


    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.jobs = []

        # Ensure view_job exists if referenced elsewhere
        if not hasattr(self.system, "view_job"):
            self.system.view_job = lambda job_id: next(
                (j for j in self.system.jobs if j.id == job_id),
                None
            )

    def test_analyze_execution_patterns_statements(self):

        job = Job(
            job_id=1,
            name="Completed Job",
            description="Statement coverage test",
            deadline=datetime.now(),
            priority=3
        )

        job.complete = True
        job.start_time = datetime.now()
        job.end_time = datetime.now() + timedelta(seconds=10)

        self.system.jobs.append(job)

        analysis = self.system.analyze_execution_patterns_52()

        self.assertEqual(analysis["total_jobs"], 1)
        self.assertGreaterEqual(analysis["avg_runtime"], 0)


if __name__ == "__main__":
    unittest.main()


import unittest
import sys
import os
from unittest.mock import mock_open, patch
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Unit, Job


class TestUS48ExportUnitActivity(unittest.TestCase):

    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.units = []
        self.system.jobs = []

    @patch("builtins.open", new_callable=mock_open)
    def test_export_unit_activity_success(self, mock_file):
        unit = Unit(unit_id=1, capabilities=["CPU"], max_capacity=10)
        unit.current_load = 5
        self.system.units.append(unit)

        job = Job(
            job_id=1,
            name="Test Job",
            description="Export test",
            deadline=datetime.now()
        )
        job.units.append("Unit 1")
        self.system.jobs.append(job)

        result = self.system.export_unit_activity_summary(1)

        self.assertIn("Success", result)
        mock_file.assert_called_once()  # ensures file writing occurred


if __name__ == "__main__":
    unittest.main()


import unittest
import sys
import os
from unittest.mock import mock_open, patch
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Unit, Job


class TestUS48StatementCoverage(unittest.TestCase):


    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.units = []
        self.system.jobs = []

    @patch("builtins.open", new_callable=mock_open)
    def test_export_unit_activity_summary_success(self, mock_file):

        unit = Unit(unit_id=1, capabilities=["CPU"], max_capacity=10)
        unit.current_load = 5
        self.system.units.append(unit)

        job = Job(
            job_id=1,
            name="Test Job",
            description="Export test",
            deadline=datetime.now()
        )
        job.units.append("Unit 1")
        self.system.jobs.append(job)

        result = self.system.export_unit_activity_summary(1)

        self.assertIn("Success", result)
        mock_file.assert_called_once()

    def test_export_unit_not_found(self):

        result = self.system.export_unit_activity_summary(999)
        self.assertIn("Error", result)


if __name__ == "__main__":
    unittest.main()
