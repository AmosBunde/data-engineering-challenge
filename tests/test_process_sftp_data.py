import pytest
import pandas as pd
from pathlib import Path
from data-processing-pipeline.process_sftp_data import process_sftp_data

def test_process_data_csv(tmp_path):
    # Create a sample CSV
    test_file = tmp_path / "test.csv"
    test_data = "name,age\nAmos,30\nBunde,35"
    test_file.write_text(test_data)

    df = process_sftp_data(str(test_file))
    assert len(df) == 2
    assert list(df.columns) == ["name", "age"]

def test_process_data_json(tmp_path):
    # Create a sample JSON
    test_file = tmp_path / "test.json"
    test_data = '{"name": "Amos", "age": 30}\n{"name": "Bunde", "age": 35}'
    test_file.write_text(test_data)

    df = process_sftp_datastr(test_file))
    assert len(df) == 2
    assert sorted(df.columns) == ["age", "name"]

def test_process_data_unsupported(tmp_path):
    # Create a dummy file
    test_file = tmp_path / "test.txt"
    test_file.write_text("some data")

    with pytest.raises(ValueError):
        process_sftp_data(str(test_file))
