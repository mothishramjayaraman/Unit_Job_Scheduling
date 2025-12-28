from job_unit_scheduler import JobUnitScheduler
from datetime import datetime

s = JobUnitScheduler()

s.add_unit(1, ['GPU', 'High_Mem', 'NVMe'])
s.units[0].current_load = 80.0
s.units[0].historical_loads = [60.0, 70.0, 80.0]
s.add_unit(2, ['CPU', 'Storage', 'NVMe'])
s.units[1].current_load = 15.0
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
    print("11. Job/Unit Configuration Menu")
    print("12. Tag Job with description(Add/Remove/Filter)(US20)")
    print("13. Unit Capacity Validation(US43)")
    print("14. Job Retry Mechanism(US44)")
    print("15. View Unit Error Logs (US46)")
    print("16. View Unit Health Status (US17)")
    print("17. Job Dependency Checker (US45)")
    print("18. Export Unit Activity Summary (US48)")
    print("19. Auto-Escalate Job Priority (US19)")
    print("20. Job Timeout Handling (US69)")
    print("21. Job Resource Overconsumption Detection (US51)")
    print("22. Schedule Job (Preemption Rules) (US14)")
    print("23. Mark Job as Failed (US42)")
    print("24. Auto-Cancel Stalled Jobs (US50)")
    print("25. Analyze Job Execution Patterns (US52)")
    print("26. Predict Next Available Unit Slot (US47)")
    print("27. Export Job Metrics (US15)")
    print("0. Exit")

def show_config_menu():
    print("\n--- Configuration & Creation Menu (Option 11) ---")
    print("1. Set Job Priority Label (US58)")
    print("2. View Unit Load History(US55)")
    print("3. View Job Priority Legend(US57)")
    print("4. Reset Unit Load History (US61)")
    print("5. List System Capabilities(US62)")
    print("6. Configure Default Deadline(US60)")
    print("7. Enable/Disable Job Logging (US59)")
    print("8. Remove Unit From Scheduler (US56)")
    print("9. Mark Unit as Preferred(US54)")
    print("0. Back to Main Menu")

def show_timeout_menu():
    print("\n--- Job Timeout Handling (US67) ---")
    print("1. Start Job Execution")
    print("2. Check Job Timeouts")
    print("0. Back to Main Menu")

def input_optional(prompt: str):
    value = input(prompt).strip()
    return value if value else None

