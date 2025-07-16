from unittest.mock import MagicMock, patch
from src.controllers.todo_controller import TodoController

def test_add_todo_flow():
    """Test complete add todo workflow"""
    mock_model = MagicMock()
    mock_view = MagicMock()
    
    # Mock view response
    mock_view.get_todo_input.return_value = {
        'title': 'New Task',
        'description': '',
        'due_date': '2099-12-31'
    }
    
    # Patch date validation
    with patch('src.models.todo_model.date') as mock_date:
        mock_date.today.return_value = date(2000, 1, 1)  # Set "today" to past
        mock_date.fromisoformat.return_value = date(2099, 12, 31)
        
        controller = TodoController(mock_model, mock_view)
        controller._add_todo()
    
    # Verify model was updated
    mock_model.todos.__setitem__.assert_called_once()
    mock_model.save_todos.assert_called_once()