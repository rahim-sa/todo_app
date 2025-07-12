class History:
    def __init__(self):
        self._undo_stack: List[Callable] = []
        self._redo_stack: List[Callable] = []

    def push_undo(self, action: Callable):
        self._undo_stack.append(action)