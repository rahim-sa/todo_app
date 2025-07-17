import sys
from pathlib import Path
import pytest
from unittest.mock import patch
from datetime import date


sys.path.insert(0, str(Path(__file__).parent.parent))
#sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import MagicMock, patch   

from src.views.todo_view import TodoView
from src.models.todo_model import TodoModel
from src.controllers.todo_controller import TodoController



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