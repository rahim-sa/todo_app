 
# version_2/src/controllers/todo_controller.py
from src.models.todo_model import TodoModel, Todo
from src.views.todo_view import TodoView
from typing import Optional

 
class TodoController:
    def __init__(self, model: TodoModel, view: TodoView):
        self.model = model
        self.view = view

<<<<<<< HEAD
    def run(self) -> None:
        while True:
            self.view.show_menu()
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                self._add_todo()
            elif choice == "4":
                self._list_todos()
            elif choice == "5":
                self.model.save_todos()
                break
            else:
                self.view.show_error("Invalid choice")

    def _add_todo(self) -> None:
        try:
            data = self.view.get_todo_input()
            new_todo = Todo(**data)
            self.model.todos[str(len(self.model.todos)+1)] = new_todo
        except ValueError as e:
            self.view.show_error(str(e))
