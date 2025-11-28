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

    #US2: List All Jobs
    def list_jobs(self):
        return self.jobs

    #US3: View a job by ID
    def view_job(self, job_id):
        for job in self.jobs:
            if job.id == job_id:
                return job

        return None

    #US4: Edit Job Description
    def edit_job_description(self, job_id, description):
        for job in self.jobs:
            if job.id == job_id:
                job.description = description
                return job
        return None

    #US5: Rename job
    def rename_job(self, old_name, new_name):
        for job in self.jobs:
            if job.id == old_name:
                job.name = new_name
                return True
        return False

    #US6: Delete a job by ID
    def delete_job(self, job_id):
        for job in self.jobs:
            if job.id == job_id:
                self.jobs.remove(job)
                return True
        return False