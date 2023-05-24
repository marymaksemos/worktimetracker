"""
Module: test_database_models
Description: Unit tests for the database_models module.
"""

import unittest
from app.database_models import Employer, WorkHours


class TestDatabaseModels(unittest.TestCase):
    """
    Test cases for the database models.
    """

    def test_employer_model(self):
        """
        Test the Employer model.
        """
        employer = Employer(
            name="Ica", additional_info="Manager", hourly_rate=10.0)
        self.assertEqual(employer.name, "Ica")
        self.assertEqual(employer.additional_info, "Manager")
        self.assertEqual(employer.hourly_rate, 10.0)

    def test_workhours_model(self):
        """
        Test the WorkHours model.
        """
        work_hours = WorkHours(employer_id=1, date="2023-05-24", hours=8.0)
        self.assertEqual(work_hours.employer_id, 1)
        self.assertEqual(work_hours.date, "2023-05-24")
        self.assertEqual(work_hours.hours, 8.0)


if __name__ == "__main__":
    unittest.main()
