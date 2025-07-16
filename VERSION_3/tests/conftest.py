import pytest
from datetime import date
from pathlib import Path
import sys

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.todo_model import Todo, TodoModel

@pytest.fixture
def sample_todo():
    """Sample Todo item with future due date"""
    return Todo(
        title="Test Todo",
        description="Test Description",
        due_date=date(2099, 12, 31)  # Future date to avoid validation errors
    )

@pytest.fixture
def empty_model(tmp_path):
    """TodoModel instance with temporary storage"""
    model = TodoModel(tmp_path / "test_todos.json")
    yield model
    # Clean up test file
    test_file = tmp_path / "test_todos.json"
    if test_file.exists():
        test_file.unlink()