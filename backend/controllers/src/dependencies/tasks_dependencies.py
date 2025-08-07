from fastapi import Depends
from sqlalchemy.orm import Session

from use_cases.src.task.update.use_case import UpdateTaskUseCase
from use_cases.src.task.delete.use_case import DeleteTaskUseCase
from use_cases.src.task.create.use_case import CreateTaskUseCase
from use_cases.src.task.get_with_filters.use_case import GetTasksUseCase
from use_cases.src.task.add_comments.use_case import AddCommentsToTaskUseCase
from use_cases.src.task.get_task_stats.use_case import GetTaskStatsUseCase

from infrastructure.src.adapters.sql_alchemy.session import get_db
from infrastructure.src.adapters.sql_alchemy import (
    SQLAlchemyTaskRepository, 
    SQLAlchemyUserRepository, 
	SQLAlchemyCommentRepository
)


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

def get_add_comment_to_task_use_case(db: Session = Depends(get_db)) -> AddCommentsToTaskUseCase:
	return AddCommentsToTaskUseCase(
			task_repository=SQLAlchemyTaskRepository(session=db),
			comment_repository=SQLAlchemyCommentRepository(session=db)
	)

def get_get_task_stats_use_case(db: Session = Depends(get_db)) -> GetTaskStatsUseCase:
	return GetTaskStatsUseCase(
		task_repository=SQLAlchemyTaskRepository(session=db)
	)

def get_update_task_use_case(db: Session = Depends(get_db)) -> UpdateTaskUseCase:
	return UpdateTaskUseCase(
		task_repository=SQLAlchemyTaskRepository(session=db),
		user_repository=SQLAlchemyUserRepository(session=db)
	)
