import pytest
from unittest.mock import patch
from datetime import date

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

#sys.path.insert(0, str(Path(__file__).parent.parent))

from src.views.todo_view import TodoView
from src.models.todo_model import TodoModel
from src.controllers.todo_controller import TodoController

from src.views.todo_view import TodoView

def test_show_menu(capsys):
    TodoView.show_menu()
    captured = capsys.readouterr()
    assert "Todo Manager" in captured.out

@patch('builtins.input', side_effect=['Test', '', '2099-12-31'])
def test_get_todo_input_valid(mock_input):
    data = TodoView.get_todo_input()
    assert data['title'] == "Test"

@patch('builtins.input', side_effect=['', '', ''])
def test_get_todo_input_invalid(mock_input):
    with pytest.raises(ValueError):
        TodoView.get_todo_input()

# Add to test_view.py

def test_show_todos(capsys):
    """Test todo listing output"""
    from src.models.todo_model import Todo
    from datetime import date, datetime

    test_todos = {
        "1": Todo(title="Test 1", due_date=date(2099, 1, 1)),
        "2": Todo(
            title="Test 2", 
            due_date=date(2099, 1, 1),  # Future date (valid)
            is_complete=True
        )
    }
    
    TodoView.show_todos(test_todos)
    captured = capsys.readouterr()
    
    assert "1. [✗] Test 1" in captured.out
    assert "2. [✓] Test 2" in captured.out