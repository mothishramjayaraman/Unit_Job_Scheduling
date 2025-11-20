from job_unit_scheduler import JobUnitScheduler
s=JobUnitScheduler()
print("Welcome to Job Scheduler")
print("\n")

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
