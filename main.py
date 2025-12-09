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
    print("0. Exit")

while True:
    show_menu()
    print("\n")
    choice=input("Enter your choice ( 1 to 6):- ")

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

    elif choice=="0":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")

#---------------------------------------------------------------------------------------------------
#---------------------MOTHISHRAM JAYARAMAN-----------------------------------------------------------

from job.Job import Job
from job.JobManager import JobManager
from datetime import datetime

def input_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Please enter a valid number.")


def input_optional(prompt: str):
    value = input(prompt).strip()
    return value if value != "" else None


def create_job(manager: JobManager):
    print("\n=== Create New Job ===")
    job_id = input_int("Enter job ID (number): ")

    description = input("Enter description: ").strip()
    priority = input("Enter priority (LOW/MEDIUM/HIGH): ").strip().upper() or "LOW"
    status = "PENDING"   # default status

    max_runtime = input_int("Enter max runtime in seconds: ")

    tags_input = input("Enter tags (comma separated), or leave empty: ").strip()
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []

    assigned_unit_id = input_optional("Enter assigned unit ID (or leave empty): ")

    # Optional: retry limit
    retry_limit_str = input_optional("Enter retry limit (leave empty for 0): ")
    retry_limit = int(retry_limit_str) if retry_limit_str else 0

    job = Job(
        job_id=job_id,
        description=description,
        priority=priority,
        status=status,
        created_at=None,          # let Job class handle timestamp if you want
        start_time=None,
        end_time=None,
        max_runtime=max_runtime,
        tags=tags,
        failure_count=0,
        last_error_message=None,
        assigned_unit_id=assigned_unit_id,
        retry_limit=retry_limit,  # make sure your Job __init__ has these
        retry_count=0
    )

    result = manager.add_job(job)
    print(result)


def view_jobs(manager: JobManager):
    print("\n=== All Jobs ===")
    if not manager.jobs:
        print("No jobs found.")
        return

    # Simple table header
    print(
        f"{'ID':<4} {'Desc':<20} {'Prio':<6} {'Status':<18} "
        f"{'MaxRT':<6} {'Fail':<5} {'Retry':<9} {'Tags'}"
    )
    print("-" * 80)

    for j in manager.jobs:
        retry_info = f"{getattr(j, 'retry_count', 0)}/{getattr(j, 'retry_limit', 0)}"
        print(
            f"{j.job_id:<4} "
            f"{str(j.description)[:20]:<20} "
            f"{j.priority:<6} "
            f"{j.status:<18} "
            f"{str(j.max_runtime):<6} "
            f"{j.failure_count:<5} "
            f"{retry_info:<9} "
            f"{','.join(j.tags)}"
        )


def update_job_console(manager: JobManager):
    print("\n=== Update Job ===")
    job_id = input_int("Enter job ID to update: ")
    job = manager.get_job(job_id)
    if not job:
        print(f"No job found with ID {job_id}")
        return

    print("Leave input empty to keep existing value.")

    newDescription = input_optional(f"New description (current: {job.description}): ")
    newPriority = input_optional(f"New priority (current: {job.priority}): ")
    if newPriority:
        newPriority = newPriority.upper()

    new_max_runtime_str = input_optional(f"New max runtime (current: {job.max_runtime}): ")
    new_max_runtime = int(new_max_runtime_str) if new_max_runtime_str else None

    new_tags_str = input_optional(f"New tags comma-separated (current: {job.tags}): ")
    new_tags = [t.strip() for t in new_tags_str.split(",")] if new_tags_str else None

    new_assigned_unit_id = input_optional(
        f"New assigned unit ID (current: {job.assigned_unit_id}): "
    )

    result = manager.update_job(
        job_id,
        description=newDescription,
        priority=newPriority,
        max_runtime=new_max_runtime,
        tags=new_tags,
        assigned_unit_id=new_assigned_unit_id,
    )

    print(result)


def deleteJob(manager: JobManager):
    print("\n=== Delete Job ===")
    job_id = input_int("Enter job ID to delete: ")
    success = manager.delete_job(job_id)
    if success is True:
        print(f"Job {job_id} deleted successfully!")
    else:
        print(success)  # "No Job found"


