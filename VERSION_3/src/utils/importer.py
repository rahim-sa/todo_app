# import json
# from typing import List
# from ..models.todo import Todo

# def import_from_json(filename: str) -> List[Todo]:
#     with open(filename) as f:
#         return [Todo.from_dict(data) for data in json.load(f)]
    

import json
from pathlib import Path
from datetime import date
from typing import Dict
from src.models.todo_model import Todo

def import_from_json(file_path: Path) -> Dict[str, Todo]:
    try:
        with open(file_path) as f:
            data = json.load(f)
            return {
                id: Todo(
                    title=todo_data['title'],
                    due_date=date.fromisoformat(todo_data['due_date']),
                    description=todo_data.get('description', '')
                )
                for id, todo_data in data.items()
            }
    except Exception as e:
        raise ValueError(f"Import failed: {str(e)}")