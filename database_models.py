from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Employer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    additional_info: str = Field(default="")
    work_hours: List["WorkHours"] = Relationship(back_populates="employer")

class WorkHours(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employer_id: int = Field(foreign_key="employer.id")
    date: str = Field(...)
    hours: float = Field(...)
    employer: Optional[Employer] = Relationship(back_populates="work_hours")
