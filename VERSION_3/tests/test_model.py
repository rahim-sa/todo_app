import pytest
import sys
from pathlib import Path
import json
from unittest.mock import call

 
from unittest.mock import patch, MagicMock
import logging
 

sys.path.insert(0, str(Path(__file__).parent.parent))

#sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.todo_model import Todo
from src.exceptions import PersistenceError

from src.views.todo_view import TodoView
from src.models.todo_model import TodoModel
from src.controllers.todo_controller import TodoController
from unittest.mock import MagicMock   
from src.exceptions import PersistenceError

def test_todo_creation(sample_todo):
    assert sample_todo.title == "Test Todo"
    assert not sample_todo.is_complete

def test_model_add_todo(empty_model, sample_todo):
    empty_model.todos["1"] = sample_todo
    assert "1" in empty_model.todos

def test_load_invalid_data(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid}")
    model = TodoModel(bad_file)
    assert model.todos == {}  # Should handle corrupt files

#def test_save_empty_todos(empty_model, tmp_path):
 #   """Test saving empty todo list"""
  #  empty_model.file_path = tmp_path / "empty.json"
   # empty_model.save_todos()
    #assert empty_model.file_path.exists()

# Add to test_model.py

#def test_save_empty_todos(empty_model, tmp_path):
  #  """Test saving empty todo list"""
  #  test_file = tmp_path / "empty.json"
  #  empty_model.file_path = test_file
  #  empty_model.save_todos()
  #  assert test_file.exists()
  #  assert test_file.read_text() == '{}'  # Verify empty dict saved

#def test_completed_todos_property(empty_model, sample_todo):
   # """Test completed_todos property"""
   # sample_todo.is_complete = True
   # empty_model.todos = {"1": sample_todo, "2": MagicMock(is_complete=False)}
   # assert len(empty_model.completed_todos) == 1
   # assert empty_model.completed_todos[0].title == "Test Todo"

def test_completed_todos_property(empty_model, sample_todo):
    """Test completed_todos property"""
    from unittest.mock import MagicMock  # Or keep at top
    sample_todo.is_complete = True
    empty_model.todos = {
        "1": sample_todo, 
        "2": MagicMock(is_complete=False)
    }
    assert len(empty_model.completed_todos) == 1
    assert empty_model.completed_todos[0].title == "Test Todo"



 

def test_model_save_empty(tmp_path):
    """Test saving empty todo list"""
    model = TodoModel(tmp_path / "empty.json")
    model.todos = {}  # Explicitly set empty
    model.save_todos()
    
    # Verify file was created with empty JSON
    assert (tmp_path / "empty.json").exists()
    assert json.loads((tmp_path / "empty.json").read_text()) == {}


def test_controller_run_exit(real_controller, monkeypatch):
    """Test clean exit behavior"""
    # Setup
    exit_called = False
    original_save = real_controller.model.save_todos
    
    def mock_save():
        nonlocal exit_called
        exit_called = True
        original_save()
    
    # Mock the inputs and save method
    input_values = ["5"]  # Exit command
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))
    monkeypatch.setattr(real_controller.model, 'save_todos', mock_save)
    
    # Execute
    real_controller.run()
    
    # Verify
    assert exit_called, "Save should be called before exit"

    
def test_controller_run_invalid_choice(real_controller):
    """Test handling of invalid menu choices"""
    with patch('builtins.input', side_effect=["99", "5"]), \
         patch.object(real_controller.view, 'show_error') as mock_error:
        real_controller.run()
        mock_error.assert_called_with("Invalid choice")