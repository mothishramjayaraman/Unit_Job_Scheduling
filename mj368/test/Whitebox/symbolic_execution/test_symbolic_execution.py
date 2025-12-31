from job_unit_scheduler import JobUnitScheduler
from datetime import datetime, timedelta

# User Story #19 – Symbolic paths based on deadline
def test_symbolic_priority_paths():
    scheduler = JobUnitScheduler()

    j1 = scheduler.add_job("J1", "ok",
        datetime.now() + timedelta(hours=10))
    j2 = scheduler.add_job("J2", "ok",
        datetime.now() + timedelta(hours=40))
    j3 = scheduler.add_job("J3", "ok",
        datetime.now() + timedelta(days=4))

    scheduler.us19_auto_escalate_job_priority()

    assert j1.priority == 1   # path: deadline < 24
    assert j2.priority == 2   # path: 24 ≤ deadline < 48
    assert j3.priority == 5   # path: deadline ≥ 48
