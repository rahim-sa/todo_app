import pytest
from pathlib import Path
from datetime import date
from src.models.todo_model import Todo  # <-- Add this import
from src.utils.exporter import export_to_json

def test_export_minimal_todo(tmp_path):
    """Test exporting simplest possible todo"""
    test_data = {
        "1": Todo(
            title="Minimal", 
            due_date=date(2099,1,1), 
            description="",
            is_complete=False
        )
    }
    output_file = tmp_path / "minimal.json"
    export_to_json(test_data, output_file)
    
    content = output_file.read_text()
    assert '"title": "Minimal"' in content
    assert '"due_date": "2099-01-01"' in content





 