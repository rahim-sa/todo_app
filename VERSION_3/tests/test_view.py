from unittest.mock import patch
from datetime import date
from src.views.todo_view import TodoView

def test_show_menu(capsys):
    """Test menu display output"""
    TodoView.show_menu()
    captured = capsys.readouterr()
    assert "Todo Manager" in captured.out
    assert "1. Add Todo" in captured.out

@patch('builtins.input', side_effect=['Test Task', '', '2099-12-31'])
def test_get_todo_input_valid(mock_input):
    """Test valid todo input"""
    data = TodoView.get_todo_input()
    assert data['title'] == "Test Task"
    assert data['due_date'] == date(2099, 12, 31)

@patch('builtins.input', side_effect=['', '', ''])  # Empty title
def test_get_todo_input_invalid(mock_input):
    """Test invalid input validation"""
    with pytest.raises(ValueError):
        TodoView.get_todo_input()