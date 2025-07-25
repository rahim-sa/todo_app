class TodoError(Exception):
    """Base class for todo-related exceptions"""
    pass

class ValidationError(TodoError):
    """Raised when data validation fails"""
    pass

class PersistenceError(TodoError):
    """Raised when there are issues with data persistence"""
    pass

class NotFoundError(TodoError):
    """Raised when a todo is not found"""
    pass