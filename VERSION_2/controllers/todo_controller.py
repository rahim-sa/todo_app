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

    def _handle_list_todos(self):
        filter_choice = input("Show [A]ll/[C]ompleted/[P]ending: ").upper()
        todos = (
            self.model.completed_todos if filter_choice == 'C' else
            self.model.pending_todos if filter_choice == 'P' else
            self.model.all_todos
        )