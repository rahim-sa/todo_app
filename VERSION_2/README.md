# Todo App (CLI Version)

## Features
- ✅ Add tasks with titles, descriptions, due dates
- ✔️ Mark tasks as complete
- 🗑️ Delete tasks
- 📋 List all tasks with status

## Quick Start
1. Install Python 3.8+
2. Run:
   ```bash
   python todo_app_v2.py

    Use menu:
    text

    1. Add Todo
    2. Complete Todo 
    3. Delete Todo
    4. List Todos
    5. Exit

Data Storage

    Tasks save automatically to data/todos.json

    Format:
    json

    {
      "1": {
        "title": "Buy milk",
        "is_complete": false,
        "due_date": "2023-12-01"
      }
    }

text


Key documentation principles applied:
1. **Code Comments**:
   - Explain the *why* not just the *what*
   - Focus on data flow
   - Highlight key technical decisions

2. **README**:
   - Feature icons for quick scanning
   - Minimal setup instructions
   - Clear example of data format