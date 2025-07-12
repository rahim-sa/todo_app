from typing import List
from dataclasses import dataclass

@dataclass
class Todo:
    title: str
    completed: bool = False
    due_date: str = None  # Add this field

    @property
    def is_overdue(self) -> bool:
        # Implement your overdue logic here
        return False

class TodoModel:
    def __init__(self):
        self.todos: List[Todo] = []
    
    def pending_todos(self) -> List[Todo]:
        return [todo for todo in self.todos if not todo.completed]