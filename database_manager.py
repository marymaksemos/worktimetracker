import datetime
import calendar
from sqlmodel import SQLModel, create_engine, Session, select
from database_models import Employer, WorkHours
from typing import Optional
from sqlalchemy import func

engine = create_engine("sqlite:///worktimetracker.db", echo=True)
session = Session(bind=engine)


def add_employer(name: str, additional_info: str = "", hourly_rate: Optional[float] = None):
    employer = Employer(name=name, additional_info=additional_info, hourly_rate=hourly_rate)
    session.add(employer)
    session.commit()


def add_work_hours(employer_id: int, date: str, hours: float):
    employer = session.exec(select(Employer).where(Employer.id == employer_id)).first()
    work_hours = WorkHours(employer=employer, date=date, hours=hours)
    session.add(work_hours)
    session.commit()


def get_all_employers():
    employers = session.exec(select(Employer)).all()
    return employers


def get_work_hours_by_employer(employer_id: int):
    work_hours = (
        session.exec(select(WorkHours).where(WorkHours.employer_id == employer_id)).all()
    )
    return work_hours


def calculate_monthly_hours(employer_id: int, month: int, year: int) -> float:
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
