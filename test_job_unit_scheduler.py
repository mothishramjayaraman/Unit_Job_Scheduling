from job_unit_scheduler import JobUnitScheduler

def test_add_job():
    s = JobUnitScheduler()
    job = s.add_job("Demo Job", "Test Description","2025-12-12")

    assert job.id==1
    assert job.name=="Demo Job"
    assert job.description=="Test Description"
    assert job.deadline=="2025-12-12"
    assert job.complete is False

def test_list_jobs():
    s = JobUnitScheduler()
    s.add_job("Job1","Description1","2025-12-12")
    s.add_job("Job2","Description2","2025-12-13")

    jobs = s.list_jobs()

    assert len(jobs)==2
    assert jobs[0].name == "Job1"
    assert jobs[1].name=="Job2"

def test_view_job():
    s = JobUnitScheduler()
    s.add_job("Job1","information related to job","2025-12-12")

    job = s.view_job(1)

    assert job is not None
    assert job.id ==1
    assert job.name=="Job1"

def test_edit_job_description():
    s = JobUnitScheduler()
    s.add_job("Job1","Old Description ","2025-12-12")
    updated = s.edit_job_description(1,"New Description")
    assert updated.description=="New Description"

def test_rename_job():
    s = JobUnitScheduler()
    s.add_job("Job1","Details","2025-12-12")

    changed = s.rename_job(1,"Updated Name")
    assert changed is True
    assert s.view_job(1).name=="Updated Name"

def test_delete_job():
    s = JobUnitScheduler()
    s.add_job("Job1","Description","2025-12-12")
    removed = s.delete_job(1)
    assert removed is True
    assert s.view_job(1) is None

def test_add_unit():
    s = JobUnitScheduler()
    s.add_job("Job1","Description","2025-12-12")

    ok = s.add_unit(1, "Unit1")
    assert ok is True
    units = s.view_units(1)
    assert len(units)==1
    assert units[0].name=="Unit1"

def test_view_units():
    s = JobUnitScheduler()
    s.add_job("Job1","Description","2025-12-12")
    s.add_unit(1, "U1")
    s.add_unit(1, "U2")
    units = s.view_units(1)
    assert units == ["U1", "U2"]

def test_complete_job():
    s = JobUnitScheduler()
    s.add_job("Job1","Description","2025-12-12")
    done = s.complete_job(1)
    assert done is True
    assert s.view_job(1).complete is True

