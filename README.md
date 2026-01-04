# UnitJobScheduling System

## 1.Introduction 

The Unit Job Scheduling System is a Python based backend application developed as part of the group assignment. 
The system provides functionality for managing jobs, assigning units, tracking execution status and exporting metrics,
using a text-based interface only.

The project focuses on:
- Software quality assurance practices
- Agile development
- Black-box and white-box testing
- Test coverage measurement 

No graphical interface or database is used in line with the assignment requirements. All data is managed in memory or 
via simple text/CSV files.

---

## 2.Feature Implemented 

The system implements multiple user stories covering job and unit scheduling, execution control and metric reporting. 
Each user story is implemented and tested using the quality assurance techniques taught in the module.
- Add, view, list, rename, edit and delete jobs.
- Add and view units associated with jobs
- Mark jobs as completed
- Handle job priorities, retries, dependencies and timeouts
- Validate unit capacity before job assignment
- Export unit activity summaries and job metrics
- Track job execution patterns and resource usage

All features were implemented collaboratively with each team member responsible for defined set of user stories.

---

## 3.Project Structure

The project contains the following files:

Unit_Job_Scheduling/
│
|──Student ID/
│
├── tests/
│ ├── blackbox/
│ │ ├── boundary_value/
│ │ ├── category_partition/
│ │ ├── equivalence_partition/
│ │ └── random_testing/
│ │
│ └── whitebox/
│ ├── statement_coverage/
│ ├── branch_coverage/
│ ├── path_coverage/
│ ├── concolic_testing/
│ └── symbolic_execution/
│
└── README.md

## 4.How to Run the Application

**Software:** Python 3.10 or later

Steps:
    1. Open the project folder in Pycharm
    2. Ensure job_unit_scheduler.py and main.py are in the root directory
    3. Run the application: python main.py
    4. Use the on-screen menu to interact with the system.

## 5.Testing Approach

Testing was carried out using both Black-Box and White-Box techniques.

- **Black-box testing**
Black-box test validate system behaviour without considering internal implementation.
Techniques used:

- Boundary Value Analysis
- Equivalence Partitioning 
- Category Partitioning 

Each technique has its own test package under: test/blackbox
Test were written to validate correct handling of:

- Valid inputs
- Invalid inputs
- Edge and boundary cases

- **White-box testing**
White-box testing focuses on internal logic and control flow.
Techniques used:
- Statement Coverage
- Branch coverage
- Path Coverage
- Symbolic Execution
- Concolic Testing

White-box tests are organised under: test/whitebox

Each test file include comments explaining:

- Which code paths are being exercised 
- Which conditions or branches are covered 

## 6.Running Tests
- Run all tests: python -m unittest discover
- Run only black-box tests: python -m unittest discover test/blackbox
- Run only white-box tests: python -m unittest discover test/whitebox

All tests are expected to pass without errors.

---

## 7.Test Coverage Measurement
Coverage reflects focused testing of allocated user stories rather than full system execution, which is
consistent with the scope of individual contributions.
Coverage was measured using the coverage tool.

Command Used: coverage run -m unittest discover
              coverage report

**Notes**
- Coverage reflects only the parts of the system exercised by the implemented test cases 
- Coverage results are interpreted in relation to individual user story responsibilities, not full system execution
- Coverage output can be viewed directly in the terminal 

## 8. Generated Output Files
Some features generate output files during execution.

**Job Metrics**
- File: storage/job_metrics.csv
- Generated automatically when the Export Job Metrics option is selected in the menu
- No manual editing is required

## 9. Development Process
The project followed an Agile development approach, including:

- User stories
- Multiple sprints
- Individual responsibility per user story
- Version control using GitHub
- Incremental implementation and testing

Each user story was implemented, tested and committed separately to provide clear evidence of individual and group contributions.

## 10. Conclusion
The Unit Job Scheduling System demonstrates the application of:

- Software quality assurance techniques
- Systematic testing strategies
- Structured project organisation
- Agile development practices

All required functionality, testing techniques and documentation have been implemented in line with the assignment specification and marking criteria.
