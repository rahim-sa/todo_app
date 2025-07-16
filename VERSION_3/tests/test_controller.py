from unittest.mock import MagicMock
from src.controllers.todo_controller import TodoController

def test_add_todo_flow():
    mock_model = MagicMock()
    mock_view = MagicMock()
    mock_view.get_todo_input.return_value = {
        'title': 'Test',
        'due_date': '2023-12-31'
    }
    
    controller = TodoController(mock_model, mock_view)
    controller._add_todo()
    assert mock_model.todos.__setitem__.called