def saveJobs(manager: JobManager):
    print("\n=== Save Jobs to CSV ===")
    manager.save_to_csv()
    print("Jobs saved to CSV!")


def loadJobs(manager: JobManager):
    print("\n=== Load Jobs from CSV ===")
    manager.load_from_csv()
    print("Jobs loaded from CSV!")


# ---------- New feature helpers below ----------

def clearCompleted(manager: JobManager):
    print("\n=== Clear Completed Jobs ===")
    msg = manager.clear_completed_jobs()
    print(msg)


def add_tag_console(manager: JobManager):
    print("\n=== Add Tag to Job ===")
    job_id = input_int("Enter job ID: ")
    tag = input("Enter tag to add: ").strip()
    msg = manager.add_tag_to_job(job_id, tag)
    print(msg)


def remove_tag_console(manager: JobManager):
    print("\n=== Remove Tag from Job ===")
    job_id = input_int("Enter job ID: ")
    tag = input("Enter tag to remove: ").strip()
    msg = manager.remove_tag_from_job(job_id, tag)
    print(msg)


def filter_by_tag_console(manager: JobManager):
    print("\n=== View Jobs by Tag ===")
    tag = input("Enter tag to filter: ").strip()
    jobs = manager.get_jobs_by_tag(tag)
    if not jobs:
        print(f"No jobs found with tag '{tag}'.")
        return

    for j in jobs:
        print(
            f"ID={j.job_id} | Desc='{j.description}' | "
            f"Priority={j.priority} | Status={j.status} | Tags={j.tags}"
        )


def sort_by_priority_console(manager: JobManager):
    print("\n=== Sort Jobs by Priority ===")
    manager.sort_jobs_by_priority()
    print("Jobs sorted by priority (HIGH → LOW).")
    view_jobs(manager)


def set_retry_limit_console(manager: JobManager):
    print("\n=== Set Retry Limit ===")
    job_id = input_int("Enter job ID: ")
    retry_limit = input_int("Enter retry limit (number): ")
    msg = manager.set_retry_limit(job_id, retry_limit)
    print(msg)


def mark_job_failed_console(manager: JobManager):
    print("\n=== Mark Job as Failed (with Retry) ===")
    job_id = input_int("Enter job ID: ")
    failure_message = input("Enter failure message: ").strip() or "Unknown error"
    msg = manager.mark_job_failed(job_id, failure_message)
    print(msg)


def export_metrics_console(manager: JobManager):
    print("\n=== Export Job Metrics ===")
    path = input_optional("Enter output CSV path (default: job_metrics.csv): ") or "job_metrics.csv"
    manager.export_job_metrics(path)
    print(f"Metrics exported to {path}")


def main():
    manager = JobManager()

    while True:
        print("\n========================")
        print(" Job Manager Console ")
        print("========================")
        print("1. Create Job")
        print("2. View All Jobs")
        print("3. Update Job")
        print("4. Delete Job")
        print("5. Save Jobs to CSV")
        print("6. Load Jobs from CSV")
        print("7. Clear Completed Jobs")
        print("8. Add Tag to Job")
        print("9. Remove Tag from Job")
        print("10. View Jobs by Tag")
        print("11. Sort Jobs by Priority")
        print("12. Set Retry Limit for Job")
        print("13. Mark Job as Failed (Retry Logic)")
        print("14. Export Job Metrics")
        print("15. Exit")

        choice = input("Choose an option (1-15): ").strip()

        if choice == "1":
            create_job(manager)
        elif choice == "2":
            view_jobs(manager)
        elif choice == "3":
            update_job_console(manager)
        elif choice == "4":
            deleteJob(manager)
        elif choice == "5":
            saveJobs(manager)
        elif choice == "6":
            loadJobs(manager)
        elif choice == "7":
            clearCompleted(manager)
        elif choice == "8":
            add_tag_console(manager)
        elif choice == "9":
            remove_tag_console(manager)
        elif choice == "10":
            filter_by_tag_console(manager)
        elif choice == "11":
            sort_by_priority_console(manager)
        elif choice == "12":
            set_retry_limit_console(manager)
        elif choice == "13":
            mark_job_failed_console(manager)
        elif choice == "14":
            export_metrics_console(manager)
        elif choice == "15":
            print("Exiting Job Manager. Bye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 15.")


if __name__ == "__main__":
    main()




