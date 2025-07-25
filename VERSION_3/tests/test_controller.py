import sys
from pathlib import Path
import pytest
from datetime import date
import logging
import json
from unittest.mock import call
from unittest.mock import patch, MagicMock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.views.todo_view import TodoView
from src.models.todo_model import TodoModel
from src.controllers.todo_controller import TodoController
from src.controllers.todo_controller import TodoError
from src.exceptions import PersistenceError 
 

def test_add_todo_success(real_controller):
    """Test successful todo addition"""
    with patch('builtins.input', side_effect=['Test Task', '', '2099-12-31']):
        real_controller._add_todo()
        assert len(real_controller.model.todos) == 1

def test_add_todo_invalid_date(real_controller):
    """Test past due date rejection"""
    with patch('builtins.input', side_effect=['Test', '', '2000-01-01']):
        with pytest.raises(ValueError, match="Invalid date format"):
            real_controller._add_todo()

def test_complete_nonexistent_todo(real_controller):
    """Test invalid ID handling"""
    with patch('builtins.input', return_value="999"):
        with pytest.raises(ValueError, match="Todo not found"):
            real_controller._complete_todo()



def test_add_todo_empty_title(real_controller):
    with patch('builtins.input', side_effect=['', '', '']):
        with pytest.raises(ValueError, match="Title cannot be empty"):
            real_controller._add_todo()


def test_complete_todo_success(real_controller):
    """Test completion with real components"""
    # Add a test todo
    test_todo = MagicMock()
    test_todo.is_complete = False
    real_controller.model.todos = {"1": test_todo}
    
    with patch('builtins.input', return_value="1"):
        real_controller._complete_todo()
        assert test_todo.is_complete is True

def test_delete_todo_success(real_controller):
    """Test deletion with real components"""
    real_controller.model.todos = {"1": MagicMock()}
    
    with patch('builtins.input', return_value="1"):
        real_controller._delete_todo()
        assert "1" not in real_controller.model.todos

# Test 1: Empty title
def test_add_todo_empty_title(real_controller):
    with patch('builtins.input', side_effect=['', '', '2099-12-31']):  # Empty title
        with pytest.raises(ValueError):
            real_controller._add_todo()

# Test 2: Invalid date (past date)
def test_add_todo_past_date(real_controller):
    with patch('builtins.input', side_effect=['Test', '', '2000-01-01']):
        with pytest.raises(ValueError):
            real_controller._add_todo()

# Test 3: Invalid date format (not YYYY-MM-DD)
def test_add_todo_bad_date_format(real_controller):
    with patch('builtins.input', side_effect=['Test', '', '31-01-2000']):
        with pytest.raises(ValueError):
            real_controller._add_todo()

# Test 1: Complete non-existent todo
def test_complete_invalid_id(real_controller):
    with patch('builtins.input', return_value="999"):  # Invalid ID
        with pytest.raises(ValueError):
            real_controller._complete_todo()

# Test 2: Complete already-completed todo
def test_complete_already_done(real_controller):
    mock_todo = MagicMock(is_complete=True)  # Already completed
    real_controller.model.todos = {"1": mock_todo}
    with patch('builtins.input', return_value="1"):
        real_controller._complete_todo()
    assert mock_todo.is_complete  # Still True

def test_save_todos_failure(real_controller, monkeypatch):
    """Test storage failure during save"""
    def mock_fail(*args, **kwargs):
        raise Exception("Storage failed")  # Match expected message
    
    monkeypatch.setattr(real_controller.model, 'save_todos', mock_fail)
    with patch('builtins.input', side_effect=['Test', '', '2099-12-31']):
        with pytest.raises(TodoError, match="Storage failed"):
            real_controller._add_todo()

def test_load_todos_failure(tmp_path):
    """Test corrupt data loading"""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid_json}")
    model = TodoModel(bad_file)
    assert model.todos == {}  # Should handle corrupt file


def test_list_empty_todos(real_controller, capsys):
    """Test listing empty todo list"""
    real_controller.model.todos = {}
    real_controller._list_todos()
    captured = capsys.readouterr()
    assert "No todos found" in captured.out

def test_complete_todo_updates_timestamp(real_controller):
    """Test completion updates timestamp"""
    test_todo = MagicMock(is_complete=False, updated_at=None)
    real_controller.model.todos = {"1": test_todo}
    with patch('builtins.input', return_value="1"):
        real_controller._complete_todo()
    assert test_todo.updated_at is not None  # Timestamp updated


