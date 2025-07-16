import json
from typing import List
from ..models.todo import Todo

def import_from_json(filename: str) -> List[Todo]:
    with open(filename) as f:
        return [Todo.from_dict(data) for data in json.load(f)]