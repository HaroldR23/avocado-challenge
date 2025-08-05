import pytest
from unittest.mock import MagicMock

from domain.src.ports.repositories import TaskRepository, UserRepository, RepositoryException
from domain.src.entities import Task, User
from use_cases.src.exceptions import UserNotFoundError, EmptyTaskTitleError
from use_cases.src.task.create import CreateTaskInput, CreateTaskUseCase, CreateTaskOutput

@pytest.fixture
def mock_task_repository() -> TaskRepository:
    return MagicMock(spec=TaskRepository)

@pytest.fixture
def mock_user_repository() -> UserRepository:
    return MagicMock(spec=UserRepository)

@pytest.fixture
def create_task_input() -> CreateTaskInput:
    return CreateTaskInput(
        title="Test Task",
        description="This is a test task",
        created_by_id=1,
        priority="MEDIUM"
    )

@pytest.fixture
def task_creator_user() -> User:
	return User(
		email="creator@example.com",
		id=1,
		username="Creator Name",
		password_hash="hashed_password",
		role="USER"
	)