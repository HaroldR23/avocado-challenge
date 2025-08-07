import pytest
from unittest.mock import patch

from domain.src.ports.repositories import RepositoryException
from use_cases.src.task.update import UpdateTaskInput
from use_cases.src.exceptions import UserNotFoundError, TaskNotFoundError, EmptyTaskTitleError


def test_update_task_use_case_raises_task_not_found_error_when_task_does_not_exist(
    update_task_use_case,
    mock_task_repository,
    update_task_input
):
    # Arrange
    task_id = 999
    mock_task_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(
        TaskNotFoundError,
        match=f"Task with ID {task_id} not found."
    ):
        update_task_use_case(task_id=task_id, update_task_input=update_task_input)

    mock_task_repository.get_by_id.assert_called_once_with(task_id)
    mock_task_repository.update.assert_not_called()


def test_update_task_use_case_raises_empty_task_title_error_when_title_is_empty(
    update_task_use_case,
    mock_task_repository,
    mock_task
):
    # Arrange
    task_id = 1
    update_input = UpdateTaskInput(title="   ")
    mock_task_repository.get_by_id.return_value = mock_task

    # Act & Assert
    with pytest.raises(EmptyTaskTitleError):
        update_task_use_case(task_id=task_id, update_task_input=update_input)

    mock_task_repository.get_by_id.assert_called_once_with(task_id)
    mock_task_repository.update.assert_not_called()


def test_update_task_use_case_raises_user_not_found_error_when_assigned_user_does_not_exist(
    update_task_use_case,
    mock_task_repository,
    mock_user_repository,
    mock_task
):
    # Arrange
    task_id = 1
    assigned_user_id = 999
    update_input = UpdateTaskInput(assigned_to_id=assigned_user_id)
    
    mock_task_repository.get_by_id.return_value = mock_task
    mock_user_repository.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(
        UserNotFoundError,
        match=f"User with ID {assigned_user_id} not found."
    ):
        update_task_use_case(task_id=task_id, update_task_input=update_input)

    mock_task_repository.get_by_id.assert_called_once_with(task_id)
    mock_user_repository.find_by_id.assert_called_once_with(assigned_user_id)
    mock_task_repository.update.assert_not_called()


@patch('use_cases.src.task.update.use_case.datetime')
def test_update_task_use_case_successfully_updates(
    mock_datetime,
    update_task_use_case,
    mock_task_repository,
    mock_user_repository,
    mock_task,
    update_task_input,
    assigned_user
):
    # Arrange
    task_id = 1
    fixed_datetime = "2023-10-01T12:00:00"
    mock_datetime.now.return_value.isoformat.return_value = fixed_datetime
    
    mock_task_repository.get_by_id.return_value = mock_task
    mock_user_repository.find_by_id.return_value = assigned_user

    # Act
    update_task_use_case(task_id=task_id, update_task_input=update_task_input)

    # Assert
    mock_task_repository.get_by_id.assert_called_once_with(task_id)
    mock_user_repository.find_by_id.assert_called_once_with(update_task_input.assigned_to_id)
    mock_task_repository.update.assert_called_once()


def test_update_task_use_case_propagates_repository_exception(
    update_task_use_case,
    mock_task_repository,
    mock_task,
    update_task_input
):
    # Arrange
    task_id = 1
    mock_task_repository.get_by_id.return_value = mock_task
    mock_task_repository.update.side_effect = RepositoryException("Database error")

    # Act & Assert
    with pytest.raises(RepositoryException, match="Database error"):
        update_task_use_case(task_id=task_id, update_task_input=update_task_input)

    mock_task_repository.get_by_id.assert_called_once_with(task_id)
    mock_task_repository.update.assert_called_once()
