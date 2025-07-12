from src.models.todo_model import Todo  # Import the Todo class

class TodoView:
    def show_todo(self, todo: Todo):  # Properly type-hinted parameter
        status = "✓" if todo.completed else " "
        print(f"[{status}] {todo.title}")
        if todo.due_date:
            print(f"Due: {todo.due_date} {'(Overdue!)' if todo.is_overdue else ''}")
    
    def show_todos(self, todos: list[Todo]):
        for todo in todos:
            self.show_todo(todo)