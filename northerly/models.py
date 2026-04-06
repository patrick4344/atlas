"""Domain models for employees, projects, and time entries."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
import uuid


def _new_id() -> str:
    return str(uuid.uuid4())[:8]


@dataclass
class Employee:
    employee_id: str
    full_name: str
    email: str
    hourly_rate_usd: float
    department: str
    active: bool = True

    @classmethod
    def create(
        cls,
        full_name: str,
        email: str,
        hourly_rate_usd: float,
        department: str,
    ) -> "Employee":
        return cls(
            employee_id=_new_id(),
            full_name=full_name.strip(),
            email=email.strip().lower(),
            hourly_rate_usd=float(hourly_rate_usd),
            department=department.strip(),
        )


@dataclass
class Project:
    project_id: str
    code: str
    name: str
    client: str
    bill_rate_usd: float

    @classmethod
    def create(cls, code: str, name: str, client: str, bill_rate_usd: float) -> "Project":
        return cls(
            project_id=_new_id(),
            code=code.strip().upper(),
            name=name.strip(),
            client=client.strip(),
            bill_rate_usd=float(bill_rate_usd),
        )


@dataclass
class TimeEntry:
    entry_id: str
    employee_id: str
    project_id: str
    work_date: date
    hours: float
    note: Optional[str] = None

    @classmethod
    def create(
        cls,
        employee_id: str,
        project_id: str,
        work_date: date,
        hours: float,
        note: Optional[str] = None,
    ) -> "TimeEntry":
        if hours <= 0:
            raise ValueError("hours must be positive")
        return cls(
            entry_id=_new_id(),
            employee_id=employee_id,
            project_id=project_id,
            work_date=work_date,
            hours=float(hours),
            note=(note or "").strip() or None,
        )


@dataclass
class CompanyState:
    employees: dict[str, Employee] = field(default_factory=dict)
    projects: dict[str, Project] = field(default_factory=dict)
    entries: dict[str, TimeEntry] = field(default_factory=dict)
