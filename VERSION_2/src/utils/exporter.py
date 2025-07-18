import json
from typing import List
from ..models.todo import Todo

def export_to_json(todos: List[Todo], filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump([todo.to_dict() for todo in todos], f, indent=2)