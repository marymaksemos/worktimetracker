"""
Module: test_database_manager
Description: Unit tests for the database manager module.
"""

import unittest
from sqlmodel import Session, select
from sqlalchemy import create_engine
from app.database.database_models import Employer, WorkHours


class DatabaseManagerTestCase(unittest.TestCase):
    """Test case for the database manager."""

    def setUp(self):
        """Set up the test case."""
        # Set up an in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:")
        Employer.metadata.create_all(self.engine)
        WorkHours.metadata.create_all(self.engine)

        # Create a session
        self.session = Session(self.engine)

    def tearDown(self):
        """Tear down the test case."""
        # Rollback the current transaction and close the session
        self.session.rollback()
        self.session.close()

    def test_add_employer(self):
        """Test adding an employer."""
        employer = Employer(name="Test Employer", additional_info="Some info", hourly_rate=10.0)
        self.session.add(employer)
        self.session.commit()

        employers = self.session.exec(select(Employer)).all()
        self.assertEqual(len(employers), 1)
        self.assertEqual(employers[0].name, "Test Employer")
        self.assertEqual(employers[0].additional_info, "Some info")
        self.assertEqual(employers[0].hourly_rate, 10.0)

    def test_add_work_hours(self):
        """Test adding work hours."""
        employer = Employer(name="Test Employer", additional_info="Some info", hourly_rate=10.0)
        self.session.add(employer)
        self.session.commit()

        work_hours = WorkHours(employer_id=employer.id, date="2023-05-01", hours=8.0)
        self.session.add(work_hours)
        self.session.commit()

        work_hours = self.session.exec(select(WorkHours)).all()
        self.assertEqual(len(work_hours), 1)
        self.assertEqual(work_hours[0].employer_id, employer.id)
        self.assertEqual(work_hours[0].date, "2023-05-01")
        self.assertEqual(work_hours[0].hours, 8.0)

    def test_calculate_monthly_earnings(self):
        """Test calculating monthly earnings."""
        employer = Employer(name="Test Employer", additional_info="Some info", hourly_rate=10.0)
        self.session.add(employer)
        self.session.commit()

        work_hours = WorkHours(employer_id=employer.id, date="2023-05-01", hours=8.0)
        self.session.add(work_hours)
        self.session.commit()

        monthly_earnings = self.session.exec(
            select(
                WorkHours.employer_id,
                WorkHours.date,
                (WorkHours.hours * Employer.hourly_rate).label("earnings"),
            )
            .join(Employer)
            .group_by(WorkHours.employer_id, WorkHours.date)
        ).all()

        self.assertEqual(len(monthly_earnings), 1)
        self.assertEqual(monthly_earnings[0].employer_id, employer.id)
        self.assertEqual(monthly_earnings[0].date, "2023-05-01")
        self.assertEqual(monthly_earnings[0].earnings, 80.0)


if __name__ == "__main__":
    unittest.main()
