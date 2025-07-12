# version_2/src/views/todo_view.py
from datetime import date
from typing import Optional, Dict
from src.models.todo_model import Todo

class TodoView:
    @staticmethod
    def show_menu() -> None:
        print("\n=== Todo Manager ===")
        print("1. Add Todo")
        print("2. Complete Todo")
        print("3. Delete Todo")
        print("4. List Todos")
        print("5. Exit")

    @staticmethod
    def get_todo_input() -> Dict:
        title = input("Title: ").strip()
        desc = input("Description (optional): ").strip()
        due = input(f"Due date ({date.today()}): ").strip() or str(date.today())
        return {"title": title, "description": desc, "due_date": date.fromisoformat(due)}

    @staticmethod
    def show_error(message: str) -> None:
        print(f"Error: {message}")