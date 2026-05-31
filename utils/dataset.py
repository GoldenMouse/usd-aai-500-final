import pandas as pd
from pathlib import Path
from pandas import DataFrame


def load_csv(filename: str) -> DataFrame:
    """Load csv of filename into pandas df"""
    utils_dir = Path(__file__).resolve().parent
    data_dir = utils_dir.parent / "data"
    DATA_PATH = data_dir / filename
    df = pd.read_csv(DATA_PATH)
    return df


def get_column_groups() -> dict:
    """Return the standard column groupings for the SUPPORT2 dataset."""
    return {
        "outcome": ["death", "hospdead", "d_time", "slos"],
        "id": ["id"],
        "target": "death_180d",
        "benchmark": ["surv2m", "surv6m", "aps", "sps", "prg2m", "prg6m", "dnr"],
        "lab": [
            "meanbp",
            "wblc",
            "hrt",
            "resp",
            "temp",
            "pafi",
            "alb",
            "bili",
            "crea",
            "sod",
            "ph",
            "glucose",
            "bun",
            "urine",
        ],
    }


def get_feature_cols(df: DataFrame) -> list:
    """Return feature column names by excluding outcome, id, target, and benchmark cols."""
    groups = get_column_groups()
    exclude = (
        groups["outcome"] + groups["id"] + [groups["target"]] + groups["benchmark"]
    )
    return [c for c in df.columns if c not in exclude]


def get_project_root() -> Path:
    current = Path.cwd().resolve()

    while current != current.parent:
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            project_root = current
            break
        current = current.parent

    return project_root
