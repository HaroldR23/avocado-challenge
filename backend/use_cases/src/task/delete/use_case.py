from domain.src.ports.repositories import TaskRepository, RepositoryException
from use_cases.src.exceptions.task_exceptions import TaskNotFoundError


class DeleteTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def __call__(self, task_id: int) -> None:
        try:
            task = self.task_repository.delete(task_id=task_id)
            if not task:
                raise TaskNotFoundError(task_id=task_id)
        except RepositoryException as e:
            raise e
