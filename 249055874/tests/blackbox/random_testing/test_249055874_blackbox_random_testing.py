import unittest
import random
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestUS52RandomTesting(unittest.TestCase):


    def setUp(self):
        self.scheduler = JobUnitScheduler()
        self.scheduler.add_unit(1, ["CPU", "NVMe"])
        self.scheduler.add_unit(2, ["GPU", "High_Mem"])

    def test_us52_random_jobs_report_invariants(self):
        rng = random.Random(20260103)  # fixed seed = reproducible

        num_jobs = 30
        created_job_ids = []

        for i in range(num_jobs):
            priority = rng.randint(1, 5)
            required_capacity = round(rng.uniform(1.0, 50.0), 1)
            deadline = datetime.now() + timedelta(days=rng.randint(1, 7))

            job = self.scheduler.add_job(
                f"RandJob{i}",
                "desc",
                deadline=deadline,
                priority=priority,
                required_capacity=required_capacity,
            )
            created_job_ids.append(job.id)

            if rng.random() < 0.6:
                runtime_seconds = rng.randint(1, 300)
                job.start_time = datetime.now() - timedelta(seconds=runtime_seconds)
                self.scheduler.complete_job(job.id)

        report = self.scheduler.analyze_execution_patterns_52()

        self.assertIsInstance(report, dict)
        self.assertIn("total_jobs", report)
        self.assertIn("avg_runtime", report)
        self.assertIn("peak_hours", report)
        self.assertIn("priority_counts", report)
        self.assertEqual(report["total_jobs"], num_jobs)
        self.assertIsInstance(report["priority_counts"], dict)
        total_counted = sum(report["priority_counts"].values())
        self.assertEqual(total_counted, num_jobs)
        self.assertIsInstance(report["avg_runtime"], (int, float))
        self.assertGreaterEqual(report["avg_runtime"], 0)
        self.assertIsInstance(report["peak_hours"], dict)

        for k, v in report["peak_hours"].items():
            self.assertIsInstance(v, int)
            self.assertGreaterEqual(v, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
