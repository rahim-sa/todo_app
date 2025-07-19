import pytest
import sys
from pathlib import Path
import json
from unittest.mock import call
from unittest.mock import patch, MagicMock
import logging
from datetime import date, datetime, timedelta
 
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.todo_model import Todo
from src.exceptions import PersistenceError

from src.views.todo_view import TodoView
from src.models.todo_model import TodoModel
from src.controllers.todo_controller import TodoController   


def test_todo_creation(sample_todo):
    assert sample_todo.title == "Test Todo"
    assert not sample_todo.is_complete

def test_model_add_todo(empty_model, sample_todo):
    empty_model.todos["1"] = sample_todo
    assert "1" in empty_model.todos

def test_load_invalid_data(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid}")
    model = TodoModel(bad_file)
    assert model.todos == {}  # Should handle corrupt files


def test_completed_todos_property(empty_model, sample_todo):
    """Test completed_todos property"""
    from unittest.mock import MagicMock  # Or keep at top
    sample_todo.is_complete = True
    empty_model.todos = {
        "1": sample_todo, 
        "2": MagicMock(is_complete=False)
    }
    assert len(empty_model.completed_todos) == 1
    assert empty_model.completed_todos[0].title == "Test Todo"


def test_model_save_empty(tmp_path):
    """Test saving empty todo list"""
    model = TodoModel(tmp_path / "empty.json")
    model.todos = {}  # Explicitly set empty
    model.save_todos()
    
    # Verify file was created with empty JSON
    assert (tmp_path / "empty.json").exists()
    assert json.loads((tmp_path / "empty.json").read_text()) == {}


def test_controller_run_exit(real_controller, monkeypatch):
    """Test clean exit behavior"""
    # Setup
    exit_called = False
    original_save = real_controller.model.save_todos
    
    def mock_save():
        nonlocal exit_called
        exit_called = True
        original_save()
    
    # Mock the inputs and save method
    input_values = ["5"]  # Exit command
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))
    monkeypatch.setattr(real_controller.model, 'save_todos', mock_save)
    
    # Execute
    real_controller.run()
    
    # Verify
    assert exit_called, "Save should be called before exit"

    
def test_controller_run_invalid_choice(real_controller):
    """Test handling of invalid menu choices"""
    with patch('builtins.input', side_effect=["99", "5"]), \
         patch.object(real_controller.view, 'show_error') as mock_error:
        real_controller.run()
        mock_error.assert_called_with("Invalid choice")

    
def test_load_corrupt_data(tmp_path, capsys):
    """Test handling of corrupt JSON files"""
    # Create corrupt file
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid}")
    
    # Test loading
    model = TodoModel(bad_file)
    captured = capsys.readouterr()
    
    # Verify behavior
    assert model.todos == {}  # Should return empty dict
    assert "Warning: Could not load todos" in captured.out  # Verify warning was printed


def test_load_single_valid_todo(tmp_path):
    test_file = tmp_path / "test.json"
    # Ensure all required fields are present
    test_file.write_text("""{
        "1": {
            "title": "Safe Test",
            "due_date": "2099-12-31",
            "description": "",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": null,
            "is_complete": false
        }
    }""")
    model = TodoModel(test_file)
    assert len(model.todos) == 1
    assert model.todos["1"].title == "Safe Test"



def test_load_invalid_data(tmp_path):
    bad_file = tmp_path / "invalid.json"
    bad_file.write_text("""{
        "1": {"title": 123, "due_date": "2099-01-01"}
    }""")  # Invalid title (number)
    model = TodoModel(bad_file)
    assert model.todos == {}

def test_load_corrupt_data(tmp_path):
    bad_file = tmp_path / "corrupt.json"
    bad_file.write_text("""{
        "1": {"title": "Test", "due_date": "not-a-date"}
    }""")  # Invalid date format
    model = TodoModel(bad_file)
    assert model.todos == {}


def test_model_init_with_nonexistent_file(tmp_path):
    """Test initialization with non-existent file"""
    non_existent = tmp_path / "nonexistent.json"
    model = TodoModel(non_existent)
    assert model.todos == {}  # Should return empty dict without errors

