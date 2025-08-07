from domain.src.ports.repositories import TaskRepository, RepositoryException
from domain.src.entities import Task, User
from infrastructure.src.adapters.sql_alchemy.models import Task as TaskModel

from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError
from typing import Tuple, Optional

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


    def find_all_with_filters(
        self, completed, priority, assigned_to, created_by,
        due_date_before, due_date_after, page, limit, order, sort_by="created_at"
    ) -> Tuple[list[Task], int]:
        try:
            query = self.session.query(TaskModel)

            if completed:
                query = query.filter(TaskModel.completed == (completed.lower() == 'completed'))
            if priority:
                query = query.filter(TaskModel.priority == priority)
            if assigned_to:
                query = query.filter(TaskModel.assigned_to_id == assigned_to)
            if created_by:
                query = query.filter(TaskModel.created_by_id == created_by)
            if due_date_before:
                query = query.filter(TaskModel.due_date <= due_date_before)
            if due_date_after:
                query = query.filter(TaskModel.due_date >= due_date_after)

            total = query.count()

            if order == "asc":
                query = query.order_by(asc(getattr(TaskModel, sort_by)))
            elif order == "desc":
                query = query.order_by(desc(getattr(TaskModel, sort_by)))

            query = query.offset((page - 1) * limit).limit(limit)

            tasks = [
                Task(
                    id=t.id,
                    title=t.title,
                    description=t.description,
                    priority=t.priority.value if hasattr(t.priority, 'value') else str(t.priority),
                    due_date=t.due_date,
                    completed=t.completed,
                    created_by=User(id=t.created_by.id, username=t.created_by.username, email=t.created_by.email),
                    assigned_to=User(id=t.assigned_to.id, username=t.assigned_to.username, email=t.assigned_to.email) if t.assigned_to else None,
                    created_at=t.created_at,
                    updated_at=t.updated_at
                )
                for t in query.all()
            ]

            return tasks, total
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryException(f"Error getting tasks: {e}") from e

    def delete(self, task_id: int) -> Optional[Task]:
        try:
            task = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
            if not task:
                return None
            
            self.session.delete(task)
            self.session.commit()
            
            return Task(
                id=task.id,
                title=task.title,
                description=task.description,
                priority=task.priority.value if hasattr(task.priority, 'value') else str(task.priority),
                due_date=task.due_date,
                completed=task.completed,
                created_by=User(id=task.created_by.id, username=task.created_by.username, email=task.created_by.email),
                assigned_to=User(id=task.assigned_to.id, username=task.assigned_to.username, email=task.assigned_to.email) if task.assigned_to else None,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryException(f"Error deleting task: {e}") from e

    def get_by_id(self, task_id: int) -> Optional[Task]:
        try:
            task = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()

            if not task:
                return None
            
            return Task(
                id=task.id,
                title=task.title,
                description=task.description,
                priority=task.priority.value if hasattr(task.priority, 'value') else str(task.priority),
                due_date=task.due_date,
                completed=task.completed,
                created_by=User(id=task.created_by.id, username=task.created_by.username, email=task.created_by.email),
                assigned_to=User(id=task.assigned_to.id, username=task.assigned_to.username, email=task.assigned_to.email) if task.assigned_to else None,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryException(f"Error getting task by ID: {e}") from e
