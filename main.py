from job_unit_scheduler import JobUnitScheduler
from datetime import datetime

s = JobUnitScheduler()

s.add_unit(1, ['GPU', 'High_Mem', 'NVMe'])
s.units[0].load = 80.0
s.units[0].historical_loads = [60.0, 70.0, 80.0]
s.add_unit(2, ['CPU', 'Storage', 'NVMe'])
s.units[1].load = 15.0
s.units[1].historical_loads = [10.0, 15.0]

print("Welcome to Job Scheduler")



def show_menu():
    print("===Job Scheduler Menu ===)")  # manage your jobs
    print("1. Add Job (US1)")
    print("2. List Jobs (US2)")
    print("3. View Job (US3)")
    print("4. Edit Job Description (US4)")
    print("5. Rename Job (Us5)")
    print("6. Delete Job (Us6)")
    print("7. Add Unit (US7)")
    print("8. View Units (US8)")
    print("9. Complete Job (US9)")
    print("10. Clear Completed Jobs (US18)")
    print("11. Job/Unit Configuration Menu (US58/US55)")
    print("0. Exit")

def show_config_menu():
    print("\n--- Configuration & Creation Menu (Option 11) ---")
    print("1. Set Job Priority Label (US58)")
    print("2. View Unit Load History(US55)")
    print("0. Back to Main Menu")
while True:
    show_menu()
    print("\n")
    choice=input("Enter your choice ( 1 to 11):- ")

    # US1: Add job
    if choice == "1":
        print("=>Add a job (US1)")
        name = input("Enter job name: ")
        description = input("Enter job description: ")
        deadline = input("Enter job deadline (YYYY-MM-DD): ")

        job = s.add_job(name, description, deadline)
        # US16: Shows Description too long without crash
        if isinstance(job, str):
            print("\n" + job)
            continue
        print(f"\nJob added successfully! Job ID: {job.id}")

    # US2: List all Jobs
    elif choice == "2":
        print("=>List Jobs (US2)")
        jobs = s.list_jobs()
        if len(jobs) == 0:
            print("No jobs found.")
        else:
            for job in jobs:
                print(f"Job ID: {job.id}, ")
                print(f"Name: {job.name}, ")


    # US3: View a job
    elif choice == "3":
        print("\n=> View Job")
        job_id = int(input("Enter job ID to view: "))

        job = s.view_job(job_id)
        if job:
            print(f"Job ID: {job.id}")
            print(f"Name: {job.name}, ")
            print(f"Description: {job.description},")
            print(f"Deadline: {job.deadline}")
        else:
            print("\nJob not found.")

    # US4: Edit job description
    elif choice == "4":
        print("\n=> Edit Job Description")
        job_id = int(input("Enter job ID to edit: "))
        new_desc = input("Enter new job description: ")

        updated_job = s.edit_job_description(job_id, new_desc)
        if updated_job:
            print("\nJob description updated successfully!")
        else:
            print("\nJob not found.")

    # US5: Rename job
    elif choice == "5":
        print("\n=> Rename Job")
        job_id = int(input("Enter job ID to rename: "))
        new_name = input("Enter new job name: ")

        s1 = s.rename_job(job_id, new_name)
        if s1:
            print("\nJob renamed successfully!")
        else:
            print("\nJob not found.")

    # US6 Delete job
    elif choice == "6":
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

    # US8: View Units
    elif choice == "8":
        print("\n=> View Units")
        job_id = int(input("Enter job ID to view units: "))
        units = s.view_units(job_id)
        if units is None:
            print("\nJob not found.")
        else:
            if len(units) == 0:
                print("\nNo units added yet.")
            else:
                print("\nUnits for this job are: ")
                for unit in units:
                    print(f"\t-,{unit}")

    #US9: Complete Job
    elif choice=="9":
        print("\n=> Complete Job")
        job_id = int(input("Enter job ID to complete: "))
        unit = s.complete_job(job_id)
        if unit:
            print("\nJob marked as completed!")
        else:
            print("\nJob not found.")

    # US18: Clear completed Job
    elif choice == "10":
        print("\n=== Clear Completed Jobs ===")
        info = s.remove_completed_jobs()
        print(info)

    # US58/US55 Configuration Menu
    elif choice == "11":
        while True:
            show_config_menu()
            config_choice = input("\nEnter your configuration choice (1-2):- ")
            # US58: Set Job Priority Label
            if config_choice == "1":
                print("\n--- Set Priority Label (US58) ---")
                try:
                    level = int(input("Enter Priority Level to change (1 to 5): "))
                    if not (1 <= level <= 5):
                        raise ValueError

                    current_label = s.us6_get_priority_legend().get(level)
                    new_label = input(f"Enter NEW label for Priority {level} (Current: {current_label}): ")

                    if s.us6_set_priority_label(level, new_label):
                        print(f"\n Success! Priority {level} is now labeled '{new_label}'.")
                    else:
                        print("Error setting label.")
                except ValueError:
                    print("Invalid priority level entered. Must be an integer between 1 and 5.")

            # US55: View Unit History
            elif config_choice == "2":
                print("\n=> View Unit History")
                try:
                    unit_id = int(input("Enter Unit ID (e.g., 1 or 2) to view history: "))

                    # Call the US4 method added to your scheduler
                    history = s.us4_view_unit_history(unit_id)

                    if history:
                        print(f"\n--- History for Unit {unit_id} ---")
                        print(f"Total entries: {len(history)}")
                        print(f"Load History: {history}")
                    else:
                        print(f"Unit {unit_id} not found or history is empty.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                except AttributeError:
                    # Catch if the setup or method definition was skipped
                    print("Error: The us4_view_unit_history method is not fully implemented in the scheduler.")

        # 0. Back to Main Menu
            elif config_choice == "0":
                 break
            else:
                print("Invalid choice. Please try again.")
    # Exit from menu
    elif choice == "0":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")