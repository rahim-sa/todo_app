from datetime import datetime
import json
import os

class Todo:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.is_complete = False  # Changed from 'completed' to 'is_complete'
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'is_complete': self.is_complete,  # Consistent naming
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @classmethod
    def from_dict(cls, data):
        todo = cls(data['title'], data['description'], data['due_date'])
        todo.is_complete = data['is_complete']  # Consistent naming
        todo.created_at = datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')
        return todo

def save_todos(todos, filename='todos.json'):
    with open(filename, 'w') as f:
        json.dump([todo.to_dict() for todo in todos], f)

def load_todos(filename='todos.json'):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as f:
            return [Todo.from_dict(todo) for todo in json.load(f)]
    except json.JSONDecodeError:
        return []

class TodoApp:
    def __init__(self):
        self.todos = load_todos()
    
    def add_todo(self, title, description, due_date):
        if not title.strip():
            raise ValueError("Title cannot be empty")
        self.todos.append(Todo(title, description, due_date))
        save_todos(self.todos)
    
    def complete_todo(self, index):
        if 0 <= index < len(self.todos):
            self.todos[index].is_complete = True  # Fixed attribute name
            save_todos(self.todos)
        else:
            raise ValueError("Invalid index")
    
    def list_todos(self):
        return self.todos.copy()

def display_todos(todos):
    print("\nYour TODOs:")
    for i, todo in enumerate(todos):
        status = "✓" if todo.is_complete else " "  # Fixed attribute name
        print(f"{i}. [{status}] {todo.title} (Due: {todo.due_date})")
        print(f"   {todo.description}\n")

def main():
    app = TodoApp()
    while True:
        print("\nTODO App Menu:")
        print("1. Add TODO")
        print("2. Complete TODO")
        print("3. List TODOs")
        print("4. Exit")
        
        choice = input("Choose option (1-4): ")
        
        try:
            if choice == '1':
                title = input("Title: ")
                description = input("Description: ")
                due_date = input("Due date (YYYY-MM-DD): ")
                app.add_todo(title, description, due_date)
                print("TODO added!")
            
            elif choice == '2':
                display_todos(app.list_todos())
                index = int(input("Enter TODO number to complete: "))
                app.complete_todo(index)
                print("Marked as complete!")
            
            elif choice == '3':
                display_todos(app.list_todos())
            
            elif choice == '4':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice")
        
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()