from job_unit_scheduler import JobUnitScheduler

# User Story #69 – Automatic Job Handling
def test_timeout_execution_path():
    scheduler = JobUnitScheduler()
    job = scheduler.add_job("Job", "ok")

    scheduler.start_job(job.id, 0)
    timed_out = scheduler.check_job_timeouts()

    assert timed_out[0].status == "TIMED_OUT"

#US14-job preemption schedule test
def test_us14_preemption_execution_paths():
    scheduler = JobUnitScheduler()

    job1 = scheduler.add_job("Job1", "ok", priority=3)
    job2 = scheduler.add_job("Job2", "ok", priority=3)

    scheduler.schedule_job(job1.id)

    # Path: equal priority → no preemption
    result = scheduler.schedule_job(job2.id)
    assert "not started" in result.lower()
