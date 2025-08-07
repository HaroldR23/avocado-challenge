from datetime import datetime

from use_cases.src.exceptions import UserNotFoundError, TaskNotFoundError, EmptyTaskTitleError
from use_cases.src.task.update.input import UpdateTaskInput
from domain.src.ports.repositories import TaskRepository, UserRepository

class UpdateTaskUseCase:
    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self.task_repository = task_repository
        self.user_repository = user_repository

    def __call__(self, task_id: int, update_task_input: UpdateTaskInput) -> None:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(task_id=task_id)

        if update_task_input.title is not None:
            if update_task_input.title.strip() == "":
                raise EmptyTaskTitleError()
            task.title = update_task_input.title

        if update_task_input.assigned_to_id is not None:
            user = self.user_repository.find_by_id(update_task_input.assigned_to_id)
            if not user:
                raise UserNotFoundError(user_id=update_task_input.assigned_to_id)
            task.assigned_to = user

        updatable_fields = ["completed", "priority", "due_date", "description"]
        for field in updatable_fields:
            value = getattr(update_task_input, field)
            if value is not None:
                setattr(task, field, value)


        task.updated_at = datetime.now().isoformat()

        self.task_repository.update(task)
