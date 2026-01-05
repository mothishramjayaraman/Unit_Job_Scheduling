import os
import csv
import tempfile
import unittest
from datetime import datetime, timedelta

from job_unit_scheduler import JobUnitScheduler


class TestJobUnitScheduler_WhiteBox(unittest.TestCase):
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
    def test_add_job_deadline_none_branch(self):
        job = self.add_job(deadline=None)
        self.assertIsNotNone(job)
        self.assertIsNotNone(job.deadline)
    def test_add_job_deadline_provided_branch(self):
        future = datetime.now() + timedelta(days=1)
        job = self.add_job(deadline=future)
        self.assertIsNotNone(job)
        self.assertEqual(job.deadline, future)
    def test_add_job_description_too_long_branch(self):
        res = self.add_job(desc="x" * 101)
        self.assertIsInstance(res, str)
        self.assertIn("description too long", res.lower())
    def test_view_job_branches(self):
        self.assertIsNone(self.s.view_job(0))
        self.assertIsNone(self.s.view_job(-1))
        self.assertIsNone(self.s.view_job(999999))
        job = self.add_job()
        self.assertIsNotNone(self.s.view_job(job.id))
    def test_complete_job_branches(self):
        self.assertFalse(self.s.complete_job(999999))
        job = self.add_job()
        self.assertTrue(self.s.complete_job(job.id))
        self.assertEqual(self.s.view_job(job.id).status, "Done")
    def test_remove_completed_jobs(self):
        j1 = self.add_job(name="A")
        j2 = self.add_job(name="B")
        self.s.complete_job(j1.id)
        msg = self.s.remove_completed_jobs()
        self.assertIn("removed", msg.lower())
        self.assertIsNone(self.s.view_job(j1.id))
        self.assertIsNotNone(self.s.view_job(j2.id))
    def test_jobtag_branches(self):
        msg_nf = self.s.add_jobtag(999999, "system")
        self.assertIn("not found", msg_nf.lower())
        job = self.add_job()
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
    def test_filter_jobtag_bug_path(self):
        self.add_job()
        with self.assertRaises(AttributeError):
            self.s.filter_jobtag("system")
    def test_priority_label_branches(self):
        self.assertTrue(self.s.us6_set_priority_label(1, "X"))
        self.assertFalse(self.s.us6_set_priority_label(0, "X"))
        self.assertFalse(self.s.us6_set_priority_label(6, "X"))
    def test_default_deadline_branches(self):
        self.assertTrue(self.s.us60_set_default_deadline(10))
        self.assertFalse(self.s.us60_set_default_deadline(0))
        self.assertFalse(self.s.us60_set_default_deadline(-5))
    def test_unit_preference_and_remove(self):
        self.add_unit(1, ["cpu"])
        self.assertTrue(self.s.us54_set_unit_preference(1, True))
        self.assertFalse(self.s.us54_set_unit_preference(999, True))
        self.assertTrue(self.s.us56_remove_unit(1))
        self.assertFalse(self.s.us56_remove_unit(1))  # already removed
    def test_unit_history_reset_branches(self):
        self.add_unit(2, ["cpu"])
        self.assertTrue(self.s.us61_reset_unit_history(2))
        self.assertFalse(self.s.us61_reset_unit_history(999))
    def test_us43_validate_and_assign_paths(self):
        self.add_unit(10, ["cpu"])
        msg = self.s.us43_validate_and_assign(999, 10)
        self.assertIn("job not found", msg.lower())
        job = self.add_job(required_capacity=10)
        msg = self.s.us43_validate_and_assign(job.id, 999)
        self.assertIn("unit not found", msg.lower())
        msg = self.s.us43_validate_and_assign(job.id, 10)
        self.assertIn("success", msg.lower())
        big = self.add_job(required_capacity=9999)
        msg2 = self.s.us43_validate_and_assign(big.id, 10)
        self.assertTrue("rejected" in msg2.lower() or "capacity" in msg2.lower())
    def test_us44_fail_and_retry_paths(self):
        msg_nf = self.s.us44_fail_and_retry_job(999999, "err")
        self.assertIn("job not found", msg_nf.lower())
        job = self.add_job()
        self.s.complete_job(job.id)
        msg_completed = self.s.us44_fail_and_retry_job(job.id, "err")
        self.assertIn("cannot retry", msg_completed.lower())
        job2 = self.add_job()
        msg_retry = self.s.us44_fail_and_retry_job(job2.id, "err")
        self.assertIn("retry", msg_retry.lower())
        job2.retry_count = job2.max_retries
        msg_max = self.s.us44_fail_and_retry_job(job2.id, "err")
        self.assertIn("maximum", msg_max.lower())
    def test_dependency_paths(self):
        a = self.add_job()
        b = self.add_job()
        msg_self = self.s.add_dependency(a.id, a.id)
        self.assertIn("cannot", msg_self.lower())
        msg_nf = self.s.add_dependency(999999, b.id)
        self.assertIn("error", msg_nf.lower())
        msg_ok = self.s.add_dependency(a.id, b.id)
        self.assertIn("success", msg_ok.lower())
    def test_schedule_job_paths(self):
        low = self.add_job(priority=5)
        high = self.add_job(priority=1)
        m1 = self.s.schedule_job(low.id)
        self.assertIn("started", m1.lower())
        m2 = self.s.schedule_job(high.id)
        self.assertTrue("preempted" in m2.lower() or "started" in m2.lower())
        self.s.complete_job(high.id)
        m3 = self.s.schedule_job(high.id)
        self.assertIn("completed", m3.lower())
    def test_start_job_and_timeouts_paths(self):
        msg_nf = self.s.start_job(999999, 5)
        self.assertIn("job not found", msg_nf.lower())
        job = self.add_job()
        msg_start = self.s.start_job(job.id, 1)
        self.assertIn("started", msg_start.lower())
        msg_again = self.s.start_job(job.id, 1)
        self.assertIn("already running", msg_again.lower())
        j = self.s.view_job(job.id)
        j.start_time = datetime.now() - timedelta(seconds=10)
        j.max_runtime = 1
        j.status = "RUNNING"
        timed_out = self.s.check_job_timeouts()
        self.assertIsInstance(timed_out, list)
    def test_mark_job_failed_paths(self):
        msg_nf = self.s.mark_job_failed(999999, "fail")
        self.assertIn("not found", msg_nf.lower())
        job = self.add_job()
        msg = self.s.mark_job_failed(job.id, "fail")
        self.assertIsInstance(msg, str)
        self.s.complete_job(job.id)
        msg2 = self.s.mark_job_failed(job.id, "fail")
        self.assertIn("cannot retry", msg2.lower())
    def test_overconsumption_paths(self):
        msg_nf = self.s.job_resource_overconsumption_detection_51(999999, 5)
        self.assertIn("job not found", msg_nf.lower())
        self.add_unit(5, ["cpu"])
        job = self.add_job(required_capacity=10)
        self.s.us43_validate_and_assign(job.id, 5)
        alert = self.s.job_resource_overconsumption_detection_51(job.id, 50)
        self.assertIn("alert", alert.lower())
        normal = self.s.job_resource_overconsumption_detection_51(job.id, 5)
        self.assertIn("normal", normal.lower())
    def test_predict_next_slot_paths(self):
        err = self.s.predict_next_slot_47(999)
        self.assertIn("error", err.lower())
        self.add_unit(100, ["cpu"])
        res = self.s.predict_next_slot_47(100)
        self.assertIsInstance(res, dict)
        self.assertIn("status", res)
    def test_auto_escalate_priority_paths(self):
        soon = datetime.now() + timedelta(hours=10)
        job = self.add_job(deadline=soon, priority=5)
        escalated = self.s.us19_auto_escalate_job_priority()
        self.assertIsInstance(escalated, list)
        self.assertIsInstance(job.priority_change_log, list)
        job2 = self.add_job(deadline=soon, priority=5)
        self.s.complete_job(job2.id)
        _ = self.s.us19_auto_escalate_job_priority()
    def test_export_job_metrics(self):
        self.add_job()
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "metrics.csv")
            msg = self.s.export_job_metrics(path)
            self.assertIn("exported", msg.lower())
            self.assertTrue(os.path.exists(path))
            with open(path, "r", newline="") as f:
                rows = list(csv.reader(f))
            self.assertGreaterEqual(len(rows), 2)
    def test_known_buggy_methods_raise(self):
        job = self.add_job()
        with self.assertRaises(Exception):
            self.s.edit_job_description(job.id, "new desc")
        with self.assertRaises(Exception):
            self.s.rename_job(job.id, "new name")
        with self.assertRaises(Exception):
            self.s.delete_job(job.id)
        with self.assertRaises(Exception):
            self.s.view_units(job.id)
        with self.assertRaises(Exception):
            self.s.auto_cancel_stalled_jobs_50(timeout_seconds=1)
        with self.assertRaises(Exception):
            self.s.analyze_execution_patterns_52()
        self.add_unit(500, ["cpu"])
        try:
            _ = self.s.export_unit_activity_summary(500)
        except Exception:
            pass
if __name__ == "__main__":
    unittest.main(verbosity=2)
