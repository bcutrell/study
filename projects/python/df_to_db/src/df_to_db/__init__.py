"""

Resources:
    https://duckdb.org/2021/05/14/sql-on-pandas.html
    https://duckdb.org/docs/guides/sql_editors/dbeaver.html
"""

from df_to_db.adapters import FileAdapter, SQLiteAdapter, DuckDBAdapter


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
