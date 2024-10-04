import pytest
import pandas as pd
import os
import shutil
from datetime import datetime
from df_to_db import FileAdapter

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