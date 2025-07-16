import pytest
from src.models.todo_model import Todo

def test_todo_creation(sample_todo):
    assert sample_todo.title == "Test Todo"
    assert not sample_todo.is_complete

def test_model_add_todo(empty_model, sample_todo):
    empty_model.todos["1"] = sample_todo
    assert "1" in empty_model.todos