def test_error_logging(real_controller, caplog):
    """Verify errors are logged"""
    caplog.set_level(logging.ERROR)
    
    with patch('builtins.input', side_effect=['', '', '']):
        with pytest.raises(ValueError):
            real_controller._add_todo()
    
    # Verify both stdout and logs
    assert "Title cannot be empty" in caplog.text


def test_todo_id_generation(real_controller):
    """Test auto-incrementing IDs"""
    # Setup - clear existing todos and mock save
    real_controller.model.todos = {}
    with patch.object(real_controller.model, 'save_todos'), \
         patch('builtins.input', side_effect=['Test', '', '2099-12-31', 
                                             'Test2', '', '2099-12-31']):
        
        # First addition
        real_controller._add_todo()
        assert "1" in real_controller.model.todos
        
        # Second addition 
        real_controller._add_todo()
        assert "2" in real_controller.model.todos


def test_controller_init_failure():
    """Test controller handles model initialization failure"""
    # Create a mock model that will fail initialization
    bad_model = MagicMock(spec=TodoModel)
    bad_model._load_todos.side_effect = PersistenceError("DB error")
    del bad_model.todos  # Force the initialization check to fail
    
    # Test that controller converts the error
    with pytest.raises(TodoError) as exc_info:
        TodoController(bad_model, MagicMock(spec=TodoView))
    
    # Verify the error message
    assert "Model initialization failed" in str(exc_info.value)
    assert "DB error" in str(exc_info.value)


def test_controller_logging_on_error(real_controller, caplog):
    """Verify errors are properly logged"""
    caplog.set_level(logging.ERROR)
    with patch('builtins.input', side_effect=['', '', '']):  # Invalid input
        with pytest.raises(ValueError):
            real_controller._add_todo()
    assert any("Title cannot be empty" in record.message 
              for record in caplog.records)



def test_controller_run_exit(real_controller):
    """Test clean exit behavior"""
    with patch('builtins.input', return_value="5"), \
         patch.object(real_controller.model, 'save_todos') as mock_save:
        real_controller.run()
        mock_save.assert_called_once()  # Verify save was called before exit    


def test_controller_run_invalid_choice(real_controller):
    """Test handling of invalid menu choices"""
    with patch('builtins.input', side_effect=["99", "5"]) as mock_input, \
         patch.object(real_controller.view, 'show_error') as mock_error:
        real_controller.run()
        mock_error.assert_called_once_with("Invalid choice")
        assert mock_input.call_count == 2 

def test_error_logging(real_controller, caplog):
    """Verify errors are logged"""
    caplog.set_level(logging.ERROR)
    with patch('builtins.input', side_effect=['', '', '']):  # Empty title
        with pytest.raises(ValueError):
            real_controller._add_todo()
    assert "Title cannot be empty" in caplog.text

def test_complete_updates_timestamp(real_controller):
    """Verify completion updates timestamp"""
    test_todo = MagicMock(is_complete=False, updated_at=None)
    real_controller.model.todos = {"1": test_todo}
    with patch('builtins.input', return_value="1"):
        real_controller._complete_todo()
    assert test_todo.updated_at is not None

def test_list_todos_format(real_controller, sample_todo, capsys):
    """Verify todo listing format"""
    real_controller.model.todos = {"1": sample_todo}
    real_controller._list_todos()
    captured = capsys.readouterr()
    assert "1. [✗] Test Todo" in captured.out
    assert "Due: 2099-12-31" in captured.out


def test_save_failure_handling(real_controller, monkeypatch, capsys):
    """Test storage failure recovery"""
    # Setup
    def mock_fail(*args, **kwargs):
        raise PersistenceError("Save failed")
    
    # Apply mock
    monkeypatch.setattr(real_controller.model, 'save_todos', mock_fail)
    
    # Test with valid input that should trigger save
    with patch('builtins.input', side_effect=['Valid', '', '2099-12-31']):
        with pytest.raises(TodoError) as exc_info:
            real_controller._add_todo()
        
        # Verify error handling
        assert "Save failed" in str(exc_info.value)
        assert "Error:" in capsys.readouterr().out  # Verify user saw error


def test_load_todos_failure(tmp_path):
    bad_file = tmp_path / "bad.json"
    # Write valid JSON format with proper structure
    bad_file.write_text("""{
        "1": {
            "title": "Test",
            "due_date": "2099-01-01",
            "description": "",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": null
        }
    }""")
    model = TodoModel(bad_file)
    assert len(model.todos) == 1  # Should load successfully


