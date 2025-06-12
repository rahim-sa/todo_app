class TodoModel:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.todos: Dict[str, Todo] = {}
        self.load_todos()

    @property
    def pending_todos(self) -> List[Todo]:
        return [t for t in self.todos.values() if not t.is_complete]
    

def search(self, keyword: str) -> List[Todo]:
    return [t for t in self.todos.values() 
            if keyword.lower() in t.title.lower() 
            or keyword.lower() in t.description.lower()]