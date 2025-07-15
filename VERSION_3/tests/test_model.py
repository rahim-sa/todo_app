from datetime import date
import pytest

class TestTodoModel:
    def test_add_todo(self, empty_model, sample_todo):
        empty_model.todos["1"] = sample_todo
        assert "1" in empty_model.todos
        assert empty_model.todos["1"].title == "Test Todo"

    def test_save_load(self, empty_model, sample_todo, tmp_path):
        empty_model.todos["1"] = sample_todo
        empty_model.file_path = tmp_path / "todos.json"
        empty_model.save_todos()
        
        new_model = empty_model.__class__(empty_model.file_path)
        assert "1" in new_model.todos
        assert new_model.todos["1"].title == "Test Todo"