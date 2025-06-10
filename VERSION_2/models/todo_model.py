class TodoModel:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.todos: Dict[str, Todo] = {}
        self.load_todos()