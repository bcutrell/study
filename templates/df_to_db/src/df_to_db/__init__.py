"""

Resources:
    https://duckdb.org/2021/05/14/sql-on-pandas.html
    https://duckdb.org/docs/guides/sql_editors/dbeaver.html

"""

"""
Resources:
    https://duckdb.org/2021/05/14/sql-on-pandas.html
    https://duckdb.org/docs/guides/sql_editors/dbeaver.html
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple
import pandas as pd


class Context:
    def __init__(self) -> None:
        self.config = {
            "adapters": {
                "sqlite": {"path": "db.sqlite"},
                "file": {"path": "data"},
                "duckdb": {"path": "db.duckdb"},
            }
        }
        self.db = None


class FileAdapter:
    def __init__(self, base_dir: str) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def store(
        self,
        date: datetime,
        key: str,
        filename: str,
        df: pd.DataFrame,
        extension: str = "csv",
    ) -> None:
        filename = f"{filename}.{extension}"
        date_str = date.strftime("%Y-%m-%d")
        key_dir = self.base_dir / date_str / key
        key_dir.mkdir(parents=True, exist_ok=True)
        file_path = key_dir / filename
        df.to_csv(file_path, index=False)

    def load(self, date: datetime, key: str) -> Optional[pd.DataFrame]:
        date_str = date.strftime("%Y-%m-%d")
        key_dir = self.base_dir / date_str / key
        if not key_dir.exists():
            return None

        for file in key_dir.iterdir():
            if file.suffix.lower() == ".csv":
                return pd.read_csv(file)
            elif file.suffix.lower() == ".parquet":
                return pd.read_parquet(file)
            elif file.suffix.lower() == ".json":
                return pd.read_json(file)
        return None

    def list_dataframes(self) -> List[Tuple[str, str, str, str]]:
        dataframes = []
        for root, dirs, files in os.walk(self.base_dir):
            root_path = Path(root)
            date_str = root_path.parent.name
            key = root_path.name
            for file in files:
                file_path = root_path / file
                if file_path.suffix.lower() in (
                    ".csv",
                    ".parquet",
                    ".json",
                ):  # Add more extensions as needed
                    filename = file_path.stem
                    extension = file_path.suffix[1:]  # Remove the leading dot
                    dataframes.append((date_str, key, filename, extension))
        return dataframes
