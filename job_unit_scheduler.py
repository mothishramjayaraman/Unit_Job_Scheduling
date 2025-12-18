# job_unit_scheduler.py

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time


class Unit:

    def __init__(self, unit_id: int, capabilities: List[str], max_capacity: float = 100.0):
        self.id = unit_id
        self.capabilities = capabilities
        # US43: Capacity management attributes
        self.max_capacity = max_capacity
        self.current_load = 0.0
        self.historical_loads = []

    def __str__(self):
        return f"[Unit {self.id}] Caps: {', '.join(self.capabilities)}"


class Job:
    def __init__(self, job_id, name, description, deadline, priority=5, required_capacity=10.0):
        # Add new job object
        self.id = job_id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.units = []
        self.complete = False
        self.tags= []
        self.priority = priority
        # US43: Requirement for validation
        self.required_capacity = required_capacity

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
        self.Des_length = 100
        self.system_capabilities: set = set()

    # US1: Add Job
    def add_job(self, name, description, deadline=None, priority=5, required_capacity=10.0):

        # US Description Validation (if characters exceed >= 100)
        if len(description) > self.Des_length:
            return "Description too long! Try to add fewer than 100 characters"
        # US9 Deadline Handling (if called without a deadline)
        if deadline is None:

            deadline_dt = datetime.now() + timedelta(hours=self.default_deadline_hours)
            print(f"(Applying US9 default deadline: {self.default_deadline_hours} hours.)")
            job = Job(self.next_id, name, description, deadline_dt, priority, required_capacity)
            self.jobs.append(job)
            self.next_id += 1
            return job
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

    # US7: Add a unit inside a job
    def add_unit(self, job_id, name):
        for job in self.jobs:
            if job.id == job_id:
                job.units.append(name)
                return True
        return False

    # US8: View units by Job ID
    def view_units(self, job_id):
        for job in self.jobs:
            if job.id == job_id:
                return job.units  # return the list of units
        return None  # job not found

    # US9: Complete a job
    def complete_job(self, job_id):
        for job in self.jobs:
            if job.id == job_id:
                job.complete = True
                return True  # job marked completed
        return False  # job not found

    # US18: Clear completed jobs
    def remove_completed_jobs(self):
        prev = len(self.jobs)
        current_job = []
        for job in self.jobs:
            if not job.complete:
                current_job.append(job)
        self.jobs = current_job
        erased = prev - len(self.jobs)

        return f"{erased} completed job(s) removed."

    def add_unit(self, unit_id, capabilities: List[str]):

        unit = Unit(unit_id, capabilities)
        self.units.append(unit)
        self.system_capabilities.update(capabilities)
        return unit

    # US59: Set Job Priority Labels
    def us6_set_priority_label(self, priority_level: int, label: str) -> bool:

        if 1 <= priority_level <= 5:
            self.priority_labels[priority_level] = label
            return True
        return False

    def us6_get_priority_legend(self) -> Dict[int, str]:

        return self.priority_labels

    # US55: View Unit History
    def us4_view_unit_history(self, unit_id: int) -> List[float]:

        for unit in self.units:
            if unit.id == unit_id:
                return unit.historical_loads
        return []

    # US20 Get job for Tag management
    def get_job(self, job_id):
        for job in self.jobs:
            if job.id == job_id:
                return job
        return None

    # US20 Tag job(add)
    TAGS_CONTAINER = {"system", "user", "batch", "maintenance"}

    def add_jobtag(self, job_id, tag: str):
        job = self.get_job(job_id)
        if job is None:
            return "Job not found"
        tag = tag.lower()
        if tag not in self.TAGS_CONTAINER:
            return "Wrong tag"
        if tag in job.tags:
            return "Tag already exists"
        job.tags.append(tag)
        return f"Tag '{tag}' added to job {job_id}"

    # US20 Tag job(remove)
    def remove_jobtag(self, job_id, tag: str):
        job = self.get_job(job_id)
        if job is None:
            return "Job not found"
        tag = tag.lower()
        if tag not in job.tags:
            return f"Tag '{tag}' not present on job {job_id}"
        job.tags.remove(tag)
        return f"Tag '{tag}' removed from job {job_id}"

    # US20 Tag job(filter)
    def filter_jobtag(self, tag: str):
        tag = tag.lower()
        return [job for job in self.jobs if tag in job.tags]

    # US57: View Job Priority Legend
    def us57_get_priority_legend(self) -> Dict[int, str]:

         return self.priority_labels

    # US61: Reset Unit Load History
    def us61_reset_unit_history(self, unit_id: int) -> bool:

        for unit in self.units:
            if unit.id == unit_id:
                current_val = getattr(unit, 'load', 0.0)
                unit.historical_loads = [current_val]
                return True
        return False

    # US43: Unit Capacity Validation
    def us43_validate_and_assign(self, job_id: int, unit_id: int) -> str:
        job = self.view_job(job_id)

        unit = next((u for u in self.units if u.id == unit_id), None)

        if not job:
            return "Error: Job not found."
        if not unit:
            return "Error: Unit not found."
        if (unit.current_load + job.required_capacity) <= unit.max_capacity:
            unit.current_load += job.required_capacity
            job.units.append(f"Unit {unit_id}")
            return f"Success! Job {job_id} assigned. Unit {unit_id} load: {unit.current_load}/{unit.max_capacity}"
        else:
            remaining = unit.max_capacity - unit.current_load
            return f"Rejected: Job needs {job.required_capacity}, but Unit only has {remaining} capacity."