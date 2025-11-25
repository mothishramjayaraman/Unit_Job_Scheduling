from job_unit_scheduler import JobUnitScheduler
s=JobUnitScheduler()
print("Welcome to Job Scheduler")


def show_menu():
    print("===Job Scheduler Menu ===)")# manage your jobs
    print("1. Add Job (US1)")
    print("2. List Jobs (US2)")
    print("3. View Job (US3)")
    print("0. Exit")

while True:
    show_menu()
    print("\n")
    choice=input("Enter your choice (1,2,3 or 0):- ")

    #US1: Add job
    if choice=="1":
         print("=>Add a job (US1)")
         name = input("Enter job name: ")
         description = input("Enter job description: ")
         deadline = input("Enter job deadline (YYYY-MM-DD): ")

         job = s.add_job(name, description, deadline)

         print(f"\nJob added successfully! Job ID: {job.id}")

    #US2: List all Jobs
    elif choice=="2":
        print("=>List Jobs (US2)")
        jobs = s.list_jobs()
        if len(jobs)==0:
            print("No jobs found.")
        else:
            for job in jobs:
                print(f"Job ID: {job.id}, ")
                print(f"Name: {job.name}, ")
                print(f"Description: {job.description},")
                print(f" Deadline: {job.deadline}")

    #US3: View a job
    elif choice=="3":
        print("\n=> View Job")
        job_id =int(input("Enter job ID to view: "))

        job = s.view_job(job_id)
        if job:
            print(f"Job ID: {job.id}")
            print(f"Name: {job.name}, ")
            print(f"Description: {job.description},")
            print(f"Deadline: {job.deadline}")
        else:
            print("\nJob not found.")

    elif choice=="0":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
