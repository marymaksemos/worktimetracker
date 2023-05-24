"""
Module: database_models
Description: Defines the database models for the WorkTimeTracker application.
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Employer(SQLModel, table=True):
    """Represents an employer."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    additional_info: str = Field(default="")
    hourly_rate: Optional[float] = Field(default=None)
    work_hours: List["WorkHours"] = Relationship(back_populates="employer")


class WorkHours(SQLModel, table=True):
    """Represents work hours."""

    id: Optional[int] = Field(default=None, primary_key=True)
    employer_id: int = Field(foreign_key="employer.id")
    date: str = Field(...)
    hours: float = Field(...)
    employer: Optional[Employer] = Relationship(back_populates="work_hours")
