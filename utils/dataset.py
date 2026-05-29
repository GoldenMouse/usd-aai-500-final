import pandas as pd
from pathlib import Path
from pandas import DataFrame


def load_csv(filename: str) -> DataFrame:
    """Load csv of filename into pandas df"""
    utils_dir = Path(__file__).resolve().parent
    data_dir = utils_dir.parent / "data"
    DATA_PATH = data_dir / "support2_complete.csv"
    df = pd.read_csv(DATA_PATH)
    return df


def get_project_root() -> Path:
    current = Path.cwd().resolve()

    while current != current.parent:
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            project_root = current
            break
        current = current.parent

    return project_root
