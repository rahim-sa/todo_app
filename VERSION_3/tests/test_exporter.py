import pytest
import os
from datetime import date
from src.models.todo_model import Todo
from src.utils.exporter import export_to_json
from src.exceptions import PersistenceError  # Added as requested

def test_export_permission_error(tmp_path):
    """Test real permission error handling"""
    # 1. Setup read-only file
    test_file = tmp_path / "readonly.json"
    test_file.write_text("")  # Create file
    
    # Make read-only (Unix)
    test_file.chmod(0o400)
    
    # 2. Prepare test data
    test_data = {
        "1": Todo(
            title="Test",
            due_date=date(2099, 1, 1),
            description="",
            is_complete=False
        )
    }

    # 3. Test and verify
    with pytest.raises(PersistenceError) as exc_info:  # Changed to PersistenceError
        export_to_json(test_data, test_file)
    
    assert "permission" in str(exc_info.value).lower()
    