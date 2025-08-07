import pytest
from fastapi import status
from use_cases.src.task.update.input import UpdateTaskInput
from domain.src.ports.repositories.exceptions import RepositoryException
from use_cases.src.exceptions import UserNotFoundError, TaskNotFoundError, EmptyTaskTitleError

def test_update_task_use_case_raises_404_on_not_found_task(client, mock_update_task_use_case):
    # Arrange
    task_id = 999
    mock_update_task_use_case.side_effect = TaskNotFoundError(task_id=task_id)

    # Act & Assert
    response = client.patch(f"/tasks/{task_id}", json={})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": f"Task with ID {task_id} not found.",
        "task_id": task_id
    }

def test_update_task_use_case_raises_400_on_empty_title(client, mock_update_task_use_case):
    # Arrange
    task_id = 1
    mock_update_task_use_case.side_effect = EmptyTaskTitleError()

    # Act & Assert
    response = client.patch(f"/tasks/{task_id}", json={"title": " "})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Task title cannot be empty."
    }

def test_update_task_use_case_raises_404_on_not_found_user(client, mock_update_task_use_case):
    # Arrange
    task_id = 1
    assigned_user_id = 999
    mock_update_task_use_case.side_effect = UserNotFoundError(user_id=assigned_user_id)

    # Act & Assert
    response = client.patch(f"/tasks/{task_id}", json={"assigned_to_id": assigned_user_id})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": f"User with ID {assigned_user_id} not found.",
        "user_id": assigned_user_id
    }

def test_update_task_success(client, mock_update_task_use_case):
    # Arrange
    task_id = 1
    mock_update_task_use_case.return_value = None

    # Act
    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Updated Task Title",
            "assigned_to_id": 2
        }
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Task updated successfully"
    }

