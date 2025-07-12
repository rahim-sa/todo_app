# File: todo_app/models/__init__.py
# Empty file to mark package

# File: todo_app/views/__init__.py
# Empty file

# File: todo_app/main.py
from src.controllers.todo_controller import TodoController
from src.models.todo_model import TodoModel
from views.todo_view import TodoView

def main():

    #model = TodoModel()
    view = TodoView()
    controller = TodoController(model, view)
    controller.run()





 


if __name__ == "__main__":
    main()
