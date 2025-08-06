from fastapi import Depends
from sqlalchemy.orm import Session

from use_cases.src.task.delete.use_case import DeleteTaskUseCase
from infrastructure.src.adapters.sql_alchemy.session import get_db
from use_cases.src.task.create.use_case import CreateTaskUseCase
from use_cases.src.task.get_with_filters.use_case import GetTasksUseCase

from infrastructure.src.adapters.sql_alchemy.sql_alchemy_task_repository import SQLAlchemyTaskRepository
from infrastructure.src.adapters.sql_alchemy.sql_alchemy_user_repository import SQLAlchemyUserRepository


def get_create_task_use_case(db: Session = Depends(get_db)) -> CreateTaskUseCase:
    note_service = CreateTaskUseCase(
        task_repository=SQLAlchemyTaskRepository(session=db),
        user_repository=SQLAlchemyUserRepository(session=db)
    )
    return note_service

def get_get_tasks_use_case(db: Session = Depends(get_db)) -> GetTasksUseCase:
    return GetTasksUseCase(
        task_repository=SQLAlchemyTaskRepository(session=db)
    )

def get_delete_task_use_case(db: Session = Depends(get_db)) -> DeleteTaskUseCase:
	return DeleteTaskUseCase(
			task_repository=SQLAlchemyTaskRepository(session=db)
	)
