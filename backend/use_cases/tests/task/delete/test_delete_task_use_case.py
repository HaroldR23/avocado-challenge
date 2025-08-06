import pytest 

from domain.src.ports.repositories import TaskRepository, RepositoryException
from use_cases.src.exceptions.task_exceptions import TaskNotFoundError
from use_cases.src.task.delete.use_case import DeleteTaskUseCase


def test_delete_task_use_case_raises_repository_exception(mock_task_repository):
    mock_task_repository.delete.side_effect = RepositoryException()
    delete_task_use_case = DeleteTaskUseCase(task_repository=mock_task_repository)

    with pytest.raises(RepositoryException, match="An error occurred in the repository."):
        delete_task_use_case(task_id=1)
    mock_task_repository.delete.assert_called_once_with(task_id=1)

def test_delete_task_use_case_raises_task_not_found_error(mock_task_repository):
    mock_task_repository.delete.return_value = None
    delete_task_use_case = DeleteTaskUseCase(task_repository=mock_task_repository)

    with pytest.raises(TaskNotFoundError, match=f"Task with ID {1} not found."):
        delete_task_use_case(task_id=1)
    mock_task_repository.delete.assert_called_once_with(task_id=1)

def test_delete_task_use_case_success(mock_task_repository, mock_task):
	mock_task_repository.delete.return_value = mock_task
	delete_task_use_case = DeleteTaskUseCase(task_repository=mock_task_repository)

	delete_task_use_case(task_id=mock_task.id)
	mock_task_repository.delete.assert_called_once_with(task_id=mock_task.id)

	assert True