while True:
    show_menu()
    print("\n")
    choice=input("Enter your choice ( 1 to 27):- ")

    # US1: Add job
    if choice == "1":
        print("=>Add a job (US1)")
        name = input("Enter job name: ")
        description = input("Enter job description: ")
        deadline = input("Enter job deadline (YYYY-MM-DD): ")
        try:
            req_cap = float(input("Enter capacity required for this job (default 10.0): ") or 10.0)
        except ValueError:
            req_cap = 10.0
        priority = int(input("Enter job priority (1=Critical, 5=Background): "))
        job = s.add_job(name, description, deadline, priority=priority, required_capacity=req_cap)
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
                print(f"Status: {job.status}")

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
            print(f"Status: {job.status}")
            print(f"Retry Count: {job.retry_count}/{job.max_retries}")
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
        completed_jobs = [job for job in s.jobs if job.complete]
        info = s.remove_completed_jobs()
        print(info)

        if completed_jobs:
            print("\nRemoved Completed Jobs:")
            for job in completed_jobs:
                print("--------------------------------")
                print(f"Job ID      : {job.id}")
                print(f"Name        : {job.name}")
                print(f"Description : {job.description}")
                print(f"Priority    : {job.priority}")
                print(f"Deadline    : {job.deadline}")
                print(f"Tags        : {job.tags}")
        else:
            print("No completed jobs to remove.")

    # US58/US55 Configuration Menu
    elif choice == "11":
        while True:
            show_config_menu()
            config_choice = input("\nEnter your configuration choice (1-9):- ")
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
                print("\n=> View Unit History(US55)")
                try:
                    unit_id = int(input("Enter Unit ID (e.g., 1 or 2) to view history: "))


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

                    print("Error: The view_unit_history method is not fully implemented in the scheduler.")
            # US57: View Job Priority Legend
            elif config_choice == "3":
                print("\n--- Job Priority Legend (US57) ---")
                legend = s.us57_get_priority_legend()
                for level, label in sorted(legend.items()):
                    print(f"Priority P{level}: {label}")
            # US61: Reset Unit Load History
            elif config_choice == "4":
                print("\n--- Reset Unit History (US61) ---")
                try:
                    u_id = int(input("Enter Unit ID to reset history: "))
                    if s.us61_reset_unit_history(u_id):
                            print(f"Success! Performance metrics for Unit {u_id} have been cleared.")
                    else:
                            print(" Error: Unit ID not found in the system.")
                except ValueError:
                        print("Invalid input. Please enter a numerical Unit ID.")

            # US62: List System Capabilities
            elif config_choice == "5":
                        print("\n--- List System Capabilities (US62) ---")
                        capabilities = s.us7_list_capabilities()
                        if capabilities:
                            print("The following capabilities are available in the cluster:")
                            for cap in capabilities:
                                print(f" - {cap}")
                        else:
                            print("No units have been added yet. The master capability list is empty.")

            # US60: Configure Default Deadline
            elif config_choice == "6":
                        print(f"\n--- Configure Default Deadline (US60) ---")

                        print(f"Current Default Deadline: {s.default_deadline_hours} hours.")

                        try:
                            new_hours = int(input("Enter NEW default hours for job deadlines (e.g., 24, 72): "))

                            if s.us60_set_default_deadline(new_hours):
                                print(f"\n Success! New default deadline set to {new_hours} hours.")
                            else:
                                print("Error: Deadline must be a positive number of hours.")
                        except ValueError:
                            print(" Invalid input. Please enter a whole number.")

            # US59: Enable/Disable Job Logging
            elif config_choice == "7":
                print("\n--- Job Logging Configuration (US59) ---")
                try:
                    j_id = int(input("Enter Job ID to configure logging: "))
                    status_input = input("Enable detailed logging? (yes/no): ").lower()

                    enable = True if status_input == "yes" else False

                    if s.us59_toggle_logging(j_id, enable):
                        status_text = "ENABLED" if enable else "DISABLED"
                        print(f"Success! Detailed logging is now {status_text} for Job {j_id}.")
                    else:
                        print("Error: Job ID not found.")
                except ValueError:
                    print("Invalid input. Please enter a numerical Job ID.")

            # US56: Remove Unit from Scheduler
            elif config_choice == "8":
                    print("\n--- Remove Unit from scheduler (US56) ---")
                    try:
                        u_id = int(input("Enter Unit ID to remove from scheduler inventory: "))
                        if s.us56_remove_unit(u_id):
                            print(f"Success! Unit {u_id} has been removed and capabilities updated.")
                        else:
                            print("Error: Unit ID not found in scheduler inventory.")
                    except ValueError:
                        print("Invalid input. Please enter a numerical Unit ID.")

            # US54: Mark Unit as Preferred
            elif config_choice == "9":
                        print("\n--- Mark Unit as Preferred (US54) ---")
                        try:
                            u_id = int(input("Enter Unit ID to change preference: "))
                            status_input = input("Mark as Preferred? (yes/no): ").lower()

                            is_pref = True if status_input == "yes" else False

                            if s.us54_set_unit_preference(u_id, is_pref):
                                status_text = "PREFERRED" if is_pref else "NORMAL"
                                print(f"Success! Unit {u_id} status updated to {status_text}.")
                            else:
                                print("Error: Unit ID not found.")
                        except ValueError:
                            print("Invalid input. Please enter a numerical Unit ID.")

        # 0. Back to Main Menu
            elif config_choice == "0":
                 break
            else:
                print("Invalid choice. Please try again.")

    # US20:Tag job with categories(add/remove/filter)
    elif choice == "12":
        print("\n=> Tag Job With Categories (US20)")
        print("1. Add Tag")
        print("2. Remove Tag")
        print("3. Filter Jobs by Tag")
        print("0. Back to Main Menu")

        sub_choice = input("Enter your choice: ")
        if sub_choice == "1":
            print("\n Tags List:")
            for tag_item in s.TAGS_CONTAINER:
                print(f"- {tag_item}")
            jobId = int(input("Enter job ID: "))
            tag_name = input("Enter tag to add: ").lower()
            result = s.add_jobtag(jobId, tag_name)
            print(result)
            job = s.get_job(jobId)
            if job:
                print("--------------------------------")
                print(f"Job ID      : {job.id}")
                print(f"Name        : {job.name}")
                print(f"Description : {job.description}")
                print(f"Priority    : {job.priority}")
                print(f"Deadline    : {job.deadline}")
                print(f"Tags        : {job.tags}")
                print(f"Completed   : {job.complete}")

        #Remove tag
        elif sub_choice == "2":
            job_id = int(input("Enter job ID: "))
            tag = input("Enter tag to remove: ")
            currentJob = s.remove_jobtag(job_id, tag)
            print(currentJob)

        #Filter tag
        elif sub_choice == "3":
            tag = input("Enter tag to filter jobs: ")
            jobs = s.filter_jobtag(tag)
            if not jobs:
                print("Give correct tag.")
            else:
                print(f"\nJobs with tag: {tag}")
                for job in jobs:
                    print("--------------------------------")
                    print(f"Job ID      : {job.id}")
                    print(f"Name        : {job.name}")
                    print(f"Description : {job.description}")
                    print(f"Priority    : {job.priority}")
                    print(f"Deadline    : {job.deadline}")
                    print(f"Tags        : {job.tags}")
                    print(f"Completed   : {job.complete}")
        elif sub_choice == "0":
            pass  # menu

        else:
            print("Invalid sub choice.")
    # US43: Unit Capacity Validation
    elif choice == "13":
        print("\n=> Assign Job with Capacity Validation & Dependency Validation (US43/45)")
        try:
            job_id_input = int(input("Enter Job ID: "))

            if not s.check_dependencies_met(job_id_input):
                print("\nRejected: Prerequisite jobs are not yet completed.")
                continue

            unit_id_input = int(input("Enter Unit ID: "))
            result = s.us43_validate_and_assign(job_id_input, unit_id_input)
            print(f"\nValidation Result: {result}")

        except ValueError:
            print("Invalid input. Please enter numerical IDs for Job and Unit.")

    # US44: Job Retry Mechanism
    elif choice == "14":
        print("\n=> Report Job Failure & Retry (US44)")
        try:
            job_id_input = int(input("Enter Job ID that failed: "))
            result = s.us44_fail_and_retry_job(job_id_input)
            print(f"\nSystem Action: {result}")
        except ValueError:
            print("Invalid input. Please enter a numerical Job ID.")
    # US46: Unit-Level Error Log Viewer
    elif choice == "15":
            print("\n=> View Unit Error Logs (US46)")
            try:
                unit_id_input = int(input("Enter Unit ID to view logs: "))
                logs = s.get_unit_error_logs(unit_id_input)

                if not logs:
                    print(f"No error logs found for Unit {unit_id_input}.")
                else:
                    print(f"\n--- Error Logs for Unit {unit_id_input} ---")
                    for log in logs:
                        print(log)
            except ValueError:
                print("Invalid input. Please enter a numerical Unit ID.")

    # US17: Unit Health Status Tracking
    elif choice == "16":
        print("\n=> Unit Health Status (US‑U8)")

        status = s.unit_health_status()

        if not status:
            print("No units available.")
        else:
            for u in status:
                print("--------------------------------")
                print(f"Unit ID        : {u['unit_id']}")
                print(f"Load           : {u['current_load']} / {u['max_capacity']}")
                print(f"Load %         : {u['load_percent']}%")
                print(f"Health Status  : {u['health']}")
    # US45: Job Dependency Checker (US45)
    elif choice == "17":
        print("\n=> Job Dependency Checker (US45)")
        try:
            target_id = int(input("Enter Job ID that needs a dependency: "))
            depends_on = int(input("Enter Job ID it must wait for: "))
            result = s.add_dependency(target_id, depends_on)
            print(f"\nResult: {result}")
        except ValueError:
            print("Invalid input. Please enter numerical IDs.")

    # US48: Export Unit Activity Summary
    elif choice == "18":
        print("\n=> Export Unit Activity Summary (US48)")
        try:
            u_id = int(input("Enter Unit ID to generate text report: "))
            result = s.export_unit_activity_summary(u_id)
            print(f"\n{result}")
        except ValueError:
            print("Invalid input. Please enter a numerical Unit ID.")

    # US19: Auto-Escalate Job Priority
    elif choice == "19":
        print("\n=> Auto-Escalate Job Priority (US19)")

        escalated = s.us19_auto_escalate_job_priority()

        if not escalated:
            print("No jobs required priority escalation.")
        else:
            print("\nEscalated Jobs:")
            for job in escalated:
                print("--------------------------------")
                print(f"Job ID        : {job.id}")
                print(f"Job Name      : {job.name}")
                print(f"New Priority  : P{job.priority}")
                print(f"Deadline      : {job.deadline}")
                print(f"Log Entries   : {len(job.priority_change_log)}")

    # US69: Automatic Job Timeout Handling(start/check)
    elif choice == "20":
        while True:
            show_timeout_menu()
            sub_choice = input("Enter your choice: ")
            # Start Job
            if sub_choice == "1":
                print("\n=> Start Job Execution")
                try:
                    job_id = int(input("Enter Job ID to start: "))
                    max_runtime = int(input("Enter max runtime in seconds: "))
                    result = s.start_job(job_id, max_runtime)
                    print(result)
                except ValueError:
                    print("Invalid input. Please enter numeric values.")

            # Check Timeouts
            elif sub_choice == "2":
                print("\n=> Checking Job Timeouts")
                timed_out_jobs = s.check_job_timeouts()

                if not timed_out_jobs:
                    print("No jobs have timed out.")
                else:
                    print("\nTimed Out Jobs:")
                    for job in timed_out_jobs:
                        print("--------------------------------")
                        print(f"Job ID        : {job.id}")
                        print(f"Job Name      : {job.name}")
                        print(f"Status        : {job.status}")
                        print(f"Failures      : {job.failure_count}")
                        print(f"Last Error    : {job.last_error_message}")
            elif sub_choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
    elif choice == "21":
        print("\n=> Job Resource Overconsumption Detection #51")
        try:
            target_job_id = int(input("Enter Job ID to validate: "))
            measured_usage = float(input("Enter measured resource usage from system: "))

            result = s.job_resource_overconsumption_detection_51(target_job_id, measured_usage)
            print(f"\n{result}")
        except ValueError:
            print("Invalid input. Please enter numbers for Job ID and Usage.")

    # US14: Schedule Job Preemption Rules
    elif choice == "22":
        print("\n=> Schedule Job with Preemption (US14)")
        try:
            job_id = int(input("Enter Job ID to schedule: "))
            result = s.schedule_job(job_id)
            print(result)
            job = s.view_job(job_id)
            if job:
                print(f"Job {job.id} status → {job.status}")
        except ValueError:
            print("Invalid input. Please enter a numerical Job ID.")
    elif choice == "23":
        print("\n=== Mark Job as Failed (US42) ===")
        try:
            job_id = int(input("Enter job ID: "))
            message = input("Enter failure reason: ").strip() or "Unknown error"

            result = s.mark_job_failed(job_id, message)
            print(result)

            job = s.view_job(job_id)
            if job:
                print("--------------------------------")
                print(f"Job ID        : {job.id}")
                print(f"Status        : {job.status}")
                print(f"Retries       : {job.retry_count}/{job.max_retries}")
                print(f"Last Error    : {job.last_error_message}")

        except ValueError:
            print("Invalid input. Please enter a numerical Job ID.")

    elif choice == "24":
        print("\n=> Auto-Cancel Stalled Jobs #50")
        try:
            threshold = int(input("Enter stall threshold in seconds (default 300): ") or 300)

            cancelled_jobs = s.auto_cancel_stalled_jobs_50(threshold)

            if not cancelled_jobs:
                print("No stalled jobs detected.")
            else:
                print(f"\nSuccessfully cancelled {len(cancelled_jobs)} stalled job(s):")
                for job in cancelled_jobs:
                    print(f" - [ID: {job.id}] {job.name} (Stalled for > {threshold}s)")
        except ValueError:
            print("Invalid input. Please enter a number for the threshold.")

        # US52: Job Execution Pattern Analyzer
    elif choice == "25":
        print("\n=> Job Execution Pattern Analyzer #52")
        analysis = s.analyze_execution_patterns_52()

        if not analysis['total_jobs']:
            print("No job data available to analyze yet.")
        else:
            print(f"--- System Analysis Report ---")
            print(f"Total Jobs Processed: {analysis['total_jobs']}")
            print(f"Average Execution Time: {analysis['avg_runtime']:.2f} seconds")

            print("\n[Peak Submission Times]")
            if not analysis['peak_hours']:
                print(" - Not enough data for peak hour mapping.")
            for hour, count in analysis['peak_hours'].items():
                print(f" - {hour:02}:00 : {count} jobs submitted")

            print("\n[Slowest Jobs (Top 3)]")
            if not analysis['slow_jobs']:
                print(" - No completed jobs found to measure speed.")
            for job_info in analysis['slow_jobs']:
                print(f" - ID: {job_info['id']} | Name: {job_info['name']} | Time: {job_info['runtime']:.2f}s")

            print("\n[Priority Distribution]")
            for p_level, count in analysis['priority_counts'].items():
                print(f" - Priority P{p_level}: {count} jobs")
    # US47: Predict Next Available Unit Slot
    elif choice == "26":
        print("\n=> Predict Next Available Unit Slot #47")
        try:
            u_id = int(input("Enter Unit ID to check availability: "))
            prediction = s.predict_next_slot_47(u_id)

            if "Error" in prediction:
                print(f"\n{prediction}")
            else:
                print(f"\n--- Availability Prediction for Unit {u_id} ---")
                print(f"Current Load: {prediction['current_load']}%")
                print(f"Status      : {prediction['status']}")
                print(f"Next Slot   : {prediction['next_slot_estimate']}")

                if prediction['available_now']:
                    print(" This unit can accept new jobs immediately.")
                else:
                    print(" This unit is currently at high capacity.")
        except ValueError:
            print("Invalid input. Please enter a numerical Unit ID.")

    #US15: Job export Metrics
    elif choice == "27":
        print("\n=== Export Job Metrics ===")
        path = input_optional(
            "Enter output CSV path (default: storage/job_metrics.csv): "
        )
        result = s.export_job_metrics(path)
        print(result)
    # Exit from menu
    elif choice == "0":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")