def test_save_empty_todos(tmp_path):
    """Test saving empty todo list"""
    model = TodoModel(tmp_path / "empty.json")
    model.save_todos()  # Should not crash
    assert Path(tmp_path / "empty.json").exists()


def test_model_with_custom_filepath(tmp_path):
    """Test model works with custom file path"""
    test_file = tmp_path / "custom.json"
    model = TodoModel(test_file)
    assert model.file_path == test_file
    assert model.todos == {}


def test_todo_with_empty_description():
    """Test Todo allows empty description"""
    from datetime import date
    todo = Todo(title="Valid", description="", due_date=date(2099,1,1))
    assert todo.description == ""

def test_model_save_empty(tmp_path):
    """Test saving empty todo list"""
    model = TodoModel(tmp_path / "empty.json")
    model.save_todos()  # Should not crash
    assert (tmp_path / "empty.json").exists()


def test_load_todos_with_none_updated_at(tmp_path):
    """Test loading todos where updated_at is None"""
    test_file = tmp_path / "test.json"
    test_file.write_text("""{
        "1": {
            "title": "Test",
            "due_date": "2099-12-31",
            "description": "",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": null,
            "is_complete": false
        }
    }""")
    model = TodoModel(test_file)
    assert model.todos["1"].updated_at is None

def test_save_todos_permission_error(tmp_path, monkeypatch):
    """Test save_todos handles permission errors"""
    def mock_open(*args, **kwargs):
        raise PermissionError("No write permission")
    
    monkeypatch.setattr("builtins.open", mock_open)
    model = TodoModel(tmp_path / "test.json")
    model.todos["1"] = Todo(title="Test", due_date=date(2099,1,1))
    model.save_todos()  # Should not raise, just print error

def test_todo_validation_errors():
    """Test Todo validation rejects bad inputs"""
    with pytest.raises(ValueError):
        Todo(title="", due_date=date(2099,1,1))  # Empty title
        
    with pytest.raises(ValueError):
        Todo(title=123, due_date=date(2099,1,1))  # Non-string title
        
    with pytest.raises(ValueError):
        Todo(title="Test", due_date=date(2020,1,1))  # Past due date

def test_is_overdue_property():
    """Test is_overdue property calculation"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    # These will pass validation because due_date is today
    todo1 = Todo(title="Due today", due_date=today)
    todo2 = Todo(title="Done today", due_date=today, is_complete=True)
    todo3 = Todo(title="Due tomorrow", due_date=tomorrow)
    
    # Manually adjust dates after creation
    todo1.due_date = yesterday
    assert todo1.is_overdue
    
    todo2.due_date = yesterday
    assert not todo2.is_overdue
    
    assert not todo3.is_overdue

def test_non_ascii_characters(tmp_path):
    """Test handling of non-ASCII characters"""
    model = TodoModel(tmp_path / "test.json")
    model.todos["1"] = Todo(title="日本語", description="áéíóú", due_date=date(2099,1,1))
    model.save_todos()
    
    # Verify roundtrip
    model2 = TodoModel(tmp_path / "test.json")
    assert model2.todos["1"].title == "日本語"


# Add these tests:
def test_persistence_error_fallback(monkeypatch):
    """Test fallback PersistenceError when import fails"""
    monkeypatch.delattr('src.exceptions.PersistenceError')
    from importlib import reload
    import src.models.todo_model
    reload(src.models.todo_model)
    assert hasattr(src.models.todo_model, 'PersistenceError')

def test_model_save_failure(tmp_path, capsys):
    """Test error handling during save"""
    model = TodoModel(tmp_path / "test.json")
    model.todos = {"1": MagicMock(spec=Todo)}
    with patch('builtins.open', side_effect=PermissionError):
        model.save_todos()
    assert "ERROR saving todos" in capsys.readouterr().out


def test_model_error_handling(tmp_path, capsys):
    """Test error handling during file operations"""
    # Test corrupt file loading
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid}")
    model = TodoModel(bad_file)
    assert "Warning: Could not load todos" in capsys.readouterr().out
    
    # Test save failure
    model.todos = {"1": MagicMock(spec=Todo)}
    with patch('builtins.open', side_effect=PermissionError("No access")):
        model.save_todos()
    assert "ERROR saving todos" in capsys.readouterr().out

