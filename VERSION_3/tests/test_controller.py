import sys
from pathlib import Path
import pytest
from unittest.mock import patch
from datetime import date
import logging




sys.path.insert(0, str(Path(__file__).parent.parent))
#sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import MagicMock, patch   

from src.views.todo_view import TodoView
from src.models.todo_model import TodoModel
from src.controllers.todo_controller import TodoController
from src.controllers.todo_controller import TodoError



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

#def test_add_todo_success(real_controller):
   # """Test successful todo addition with real components"""
   # with patch('builtins.input', side_effect=['Test Task', '', '2099-12-31']):
    #    real_controller._add_todo()
        
        # Verify by checking actual model state
    #    assert len(real_controller.model.todos) == 1
    #    todo = list(real_controller.model.todos.values())[0]
     #   assert todo.title == "Test Task"
     #   assert todo.due_date == date(2099, 12, 31)

#def test_add_todo_invalid_date(real_controller):
  #  """Test past due date rejection"""
   # with patch('builtins.input', side_effect=['Test', '', '2000-01-01']):
      #  with pytest.raises(ValueError, match="Invalid date format"):
       #     real_controller._add_todo()

 
#def test_complete_nonexistent_todo(real_controller):
   # """Test invalid ID handling"""
  #  with patch('builtins.input', return_value="999"):
    #    with pytest.raises(ValueError):
     #       real_controller._complete_todo()

#def test_complete_nonexistent_todo(real_controller):
  #  """Test invalid ID handling"""
   # with patch('builtins.input', return_value="999"):
   #     with pytest.raises(ValueError, match="Todo not found"):
     #       real_controller._complete_todo()

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


#def test_save_todos_failure(real_controller, monkeypatch):
    #"""Test storage failure during save"""
    #def mock_fail(*args, **kwargs):
        #raise Exception("Save failed")

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

#def test_error_logging(real_controller, caplog):
   # """Verify errors are logged"""
   # with patch('builtins.input', side_effect=['', '', '']):  # Empty title
       # with pytest.raises(ValueError):
      #      real_controller._add_todo()
    #assert "Title cannot be empty" in caplog.text



def test_error_logging(real_controller, caplog):
    """Verify errors are logged"""
    caplog.set_level(logging.ERROR)
    
    with patch('builtins.input', side_effect=['', '', '']):
        with pytest.raises(ValueError):
            real_controller._add_todo()
    
    # Verify both stdout and logs
    assert "Title cannot be empty" in caplog.text

#def test_todo_id_generation(real_controller):
   # """Test auto-incrementing IDs"""
   # with patch('builtins.input', side_effect=['Test', '', '2099-12-31']):
      #  real_controller._add_todo()
      #  assert "1" in real_controller.model.todos  # First ID should be "1"
        
       # real_controller._add_todo()
       # assert "2" in real_controller.model.todos  # Next ID should be "2"

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