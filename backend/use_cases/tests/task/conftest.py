import pytest
from unittest.mock import MagicMock

from domain.src.ports.repositories import TaskRepository, UserRepository, CommentRepository
from domain.src.entities import User, Task, Comment
from use_cases.src.task.add_comments.use_case import AddCommentsToTask
from use_cases.src.task.create import CreateTaskInput
from use_cases.src.task.get_with_filters import GetTasksInput

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

@pytest.fixture
def get_tasks_input():
    return GetTasksInput(
        completed=None,
        priority=None,
        assigned_to_id=None,
        created_by_id=None,
        due_date_before=None,
        due_date_after=None,
        page=1,
        limit=10,
        order="asc"
    )

@pytest.fixture
def mock_task():
     return Task(
        id=1,
        title="Test Task",
        description="This is a test task",
        priority="MEDIUM",
        due_date=None,
        created_by=User(id=1, username="creator", email="creator@example.com"),
        created_at="2023-10-01T00:00:00Z",
        updated_at="2023-10-01T00:00:00Z",
        assigned_to=None,
        comments=[]
    )

@pytest.fixture
def mock_comment_repository():
    return MagicMock(spec=CommentRepository)


@pytest.fixture
def add_comments_use_case(mock_task_repository, mock_comment_repository):
    return AddCommentsToTask(
            task_repository=mock_task_repository, 
            comment_repository=mock_comment_repository
        )

@pytest.fixture
def mock_comment():
    return Comment(
        content="This is a comment",
        task_id=1,
    )
