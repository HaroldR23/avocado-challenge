from fastapi import status

from use_cases.src.exceptions.task_exceptions import TaskNotFoundError
from domain.src.ports.repositories.exceptions import RepositoryException


def test_delete_task_returns_200_on_success(client, mock_delete_task_use_case):

	mock_delete_task_use_case.return_value = None

	response = client.delete("/tasks/1")

	assert response.status_code == status.HTTP_200_OK
	assert response.json() == {
		"message": "Task deleted successfully"
	}

def test_delete_task_returns_404_on_not_found(client, mock_delete_task_use_case):
	task_id = 999
	mock_delete_task_use_case.side_effect = TaskNotFoundError(task_id=task_id)

	response = client.delete(f"/tasks/{task_id}")

	assert response.status_code == status.HTTP_404_NOT_FOUND
	assert response.json() == {
		"detail": f"Task with ID {task_id} not found.",
		"task_id": task_id
	}

def test_delete_task_returns_500_on_repository_exception(client, mock_delete_task_use_case):

	mock_delete_task_use_case.side_effect = RepositoryException()

	response = client.delete("/tasks/1")

	assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
	assert response.json() == {
		"detail": "An error occurred in the repository."
	}
