# job_unit_scheduler.py

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import csv
import os
from datetime import datetime

class Unit:

    def __init__(self, unit_id: int, capabilities: List[str], max_capacity: float = 100.0):
        self.id = unit_id
        self.capabilities = capabilities
        self.max_capacity = max_capacity
        self.current_load = 0.0
        self.historical_loads = []
        self.error_logs = []
        self.dependencies: List[int] = []
        self.is_preferred = False

    def __str__(self):
                pref_status = " [PREFERRED]" if self.is_preferred else ""
                return f"[Unit {self.id}] Caps: {', '.join(self.capabilities)} | Load: {self.current_load}/{self.max_capacity} | Errors: {len(self.error_logs)}"



class Job:
   # def __init__(self, job_id, name, description, deadline, priority):
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
        self.required_capacity = required_capacity
        self.max_retries = 3
        self.retry_count = 0
        self.status = "Pending"
        self.dependencies: List[int] = []
        self.detailed_logging = False
        self.start_time = None
        self.max_runtime = None
        self.failure_count = 0
        self.last_error_message = ""
        self.priority_change_log = []

        # timeout_handling
        self.start_time = None
        self.end_time = None
        self.max_runtime = None
        self.failure_count = 0
        self.last_error_message = None
        self.created_at = datetime.now()
        self.end_time = None
        self.priority_change_log = []

    def __str__(self):
        status = "Completed" if self.complete else "Pending"

        return f"[{self.id}] {self.name} (P{self.priority}) | Status: {status}"


class JobUnitScheduler:


    #Priority Rules
    PRIORITY_ORDER = {
        1: 1,  # Critical
        2: 2,  # Urgent
        3: 3,  # Standard
        4: 4,  # Low
        5: 5  # Background
    }

    #US14: Comparison Priority(Preemption)
    def preempting(self, new_job, running_job):
        return self.PRIORITY_ORDER[new_job.priority] < self.PRIORITY_ORDER[running_job.priority]

    def __init__(self):

        self.jobs = {}
        self.next_job_id = 1
        self.units = []
        self.default_deadline_hours = 24
        self.current_running_job_id = None
       # self.jobs: List[Job] = []
        #self.next_id = 1

        #self.units: List[Unit] = []
        #self.default_deadline_hours = 24


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
        self.default_deadline_hours = 24
        self.current_running_job_id = None

    # US1: Add Job
    def add_job(self, name, description, deadline=None, priority=5, required_capacity=10.0):

        # US Description Validation (if characters exceed >= 100)
        if len(description) > self.Des_length:
            return None
        # US9 Deadline Handling (if called without a deadline)
        if deadline is None:

            deadline_dt = datetime.now() + timedelta(hours=self.default_deadline_hours)
            print(f"(Applying US9 default deadline: {self.default_deadline_hours} hours.)")
            job = Job(self.next_job_id, name, description, deadline_dt, priority, required_capacity)
            self.jobs[self.next_job_id] = job
            self.next_job_id += 1
            return job

        else:
            deadline_dt = deadline

        job = Job(self.next_job_id, name, description, deadline_dt, priority, required_capacity)
        self.jobs[self.next_job_id] = job
        self.next_job_id += 1
        return job

    # US2: List All Jobs
    def list_jobs(self):
        return self.jobs

    # US3: View a job by ID
    def view_job(self, job_id):
        if job_id <=0:
            return None
        if job_id not in self.jobs:
            return None
        return self.jobs[job_id]

       # for job in self.jobs:
        # if job.id == job_id:
         # return job
        #return None

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
                job.status = "Done"
                job.end_time = datetime.now()
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

    # US54: Mark Unit as Preferred
    def us54_set_unit_preference(self, unit_id: int, preferred: bool) -> bool:
            for unit in self.units:
                if unit.id == unit_id:
                    unit.is_preferred = preferred
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
            job.status = "In Progress"
            job.start_time = datetime.now()
            job.units.append(f"Unit {unit_id}")
            return f"Success! Job {job_id} assigned. Unit {unit_id} load: {unit.current_load}/{unit.max_capacity}"
        else:
            remaining = unit.max_capacity - unit.current_load
            return f"Rejected: Job needs {job.required_capacity}, but Unit only has {remaining} capacity."

    # US44: Job Retry Mechanism
    def us44_fail_and_retry_job(self, job_id: int, error_msg: str = "Execution Error") -> str:
                job = self.view_job(job_id)
                if not job:
                    return "Error: Job not found."

                if job.complete:
                    return "Error: Cannot retry a completed job."

                # US46 Integration: Log the error to any units associated with the job
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for u_str in job.units:

                        try:
                            u_id = int(u_str.split()[-1])
                            unit = next((u for u in self.units if u.id == u_id), None)
                            if unit:
                                unit.error_logs.append(f"[{timestamp}] Job {job_id}: {error_msg}")
                        except:
                             continue
                if job.retry_count < job.max_retries:
                    job.retry_count += 1
                    job.status = "Retrying"
                    return f"Job {job_id} failed. Automatically retrying... (Attempt {job.retry_count}/{job.max_retries})"
                else:
                    job.status = "Failed (Max Retries)"
                    return f"Job {job_id} failed. Maximum retries ({job.max_retries}) reached. Manual intervention required."

 # US46: Unit-Level Error Log Viewer retrieval method
    def get_unit_error_logs(self, unit_id: int) -> List[str]:
        unit = next((u for u in self.units if u.id == unit_id), None)
        return unit.error_logs if unit else []

