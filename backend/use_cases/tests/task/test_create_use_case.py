import pytest

from domain.src.ports.repositories import RepositoryException
from domain.src.entities import Task
from use_cases.src.exceptions import UserNotFoundError, EmptyTaskTitleError
from use_cases.src.task.create import CreateTaskInput, CreateTaskUseCase, CreateTaskOutput


def test_create_task_use_case_raises_exception_when_task_creator_user_not_found(
		mock_task_repository, 
		mock_user_repository, 
		create_task_input
	):

		# Arrange
		mock_user_repository.find_by_id.return_value = None
		create_task_use_case = CreateTaskUseCase(
			task_repository=mock_task_repository,
			user_repository=mock_user_repository
		)


		# Act & Assert
		with pytest.raises(
			UserNotFoundError,
			match=f"User with ID {create_task_input.created_by_id} not found."
		):
			create_task_use_case(task_input=create_task_input)
			
		assert mock_task_repository.create.call_count == 0
		assert mock_user_repository.find_by_id.call_count == 1
		mock_user_repository.find_by_id.assert_called_with(create_task_input.created_by_id)


def test_create_task_use_case_raises_empty_task_title_error(
		mock_task_repository, 
		mock_user_repository,
		task_creator_user
	):

		# Arrange
		create_task_input = CreateTaskInput(
			title="   ",
			description="This is a test task",
			created_by_id=1,
			priority="MEDIUM"
		)
		mock_user_repository.find_by_id.return_value = task_creator_user
		create_task_use_case = CreateTaskUseCase(
			task_repository=mock_task_repository,
			user_repository=mock_user_repository
		)

		# Act & Assert
		with pytest.raises(EmptyTaskTitleError, match="Task title cannot be empty."):
			create_task_use_case(task_input=create_task_input)


def test_create_task_use_case_raises_exception_when_user_assigned_to_task_not_found(
		mock_task_repository, 
		mock_user_repository,
		create_task_input,
		task_creator_user
	):

		# Arrange
		create_task_input = CreateTaskInput(
			title="Test Task",
			description="This is a test task",
			created_by_id=1,
			assigned_to_id=2,
			priority="MEDIUM"
		)
		mock_user_repository.find_by_id.side_effect = [task_creator_user, None]
		create_task_use_case = CreateTaskUseCase(
			task_repository=mock_task_repository,
			user_repository=mock_user_repository
		)

		# Act & Assert
		with pytest.raises(
			UserNotFoundError,
			match=f"User with ID {create_task_input.assigned_to_id} not found."
		):
			create_task_use_case(task_input=create_task_input)

		assert mock_task_repository.create.call_count == 0
		assert mock_user_repository.find_by_id.call_count == 2
		mock_user_repository.find_by_id.assert_any_call(create_task_input.created_by_id)
		mock_user_repository.find_by_id.assert_any_call(create_task_input.assigned_to_id)


def test_create_task_use_case_raises_repository_exception_when_task_creation_fails(
		mock_task_repository, 
		mock_user_repository, 
		create_task_input,
		task_creator_user
	):

		# Arrange
		mock_user_repository.find_by_id.return_value = task_creator_user
		mock_task_repository.create.side_effect = RepositoryException("Failed to create task.")

		create_task_use_case = CreateTaskUseCase(
			task_repository=mock_task_repository,
			user_repository=mock_user_repository
		)

		# Act & Assert
		with pytest.raises(RepositoryException, match="Failed to create task."):
			create_task_use_case(task_input=create_task_input)


def test_create_task_use_case_success(
		mock_task_repository, 
		mock_user_repository, 
		create_task_input,
		task_creator_user
	):
		# Arrange
		mock_task_created = Task(
			title=create_task_input.title,
			description=create_task_input.description,
			priority=create_task_input.priority,
			created_by=task_creator_user,
			created_at="2023-10-01T00:00:00Z",
			updated_at="2023-10-01T00:00:00Z",
		)
		mock_user_repository.find_by_id.return_value = task_creator_user
		mock_task_repository.create.return_value = mock_task_created

		create_task_use_case = CreateTaskUseCase(
			task_repository=mock_task_repository,
			user_repository=mock_user_repository
		)

		# Act
		task_created = create_task_use_case(task_input=create_task_input)

		# Assert
		assert isinstance(task_created, CreateTaskOutput)
		assert mock_task_repository.create.call_count == 1
		assert mock_user_repository.find_by_id.call_count == 1
		mock_user_repository.find_by_id.assert_called_with(create_task_input.created_by_id)
