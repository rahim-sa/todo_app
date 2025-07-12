from src.models.todo_model import TodoModel, Todo
from src.views.todo_view import TodoView

class TodoController:
    def __init__(self, model: TodoModel, view: TodoView):
        self.model = model
        self.view = view
    
    def run(self):
        # Add sample todos
        self.model.todos.append(Todo("Buy milk", due_date="2023-12-01"))
        self.model.todos.append(Todo("Pay bills", completed=True))
        
        # Show all todos
        self.view.show_todos(self.model.todos)