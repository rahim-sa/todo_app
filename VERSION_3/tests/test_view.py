from unittest.mock import patch
from src.views.todo_view import TodoView

def test_show_menu(capsys):
    TodoView.show_menu()
    captured = capsys.readouterr()
    assert "Todo Manager" in captured.out

@patch('builtins.input', side_effect=['Test', '', '2023-12-31'])
def test_get_todo_input(mock_input):
    data = TodoView.get_todo_input()
    assert data['title'] == "Test"
    assert data['due_date'].year == 2023