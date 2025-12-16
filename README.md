# UnitJobScheduling System

## 1.Introduction 
The Unit Job Scheduling System is a simple command-line application developed in Python.
This system is used to help users manage jobs by breaking them into smaller units, tracking progress and marking jobs as completed.

This project was developed following Agile principles using user stories, sprints and unit testing as covered in lecture and lab session.

---

## 2.Feature Implemented 
The system supports the following features, each mapped to user story:
- Add a new job
- List all jobs
- View a job by its ID
- Edit a job description
- Rename a job
- Delete a job
- Add units to a job
- View units of a job
- Mark a job as completed 
All features are implemented in accordance with the defined user stories (US1- US9).

---

## 3.User Story Trackable 

Each user story is apply in the core system and validated according with unit test

| User Story   |   Description          | Implementation               |   Test Case
|--------------|------------------------|------------------------------|----------------------
| US1          |   Add Job              |  'add_job()'                 | test_add_job()
| US2          |   List Job             |  'list_jobs()'               | test_list_jobs()
| US3          |   View Job             |  'view_job()'                | test_view_job()
| US4          |   Edit Job Description |  'edit_job_description()'    | test_edit_job_description()
| US5          |   Rename Job           |  'rename_job()'              | test_rename_job()
| US6          |   Delete Job           |  'delete_job()'              | test_delete_job()
| US7          |   Add Unit             |  'add_unit()'                | test_add_unit()
| US8          |   View Units           |  'view_units()'              | test_view_units()
| US9          |   Complete Job         |  'complete_job()'            | test_complete_job()

This ensures full trackable between requirements, implementation and testing.


## 4.Project Structure
The project contains the following files:
Unit_Job_scheduling/
|
|-Job_unit_Scheduler.py         #Core application logic
|-main.py                       #Command-line interface
|-test_job_unit_scheduler.py    #Unit tests
|-README.md                     #Project documentation 

## 5.How to Run the Application
**Software:** Python 3.10 or later

Steps:
    1. Open terminal in the project directory
    2. Run the application using : python main.py
    3. Follow the on-screen menu to perform job scheduling operations.

## 6.How to Run UnitTests
Unittests are written to verify the behaviour of all executed user stories.

Steps:
    1. Open terminal in the project directory
    2. Run the test file using: python test_job_unit_scheduler.py
    3. If all tests pass, the process will end with exit code 0.

## 7.Testing Approach
Each user story has a corresponding unit test to validate:

- Correct functionality
- Expected output
- Proper handling of invalid inputs

This ensures the reliability and correctness of the system.

---

## 8.Conclusion

The Unit Job Scheduling System show the use of Agile development practices, modular design and unit testing.
All required features have been implemented, tested and documented according to the module guideline.

