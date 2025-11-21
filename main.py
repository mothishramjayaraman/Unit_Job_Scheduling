from job_unit_scheduler import JobUnitScheduler
s=JobUnitScheduler()
print("\n")
print("Welcome to Job Scheduler")


def show_menu():
    print("\n===Job Scheduler Menu ===)")# manage your jobs
    print("\n 1. Add Job (US1")
    print("2. View All Jobs (US2")
    print("10. Exit")


#US1: Add job
print("1. Add a job (US1)")
name = input("Enter job name: ")
description = input("Enter job description: ")
deadline = input("Enter job deadline (YYYY-MM-DD): ")

job = s.add_job(name, description, deadline)

print(f"\nJob added successfully! Job ID: {job.id}")

#Us2: View all jobs
print("\n2. View All Jobs (US2)")
jobs = s.view_all_jobs()

if len(jobs) == 0:
    print("No jobs found.")
else:
    print("\n All Jobs")
    for job in jobs:
        print(f"ID: {job.id}, Name: {job.name}, Description: {job.description}, Deadline: {job.deadline}, Units:{len(job.units)}")
