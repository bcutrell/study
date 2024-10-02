class TestDuckDBAdapter:
    @pytest.fixture
    def duckdb_adapter(self, tmp_path):
        db_path = str(tmp_path / "test.duckdb")
        adapter = DuckDBAdapter(db_path)
        yield adapter
        adapter.conn.close()

    def test_store_and_load(self, duckdb_adapter, sample_df, date, key):
        duckdb_adapter.store(date, key, sample_df)
        loaded_df = duckdb_adapter.load(date, key)
        pd.testing.assert_frame_equal(sample_df, loaded_df)

    def test_list_dataframes(self, duckdb_adapter, sample_df, date):
        duckdb_adapter.store(date, "key1", sample_df)
        duckdb_adapter.store(date, "key2", sample_df)
        dataframes = duckdb_adapter.list_dataframes()
        assert set(dataframes) == {("2021-01-01", "key1"), ("2021-01-01", "key2")}

    def test_load_nonexistent(self, duckdb_adapter, date, key):
        assert duckdb_adapter.load(date, key) is None

class TestSQLiteAdapter:
    @pytest.fixture
    def sqlite_adapter(self, tmp_path):
        db_path = str(tmp_path / "test.sqlite")
        adapter = SQLiteAdapter(db_path)
        yield adapter
        adapter.conn.close()

    def test_store_and_load(self, sqlite_adapter, sample_df, date, key):
        sqlite_adapter.store(date, key, sample_df)
        loaded_df = sqlite_adapter.load(date, key)
        pd.testing.assert_frame_equal(sample_df, loaded_df)

    def test_list_dataframes(self, sqlite_adapter, sample_df, date):
        sqlite_adapter.store(date, "key1", sample_df)
        sqlite_adapter.store(date, "key2", sample_df)
        dataframes = sqlite_adapter.list_dataframes()
        assert set(dataframes) == {("2021-01-01", "key1"), ("2021-01-01", "key2")}

    def test_load_nonexistent(self, sqlite_adapter, date, key):
        assert sqlite_adapter.load(date, key) is None

    class DuckDBAdapter:
    def __init__(self, db_path):
        self.conn = duckdb.connect(db_path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS metadata (date DATE, key VARCHAR, table_name VARCHAR)")

    def store(self, date, key, df):
        table_name = f"data_{date.strftime('%Y_%m_%d')}_{key}"
        self.conn.register(table_name, df)
        self.conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM {table_name}")
        self.conn.execute("INSERT INTO metadata VALUES (?, ?, ?)", [date, key, table_name])

    def load(self, date, key):
        result = self.conn.execute("SELECT table_name FROM metadata WHERE date = ? AND key = ?", [date, key]).fetchone()
        if result:
            return self.conn.execute(f"SELECT * FROM {result[0]}").df()
        return None

    def list_dataframes(self):
        return self.conn.execute("SELECT date, key FROM metadata").fetchall()

class SQLiteAdapter:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS metadata (date TEXT, key TEXT, table_name TEXT)")

    def store(self, date, key, df):
        table_name = f"data_{date.strftime('%Y_%m_%d')}_{key}"
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        self.conn.execute("INSERT OR REPLACE INTO metadata VALUES (?, ?, ?)", (date.strftime("%Y-%m-%d"), key, table_name))
        self.conn.commit()

    def load(self, date, key):
        result = self.conn.execute("SELECT table_name FROM metadata WHERE date = ? AND key = ?", (date.strftime("%Y-%m-%d"), key)).fetchone()
        if result:
            return pd.read_sql_query(f"SELECT * FROM {result[0]}", self.conn)
        return None

    def list_dataframes(self):
        return self.conn.execute("SELECT date, key FROM metadata").fetchall()

if __name__ == "__main__":
    ctx = Context()

    demo_df = pd.DataFrame({"a": [1, 2, 3]})
    cash_df = pd.DataFrame({"a": [4, 5, 6]})
    some_df = pd.DataFrame({"a": [7, 8, 9]})

    # FileAdapter
    file_adapter = FileAdapter(ctx.config["adapters"]["file"]["path"])
    file_adapter.store(pd.Timestamp("2021-01-01"), "demo", demo_df)
    df = file_adapter.load(pd.Timestamp("2021-01-01"), "demo")
    print("FileAdapter:")
    print(df)
    print(file_adapter.list_dataframes())

    # DuckDBAdapter
    duckdb_adapter = DuckDBAdapter(ctx.config["adapters"]["duckdb"]["path"])
    duckdb_adapter.store(pd.Timestamp("2021-01-01"), "cash", cash_df)
    df = duckdb_adapter.load(pd.Timestamp("2021-01-01"), "cash")
    print("\nDuckDBAdapter:")
    print(df)
    print(duckdb_adapter.list_dataframes())

    # SQLiteAdapter
    sqlite_adapter = SQLiteAdapter(ctx.config["adapters"]["sqlite"]["path"])
    sqlite_adapter.store(pd.Timestamp("2021-01-01"), "some", some_df)
    df = sqlite_adapter.load(pd.Timestamp("2021-01-01"), "some")
    print("\nSQLiteAdapter:")
    print(df)
    print(sqlite_adapter.list_dataframes())
