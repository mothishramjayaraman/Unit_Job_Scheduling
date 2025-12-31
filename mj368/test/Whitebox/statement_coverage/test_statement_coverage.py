from job_unit_scheduler import JobUnitScheduler
import tempfile
# User Story #18 – Clear Completed Jobs
def test_statement_coverage_clear_completed():
    scheduler = JobUnitScheduler()
    job = scheduler.add_job("Job", "ok")

    scheduler.complete_job(job.id)
    scheduler.remove_completed_jobs()

    assert len(scheduler.jobs) == 0


#US15- job-export-metrics-testing
def test_us15_statement_coverage_export():
    scheduler = JobUnitScheduler()

    job = scheduler.add_job("Job1", "ok")
    scheduler.complete_job(job.id)

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "job_metrics.csv")
        scheduler.export_job_metrics(path)

        assert os.path.exists(path)
