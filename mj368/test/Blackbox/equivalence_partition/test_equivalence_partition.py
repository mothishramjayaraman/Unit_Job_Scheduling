from job_unit_scheduler import JobUnitScheduler
import os
# User Story #20 – Tag Jobs With Categories
def test_job_tag_equivalence_classes():
    scheduler = JobUnitScheduler()
    job = scheduler.add_job("Job", "ok")

    # valid equivalence class
    assert "added" in scheduler.add_jobtag(job.id, "system")

    # invalid equivalence class
    assert scheduler.add_jobtag(job.id, "wrongtag") == "Wrong tag"


#us15_export_metrics testing
def test_us15_export_job_metrics_equivalence(tmp_path):
    scheduler = JobUnitScheduler()

    # Equivalence class: no jobs
    output_file = tmp_path / "metrics.csv"
    result = scheduler.export_job_metrics(str(output_file))

    assert "exported" in result
    assert os.path.exists(output_file)

    # Equivalence class: job with execution data
    job = scheduler.add_job("Job1", "ok")
    scheduler.complete_job(job.id)

    result = scheduler.export_job_metrics(str(output_file))
    assert os.path.exists(output_file)
