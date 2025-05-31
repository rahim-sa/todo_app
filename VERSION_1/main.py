 


import time
import json
from datetime import datetime


class Todo:
    def __init__(self, title: str, description: str, due_date: date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.is_complete = False
        self.created_at = datetime.now()

class TodoApp:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.todos = {}


#### Required Functions
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