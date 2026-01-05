import os
import csv
import random
import string
import tempfile
import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler

class TestBlackBox_SpecAndRandom_FullAPI(unittest.TestCase):
    def setUp(self):
        self.s = JobUnitScheduler()
    def add_job(self, name="Job", desc="Desc", deadline=None, priority=5, required_capacity=10.0):
        return self.s.add_job(
            name=name,
            description=desc,
            deadline=deadline,
            priority=priority,
            required_capacity=required_capacity,
        )
    def add_unit(self, unit_id=1, caps=None):
        if caps is None:
            caps = ["cpu"]
        return self.s.add_unit(unit_id, caps)
    def test_us60_set_default_deadline_ep_bva(self):
        self.assertTrue(self.s.us60_set_default_deadline(48))   # valid EP
        self.assertFalse(self.s.us60_set_default_deadline(0))   # BVA
        self.assertFalse(self.s.us60_set_default_deadline(-1))  # BVA
    def test_default_deadline_applied_when_deadline_none(self):
        self.s.us60_set_default_deadline(48)
        job = self.add_job(name="D", desc="Desc", deadline=None)
        self.assertIsNotNone(job)
        self.assertIsNotNone(job.deadline)
        expected = datetime.now() + timedelta(hours=48)
        self.assertTrue(abs((job.deadline - expected).total_seconds()) < 7200)
    def test_us6_set_priority_label_ep_bva(self):
        self.assertTrue(self.s.us6_set_priority_label(1, "Critical"))
        self.assertFalse(self.s.us6_set_priority_label(0, "Invalid"))
        self.assertFalse(self.s.us6_set_priority_label(6, "Invalid"))
        legend = self.s.us57_get_priority_legend()
        self.assertEqual(legend[1], "Critical")
    def test_us57_get_priority_legend(self):
        legend = self.s.us57_get_priority_legend()
        self.assertIsInstance(legend, dict)
        for k in [1, 2, 3, 4, 5]:
            self.assertIn(k, legend)
    def test_us7_list_capabilities(self):
        self.assertEqual(self.s.us7_list_capabilities(), [])
        self.add_unit(1, ["cpu", "gpu"])
        self.add_unit(2, ["net"])
        caps = self.s.us7_list_capabilities()
        self.assertIn("cpu", caps)
        self.assertIn("gpu", caps)
        self.assertIn("net", caps)
    def test_us54_set_unit_preference(self):
        self.add_unit(10, ["cpu"])
        self.assertTrue(self.s.us54_set_unit_preference(10, True))
        self.assertFalse(self.s.us54_set_unit_preference(999, True))

    def test_us56_remove_unit(self):
        self.add_unit(11, ["cpu"])
        self.add_unit(12, ["gpu"])
        self.assertTrue(self.s.us56_remove_unit(11))
        self.assertFalse(self.s.us56_remove_unit(999))
        caps = self.s.us7_list_capabilities()
        self.assertNotIn("cpu", caps)
        self.assertIn("gpu", caps)

    def test_us59_toggle_logging(self):
        job = self.add_job(name="Log", desc="Desc", deadline=None)
        self.assertTrue(self.s.us59_toggle_logging(job.id, True))
        self.assertTrue(self.s.view_job(job.id).detailed_logging)
        self.assertTrue(self.s.us59_toggle_logging(job.id, False))
        self.assertFalse(self.s.view_job(job.id).detailed_logging)
        self.assertFalse(self.s.us59_toggle_logging(999999, True))

    def test_us4_view_unit_history_and_us61_reset(self):
        self.add_unit(20, ["cpu"])
        self.assertEqual(self.s.us4_view_unit_history(999), [])
        self.assertIsInstance(self.s.us4_view_unit_history(20), list)

        self.assertTrue(self.s.us61_reset_unit_history(20))
        self.assertFalse(self.s.us61_reset_unit_history(999))
        hist = self.s.us4_view_unit_history(20)
        self.assertEqual(len(hist), 1)

    def test_tag_add_remove_branches(self):
        job = self.add_job(name="Tag", desc="Desc", deadline=None)

        msg_nf = self.s.add_jobtag(999999, "system")
        self.assertIn("not found", msg_nf.lower())

        msg_wrong = self.s.add_jobtag(job.id, "bad_tag")
        self.assertIn("wrong tag", msg_wrong.lower())

        msg_ok = self.s.add_jobtag(job.id, "system")
        self.assertIn("added", msg_ok.lower())

        msg_dup = self.s.add_jobtag(job.id, "system")
        self.assertIn("already", msg_dup.lower())

        msg_rm_missing = self.s.remove_jobtag(job.id, "user")
        self.assertIn("not present", msg_rm_missing.lower())

        msg_rm_ok = self.s.remove_jobtag(job.id, "system")
        self.assertIn("removed", msg_rm_ok.lower())

    def test_complete_and_remove_completed(self):
        j1 = self.add_job(name="C1", desc="Desc", deadline=None)
        j2 = self.add_job(name="C2", desc="Desc", deadline=None)

        self.assertTrue(self.s.complete_job(j1.id))
        msg = self.s.remove_completed_jobs()
        self.assertIn("removed", msg.lower())

        self.assertIsNone(self.s.view_job(j1.id))
        self.assertIsNotNone(self.s.view_job(j2.id))

    def test_us43_validate_and_assign(self):
        self.add_unit(1, ["cpu"])

        msg = self.s.us43_validate_and_assign(999, 1)
        self.assertIn("job not found", msg.lower())

        job = self.add_job(name="A", desc="Desc", deadline=None, required_capacity=10)
        msg = self.s.us43_validate_and_assign(job.id, 999)
        self.assertIn("unit not found", msg.lower())

        msg = self.s.us43_validate_and_assign(job.id, 1)
        self.assertIn("success", msg.lower())

        big = self.add_job(name="Big", desc="Desc", deadline=None, required_capacity=1000)
        msg2 = self.s.us43_validate_and_assign(big.id, 1)
        self.assertTrue("rejected" in msg2.lower() or "capacity" in msg2.lower())

    def test_us44_fail_and_retry_and_logs(self):
        self.add_unit(7, ["cpu"])
        job = self.add_job(name="R", desc="Desc", deadline=None, required_capacity=10)
        self.s.us43_validate_and_assign(job.id, 7)  # so job.units contains "Unit 7"

        msg1 = self.s.us44_fail_and_retry_job(job.id, "Boom")
        self.assertIn("retry", msg1.lower())

        logs = self.s.get_unit_error_logs(7)
        self.assertIsInstance(logs, list)

        job.retry_count = job.max_retries
        msg2 = self.s.us44_fail_and_retry_job(job.id, "Boom2")
        self.assertIn("maximum", msg2.lower())

    def test_dependencies(self):
        a = self.add_job(name="A", desc="Desc", deadline=None)
        b = self.add_job(name="B", desc="Desc", deadline=None)

        msg = self.s.add_dependency(a.id, b.id)
        self.assertIn("depends", msg.lower())
        self.assertFalse(self.s.check_dependencies_met(a.id))

        self.s.complete_job(b.id)
        self.assertTrue(self.s.check_dependencies_met(a.id))

        msg_self = self.s.add_dependency(a.id, a.id)
        self.assertIn("cannot", msg_self.lower())

    def test_schedule_job(self):
        low = self.add_job(name="Low", desc="Desc", deadline=None, priority=5)
        high = self.add_job(name="High", desc="Desc", deadline=None, priority=1)

        m1 = self.s.schedule_job(low.id)
        self.assertIsInstance(m1, str)

        m2 = self.s.schedule_job(high.id)
        self.assertIsInstance(m2, str)

        self.s.complete_job(high.id)
        m3 = self.s.schedule_job(high.id)
        self.assertIn("completed", m3.lower())

    def test_start_and_timeout(self):
        job = self.add_job(name="Run", desc="Desc", deadline=None)
        msg = self.s.start_job(job.id, 1)
        self.assertIn("started", msg.lower())

        j = self.s.view_job(job.id)
        j.start_time = datetime.now() - timedelta(seconds=5)
        j.max_runtime = 1
        j.status = "RUNNING"

        timed_out = self.s.check_job_timeouts()
        self.assertIsInstance(timed_out, list)

    def test_mark_job_failed(self):
        job = self.add_job(name="Fail", desc="Desc", deadline=None)
        msg = self.s.mark_job_failed(job.id, "oops")
        self.assertIsInstance(msg, str)

        self.s.complete_job(job.id)
        msg2 = self.s.mark_job_failed(job.id, "oops")
        self.assertIn("cannot", msg2.lower())
    def test_overconsumption(self):
        self.add_unit(5, ["cpu"])
        job = self.add_job(name="OC", desc="Desc", deadline=None, required_capacity=10)
        self.s.us43_validate_and_assign(job.id, 5)

        alert = self.s.job_resource_overconsumption_detection_51(job.id, 50)
        self.assertIn("alert", alert.lower())

        normal = self.s.job_resource_overconsumption_detection_51(job.id, 5)
        self.assertIn("normal", normal.lower())
    def test_unit_health(self):
        u = self.add_unit(100, ["cpu"])
        s1 = self.s.unit_health_status()
        self.assertIsInstance(s1, list)

        u.current_load = 90.0
        s2 = self.s.unit_health_status()
        self.assertIsInstance(s2, list)
    def test_predict_next_slot(self):
        self.add_unit(200, ["cpu"])
        res = self.s.predict_next_slot_47(200)
        self.assertIsInstance(res, dict)
        err = self.s.predict_next_slot_47(999)
        self.assertIsInstance(err, str)
        self.assertIn("error", err.lower())
    def test_auto_escalate_priority(self):
        soon = datetime.now() + timedelta(hours=10)
        job = self.add_job(name="Soon", desc="Desc", deadline=soon, priority=5)
        escalated = self.s.us19_auto_escalate_job_priority()
        self.assertIsInstance(escalated, list)
        self.assertIsInstance(job.priority_change_log, list)
    def test_export_job_metrics(self):
        self.add_job(name="M1", desc="Desc", deadline=None)
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "metrics.csv")
            msg = self.s.export_job_metrics(path)
            self.assertIn("exported", msg.lower())
            self.assertTrue(os.path.exists(path))
            with open(path, "r", newline="") as f:
                rows = list(csv.reader(f))
            self.assertGreaterEqual(len(rows), 2)
    def test_random_based_add_jobs_valid(self):
        for _ in range(20):
            name = "Job_" + "".join(random.choices(string.ascii_letters, k=8))
            desc = "x" * random.randint(0, 100)
            priority = random.randint(1, 5)
            req = float(random.randint(1, 50))
            res = self.add_job(name=name, desc=desc, deadline=None, priority=priority, required_capacity=req)
            self.assertFalse(isinstance(res, str))

    def test_random_based_invalid_descriptions(self):
        for _ in range(10):
            name = "Job_" + "".join(random.choices(string.ascii_letters, k=6))
            desc = "x" * random.randint(101, 160)
            res = self.add_job(name=name, desc=desc, deadline=None)
            self.assertIsInstance(res, str)
            self.assertIn("description too long", res.lower())
if __name__ == "__main__":
    unittest.main(verbosity=2)
