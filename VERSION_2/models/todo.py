@dataclass
class Todo:
    title: str
    description: str
    due_date: date
    is_complete: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def is_overdue(self) -> bool:
        return self.due_date < date.today() and not self.is_complete