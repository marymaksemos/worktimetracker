"""
Module: database_manager
Description: Provides functions to manage the database for the WorkTimeTracker application.
"""

import datetime
import calendar
from typing import Optional
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy import func
from database_models import Employer, WorkHours


engine = create_engine("sqlite:///worktimetracker.db", echo=True)
session = Session(bind=engine)


def add_employer(name: str, additional_info: str = "", hourly_rate: Optional[float] = None):
    """
    Adds a new employer to the database.

    Args:
        name: The name of the employer.
        additional_info: Additional information about the employer (optional).
        hourly_rate: The hourly rate of the employer (optional).
    """
    employer = Employer(name=name, additional_info=additional_info, hourly_rate=hourly_rate)
    session.add(employer)
    session.commit()


def add_work_hours(employer_id: int, date: str, hours: float):
    """
    Adds work hours for a specific employer to the database.

    Args:
        employer_id: The ID of the employer.
        date: The date of the work hours in the format 'YYYY-MM-DD'.
        hours: The number of work hours.
    """
    employer = session.exec(select(Employer).where(Employer.id == employer_id)).first()
    work_hours = WorkHours(employer=employer, date=date, hours=hours)
    session.add(work_hours)
    session.commit()


def get_all_employers():
    """
    Retrieves all employers from the database.

    Returns:
        A list of all employers.
    """
    employers = session.exec(select(Employer)).all()
    return employers


def get_work_hours_by_employer(employer_id: int):
    """
    Retrieves work hours for a specific employer from the database.

    Args:
        employer_id: The ID of the employer.

    Returns:
        A list of work hours for the specified employer.
    """
    work_hours = (
        session.exec(select(WorkHours).where(WorkHours.employer_id == employer_id)).all()
    )
    return work_hours


def calculate_monthly_hours(employer_id: int, month: int, year: int) -> float:
    """
    Calculates the total work hours for a specific employer in a given month and year.

    Args:
        employer_id: The ID of the employer.
        month: The month (1-12).
        year: The year.

    Returns:
        The total work hours for the specified employer in the given month and year.
    """
    start_date = datetime.date(year, month, 1)
    end_date = start_date.replace(day=calendar.monthrange(year, month)[1])

    total_hours = (
        session.query(func.sum(WorkHours.hours))
        .filter(WorkHours.employer_id == employer_id)
        .filter(WorkHours.date >= start_date)
        .filter(WorkHours.date <= end_date)
        .scalar()
    )

    return total_hours or 0.0


def calculate_monthly_earnings(
    employer_id: int, month: int, year: int, pre_tax: bool = True
) -> float:
    """
        Calculates the monthly earnings for a specific employer in a given month and year.

        Args:
            employer_id: The ID of the employer.
            month: The month (1-12).
            year: The year.
            pre_tax: Whether to calculate earnings before tax (default: True).

        Returns:
            The monthly earnings for the specified employer in the given month and year.
        """
    employer = session.exec(select(Employer).where(Employer.id == employer_id)).first()
    hourly_rate = employer.hourly_rate
    total_hours = calculate_monthly_hours(employer_id, month, year)
    earnings = total_hours * hourly_rate
    if not pre_tax:
        # Apply tax rate (e.g., 0.3 for 30% tax)
        tax_rate = 0.3
        earnings *= (1 - tax_rate)
    return earnings


SQLModel.metadata.create_all(engine)
