class TodoController:
    def __init__(self, model: TodoModel, view: TodoView):
        self.model = model
        self.view = view

    def run(self):
        while True:
            self.view.show_menu()
            choice = self.view.get_input("Choose option: ")
            if choice == '1':
                self._handle_add_todo()