class JobUnitScheduler:
    def __init__(self):
        # make an empty list to store all jobs
        self.jobs = []
    #add job
    def add_job(self, name, description, deadline):
        #create a new job id by counting how many jobs are already there
        jobid = len(self.jobs) + 1
        #put all job details into one dictionary
        job = {
            "id": jobid,
            "name": name,
            "description": description,
            "deadline": deadline,
            "status": "active",
            "units": []
        }
        #add this job into the main list
        self.jobs.append(job)
        #give back the job id so i can use it later
        return jobid
