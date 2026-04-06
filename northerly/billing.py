"""Simple utilization and billing helpers (internal reporting)."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import CompanyState, TimeEntry


def billable_hours_by_project(
    state: CompanyState,
    entries: Iterable[TimeEntry],
) -> dict[str, dict[str, float]]:
    """
    Aggregate hours and notional revenue per project.

    Revenue = hours * project bill_rate (mock; ignores write-offs).
    """
    hours: dict[str, float] = defaultdict(float)
    for entry in entries:
        hours[entry.project_id] += entry.hours

    result: dict[str, dict[str, float]] = {}
    for pid, hrs in hours.items():
        proj = state.projects.get(pid)
        rate = proj.bill_rate_usd if proj else 0.0
        result[pid] = {
            "hours": round(hrs, 2),
            "notional_revenue_usd": round(hrs * rate, 2),
        }
    return result
