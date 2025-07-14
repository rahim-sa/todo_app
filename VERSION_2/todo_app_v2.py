#!/usr/bin/env python3
"""
Main application entry point.
Initializes the MVC components and starts the program.
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.controllers.todo_controller import TodoController
from src.models.todo_model import TodoModel
from src.views.todo_view import TodoView

def main():
    # Initialize MVC components and start application.
    controller = TodoController(TodoModel(), TodoView())
    controller.run()  # Start main loop

if __name__ == "__main__":
    main()