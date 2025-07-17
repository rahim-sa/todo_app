import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

#sys.path.insert(0, str(Path(__file__).parent.parent))
from src.models.todo_model import Todo

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