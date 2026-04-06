"""Payroll calculations from logged time."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Iterable

from .config import OVERTIME_MULTIPLIER, STANDARD_WEEKLY_HOURS
from .models import CompanyState, TimeEntry


def _week_key(d: date) -> tuple[int, int]:
    """ISO year and week number for grouping."""
    iso = d.isocalendar()
    return (iso.year, iso.week)


def labor_cost_for_entries(
    state: CompanyState,
    entries: Iterable[TimeEntry],
) -> dict[str, float]:
    """
    Return per-employee gross labor cost for the given entries.

    Overtime applies to hours beyond STANDARD_WEEKLY_HOURS per ISO week,
    per employee (simplified rule).
    """
    by_emp_week: dict[tuple[str, tuple[int, int]], float] = defaultdict(float)
    for entry in entries:
        emp = state.employees.get(entry.employee_id)
        if not emp or not emp.active:
            continue
        key = (entry.employee_id, _week_key(entry.work_date))
        by_emp_week[key] += entry.hours

    regular: dict[tuple[str, tuple[int, int]], float] = {}
    overtime: dict[tuple[str, tuple[int, int]], float] = {}
    for key, total in by_emp_week.items():
        reg = min(total, STANDARD_WEEKLY_HOURS)
        ot = max(0.0, total - STANDARD_WEEKLY_HOURS)
        regular[key] = reg
        overtime[key] = ot

    costs: dict[str, float] = defaultdict(float)
    for (emp_id, _), hours in regular.items():
        rate = state.employees[emp_id].hourly_rate_usd
        costs[emp_id] += hours * rate
    for (emp_id, _), hours in overtime.items():
        rate = state.employees[emp_id].hourly_rate_usd
        costs[emp_id] += hours * rate * OVERTIME_MULTIPLIER

    return dict(costs)


def summarize_payroll(state: CompanyState, entries: Iterable[TimeEntry]) -> list[dict]:
    """Rows suitable for printing or CSV export."""
    entry_list = list(entries)
    costs = labor_cost_for_entries(state, entry_list)
    rows = []
    for emp_id, amount in sorted(costs.items(), key=lambda x: x[1], reverse=True):
        emp = state.employees.get(emp_id)
        name = emp.full_name if emp else emp_id
        rows.append(
            {
                "employee_id": emp_id,
                "name": name,
                "gross_labor_usd": round(amount, 2),
            }
        )
    return rows
