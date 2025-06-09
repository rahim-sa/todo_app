import time
import json
from datetime import date
from datetime import datetime


class Todo:
    def __init__(self, title: str, description: str, due_date: date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.is_complete = False
        self.created_at = datetime.now()


    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    @classmethod
    def from_dict(cls, data):
        todo = cls(data['title'], data['description'], data['due_date'])
        todo.completed = data['completed']
        todo.created_at = datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')
        return todo

class TodoApp:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.todos = {}


##### Required Functions
#1. TODO Management
 #  - add_todo(title, description, due_date)
  # - complete_todo(title)
   #- delete_todo(title)
   #- list_todos()

#2. File Operations
 #  - save_to_file()
  # - load_from_file()

#### Success Criteria
#- [ ] Basic CRUD operations working
#- [ ] Data persists between sessions
#- [ ] Basic error handling implemented
#- [ ] Input validation working

def main():
    print("Hello from todo-app-v1!")


if __name__ == "__main__":
    main()

print("base feature is on going")