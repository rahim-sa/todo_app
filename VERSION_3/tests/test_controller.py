from unittest.mock import MagicMock
import pytest

class TestTodoController:
    def test_add_todo_flow(self):
        from src.controllers.todo_controller import TodoController
        mock_model = MagicMock()
        mock_view = MagicMock()
        mock_view.get_todo_input.return_value = {
            'title': 'Test',
            'description': '',
            'due_date': '2023-12-31'
        }
        
        controller = TodoController(mock_model, mock_view)
        controller._add_todo()
        
        mock_model.todos.__setitem__.assert_called()