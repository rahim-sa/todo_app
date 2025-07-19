import pytest
from datetime import date
from pathlib import Path
import sys
from unittest.mock import call

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.todo_model import Todo, TodoModel
from src.views.todo_view import TodoView  # Add this
from src.controllers.todo_controller import TodoController


@pytest.fixture
def sample_todo():
    return Todo(
        title="Test Todo",
        description="Test Description",
        due_date=date(2099, 12, 31)  # Future date
    )

@pytest.fixture
def empty_model(tmp_path):
    model = TodoModel(tmp_path / "test_todos.json")
    yield model
    if Path(tmp_path / "test_todos.json").exists():
        Path(tmp_path / "test_todos.json").unlink()


@pytest.fixture
def real_controller(tmp_path):
    """Controller with real components using test data"""
    model = TodoModel(tmp_path / "test_todos.json")
    view = TodoView()
    return TodoController(model, view)