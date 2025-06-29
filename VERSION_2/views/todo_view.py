# File: todo_app/views/todo_view.py
class TodoView:
    @staticmethod
    def show_menu() -> None:
        print("1. Add Todo")

    @staticmethod
    def get_input(prompt: str) -> str:
        return input(prompt).strip()
    print(f"Due: {todo.due_date} {'(Overdue!)' if todo.is_overdue else ''}")