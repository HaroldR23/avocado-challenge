from domain.src.ports.repositories import TaskRepository
from use_cases.src.task.get_with_filters import GetTasksInput, GetTasksOutput, TaskOutput
from domain.src.entities.user import User
from domain.src.ports.repositories.exceptions import RepositoryException

class GetTasksUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def __call__(self, filters: GetTasksInput) -> GetTasksOutput:
        try: 
            tasks, total = self.task_repository.find_all_with_filters(
                completed=filters.completed,
                priority=filters.priority,
                assigned_to_id=filters.assigned_to_id,
                created_by_id=filters.created_by_id,
                due_date_before=filters.due_date_before,
                due_date_after=filters.due_date_after,
                page=filters.page,
                limit=filters.limit,
                order=filters.order
            )
        except RepositoryException as e:
            raise e

        if not tasks:
            return GetTasksOutput(tasks=[], total=0, page=filters.page, limit=filters.limit)
        
        return GetTasksOutput(
            tasks=[
                TaskOutput(
                    id=t.id,
                    title=t.title,
                    description=t.description,
                    priority=t.priority,
                    due_date=t.due_date,
                    completed=t.completed,
                    created_by=User(
                        id=t.created_by.id,
                        username=t.created_by.username,
                        email=t.created_by.email,
                    ),
                    assigned_to=User(
                        id=t.assigned_to.id,
                        username=t.assigned_to.username,
                        email=t.assigned_to.email,
                    ) if t.assigned_to else None,
                    created_at=t.created_at,
                    updated_at=t.updated_at
                )
                for t in tasks
            ],
            total=total,
            page=filters.page,
            limit=filters.limit
        )
