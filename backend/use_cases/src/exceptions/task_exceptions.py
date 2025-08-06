class EmptyTaskTitleError(Exception):
    def __init__(self, message="Task title cannot be empty."):
        self.message = message
        super().__init__(self.message)


class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.message = f"Task with ID {task_id} not found."
        super().__init__(self.message)
        self.task_id = task_id
