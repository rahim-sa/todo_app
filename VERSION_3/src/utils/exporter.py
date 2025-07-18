# import json
# from typing import List

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.exceptions import PersistenceError 
import json
import csv
from pathlib import Path
from src.models.todo_model import Todo

def export_to_csv(todos: dict, file_path: Path) -> None:
    """Simplified CSV export"""
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'due_date'])
        for id, todo in todos.items():
            writer.writerow([id, todo.title, todo.due_date.isoformat()])

# def export_to_json(todos: dict, file_path):
#     try:
#         with open(file_path, 'w') as f:
#             json.dump(...)  # Your existing code
#     except (PermissionError, IOError) as e:
#         raise PersistenceError(f"Export failed: {str(e)}") from e
    

def export_to_json(todos: dict, file_path: Path) -> None:
    """Export todos to JSON file with proper error handling"""
    try:
        with open(file_path, 'w') as f:
            # Convert Todo objects to serializable dictionaries
            serializable = {
                k: {
                    'title': v.title,
                    'description': v.description,
                    'due_date': v.due_date.isoformat(),
                    'is_complete': v.is_complete,
                    'created_at': v.created_at.isoformat(),
                    'updated_at': v.updated_at.isoformat() if v.updated_at else None
                }
                for k, v in todos.items()
            }
            json.dump(serializable, f, indent=2)
    except (PermissionError, IOError) as e:
        raise PersistenceError(f"Export failed: {str(e)}") from e