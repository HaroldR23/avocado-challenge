import pytest

from domain.src.entities import User, Task
from use_cases.src.task.get_with_filters import GetTasksInput, GetTasksOutput
from use_cases.src.task.get_with_filters.use_case import GetTasksUseCase
from domain.src.ports.repositories.exceptions import RepositoryException


def test_get_tasks_with_filters_raises_repository_exception(mock_task_repository, get_tasks_input):
    # Arrange
    mock_task_repository.find_all_with_filters.side_effect = RepositoryException("Repository error")
    get_tasks_use_case = GetTasksUseCase(task_repository=mock_task_repository)

    # Act & Assert
    with pytest.raises(RepositoryException, match="Repository error"):
        get_tasks_use_case(filters=get_tasks_input)

    mock_task_repository.find_all_with_filters.assert_called_once_with(**get_tasks_input.__dict__)
    

def test_get_tasks_with_filters_returns_empty_output_when_no_tasks(mock_task_repository, get_tasks_input):
	# Arrange
	mock_task_repository.find_all_with_filters.return_value = ([], 0)
	get_tasks_use_case = GetTasksUseCase(task_repository=mock_task_repository)

	# Act
	result = get_tasks_use_case(filters=get_tasks_input)

	# Assert
	assert isinstance(result, GetTasksOutput)
	assert result.tasks == []
	assert result.total == 0
	assert result.page == 1
	assert result.limit == 10

	mock_task_repository.find_all_with_filters.assert_called_once_with(**get_tasks_input.__dict__)


def test_get_tasks_with_filters_returns_tasks(mock_task_repository):
	  
	# Arrange
	task_input = GetTasksInput(
		completed="completed",
		priority=None,
		assigned_to_id=None,
		created_by_id=None,
		due_date_before=None,
		due_date_after=None,
		page=1,
		limit=10,
		order="asc"
	)
	mock_task_returned_by_repository = Task(
		id=1,
		title="Test Task",
		description="This is a test task",
		priority="MEDIUM",
		due_date=None,
		completed=True,
		created_by=User(
			id=1,
			username="testuser",
			email="testuser@example.com"
		),
		assigned_to=None,
		created_at="2023-10-01T00:00:00Z",
		updated_at="2023-10-01T00:00:00Z"
	)
      
	mock_task_repository.find_all_with_filters.return_value = ([mock_task_returned_by_repository], 1)
	get_tasks_use_case = GetTasksUseCase(task_repository=mock_task_repository)

	# Act
	result = get_tasks_use_case(filters=task_input)

	# Assert
	assert isinstance(result, GetTasksOutput)
	assert len(result.tasks) == 1
	assert result.tasks[0].completed == mock_task_returned_by_repository.completed
	assert result.total == 1
	assert result.page == 1
	assert result.limit == 10

	mock_task_repository.find_all_with_filters.assert_called_once_with(**task_input.__dict__)
