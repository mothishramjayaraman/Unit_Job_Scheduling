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

        # US7: Set to store all unique capabilities in the system
        self.system_capabilities: set = set()

        # US9: Default job deadline setting (in hours)
        self.default_deadline_hours: int = 48


    # US1: Add Job
    def add_job(self, name, description, deadline=None, priority=5):


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




    def add_unit(self, unit_id, capabilities: List[str]):

        unit = Unit(unit_id, capabilities)
        self.units.append(unit)
        self.system_capabilities.update(capabilities)  # US7 update
        return unit

    # US59: Set Job Priority Labels
    def us6_set_priority_label(self, priority_level: int, label: str) -> bool:

        if 1 <= priority_level <= 5:
            self.priority_labels[priority_level] = label
            return True
        return False

    # US62: List System Capabilities
    def us7_list_capabilities(self) -> List[str]:

        return sorted(list(self.system_capabilities))

    # US60: Configure Default Deadline
    def us9_set_default_deadline(self, hours: int) -> bool:

        if hours > 0:
            self.default_deadline_hours = hours
            return True
        return False

    def us6_get_priority_legend(self) -> Dict[int, str]:

        return self.priority_labels