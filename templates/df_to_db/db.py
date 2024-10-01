import os

import pandas as pd

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

    def store(self, date, key, df):
        # TODO key should be a subdirectory of date
        date_str = date.strftime("%Y-%m-%d")
        date_dir = os.path.join(self.base_dir, date_str)
        os.makedirs(date_dir, exist_ok=True)
        file_path = os.path.join(date_dir, f"{key}.csv")
        df.to_csv(file_path, index=False)

    def load(self, date, key):
        date_str = date.strftime("%Y-%m-%d")
        file_path = os.path.join(self.base_dir, date_str, f"{key}.csv")
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        return None
    
    def list_dataframes(self):
        dataframes = []
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith('.csv'):
                    date_str = os.path.basename(root)
                    key = os.path.splitext(file)[0]
                    dataframes.append((date_str, key))
        return dataframes


class DuckDBAdapter:
    pass

class SQLiteAdapter:
    pass

if __name__ == "__main__":
    ctx = Context()
    # FileAdapter
    file_adapter = FileAdapter(ctx.config["adapters"]["file"]["path"])
    file_adapter.store(pd.Timestamp("2021-01-01"), "example", pd.DataFrame({"a": [1, 2, 3]}))
    print(file_adapter.load(pd.Timestamp("2021-01-01"), "example"))
    print(file_adapter.list_dataframes())

    # DuckDBAdapter

    # SQLiteAdapter