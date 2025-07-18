# class History:
#     def __init__(self):
#         self._undo_stack: List[Callable] = []
#         self._redo_stack: List[Callable] = []

#     def push_undo(self, action: Callable):
#         self._undo_stack.append(action)

from typing import Callable, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class HistoryEntry:
    """Represents a single history entry"""
    action: str
    todo_id: str
    timestamp: datetime = datetime.now()

class History:
    """Tracks todo operations history"""
    def __init__(self):
        self.entries: List[HistoryEntry] = []
        self._undo_stack: List[Callable] = []
    
    def add_entry(self, action: str, todo_id: str) -> None:
        """Add a new history entry"""
        self.entries.append(HistoryEntry(action, todo_id))
    
    def push_undo(self, action: Callable) -> None:
        """Register an undo operation"""
        self._undo_stack.append(action)
    
    def pop_undo(self) -> Optional[Callable]:
        """Get the last undo operation"""
        return self._undo_stack.pop() if self._undo_stack else None
    
    def clear(self) -> None:
        """Clear all history"""
        self.entries.clear()
        self._undo_stack.clear()
