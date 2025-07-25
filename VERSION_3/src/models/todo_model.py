# version_3/src/models/todo_model.py
"""
Data model: Handles storage and business logic.
Uses JSON for persistence.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List
import json
from pathlib import Path


try:
    from src.exceptions import PersistenceError
except ImportError:
    class PersistenceError(Exception):
        """Fallback if exceptions.py doesn't exist"""
        pass

@dataclass
class Todo:
    # Dataclass representing a single todo item
    title: str              # Required task name        
    description: str = ""   # Optional details
    due_date: date = date.today() # Default: today
    is_complete: bool = False   # Completion status
    created_at: datetime = field(default_factory=datetime.now)  # Auto-timestamp
    updated_at: datetime = None  # Set when modified

    @property
    def is_overdue(self) -> bool:
        #Check if incomplete todo is past due
        return self.due_date < date.today() and not self.is_complete

    def __post_init__(self):

        #Validate todo data on initialization"""
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Title must be a non-empty string")
        if self.due_date < date.today():
            raise ValueError("Due date cannot be in the past")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")
 
class TodoModel:
    # Manages todo collection and JSON persistence
    def __init__(self, file_path: str = "todos.json"):
        # Initialize with JSON storage path
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
                        # Keep original date/datetime handling
                        v['due_date'] = date.fromisoformat(v['due_date'])
                        v['created_at'] = datetime.fromisoformat(v['created_at'])
                        if v['updated_at']:
                            v['updated_at'] = datetime.fromisoformat(v['updated_at'])
                        
                        # Add your safety check
                        v.setdefault('description', '')
                        
                        todos[k] = Todo(**v)
                    except (ValueError, KeyError) as e:
                        print(f"Warning: Skipping invalid todo {k}: {e}")  # Keep warnings
                return todos
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load todos: {e}")
            return {}


    def save_todos(self):
        # Save todos to JSON with atomic write
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                data = {
                    k: {
                        'title': v.title,
                        'description': v.description,
                        'due_date': v.due_date.isoformat(),
                        'is_complete': v.is_complete,
                        'created_at': v.created_at.isoformat(),
                        'updated_at': v.updated_at.isoformat() if v.updated_at else None
                    } 
                    for k, v in self.todos.items()
                }
                json.dump(data, f, indent=2)
            print(f"DEBUG: Saved {len(self.todos)} todos")  # Verify saving
        except Exception as e:
            print(f"ERROR saving todos: {str(e)}")  # Debug failures

    @property
    def completed_todos(self) -> List[Todo]:
        # Get all completed todos (read-only property)
        return [t for t in self.todos.values() if t.is_complete]
    
 
