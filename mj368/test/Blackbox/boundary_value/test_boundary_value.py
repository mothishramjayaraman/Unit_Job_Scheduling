from job_unit_scheduler import JobUnitScheduler
from job_unit_scheduler import JobUnitScheduler

# User Story #16 – Job Description Character Limit
def test_description_length_at_upper_boundary():
    scheduler = JobUnitScheduler()

    desc_100 = "a" * 100        # upper valid boundary
    desc_101 = "a" * 101        # just above boundary

    assert scheduler.add_job("Job1", desc_100) is not None
    assert scheduler.add_job("Job2", desc_101) == \
        "Description too long! Try to add fewer than 100 characters"

#US42-job retry limit
def test_us42_retry_limit_boundary():
    scheduler = JobUnitScheduler()
    job = scheduler.add_job("RetryJob", "ok")

    # max_retries = 3
    r1 = scheduler.mark_job_failed(job.id, "err1")
    r2 = scheduler.mark_job_failed(job.id, "err2")
    r3 = scheduler.mark_job_failed(job.id, "err3")

    assert "retrying" in r1.lower()
    assert "retrying" in r2.lower()
    assert "failed_permanently" in r3.lower()
