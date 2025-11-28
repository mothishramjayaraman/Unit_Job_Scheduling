from job_unit_scheduler import JobUnitScheduler
s=JobUnitScheduler()
print("Welcome to Job Scheduler")


def show_menu():
    print("===Job Scheduler Menu ===)")# manage your jobs
    print("1. Add Job (US1)")
    print("2. List Jobs (US2)")
    print("3. View Job (US3)")
    print("4. Edit Job Description (US4)")
    print("5. Rename Job (Us5)")
    print("6. Delete Job (Us6)")
    print("7. Add Unit (US7)")
    print("0. Exit")

while True:
    show_menu()
    print("\n")
    choice=input("Enter your choice ( 1 to 7):- ")

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

    #US4: Edit job description
    elif choice=="4":
        print("\n=> Edit Job Description")
        job_id = int(input("Enter job ID to edit: "))
        new_desc = input("Enter new job description: ")

        updated_job = s.edit_job_description(job_id, new_desc)
        if updated_job:
            print("\nJob description updated successfully!")
        else:
            print("\nJob not found.")

    #US5: Rename job
    elif choice=="5":
        print("\n=> Rename Job")
        job_id = int(input("Enter job ID to rename: "))
        new_name = input("Enter new job name: ")

        s1 = s.rename_job(job_id, new_name)
        if s1:
            print("\nJob renamed successfully!")
        else:
            print("\nJob not found.")

    #US6 Delete job
    elif choice=="6":
        print("\n=> Delete Job")
        job_id = int(input("Enter job ID to delete: "))

        s1 = s.delete_job(job_id)
        if s1:
            print("\nJob deleted successfully!")
        else:
            print("\nJob not found.")

    #US7 Add Unit
    elif choice=="7":
        print("\n=> Add Job Unit")
        job_id = int(input("Enter job ID to add unit into: "))
        name = input("Enter unit name: ")

        Done = s.add_unit(job_id, name)

        if Done:
            print("\nUnit added successfully!")
        else:
            print("\nJob not found. Please enter a valid Job ID.")

    elif choice=="0":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
