@dataclass
class Todo:
    title: str
    description: str
    due_date: date
    is_complete: bool = False
    created_at: datetime = field(default_factory=datetime.now)