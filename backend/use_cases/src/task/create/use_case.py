from domain.src.ports.repositories import TaskRepository, UserRepository, RepositoryException
from domain.src.entities.task import Task
from use_cases.src.task.create import CreateTaskInput, CreateTaskOutput
from use_cases.src.exceptions import UserNotFoundError, EmptyTaskTitleError

from datetime import datetime as Datetime

class CreateTaskUseCase:
    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self.task_repository = task_repository
        self.user_repository = user_repository

    def __call__(self, task_input: CreateTaskInput) -> CreateTaskOutput:
        task_creator_user = self.user_repository.find_by_id(task_input.created_by_id)
        user_assigned_to_task = None

        if task_input.assigned_to_id:
            user_assigned_to_task = self.user_repository.find_by_id(task_input.assigned_to_id)

            if not user_assigned_to_task:
                raise UserNotFoundError(user_id=task_input.assigned_to_id)
    
        if not task_creator_user:
            raise UserNotFoundError(user_id=task_input.created_by_id)

        if task_input.title.strip() == "":
            raise EmptyTaskTitleError()
        
        task = Task(
            title=task_input.title,
            description=task_input.description,
            priority=task_input.priority,
            due_date=task_input.due_date,
            created_by=task_creator_user,
            assigned_to=user_assigned_to_task,
            created_at=Datetime.now().isoformat(),
            updated_at=Datetime.now().isoformat()
        )

        try:
            created_task = self.task_repository.create(task=task)
        except RepositoryException as e:
            raise e

        return CreateTaskOutput(
            id=created_task.id,
            title=created_task.title,
            description=created_task.description,
            priority=created_task.priority,
            due_date=str(created_task.due_date),
            assigned_to=created_task.assigned_to,
            created_by=created_task.created_by,
            created_at=str(created_task.created_at),
            comments=created_task.comments,
            completed=created_task.completed
        )
