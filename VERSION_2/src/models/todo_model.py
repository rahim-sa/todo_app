# version_2/src/models/todo_model.py
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List
import json
from pathlib import Path


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
        if not self.title:
            raise ValueError("Title cannot be empty")
        if self.due_date < date.today():
            raise ValueError("Due date cannot be in the past")


class TodoModel:
    def __init__(self, file_path: str = "todos.json"):
        self.file_path = Path(file_path)
        self.todos: Dict[str, Todo] = self._load_todos()

    def _load_todos(self) -> Dict[str, Todo]:
        try:
            if not self.file_path.exists():
                return {}
                
            with open(self.file_path) as f:
                data = json.load(f)
                todos = {}
                for k, v in data.items():
                    try:
                        # Convert string dates back to date/datetime objects
                        v['due_date'] = date.fromisoformat(v['due_date'])
                        v['created_at'] = datetime.fromisoformat(v['created_at'])
                        if v['updated_at']:
                            v['updated_at'] = datetime.fromisoformat(v['updated_at'])
                        todos[k] = Todo(**v)
                    except (ValueError, KeyError) as e:
                        print(f"Warning: Skipping invalid todo {k}: {e}")
                return todos
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load todos: {e}")
            return {}

    def save_todos(self) -> None:
        try:
            # Ensure directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.file_path, 'w') as f:
                json.dump(
                    {k: vars(v) for k, v in self.todos.items()}, 
                    f, 
                    default=str,
                    indent=2
                )
        except (IOError, TypeError) as e:
            raise RuntimeError(f"Failed to save todos: {e}")

    @property
    def completed_todos(self) -> List[Todo]:
        return [t for t in self.todos.values() if t.is_complete]