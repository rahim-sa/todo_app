import pytest
from pathlib import Path
from datetime import date
from src.utils.importer import import_from_json

@pytest.fixture
def sample_json_file(tmp_path):
    file_path = tmp_path / "todos.json"
    file_path.write_text("""{
        "1": {
            "title": "Test Task",
            "due_date": "2099-12-31",
            "description": "Test Description"
        }
    }""")
    return file_path

def test_import_json_success(sample_json_file):
    todos = import_from_json(sample_json_file)
    assert todos["1"].title == "Test Task"

def test_import_json_missing_file():
    with pytest.raises(ValueError):
        import_from_json(Path("nonexistent.json"))

def test_import_invalid_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid}")
    with pytest.raises(ValueError):
        import_from_json(bad_file)

def test_import_past_date_fails(tmp_path):
    past_file = tmp_path / "past.json"
    past_file.write_text("""{
        "1": {
            "title": "Fail Task",
            "due_date": "2020-01-01"
        }
    }""")
    with pytest.raises(ValueError):
        import_from_json(past_file)