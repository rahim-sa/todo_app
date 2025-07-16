import pytest
from datetime import date
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from src.models.todo_model import Todo, TodoModel

sys.path.append(str(Path(__file__).parent.parent))

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