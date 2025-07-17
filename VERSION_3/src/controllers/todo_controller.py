# version_2/src/controllers/todo_controller.py
"""
Controller: Mediates between View and Model.
Handles user input and coordinates data operations.
"""


from src.models.todo_model import TodoModel, Todo
from src.views.todo_view import TodoView
from typing import Optional
import logging
from datetime import datetime

# Fallback exception class  
class TodoError(Exception):
    # Base exception for todo-related errors"""
    pass

class TodoController:
    # Initialize with model and view components
    def __init__(self, model: TodoModel, view: TodoView):
        self.model = model  # Data operations (storage/retrieval)
        self.view = view  # User interface rendering
        logging.basicConfig(
            filename='todo_app.log',
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def run(self) -> None:
        try:
            while True:
                self.view.show_menu()
                choice = input("Choose an option: ").strip()
                
                # CRUD operation routing
                if choice == "1":
                    self._add_todo()
                elif choice == "2":
                    self._complete_todo()
                elif choice == "3":
                    self._delete_todo()
                elif choice == "4":
                    self._list_todos()
                elif choice == "5":
                    self.model.save_todos()  # Persist data before exit
                    break
                else:
                    self.view.show_error("Invalid choice")
        except TodoError as e:
            self.view.show_error(f"Application error: {str(e)}")
            logging.error(f"TodoError: {str(e)}")
        except Exception as e:
            self.view.show_error("An unexpected error occurred")
            logging.critical(f"Unexpected error: {str(e)}", exc_info=True)

    # Create new todo from user input
     

    
    def _add_todo(self):
        try:
            data = self.view.get_todo_input()
            new_todo = Todo(**data)
            todo_id = str(len(self.model.todos) + 1)
            self.model.todos[todo_id] = new_todo
            self.model.save_todos()
        except ValueError as e:
            self.view.show_error(str(e))
            raise  # Re-raise for tests
        except Exception as e:  # Catch storage errors
            self.view.show_error("Failed to save todo")
            logging.error(f"Storage error: {str(e)}")
            raise TodoError("Storage failed") from e  # This is the key line
    
    
    
    
    

    # Completes the selected todo 
    #def _complete_todo(self) -> None:
      #  try:
       #     todo_id = self.view.get_todo_id()
         #   if todo_id in self.model.todos:
          #      self.model.todos[todo_id].is_complete = True
          #      self.model.todos[todo_id].updated_at = datetime.now()
          #      self.view.show_success(f"Todo {todo_id} marked as complete")
           # else:
          #      self.view.show_error("Todo not found")
       # except ValueError as e:
           # self.view.show_error(str(e))
        #except Exception as e:
            #self.view.show_error("Failed to complete todo")
           # logging.error(f"Complete todo error: {str(e)}", exc_info=True)

    def _complete_todo(self) -> None:
        try:
            todo_id = self.view.get_todo_id()
            if todo_id in self.model.todos:
                self.model.todos[todo_id].is_complete = True
                self.model.todos[todo_id].updated_at = datetime.now()
                self.view.show_success(f"Todo {todo_id} marked as complete")
            else:
                raise ValueError("Todo not found")  # Add this line
        except ValueError as e:
            self.view.show_error(str(e))
            raise  # Re-raise after showing
        except Exception as e:
            self.view.show_error("Failed to complete todo")
            logging.error(f"Complete todo error: {str(e)}", exc_info=True)

    # Delete selected todo from list
    def _delete_todo(self):
        try:
            todo_id = self.view.get_todo_id()
            if todo_id in self.model.todos:
                del self.model.todos[todo_id]
                self.model.save_todos()   
                self.view.show_success(f"Todo {todo_id} deleted")
            else:
                self.view.show_error("Todo not found")
        except Exception as e:
            self.view.show_error(f"Delete failed: {str(e)}")
            logging.error(f"Delete error: {str(e)}")

    # Shows the list of available todos
    def _list_todos(self) -> None:
        try:
            self.view.show_todos(self.model.todos)
        except Exception as e:
            self.view.show_error("Failed to load todos")
            logging.error(f"List todos error: {str(e)}", exc_info=True)