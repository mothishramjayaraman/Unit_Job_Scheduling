import unittest
import random
import string

from job_unit_scheduler import JobUnitScheduler


class TestRandomDescriptionLengths(unittest.TestCase):
    """
    Black-box Testing – Random Testing
    User Story #16: Randomised Job Description Lengths
    """

    def test_random_description_lengths(self):
        scheduler = JobUnitScheduler()

        for _ in range(10):
            length = random.randint(1, 150)
            desc = ''.join(random.choices(string.ascii_letters, k=length))

            # The system should handle random inputs without crashing
            result = scheduler.add_job("Job", desc)
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
