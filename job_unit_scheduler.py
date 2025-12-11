# job_unit_scheduler.py

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time



class Unit:


    def __init__(self, unit_id: int, capabilities: List[str]):
        self.id = unit_id

        self.capabilities = capabilities

    def __str__(self):
        return f"[Unit {self.id}] Caps: {', '.join(self.capabilities)}"




class Job:



    def __init__(self, job_id, name, description, deadline, priority: int = 5):
        self.id = job_id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.units = []
        self.complete = False


        self.priority = priority

    def __str__(self):

        status = "Completed" if self.complete else "Pending"

        return f"[{self.id}] {self.name} (P{self.priority}) | Status: {status}"



class JobUnitScheduler:


    def __init__(self):

        self.jobs: List[Job] = []
        self.next_id = 1


        self.units: List[Unit] = []

        # US6: Dictionary to store priority labels (default values)
        self.priority_labels: Dict[int, str] = {
            1: "Critical",
            2: "Urgent",
            3: "Standard",
            4: "Low",
            5: "Background"
        }
        self.Des_length=100
        self.system_capabilities: set = set()
    # US1: Add Job
    def add_job(self, name, description, deadline=None, priority=5):

        # US Description Validation (if characters exceed >= 100)
        if len(description) > self.Des_length:
            return "Description too long! Try to add fewer than 100 characters"
        # US9 Deadline Handling (if called without a deadline)
        if deadline is None:

            deadline_dt = datetime.now() + timedelta(hours=self.default_deadline_hours)
            print(f"(Applying US9 default deadline: {self.default_deadline_hours} hours.)")
        else:

            deadline_dt = deadline


        job = Job(self.next_id, name, description, deadline_dt, priority)
        self.jobs.append(job)
        self.next_id += 1
        return job

    # US2: List All Jobs
    def list_jobs(self):
        return self.jobs

    # US3: View a job by ID
    def view_job(self, job_id):
        for job in self.jobs:
            if job.id == job_id:
                return job
        return None

    # US4: Edit Job Description
    def edit_job_description(self, job_id, description):
        for job in self.jobs:
            if job.id == job_id:
                job.description = description
                return job
        return None

    # US5: Rename job
    def rename_job(self, job_id, new_name):

        for job in self.jobs:
            if job.id == job_id:
                job.name = new_name
                return True
        return False

    # US6: Delete a job by ID
    def delete_job(self, job_id):
        for job in self.jobs:
            if job.id == job_id:
                self.jobs.remove(job)
                return True
        return False

    #US7: Add a unit inside a job
    def add_unit(self, job_id, name):
        for job in self.jobs:
            if job.id == job_id:
                job.units.append(name)
                return True
        return False

    #US8: View units by Job ID
    def view_units(self, job_id):
        for job in self.jobs:
            if job.id == job_id:
                return job.units # return the list of units
        return None #job not found

    # US9: Complete a job
    def complete_job(self, job_id):
        for job in self.jobs:
            if job.id == job_id:
                job.complete = True
                return True  # job marked completed
        return False  # job not found