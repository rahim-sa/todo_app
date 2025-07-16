import sys
from pathlib import Path

# Add root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Fixtures available for all tests
import pytest
from datetime import date
from src.models.todo_model import Todo, TodoModel

@pytest.fixture
def sample_todo():
    return Todo(title="Test", due_date=date.today())

@pytest.fixture
def empty_model(tmp_path):
    return TodoModel(tmp_path / "test_todos.json")