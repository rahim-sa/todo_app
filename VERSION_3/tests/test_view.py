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