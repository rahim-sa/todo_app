# version_2/src/views/todo_view.py
from datetime import date
from typing import Optional, Dict, Any
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
    def get_todo_input() -> Dict[str, Any]:
        title = input("Title: ").strip()
        if not title:
            raise ValueError("Title cannot be empty")
        desc = input("Description (optional): ").strip()
        due = input(f"Due date ({date.today()}): ").strip() or str(date.today())
        try:
            due_date = date.fromisoformat(due)
            if due_date < date.today():
                raise ValueError("Due date cannot be in the past")
            return {
                "title": title, 
                "description": desc, 
                "due_date": due_date
            }
        except ValueError as e:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD")

    @staticmethod
    def get_todo_id() -> str:
        todo_id = input("Enter Todo ID: ").strip()
        if not todo_id:
            raise ValueError("ID cannot be empty")
        return todo_id

    @staticmethod
    def show_todos(todos: Dict[str, Todo]) -> None:
        if not todos:
            print("No todos found")
            return
            
        print("\n=== Todos ===")
        for todo_id, todo in todos.items():
            status = "✓" if todo.is_complete else "✗"
            overdue = " (overdue)" if todo.is_overdue else ""
            print(f"{todo_id}. [{status}] {todo.title}{overdue}")
            print(f"   Due: {todo.due_date}, Created: {todo.created_at}")
            if todo.description:
                print(f"   Description: {todo.description}")
            print()

    @staticmethod
    def show_error(message: str) -> None:
        print(f"Error: {message}")

    @staticmethod
    def show_success(message: str) -> None:
 
        #Display success messages"""
        print(f"Success: {message}")

    
     
    @staticmethod
    def get_todo_input() -> Dict:
        title = input("Title: ").strip()
        if not title:
            raise ValueError("Title cannot be empty")
        
        desc = input("Description (optional): ").strip()
        due = input(f"Due date ({date.today()}): ").strip() or str(date.today())
        
        try:
            due_date = date.fromisoformat(due)
            if due_date < date.today():
                raise ValueError("Due date cannot be in the past")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        
        return {"title": title, "description": desc, "due_date": due_date}

    
 
