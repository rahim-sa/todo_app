# version_2/src/controllers/todo_controller.py
from src.models.todo_model import TodoModel, Todo
from src.views.todo_view import TodoView
from typing import Optional


class TodoController:
    def __init__(self, model: TodoModel, view: TodoView):
        self.model = model
        self.view = view

    def run(self) -> None:
        while True:
            self.view.show_menu()
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                self._add_todo()
            elif choice == "2":
                self._complete_todo()
            elif choice == "3":
                self._delete_todo()
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
            todo_id = str(len(self.model.todos)+1)
            self.model.todos[todo_id] = new_todo
            self.view.show_success(f"Todo added with ID: {todo_id}")
        except ValueError as e:
            self.view.show_error(str(e))

    def _complete_todo(self) -> None:
        try:
            todo_id = self.view.get_todo_id()
            if todo_id in self.model.todos:
                self.model.todos[todo_id].is_complete = True
                self.model.todos[todo_id].updated_at = datetime.now()
                self.view.show_success(f"Todo {todo_id} marked as complete")
            else:
                self.view.show_error("Todo not found")
        except ValueError as e:
            self.view.show_error(str(e))

    def _delete_todo(self) -> None:
        try:
            todo_id = self.view.get_todo_id()
            if todo_id in self.model.todos:
                del self.model.todos[todo_id]
                self.view.show_success(f"Todo {todo_id} deleted")
            else:
                self.view.show_error("Todo not found")
        except ValueError as e:
            self.view.show_error(str(e))

    def _list_todos(self) -> None:

        self.view.show_todos(self.model.todos)