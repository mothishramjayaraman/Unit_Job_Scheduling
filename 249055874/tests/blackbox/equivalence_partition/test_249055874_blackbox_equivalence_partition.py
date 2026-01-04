import unittest
import sys
import os
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Job


class TestEquivalencePartition(unittest.TestCase):

    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.jobs = []
        self.system.view_job = lambda job_id: next(
            (j for j in self.system.jobs if j.id == job_id),
            None
        )

    def test_normal_resource_usage_partition(self):

        job = Job(
            job_id=1,
            name="Normal Job",
            description="Within capacity",
            deadline=datetime.now(),
            required_capacity=10
        )
        self.system.jobs.append(job)

        result = self.system.job_resource_overconsumption_detection_51(1, 8)
        self.assertIn("Normal", result)

    def test_overconsumption_partition(self):

        job = Job(
            job_id=2,
            name="Overuse Job",
            description="Exceeds capacity",
            deadline=datetime.now(),
            required_capacity=5
        )
        self.system.jobs.append(job)

        result = self.system.job_resource_overconsumption_detection_51(2, 9)
        self.assertIn("ALERT", result)
        self.assertEqual(job.status, "FLAGGED: Overconsumption")

    def test_invalid_job_id_partition(self):

        result = self.system.job_resource_overconsumption_detection_51(999, 5)
        self.assertIn("Error", result)


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
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Job


class TestUS45EquivalencePartition(unittest.TestCase):


    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.jobs = []

        # Make job lookup deterministic for black-box testing
        self.system.view_job = lambda job_id: next(
            (j for j in self.system.jobs if j.id == job_id),
            None
        )

    def test_valid_dependency_partition(self):

        prereq_job = Job(1, "Prerequisite Job", "Desc", datetime.now())
        target_job = Job(2, "Target Job", "Desc", datetime.now())

        self.system.jobs.extend([prereq_job, target_job])

        result = self.system.add_dependency(2, 1)

        self.assertIn("Success", result)
        self.assertIn(1, target_job.dependencies)

    def test_self_dependency_partition(self):

        job = Job(3, "Job", "Desc", datetime.now())
        self.system.jobs.append(job)

        result = self.system.add_dependency(3, 3)

        self.assertIn("Error", result)

    def test_missing_job_partition(self):

        result = self.system.add_dependency(10, 20)
        self.assertIn("Error", result)


if __name__ == "__main__":
    unittest.main()


import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from job_unit_scheduler import JobUnitScheduler, Unit


class TestUS46EquivalencePartition(unittest.TestCase):

    def setUp(self):
        self.system = JobUnitScheduler()
        self.system.units = []

    def test_valid_unit_with_error_logs_partition(self):

        unit = Unit(unit_id=1, capabilities=["CPU"])
        unit.error_logs.append("Error: overheating detected")
        self.system.units.append(unit)

        logs = self.system.get_unit_error_logs(1)

        self.assertIsInstance(logs, list)
        self.assertEqual(len(logs), 1)
        self.assertIn("overheating", logs[0])

    def test_valid_unit_without_error_logs_partition(self):

        unit = Unit(unit_id=2, capabilities=["GPU"])
        self.system.units.append(unit)

        logs = self.system.get_unit_error_logs(2)

        self.assertEqual(logs, [])

    def test_invalid_unit_id_partition(self):

        logs = self.system.get_unit_error_logs(999)
        self.assertEqual(logs, [])


if __name__ == "__main__":
    unittest.main()
