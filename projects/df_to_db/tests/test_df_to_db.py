import pytest
import pandas as pd
import os
import shutil
from datetime import datetime
from df_to_db import FileAdapter, SQLiteAdapter, DuckDBAdapter

@pytest.fixture
def sample_df():
    return pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

@pytest.fixture
def date():
    return pd.Timestamp("2021-01-01")

@pytest.fixture
def key():
    return "test_data"

@pytest.fixture
def file_adapter(tmp_path):
    return FileAdapter(str(tmp_path))

def test_store_and_load(file_adapter, sample_df, date, key):
    filename = "sample"
    file_adapter.store(date, key, filename, sample_df)
    loaded_df = file_adapter.load(date, key)
    pd.testing.assert_frame_equal(sample_df, loaded_df)

def test_list_dataframes(file_adapter, sample_df, date):
    file_adapter.store(date, "key1", "sample1", sample_df)
    file_adapter.store(date, "key2", "sample2", sample_df)
    dataframes = file_adapter.list_dataframes()
    assert set(dataframes) == {('2021-01-01', 'key2', 'sample2', 'csv'), ('2021-01-01', 'key1', 'sample1', 'csv')}

def test_load_nonexistent(file_adapter, date, key):
    assert file_adapter.load(date, key) is None

@pytest.fixture
def sqlite_adapter():
    return SQLiteAdapter(":memory:")  # Use in-memory database for testing

def test_sqlite_adapter_store_and_load(sqlite_adapter):
    date = datetime(2023, 1, 1)
    key = "test_key"
    filename = "test_file"
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    
    sqlite_adapter.store(date, key, filename, df)
    loaded_df = sqlite_adapter.load(date, key)
    
    assert loaded_df is not None
    assert loaded_df.equals(df)

def test_sqlite_adapter_list_dataframes(sqlite_adapter):
    date1 = datetime(2023, 1, 1)
    date2 = datetime(2023, 1, 2)
    sqlite_adapter.store(date1, "key1", "file1", pd.DataFrame({"A": [1, 2]}))
    sqlite_adapter.store(date2, "key2", "file2", pd.DataFrame({"B": [3, 4]}))
    
    dataframes = sqlite_adapter.list_dataframes()
    assert len(dataframes) == 2
    assert ("2023-01-01", "key1", "file1", "csv") in dataframes
    assert ("2023-01-02", "key2", "file2", "csv") in dataframes

@pytest.fixture
def duckdb_adapter(tmp_path):
    db_path = str(tmp_path / "test.duckdb")
    return DuckDBAdapter(db_path)

def test_store_and_load(duckdb_adapter):
    date = datetime(2023, 4, 18)
    key = "test_key"
    filename = "test_file"
    df = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})

    duckdb_adapter.store(date, key, filename, df)
    loaded_df = duckdb_adapter.load(date, key)

    assert loaded_df is not None
    pd.testing.assert_frame_equal(df, loaded_df)

def test_list_dataframes(duckdb_adapter):
    date1 = datetime(2023, 4, 18)
    date2 = datetime(2023, 4, 19)
    df1 = pd.DataFrame({"A": [1, 2, 3]})
    df2 = pd.DataFrame({"B": [4, 5, 6]})

    duckdb_adapter.store(date1, "key1", "file1", df1)
    duckdb_adapter.store(date2, "key2", "file2", df2)

    dataframes = duckdb_adapter.list_dataframes()
    assert len(dataframes) == 2
    assert ("2023-04-18", "key1", "file1", "csv") in dataframes
    assert ("2023-04-19", "key2", "file2", "csv") in dataframes

def test_load_nonexistent(duckdb_adapter):
    date = datetime(2023, 4, 18)
    key = "nonexistent_key"

    loaded_df = duckdb_adapter.load(date, key)
    assert loaded_df is None