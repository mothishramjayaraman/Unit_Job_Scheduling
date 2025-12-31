import time
from job_unit_scheduler import JobUnitScheduler

# User Story #69 – Concrete execution + symbolic timeout condition
def test_concolic_job_timeout():
    scheduler = JobUnitScheduler()
    job = scheduler.add_job("Job", "ok")

    scheduler.start_job(job.id, 1)   # concrete input
    time.sleep(2)

    timed_out = scheduler.check_job_timeouts()
    assert len(timed_out) == 1