def test_controller_init_failure():
    """Test controller handles model initialization failure"""
    bad_model = MagicMock()
    bad_model._load_todos.side_effect = PersistenceError("DB error")
    del bad_model.todos  # Make it fail initialization check
    
    with pytest.raises(TodoError) as exc_info:
        TodoController(bad_model, MagicMock())
    assert "Model initialization failed" in str(exc_info.value)

def test_add_todo_storage_failure(real_controller, monkeypatch):
    """Test storage failure during todo addition"""
    def mock_fail():
        raise PersistenceError("Save failed")
    
    monkeypatch.setattr(real_controller.model, 'save_todos', mock_fail)
    with patch('builtins.input', side_effect=['Test', '', '2099-12-31']):
        with pytest.raises(TodoError):
            real_controller._add_todo()


def test_complete_todo_unexpected_error(real_controller, monkeypatch):
    """Test unexpected error during completion"""
    # Create a mock todo that will raise when is_complete is set
    mock_todo = MagicMock()
    
    # Create a side effect that raises when is_complete is set
    def raise_error(*args, **kwargs):
        raise Exception("Simulated error")
    
    # Apply the side effect to is_complete assignment
    type(mock_todo).is_complete = property(fset=raise_error)
    
    real_controller.model.todos = {"1": mock_todo}
    
    with patch('builtins.input', return_value="1"):
        with pytest.raises(Exception) as exc_info:
            real_controller._complete_todo()
        assert "Simulated error" in str(exc_info.value)


def test_delete_todo_storage_failure(real_controller, monkeypatch):
    """Test storage failure during deletion"""
    real_controller.model.todos = {"1": MagicMock()}
    
    def mock_fail():
        raise PersistenceError("Save failed")
    
    monkeypatch.setattr(real_controller.model, 'save_todos', mock_fail)
    with patch('builtins.input', return_value="1"):
        with pytest.raises(PersistenceError, match="Save failed"):
            real_controller._delete_todo()
    
    def mock_fail():
        raise PersistenceError("Save failed")
    
    monkeypatch.setattr(real_controller.model, 'save_todos', mock_fail)
    with patch('builtins.input', return_value="1"):
        with pytest.raises(Exception):
            real_controller._delete_todo()

def test_list_todos_failure(real_controller, monkeypatch, capsys):
    """Test failure during todo listing"""
    def mock_fail(*args, **kwargs):
        raise Exception("Display error")
    
    monkeypatch.setattr(real_controller.view, 'show_todos', mock_fail)
    real_controller._list_todos()
    
    captured = capsys.readouterr()
    assert "Failed to load todos" in captured.out

def test_run_unexpected_error(real_controller):
    """Test unexpected error handling in run()"""
    with patch('builtins.input', side_effect=["1", "5"]), \
         patch.object(real_controller, '_add_todo', side_effect=Exception("Boom")) as mock_add:
        
        real_controller.run()
        mock_add.assert_called_once()


def test_add_todo_logging(real_controller, caplog):
    """Test error logging in _add_todo"""
    caplog.set_level(logging.ERROR)
    with patch('builtins.input', side_effect=['', '', '']):  # Invalid input
        with pytest.raises(ValueError):
            real_controller._add_todo()
    assert "Title cannot be empty" in caplog.text

def test_complete_todo_edge_cases(real_controller):
    """Test error paths in _complete_todo"""
    # Test invalid ID
    with patch('builtins.input', return_value="invalid"):
        with pytest.raises(ValueError):
            real_controller._complete_todo()



def test_add_todo_error_handling(real_controller):
    """Test error paths in todo addition"""
    with patch('builtins.input', side_effect=['', '', '']):  # Empty title
        with pytest.raises(ValueError):
            real_controller._add_todo()
    
    with patch.object(real_controller.model, 'save_todos', side_effect=Exception("DB error")):
        with pytest.raises(TodoError):
            real_controller._add_todo()


def test_controller_init_failure():
    """Test initialization error handling"""
    # Create model missing required attributes
    broken_model = MagicMock()
    del broken_model._load_todos  # Remove critical method
    del broken_model.todos  # Remove required attribute
    
    with pytest.raises(TodoError) as exc_info:
        TodoController(broken_model, MagicMock())
    
    # Verify the error contains the expected message
    assert "Model not properly initialized" in str(exc_info.value)

