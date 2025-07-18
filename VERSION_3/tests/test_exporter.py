import pytest
import os
import json
from unittest.mock import patch, mock_open
from datetime import date
from src.models.todo_model import Todo
from src.utils.exporter import export_to_json
from src.exceptions import PersistenceError  # Added as requested

def test_export_permission_error(tmp_path):
    """Test real permission error handling"""
    # 1. Setup read-only file
    test_file = tmp_path / "readonly.json"
    test_file.write_text("")  # Create file
    
    # Make read-only (Unix)
    test_file.chmod(0o400)
    
    # 2. Prepare test data
    test_data = {
        "1": Todo(
            title="Test",
            due_date=date(2099, 1, 1),
            description="",
            is_complete=False
        )
    }

    # 3. Test and verify
    with pytest.raises(PersistenceError) as exc_info:  # Changed to PersistenceError
        export_to_json(test_data, test_file)
    
    assert "permission" in str(exc_info.value).lower()


# new tests

# def test_export_to_json_success(tmp_path):
#     """Test successful JSON export"""
#     from src.utils.exporter import export_to_json
#     test_file = tmp_path / "test.json"
#     test_data = {
#         "1": Todo(
#             title="Test",
#             due_date=date(2099, 1, 1),
#             description="Test description",
#             is_complete=False
#         )
#     }
    
#     export_to_json(test_data, test_file)
    
#     # Verify file content
#     with open(test_file) as f:
#         data = json.load(f)
#         assert "1" in data
#         assert data["1"]["title"] == "Test"



# def test_export_to_json_failure():
#     """Test JSON export failure"""
#     from src.utils.exporter import export_to_json
#     test_data = {"1": Todo(title="Test", due_date=date(2099, 1, 1))}
    
#     # Mock a failure during file writing
#     m = mock_open()
#     m.side_effect = IOError("Disk full")
    
#     with patch('builtins.open', m):
#         with pytest.raises(PersistenceError, match="Disk full"):
#             export_to_json(test_data, "fake_path.json")

def test_export_to_csv(tmp_path):
    """Test CSV export functionality"""
    from src.utils.exporter import export_to_csv
    test_file = tmp_path / "test.csv"
    test_data = {
        "1": Todo(title="Test", due_date=date(2099, 1, 1))
    }
    
    export_to_csv(test_data, test_file)
    
    # Verify CSV content
    with open(test_file) as f:
        lines = f.readlines()
        assert lines[0].strip() == "id,title,due_date"
        assert lines[1].strip() == "1,Test,2099-01-01"

def test_export_to_json_success(tmp_path):
    """Test successful JSON export"""
    test_file = tmp_path / "test.json"
    test_data = {
        "1": Todo(
            title="Test",
            due_date=date(2099, 1, 1),
            description="Test description",
            is_complete=False
        )
    }
    
    export_to_json(test_data, test_file)
    
    # Verify file content
    with open(test_file) as f:
        data = json.load(f)
        assert "1" in data
        assert data["1"]["title"] == "Test"
        assert data["1"]["due_date"] == "2099-01-01"
        assert data["1"]["is_complete"] is False

def test_export_to_json_empty(tmp_path):
    """Test exporting empty dict"""
    test_file = tmp_path / "empty.json"
    export_to_json({}, test_file)
    
    with open(test_file) as f:
        assert json.load(f) == {}

def test_export_to_json_failure():
    """Test JSON export failure"""
    test_data = {"1": Todo(title="Test", due_date=date(2099, 1, 1))}
    
    # Mock a failure during file writing
    with patch('builtins.open', side_effect=PermissionError("No write access")):
        with pytest.raises(PersistenceError, match="No write access"):
            export_to_json(test_data, "no_access.json")

 
 