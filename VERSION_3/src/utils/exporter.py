# import json
# from typing import List

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.exceptions import PersistenceError 

# from src.models.todo_model import Todo  # Correct path
# #from ..models.todo import Todo
# #from src.models.todo_model import Todo

# def export_to_json(todos: List[Todo], filename: str) -> None:
#     with open(filename, 'w') as f:
#         json.dump([todo.to_dict() for todo in todos], f, indent=2)

import json
import csv
from pathlib import Path
from src.models.todo_model import Todo


# def export_to_json(todos: dict, file_path: Path) -> None:
#     """Simplified JSON export"""
#     with open(file_path, 'w') as f:
#         json.dump({
#             id: {
#                 'title': todo.title,
#                 'due_date': todo.due_date.isoformat()
#             }
#             for id, todo in todos.items()
#         }, f)

def export_to_csv(todos: dict, file_path: Path) -> None:
    """Simplified CSV export"""
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'due_date'])
        for id, todo in todos.items():
            writer.writerow([id, todo.title, todo.due_date.isoformat()])

def export_to_json(todos: dict, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(...)  # Your existing code
    except (PermissionError, IOError) as e:
        raise PersistenceError(f"Export failed: {str(e)}") from e