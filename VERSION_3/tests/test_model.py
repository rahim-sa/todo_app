import pytest
from src.models.todo_model import Todo

def test_todo_creation(sample_todo):
    """Test Todo dataclass initialization"""
    assert sample_todo.title == "Test Todo"
    assert sample_todo.description == "Test Description"
    assert not sample_todo.is_complete
    assert sample_todo.due_date.year == 2099

def test_model_add_todo(empty_model, sample_todo):
    """Test adding todo to model"""
    empty_model.todos["1"] = sample_todo
    assert "1" in empty_model.todos
    assert empty_model.todos["1"].title == "Test Todo"