# US45: Job Dependency Checker Logic
    def add_dependency(self, target_id: int, prerequisite_id: int) -> str:

        target = self.view_job(target_id)
        prereq = self.view_job(prerequisite_id)

        if not target or not prereq:
            return "Error: One or both jobs not found."
        if target_id == prerequisite_id:
            return "Error: A job cannot depend on itself."

        target.dependencies.append(prerequisite_id)
        return f"Success: Job {target_id} now depends on Job {prerequisite_id}."

    #US62: List System Capabilities
    def us7_list_capabilities(self) -> List[str]:

            return sorted(list(self.system_capabilities))

    # US60: Configure Default Deadline
    def us60_set_default_deadline(self, hours: int) -> bool:

        if hours > 0:
            self.default_deadline_hours = hours
            return True
        return False

    def check_dependencies_met(self, job_id: int) -> bool:

        job = self.view_job(job_id)
        if not job:
            return False

        for dep_id in job.dependencies:
            dep_job = self.view_job(dep_id)
            if not dep_job or not dep_job.complete:
                return False
        return True

    # US59: Enable/Disable Job Logging
    def us59_toggle_logging(self, job_id: int, enable: bool) -> bool:
            job = self.view_job(job_id)
            if job:
                job.detailed_logging = enable
                return True
            return False

    # US56: Remove Unit From Scheduler
    def us56_remove_unit(self, unit_id: int) -> bool:
        unit_to_remove = None
        for unit in self.units:
            if unit.id == unit_id:
                unit_to_remove = unit
                break
        if unit_to_remove:
            self.units.remove(unit_to_remove)
            self.system_capabilities = set()
            for u in self.units:
                self.system_capabilities.update(u.capabilities)
            return True
        return False

    # US48: EXPORT UNIT ACTIVITY SUMMARY

    def export_unit_activity_summary(self, unit_id: int) -> str:

        unit = next((u for u in self.units if u.id == unit_id), None)
        if not unit:
           return f"Error: Unit {unit_id} not found."

        search_label = f"Unit {unit_id}"
        unit_jobs = [j for j in self.jobs if search_label in j.units]

        filename = f"Unit_{unit_id}_Activity_Log.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(filename, "w") as file:
                file.write(f"UNIT ACTIVITY REPORT\n")
                file.write(f"====================\n")
                file.write(f"Unit ID: {unit_id}\n")
                file.write(f"Report Generated: {timestamp}\n")
                file.write(f"Capabilities: {', '.join(unit.capabilities)}\n")
                file.write(f"Final Load: {unit.current_load}/{unit.max_capacity}\n")
                file.write(f"--------------------\n\n")

                if not unit_jobs:
                    file.write("No jobs executed on this unit.\n")
                else:
                    file.write(f"{'Job ID':<8} | {'Name':<20} | {'Status':<15}\n")
                    file.write(f"{'-' * 45}\n")
                    for j in unit_jobs:
                        file.write(f"{j.id:<8} | {j.name[:20]:<20} | {j.status:<15}\n")

                file.write(f"\nError Logs Found: {len(unit.error_logs)}\n")
                for log in unit.error_logs:
                    file.write(f"- {log}\n")

            return f"Success! Activity exported to {filename}"
        except Exception as e:
            return f"File Error: {str(e)}"

    # US19: Auto-Escalate Job Priority
    def us19_auto_escalate_job_priority(self):
        now = datetime.now()
        escalated_jobs = []

        for job in self.jobs:
            if job.complete or not job.deadline:
                continue

            if isinstance(job.deadline, str):
                try:
                    deadline_dt = datetime.strptime(job.deadline, "%Y-%m-%d")
                except ValueError:
                    continue
            else:
                deadline_dt = job.deadline

            hours_left = (deadline_dt - now).total_seconds() / 3600
            old_priority = job.priority

            if hours_left < 24 and job.priority > 1:
                job.priority = 1
            elif hours_left < 48 and job.priority > 2:
                job.priority = 2
            else:
                continue

            job.priority_change_log.append({
                    "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "old_priority": old_priority,
                    "new_priority": job.priority,
                    "reason": "Deadline approaching"
            })

            escalated_jobs.append(job)

        return escalated_jobs

    # US69: Automatic job timeout handling(start)
    def start_job(self, job_id: int, max_runtime: int):
            job = self.view_job(job_id)
            if not job:
                return "Error: Job not found."

            if job.status == "RUNNING":
                return "Job is already running."

            job.start_time = datetime.now()
            job.max_runtime = max_runtime  # in seconds
            job.status = "RUNNING"

            return f"Job {job_id} started with max runtime {max_runtime} seconds."

    # US42: Job retry limit
    def mark_job_failed(self, job_id: int, failure_message: str):
        job = self.view_job(job_id)
        if not job:
            return "Job not found"

        if job.complete:
            return "Cannot retry a completed job"

        result = JobUnitScheduler.retry_handler(job, failure_message)

        if result == "RETRYING":
            return (
                f"Job {job_id} failed → retrying "
                f"({job.retry_count}/{job.max_retries})"
            )

        return (
            f"Job {job_id} reached retry limit "
            f"({job.retry_count}/{job.max_retries}) → FAILED_PERMANENTLY"
        )

    # US42: Static retry policy
    @staticmethod
    def retry_handler(job, failure_message: str):
        job.failure_count += 1
        job.last_error_message = failure_message

        job.retry_count += 1

        if job.retry_count < job.max_retries:
            job.status = "RETRYING"
            return "RETRYING"

        job.status = "FAILED_PERMANENTLY"
        return "FAILED_PERMANENTLY"
    # US69: Automatic job timeout handling(check timeout)
    def check_job_timeouts(self):
            now = datetime.now()
            timed_out_jobs = []

            for job in self.jobs:
                if job.status == "RUNNING":
                    if job.start_time and job.max_runtime:
                        elapsed = (now - job.start_time).total_seconds()
                        if elapsed > job.max_runtime:
                            job.status = "TIMED_OUT"
                            job.failure_count += 1
                            job.last_error_message = "Exceeded maximum runtime"
                            timed_out_jobs.append(job)
            return timed_out_jobs

    def job_resource_overconsumption_detection_51(self, job_id: int, actual_usage: float) -> str:
        job = self.view_job(job_id)
        if not job:
            return "Error: Job not found."

        if actual_usage > job.required_capacity:
            variance = actual_usage - job.required_capacity
            job.status = "FLAGGED: Overconsumption"

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for u_str in job.units:
                try:
                    u_id = int(u_str.split()[-1])
                    unit = next((u for u in self.units if u.id == u_id), None)
                    if unit:
                        unit.error_logs.append(
                            f"[{timestamp}] ALERT #51: Job {job_id} used {actual_usage}, "
                            f"exceeding declared {job.required_capacity} by {variance}."
                        )
                except:
                    continue
            return f" ALERT: Job Resource Overconsumption Detected (#51)! Job {job_id} flagged."

        return f" Normal: Job {job_id} usage is within declared capacity."


    # US17: Unit Health Status Tracking
    def unit_health_status(self):
        status = []

        for unit in self.units:
            load_percent = (unit.current_load / unit.max_capacity) * 100

            if load_percent < 30:
                health = "IDLE"
            elif load_percent <= 80:
                health = "BUSY"
            else:
                health = "OVERLOADED"

            status.append({
                    "unit_id": unit.id,
                    "current_load": unit.current_load,
                    "max_capacity": unit.max_capacity,
                    "load_percent": round(load_percent, 2),
                    "health": health
            })

        return status

    # US14: Schedule Job Preemption Rules
    def schedule_job(self, job_id: int):
        new_job = self.view_job(job_id)
        if not new_job:
            return "Error: Job not found."

        if new_job.complete:
            return "Cannot schedule a completed job."

        if self.current_running_job_id is None:
            new_job.status = "RUNNING"
            new_job.start_time = datetime.now()
            self.current_running_job_id = new_job.id
            return f"Job {job_id} started."

        running_job = self.view_job(self.current_running_job_id)

        if not running_job:
            new_job.status = "RUNNING"
            new_job.start_time = datetime.now()
            self.current_running_job_id = new_job.id
            return f"Job {job_id} started."

        if self.preempting(new_job, running_job):
            running_job.status = "PAUSED"

            new_job.status = "RUNNING"
            new_job.start_time = datetime.now()
            self.current_running_job_id = new_job.id

            return f"Job {job_id} preempted Job {running_job.id} and started execution."

        return f"Job {job_id} not started. Running Job {running_job.id} has higher or equal priority."

        # US50: Auto-Cancel Stalled Jobs
    def auto_cancel_stalled_jobs_50(self, timeout_seconds):
            stalled_jobs = []
            now = datetime.now()
            for job in self.jobs:

                if job.status == "In Progress" and job.start_time:
                    elapsed_time = (now - job.start_time).total_seconds()
                    if elapsed_time > timeout_seconds:
                        job.status = "Cancelled (Stalled)"
                        job.complete = False
                        job.last_error_message = f"Auto-cancelled after {elapsed_time:.1f}s of inactivity."
                        stalled_jobs.append(job)

            return stalled_jobs

    # US52: Job Execution Pattern Analyzer

    def analyze_execution_patterns_52(self):

        completed_jobs = [j for j in self.jobs if j.complete and j.start_time and j.end_time]
        peak_hours = {}
        for job in self.jobs:
            hour = job.created_at.hour
            peak_hours[hour] = peak_hours.get(hour, 0) + 1
        runtimes = []
        slow_jobs_list = []
        for job in completed_jobs:
            duration = (job.end_time - job.start_time).total_seconds()
            runtimes.append(duration)
            slow_jobs_list.append({'id': job.id, 'name': job.name, 'runtime': duration})
        slow_jobs_list.sort(key=lambda x: x['runtime'], reverse=True)
        avg_runtime = sum(runtimes) / len(runtimes) if runtimes else 0
        priority_counts = {}
        for job in self.jobs:
            priority_counts[job.priority] = priority_counts.get(job.priority, 0) + 1

        return {
            'total_jobs': len(self.jobs),
            'avg_runtime': avg_runtime,
            'peak_hours': peak_hours,
            'slow_jobs': slow_jobs_list[:3],
            'priority_counts': priority_counts
        }

        # US47: Predict Next Available Unit Slot
    def predict_next_slot_47(self, unit_id: int):
            unit = next((u for u in self.units if u.id == unit_id), None)

            if not unit:
                return "Error: Unit not found in the system."

            is_available = unit.current_load < unit.max_capacity
            load_percentage = (unit.current_load / unit.max_capacity) * 100

            if is_available and load_percentage < 70:
                status = "High Availability"
                estimate = "Immediate - Plenty of space available."
            elif is_available:
                status = "Limited Capacity"
                estimate = "Soon - Unit is nearly full, expect small delays."
            else:
                status = "Unit Full"
                estimate = "Delayed - Waiting for active jobs to complete or timeout."

            return {
                'unit_id': unit_id,
                'current_load': round(load_percentage, 2),
                'available_now': is_available,
                'status': status,
                'next_slot_estimate': estimate
            }

    #US15: Job Export Metrics
    def export_job_metrics(self, path: str | None = None):
        # Default path
        if path is None:
            path = "storage/job_metrics.csv"

        # Ensure storage directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "job_id",
                "execution_time_seconds",
                "failure_count",
                "status"
            ])

            for j in self.jobs:
                exec_time = None
                if j.start_time and j.end_time:
                    exec_time = round(
                        (j.end_time - j.start_time).total_seconds(), 2
                    )

                writer.writerow([
                    j.id,
                    exec_time,
                    j.failure_count,
                    j.status
                ])

        return f"Job metrics exported to {path}"