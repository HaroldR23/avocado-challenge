class EmptyTaskTitleError(Exception):
    def __init__(self, message="Task title cannot be empty."):
        self.message = message
        super().__init__(self.message)
