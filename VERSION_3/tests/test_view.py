from unittest.mock import patch
import pytest

class TestTodoView:
    @patch('builtins.input', side_effect=['Test', '', '2023-12-31'])

    def test_get_todo_input(self, mock_input):
        from src.views.todo_view import TodoView
        view = TodoView()
        result = view.get_todo_input()
        assert result['title'] == 'Test'
        assert result['due_date'].year == 2023