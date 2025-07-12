import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.controllers.todo_controller import TodoController
from src.models.todo_model import TodoModel
from src.views.todo_view import TodoView

def main():
    controller = TodoController(TodoModel(), TodoView())
    controller.run()

if __name__ == "__main__":
    main()