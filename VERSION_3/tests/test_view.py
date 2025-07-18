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

 

@patch('builtins.input')
def test_get_todo_id(mock_input):
    """Test ID input validation"""
    # Test valid input
    mock_input.return_value = "1"
    assert TodoView.get_todo_id() == "1"
    
    # Test empty input
    mock_input.return_value = ""
    with pytest.raises(ValueError, match="ID cannot be empty"):
        TodoView.get_todo_id()

def test_show_error(capsys):
    """Test error message display"""
    TodoView.show_error("Test error message")
    captured = capsys.readouterr()
    assert "Error: Test error message" in captured.out

def test_show_success(capsys):
    """Test success message display"""
    TodoView.show_success("Test success message")
    captured = capsys.readouterr()
    assert "Success: Test success message" in captured.out