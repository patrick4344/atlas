"""Text and CSV report builders."""

from __future__ import annotations

import csv
import io
from typing import Iterable

from .billing import billable_hours_by_project
from .models import CompanyState, TimeEntry
from .payroll import summarize_payroll


def payroll_text_report(state: CompanyState, entries: Iterable[TimeEntry]) -> str:
    rows = summarize_payroll(state, entries)
    lines = ["Payroll summary (gross labor, mock rules)", "-" * 40]
    for row in rows:
        lines.append(f"{row['name']:<24} ${row['gross_labor_usd']:>10,.2f}")
    if not rows:
        lines.append("(no billable labor in selection)")
    return "\n".join(lines) + "\n"


def utilization_csv(state: CompanyState, entries: Iterable[TimeEntry]) -> str:
    by_proj = billable_hours_by_project(state, entries)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["project_id", "code", "name", "hours", "notional_revenue_usd"])
    for pid in sorted(by_proj.keys()):
        proj = state.projects.get(pid)
        code = proj.code if proj else ""
        name = proj.name if proj else ""
        row = by_proj[pid]
        writer.writerow([pid, code, name, row["hours"], row["notional_revenue_usd"]])
    return buf.getvalue()
