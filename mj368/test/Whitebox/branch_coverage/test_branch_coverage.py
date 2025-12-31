from job_unit_scheduler import JobUnitScheduler
from datetime import datetime, timedelta
from job_unit_scheduler import JobUnitScheduler

# User Story #19 – Auto-Escalate Job Priority
def test_priority_escalation_branches():
    scheduler = JobUnitScheduler()

    urgent = scheduler.add_job("Urgent", "ok",
        datetime.now() + timedelta(hours=10))
    normal = scheduler.add_job("Normal", "ok",
        datetime.now() + timedelta(days=5))

    scheduler.us19_auto_escalate_job_priority()

    assert urgent.priority == 1      # escalation branch
    assert normal.priority == 5      # no-escalation branch

#US42-Job retry limit testing
def test_us42_retry_branch_paths():
    scheduler = JobUnitScheduler()
    job = scheduler.add_job("RetryJob", "ok")

    # Branch: retry < max
    scheduler.mark_job_failed(job.id, "fail1")
    assert job.status == "RETRYING"

    # Branch: retry == max
    scheduler.mark_job_failed(job.id, "fail2")
    scheduler.mark_job_failed(job.id, "fail3")
    assert job.status == "FAILED_PERMANENTLY"
