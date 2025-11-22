from job_unit_scheduler import JobUnitScheduler
s=JobUnitScheduler()
print("Welcome to Job Scheduler")


def show_menu():
    print("===Job Scheduler Menu ===)")# manage your jobs
    print("1. Add Job (US1)")
    print("0. Exit")

while True:
    show_menu()
    print("\n")
    choice=input("Enter your choice (1 or 10):- ")

    #US1: Add job
    if choice=="1":
         print("=>Add a job (US1)")
         name = input("Enter job name: ")
         description = input("Enter job description: ")
         deadline = input("Enter job deadline (YYYY-MM-DD): ")

         job = s.add_job(name, description, deadline)

         print(f"\nJob added successfully! Job ID: {job.id}")
    elif choice=="0":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
