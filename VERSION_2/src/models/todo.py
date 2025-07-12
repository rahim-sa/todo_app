from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Set

@dataclass
class Todo:
    title: str
    description: str
    due_date: date
    is_complete: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    categories: List[str] = field(default_factory=list)  # Added for Feature 9
    tags: Set[str] = field(default_factory=set)         # Added for Feature 9

    @property
    def is_overdue(self) -> bool:
        return self.due_date < date.today() and not self.is_complete