import pytest
from datetime import date

class TestIntegration:
    def test_full_workflow(self, empty_model, sample_todo):
        # Test model
        empty_model.todos["1"] = sample_todo
        assert "1" in empty_model.todos
        
        # Test marking complete
        empty_model.todos["1"].is_complete = True
        assert empty_model.todos["1"].is_complete
        
        # Test deletion
        del empty_model.todos["1"]
        assert "1" not in empty_model.todos