import pytest
from unittest.mock import patch
from datetime import date, timedelta
from src.views.todo_view import TodoView
from src.models.todo_model import Todo

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



def test_show_messages(capsys):
    """Test both error and success message display"""
    # Test error message
    TodoView.show_error("Database error")
    captured = capsys.readouterr()
    assert "Error: Database error" in captured.out
    
    # Test success message
    TodoView.show_success("Item created")
    captured = capsys.readouterr()
    assert "Success: Item created" in captured.out


def test_show_success(capsys):
    """Test success message display"""
    # First call
    TodoView.show_success("Saved successfully")
    captured = capsys.readouterr()
    assert "Success: Saved successfully" in captured.out
    
    # Second call with different message
    TodoView.show_success("Item deleted")
    captured = capsys.readouterr()
    assert "Success: Item deleted" in captured.out


# def test_show_todos(capsys):
#     """Test todo list display"""
#     from datetime import datetime, timedelta
#     from src.models.todo_model import Todo
    
#     # Create test todos with safe dates
#     today = date.today()
#     future_date = today + timedelta(days=1)
#     past_date = today - timedelta(days=1)
    
#     # Create completed todo first (can have past date)
#     completed_todo = Todo(
#         title="Complete",
#         due_date=future_date,  # Start with future date
#         description="Sample"
#     )
#     completed_todo.is_complete = True  # Mark complete AFTER creation
#     completed_todo.due_date = past_date  # THEN set past date (allowed for completed)
#     completed_todo.updated_at = datetime.now()
    
#     todos = {
#         "1": Todo(title="Incomplete", due_date=future_date),
#         "2": completed_todo
#     }
    
#     TodoView.show_todos(todos)
#     captured = capsys.readouterr().out
    
    # Verify output
    # assert "=== Todos ===" in captured
    # assert "[✗] Incomplete" in captured
    # assert "[✓] Complete" in captured
    # assert "(overdue!)" in captured
    # assert "Sample" in captured
    # assert "Total todos: 2" in captured

# def test_show_todos(capsys):
#     """Test todo list display"""
#     from datetime import datetime, timedelta
#     from src.models.todo_model import Todo
    
#     # Create test todos with safe dates
#     today = date.today()
#     todos = {
#         "1": Todo(
#             title="Incomplete",
#             due_date=today + timedelta(days=1)  # Future date
#         ),
#         "2": Todo(
#             title="Complete",
#             due_date=today - timedelta(days=1),  # Past date (overdue)
#             is_complete=True,
#             updated_at=datetime.now(),
#             description="Sample"
#         )
#     }
    
#     TodoView.show_todos(todos)
#     captured = capsys.readouterr().out
    
#     # Verify output
#     assert "=== Todos ===" in captured
#     assert "[✗] Incomplete" in captured
#     assert "[✓] Complete" in captured
#     assert "(overdue!)" in captured
#     assert "Sample" in captured
#     assert "Total todos: 2" in captured


# def test_show_todos(capsys):
#     """Test todo list display"""
#     from datetime import datetime
#     from src.models.todo_model import Todo
    
#     # Create test todos
#     todos = {
#         "1": Todo(title="Test 1", due_date=date(2099, 1, 1)),
#         "2": Todo(title="Test 2", due_date=date(2020, 1, 1),  # Overdue
#                  description="Test description", 
#                  is_complete=True,
#                  updated_at=datetime.now())
#     }
    
#     TodoView.show_todos(todos)
#     captured = capsys.readouterr().out
    
#     # Verify output contains expected elements
#     assert "=== Todos ===" in captured
#     assert "[✓] Test 2" in captured  # Completed
#     assert "[✗] Test 1" in captured  # Incomplete
#     assert "(overdue!)" in captured  # Overdue
#     assert "Test description" in captured
#     assert "Total todos: 2" in captured
#     assert "Completed: 1" in captured
#     assert "Overdue: 1" in captured
 

# def test_show_todos(capsys):
#     """Test todo list display with all states"""
#     from datetime import datetime, timedelta
#     from src.models.todo_model import Todo

#     today = date.today()
    
#     # 1. Create VALID todos first (all with future dates)
#     future_date = today + timedelta(days=1)
#     todos = {
#         "1": Todo(title="Normal", due_date=future_date),
#         "2": Todo(title="Completed", due_date=future_date),
#         "3": Todo(title="Overdue", due_date=future_date)
#     }
    
#     # 2. THEN modify them to test states (bypassing validation)
#     todos["2"].is_complete = True  # Completed
#     todos["3"].due_date = today - timedelta(days=1)  # Now overdue
    
#     # 3. Test display
#     TodoView.show_todos(todos)
#     output = capsys.readouterr().out
    
#     # Verify all states appear correctly
#     assert "[✗] Normal" in output
#     assert "[✓] Completed" in output
#     assert "[✗] Overdue (overdue!)" in output 


def test_show_todos(capsys):
    """Test todo display with all states"""
    today = date.today()
    
    # Create valid todos
    todos = {
        "1": Todo(title="Normal", due_date=today + timedelta(days=1)),
        "2": Todo(title="Completed", due_date=today + timedelta(days=1)),
        "3": Todo(title="Overdue", due_date=today + timedelta(days=1))
    }
    
    # Modify states
    todos["2"].is_complete = True
    todos["3"].due_date = today - timedelta(days=1)  # Make overdue
    
    TodoView.show_todos(todos)
    output = capsys.readouterr().out
    
    assert "=== Todos ===" in output
    assert "[✗] Normal" in output
    assert "[✓] Completed" in output
    assert "[✗] Overdue (overdue!)" in output

@patch('builtins.input')
def test_get_todo_id(mock_input):
    """Test ID input validation"""
    # Test cases
    test_cases = [
        ("1", "1"),  # Normal
        (" 2 ", "2"),  # Whitespace
        ("", ValueError),  # Empty
        ("   ", ValueError)  # Whitespace-only
    ]
    
    for input_val, expected in test_cases:
        mock_input.return_value = input_val
        if expected is ValueError:
            with pytest.raises(ValueError, match="ID cannot be empty"):
                TodoView.get_todo_id()
        else:
            assert TodoView.get_todo_id() == expected


def test_get_todo_id_validation():
    """Test ID input validation"""
    with patch('builtins.input') as mock_input:
        # Test valid input
        mock_input.return_value = "1"
        assert TodoView.get_todo_id() == "1"
        
        # Test empty input
        mock_input.return_value = ""
        with pytest.raises(ValueError):
            TodoView.get_todo_id()

def test_show_success(capsys):
    """Test success message display"""
    TodoView.show_success("Operation succeeded")
    captured = capsys.readouterr()
    assert "Success: Operation succeeded" in captured.out