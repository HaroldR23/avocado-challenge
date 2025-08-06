from domain.src.ports.repositories import TaskRepository, RepositoryException
from domain.src.entities import Task, User
from infrastructure.src.adapters.sql_alchemy.models import Task as TaskModel

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, task: Task) -> Task:
        try:
            task_to_create = TaskModel(
                title=task.title,
                description=task.description,
                priority=task.priority,
                due_date=task.due_date,
                created_by_id=task.created_by.id,
                assigned_to_id=task.assigned_to.id if task.assigned_to else None,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            self.session.add(task_to_create)
            self.session.commit()
            self.session.refresh(task_to_create)

            return Task(
                id=task_to_create.id,
                title=task_to_create.title,
                description=task_to_create.description,
                priority=task_to_create.priority.value if hasattr(task_to_create.priority, 'value') else str(task_to_create.priority),
                due_date=task_to_create.due_date,
                created_by=User(
                    id=task_to_create.created_by.id,
                    username=task_to_create.created_by.username,
                    email=task_to_create.created_by.email,
                    role=task_to_create.created_by.role.name if hasattr(task_to_create.created_by.role, 'name') else str(task_to_create.created_by.role)
                ),
                assigned_to=User(
                    id=task_to_create.assigned_to.id,
                    username=task_to_create.assigned_to.username,
                    email=task_to_create.assigned_to.email,
                    role=task_to_create.assigned_to.role.name if hasattr(task_to_create.assigned_to.role, 'name') else str(task_to_create.assigned_to.role)
                ) if task_to_create.assigned_to else None,
                created_at=task_to_create.created_at,
                updated_at=task_to_create.updated_at
            )
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryException(f"Error creating task: {e}") from e
