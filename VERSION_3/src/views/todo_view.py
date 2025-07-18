# version_2/src/views/todo_view.py
"""
View: Handles all user input/output.
Separates UI concerns from business logic.
"""

from datetime import date
from typing import Optional, Dict, Any
from src.models.todo_model import Todo

class TodoView:
    @staticmethod
    def show_menu() -> None:
        # Display main menu options
        print("\n=== Todo Manager ===")
        print("1. Add Todo")
        print("2. Complete Todo")
        print("3. Delete Todo")
        print("4. List Todos")
        print("5. Exit")

    @staticmethod
    def get_todo_input() -> Dict[str, Any]:
        # Collect validated todo data from user
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
        # Collect validated id from user
        todo_id = input("Enter Todo ID: ").strip()
        if not todo_id:
            raise ValueError("ID cannot be empty")
        return todo_id

    # In todo_view.py
    @staticmethod
    def show_todos(todos: Dict[str, Todo]) -> None:
        # Shows available todo tasks
        if not todos:
            print("\nNo todos found")
            return
            
        print("\n=== Todos ===")
        for todo_id, todo in todos.items():
            status = "✓" if todo.is_complete else "✗"
            overdue = " (overdue!)" if todo.is_overdue else ""
            print(f"\n{todo_id}. [{status}] {todo.title}{overdue}")
            print(f"   Due: {todo.due_date}")
            print(f"   Created: {todo.created_at.strftime('%Y-%m-%d %H:%M')}")
            if todo.updated_at:
                print(f"   Updated: {todo.updated_at.strftime('%Y-%m-%d %H:%M')}")
            if todo.description:
                print(f"   Description: {todo.description}")
        
        print(f"\nTotal todos: {len(todos)}")
        print(f"Completed: {sum(1 for t in todos.values() if t.is_complete)}")
        print(f"Overdue: {sum(1 for t in todos.values() if t.is_overdue)}")

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

    
 
