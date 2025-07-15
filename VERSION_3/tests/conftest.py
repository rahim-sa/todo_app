import pytest
from datetime import date
from src.models.todo_model import Todo

@pytest.fixture
def sample_todo():
    return Todo(
        title="Test Todo",
        description="Test Description",
        due_date=date(2023, 12, 31)
    )

@pytest.fixture
def empty_model(tmp_path):
    from src.models.todo_model import TodoModel
    return TodoModel(tmp_path / "test_todos.json")