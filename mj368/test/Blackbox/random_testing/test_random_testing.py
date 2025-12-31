import random
import string
from job_unit_scheduler import JobUnitScheduler

# User Story #16 – Randomised description testing
def test_random_description_lengths():
    scheduler = JobUnitScheduler()

    for _ in range(10):
        length = random.randint(1, 150)
        desc = ''.join(random.choices(string.ascii_letters, k=length))
        scheduler.add_job("Job", desc)
