"""Application paths and constants."""

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent
DATA_DIR = REPO_ROOT / "data"
DEFAULT_DB_PATH = DATA_DIR / "northerly_state.json"

# Fiscal settings (simplified US-style mock)
STANDARD_WEEKLY_HOURS = 40.0
OVERTIME_MULTIPLIER = 1.5
