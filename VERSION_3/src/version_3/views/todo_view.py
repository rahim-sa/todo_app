class Todo:
    def __init__(self, task: str, done: bool = False):
        self.task = task
        self.done = done

    def mark_done(self):
        self.done = True
