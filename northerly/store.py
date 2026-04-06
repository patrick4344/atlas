"""JSON-backed persistence for company state."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any

from .config import DATA_DIR, DEFAULT_DB_PATH
from .models import CompanyState, Employee, Project, TimeEntry


def _date_encoder(obj: Any) -> Any:
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def state_to_dict(state: CompanyState) -> dict[str, Any]:
    return {
        "employees": {k: asdict(v) for k, v in state.employees.items()},
        "projects": {k: asdict(v) for k, v in state.projects.items()},
        "entries": {k: asdict(v) for k, v in state.entries.items()},
    }


def state_from_dict(payload: dict[str, Any]) -> CompanyState:
    state = CompanyState()
    for eid, row in payload.get("employees", {}).items():
        state.employees[eid] = Employee(**row)
    for pid, row in payload.get("projects", {}).items():
        state.projects[pid] = Project(**row)
    for xid, row in payload.get("entries", {}).items():
        row = dict(row)
        row["work_date"] = _parse_date(row["work_date"])
        state.entries[xid] = TimeEntry(**row)
    return state


def load_state(path: Path | None = None) -> CompanyState:
    path = path or DEFAULT_DB_PATH
    if not path.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return CompanyState()
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return state_from_dict(payload)


def save_state(state: CompanyState, path: Path | None = None) -> None:
    path = path or DEFAULT_DB_PATH
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(state_to_dict(state), f, indent=2, default=_date_encoder)
        f.write("\n")
    tmp.replace(path)
