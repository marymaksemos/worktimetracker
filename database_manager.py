from sqlmodel import SQLModel, create_engine, Session, select
from database_models import Employer, WorkHours

def add_employer(name: str, additional_info: str = ""):
    with Session(engine) as session:
        employer = Employer(name=name, additional_info=additional_info)
        session.add(employer)
        session.commit()

def add_work_hours(employer_id: int, date: str, hours: float):
    with Session(engine) as session:
        employer = session.exec(select(Employer).where(Employer.id == employer_id)).first()
        work_hours = WorkHours(employer=employer, date=date, hours=hours)
        session.add(work_hours)
        session.commit()


def get_all_employers():
    with Session(engine) as session:
        employers = session.exec(select(Employer)).all()
        return employers

def get_work_hours_by_employer(employer_id: int):
    with Session(engine) as session:
        work_hours = (
            session.exec(select(WorkHours).where(WorkHours.employer_id == employer_id)).all()
        )
        return work_hours

engine = create_engine("sqlite:///worktimetracker.db", echo=True)
SQLModel.metadata.create_all(engine)
