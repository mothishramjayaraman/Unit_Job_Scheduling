from job_unit_scheduler import JobUnitScheduler

# User Story #69 – Automatic Job Handling
def test_job_handling_categories():
    scheduler = JobUnitScheduler()
    job = scheduler.add_job("Job", "ok")

    # Category: job not running
    assert "started" in scheduler.start_job(job.id, 5)

    # Category: job already running
    assert "already running" in scheduler.start_job(job.id, 5)

#US14-Preemption rules job schedule test
def test_us14_preemption_categories():
    scheduler = JobUnitScheduler()

    low = scheduler.add_job("Low", "ok", priority=5)
    high = scheduler.add_job("High", "ok", priority=1)

    # Category 1: no running job
    result1 = scheduler.schedule_job(low.id)
    assert "started" in result1.lower()

    # Category 2: preemption
    result2 = scheduler.schedule_job(high.id)
    assert "preempted" in result2.lower()
