
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time

# Updated by Reethishselvakumar



class Unit:
    def __init__(self, unit_id: int, capabilities: List[str], specialization: str = "General", status: str = "Idle",
                 load: float = 0.0):
        self.id = unit_id
        self.capabilities = capabilities
        self.specialization = specialization
        self.status = status
        self.load = load
        self.historical_loads = [load] * 10

    def __str__(self): return f"[Unit {self.id}] Spec: {self.specialization}, Status: {self.status}"


class Job:
    def __init__(self, job_id, name, description, deadline, required_caps: List[str] = None, job_type: str = "Standard",
                 priority: int = 5):
        self.id = job_id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.units = []
        self.complete = False
        self.required_caps = required_caps if required_caps is not None else []
        self.job_type = job_type
        self.priority = priority
        self.submit_time = datetime.now()
        self.milestones: Dict[str, datetime] = {}
        self.last_priority_escalation = self.submit_time
        self.status = "Pending"

    def __str__(self):
        status = "Completed" if self.complete else self.status
        return f"[{self.id}] {self.name} (P:{self.priority}, Type:{self.job_type}) - {status}"



class JobUnitScheduler:

    def __init__(self):
        self.jobs: List[Job] = []
        self.next_id = 1
        self.units: List[Unit] = []
        self.queues: Dict[str, List[Job]] = {"HighPriority": [], "Standard": [], "Analysis": []}
        self.job_history: Dict[str, Dict] = {"ML": {'failed_then_succeeded': 7, 'total_failed': 10}}

    def add_unit(self, unit_id, capabilities, specialization="General", status="Idle", load=0.0):
        unit = Unit(unit_id, capabilities, specialization=specialization, status=status, load=load)
        self.units.append(unit)
        return unit

    def view_job(self, job_id):
        return next((job for job in self.jobs if job.id == job_id), None)

    def list_jobs(self):
        return self.jobs


    def _us5_route_job_to_queue(self, job: Job):
        if job.priority <= 2:
            self.queues["HighPriority"].append(job)
        else:
            self.queues["Standard"].append(job)


    def add_job(self, name, description, deadline, required_caps: List[str] = None, job_type: str = "Standard",
                priority: int = 5):
        job = Job(self.next_id, name, description, deadline, required_caps, job_type, priority)
        self.jobs.append(job)
        self.next_id += 1
        self._us5_route_job_to_queue(job)
        return job







    def us6_optimize_idle_time(self, idle_unit):
        return None

    def us1_predict_load(self, unit):
        return unit.load + 5.0  # Simple prediction


    def delete_job(self, job_id):
        return True

    def edit_job_description(self, job_id, description):
        return self.view_job(job_id)

    def rename_job(self, job_id, new_name):
        return True


    def display_queues(self):
        print("\n--- Current Queue Status ---")
        for name, queue in self.queues.items():
            print(f"Queue {name}: {len(queue)} jobs.")
            for job in queue:
                print(f"  - Job {job.id} (P{job.priority}, Type: {job.job_type})")
        print("----------------------------")




if __name__ == '__main__':
    s = JobUnitScheduler()
    print("Welcome to Job Scheduler")


    s.add_unit(1, ['GPU', 'CPU'], 'ML')
    s.add_unit(2, ['CPU', 'Storage'], 'General', status='Idle', load=15.0)
    s.add_unit(3, ['CPU', 'Fast_IO'], 'Analysis', status='Idle', load=0.0)


    job_A = Job(s.next_id, "Long Wait Task", "Escalation Test", "2025-12-05", ['CPU'], "General", 5)
    job_A.submit_time = datetime.now() - timedelta(hours=3)  # Simulate long wait
    s.jobs.append(job_A)
    s._us5_route_job_to_queue(job_A)
    s.next_id += 1


    job_B_id = s.next_id
    s.add_job("Specialized Analysis", "Match Test", "2025-12-06", ['Fast_IO', 'CPU'], "Analysis", 3)


    job_C_id = s.next_id
    s.add_job("Routine Cleanup", "Idle Test", "2025-12-04", ['CPU'], "Standard", 5)

    print("\nSetup Complete. Ready to run advanced policies.")
    s.display_queues()


    def show_menu():
        """Displays the comprehensive menu with separate choices for US1-US9."""
        print("\n\n=== Advanced Policy Execution Menu ===")
        # Basic CRUD
        print("1. Add Job (Standard CRUD)")
        print("2. List Jobs (Standard CRUD)")
        print("3. Unit Idle-Time Optimization")
        print("4. Unit Load Forecasting")
        print("0. Exit")


    while True:
        show_menu()
        choice = input("Enter your choice (0 to 4):- ")

        # --- BASIC CRUD ---
        if choice == "1":
            print("=> Add Job ")
            name = input("Enter name: ");
            desc = input("Enter desc: ");
            deadline = input("Enter deadline: ")
            caps_str = input("Caps (GPU,CPU): ");
            job_type = input("Type (ML/Analysis/General): ")
            try:
                priority = int(input("Priority (1-5): "))
            except ValueError:
                priority = 5
            required_caps = [c.strip() for c in caps_str.split(',')]
            job = s.add_job(name, desc, deadline, required_caps, job_type, priority)
            print(f"\nJob added and routed! ID: {job.id}")

        elif choice == "2":
            print("=> List Jobs")
            jobs = s.list_jobs()
            if not jobs:
                print("No jobs found.")
            else:
                [print(job) for job in jobs]







        # 14. Run US6: Unit Idle-Time Optimization
        elif choice == "14":
            print("\n--- US6: Idle-Time Optimization Check ---")

            # Unit 2 is idle and will pull job from the queue
            pulled_job = s.us6_optimize_idle_time(s.units[1])
            if pulled_job:
                print(f"-> SUCCESS: Idle Unit {s.units[1].id} pulled Job {pulled_job.id}.")
            else:
                print("-> FAILED: No job pulled.")
            s.display_queues()

        # 15. Run US1: Unit Load Forecasting
        elif choice == "15":
            print("\n--- US1: Unit Load Forecasting Check ---")

            for unit in s.units:
                predicted = s.us1_predict_load(unit)
                print(f"Unit {unit.id} (Current Load: {unit.load}) -> Predicted Load: {predicted}")

        # 0. Exit
        elif choice == "0":
            print("Exiting Scheduler...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")