# UnitJobScheduling System

## 1.Introduction 

The Unit Job Scheduling System is a command-line application developed in Python.
It allows users to manage jobs by creating, updating and tracking their completion status.
Each job can be associated with multiple units and jobs can be marked as completed once finished.

This project was developed following Agile principles using user stories, sprints and 
unit testing as covered in lecture and lab session.

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
- 
All features are implemented in accordance with the defined user stories (US1- US9).

---

## 3.User Story Trackable

Each user story is apply in the core system and validated according with unit tests

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
|-job_unit_scheduler.py         #Core application logic
|-main.py                       #Command-line interface
|-README.md                     #Project documentation 
|-.gitignore                    #Git ignore layout
|-.coverage
|
|-239067430
|-tests/
|-blackbox/
||--random_based/
|||---test_239067430_blackbox_random.py
||--specification_based/
|||---test_239067430_blackbox_specification.py
|-whitebox/
|-statement_branch/
|-test_239067430_whitebox_statement_branch.py

## 5.How to Run the Application

**Software:** Python 3.10 or later

Steps:
    1. Open terminal in the project root directory
    2. Run the application using : python main.py
    3. Follow the on-screen menu to perform job scheduling operations.

## 6.How to Run Tests

Automated tests are implemented using the unittest framework.

Steps:
    1. Open terminal in the project root directory
    2. Run all the tests using: python -m unittest discover -s 239067430/tests -p "test_*.py"
    3. If all tests pass, the process will end with exit code 0.

## 7.Testing Approach

The testing strategy includes:

- **Black-box testing**
- Random-based testing
- Specification-based testing
- **White-box testing**
- Statement and branch coverage

Each test validates:
- Correct system behaviour
- Expected outputs
- Proper handling of invalid inputs

Code coverage analysis was performed using the coverage tool to evaluate test effectiveness.

---

## 8.Conclusion

The Unit Job Scheduling System show the use of Agile development practices, modular design and systematic testing.
All required user stories have been implemented, tested and documented according to the module guideline.

