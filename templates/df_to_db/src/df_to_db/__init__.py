"""

Resources:
    https://duckdb.org/2021/05/14/sql-on-pandas.html
    https://duckdb.org/docs/guides/sql_editors/dbeaver.html

"""
import os
import pandas as pd
from datetime import datetime

class Context:
    def __init__(self) -> None:
        self.config = { 
            "adapters": {
                "sqlite":   { "path": "db.sqlite" },
                "file":     { "path": "data" },
                "duckdb":   { "path": "db.duckdb" }
            }
        }
        self.db = None

class FileAdapter:
    def __init__(self, base_dir) -> None:
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def store(self, date, key, filename, df, extension="csv"):
        filename = f"{filename}.{extension}"
        date_str = date.strftime("%Y-%m-%d")
        key_dir = os.path.join(self.base_dir, date_str, key)
        os.makedirs(key_dir, exist_ok=True)
        file_path = os.path.join(key_dir, filename)
        df.to_csv(file_path, index=False)

    def load(self, date, key):
        date_str = date.strftime("%Y-%m-%d")
        key_dir = os.path.join(self.base_dir, date_str, key)
        if not os.path.exists(key_dir):
            return None
        
        for file in os.listdir(key_dir):
            file_path = os.path.join(key_dir, file)
            if file.lower().endswith('.csv'):
                return pd.read_csv(file_path)
            elif file.lower().endswith('.parquet'):
                return pd.read_parquet(file_path)
            elif file.lower().endswith('.json'):
                return pd.read_json(file_path)
        
        return None

    def list_dataframes(self):
        dataframes = []
        for root, dirs, files in os.walk(self.base_dir):
            date_str = os.path.basename(os.path.dirname(root))
            key = os.path.basename(root)
            for file in files:
                if file.lower().endswith(('.csv', '.parquet', '.json')):  # Add more extensions as needed
                    filename, extension = os.path.splitext(file)
                    dataframes.append((date_str, key, filename, extension[1:]))  # extension[1:] removes the leading dot
        return dataframes