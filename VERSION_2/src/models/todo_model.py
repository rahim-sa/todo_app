 
# version_2/src/models/todo_model.py
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List
import json

@dataclass
class Todo:
    title: str
    description: str = ""
    due_date: date = date.today()
    is_complete: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = None

    @property
    def is_overdue(self) -> bool:
        return self.due_date < date.today() and not self.is_complete

    def __post_init__(self):
        """Validate todo data on initialization"""
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Title must be a non-empty string")
        if self.due_date < date.today():
            raise ValueError("Due date cannot be in the past")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")
class TodoModel:
    def __init__(self, file_path: str = "todos.json"):
        self.file_path = file_path
        self.todos: Dict[str, Todo] = self._load_todos()

    def _load_todos(self) -> Dict[str, Todo]:
        try:
            with open(self.file_path) as f:
                data = json.load(f)
                return {k: Todo(**v) for k,v in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_todos(self) -> None:
        with open(self.file_path, 'w') as f:
            json.dump({k: vars(v) for k,v in self.todos.items()}, f, default=str)

    @property
    def completed_todos(self) -> List[Todo]:
        return [t for t in self.todos.values() if t.is_complete]
