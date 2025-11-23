class Job:
    def __init__(self, job_id, name, description, deadline):
        self.id = job_id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.units=[]
        self.complete=False

    def __str__(self):
        status = "Completed" if self.complete else "Pending"
        return f"[{self.id}] {self.name} - {status}"

class JobUnitScheduler:
    def __init__(self):
        self.jobs=[]
        self.next_id = 1

    #US1: Add Job
    def add_job(self, name, description, deadline):
        job = Job(self.next_id, name, description, deadline)
        self.jobs.append(job)
        self.next_id += 1
        return job

    #US2: List of All Jobs
    def list_jobs(self):
        return self.jobs
