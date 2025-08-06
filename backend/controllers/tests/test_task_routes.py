from fastapi import status
from domain.src.entities.user import User
from use_cases.src.task.create import CreateTaskOutput
from use_cases.src.task.get_with_filters import GetTasksOutput, TaskOutput
from use_cases.src.exceptions.user_exceptions import UserNotFoundError
from use_cases.src.exceptions.task_exceptions import EmptyTaskTitleError, TaskNotFoundError
from domain.src.ports.repositories.exceptions import RepositoryException


def test_create_task_post_raises_404_on_not_found_user(client, mock_task_use_case):

    mock_task_use_case.side_effect = UserNotFoundError(user_id=1)

    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "created_by_id": 1
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "User with ID 1 not found.",
        "user_id": 1
    }


def test_create_task_post_raises_422_on_empty_title(client, mock_task_use_case):

	mock_task_use_case.side_effect = EmptyTaskTitleError()

	response = client.post(
		"/tasks",
		json={
			"title": " ",
			"description": "This is a test task",
			"created_by_id": 1
		}
	)

	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert response.json() == {
		"detail": "Task title cannot be empty."
	}
      

def test_create_task_post_raises_500_on_repository_exception(client, mock_task_use_case):

	mock_task_use_case.side_effect = RepositoryException()

	response = client.post(
		"/tasks",
		json={
			"title": "Test Task",
			"description": "This is a test task",
			"created_by_id": 1
		}
	)

	assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
	assert response.json() == {
		"detail": "An error occurred in the repository."
	}


def test_create_task_post_returns_201_on_success(client, mock_task_use_case):

	mock_task_use_case.return_value = CreateTaskOutput(
		id=1,
		title="Test Task",
		description="This is a test task",
		created_by=User(email="testuser", id=1, username="testuser", role="user"),
		completed=False,
		priority="baja",
		created_at="2023-10-01T00:00:00Z",
		due_date=None,
		assigned_to=None,
		comments=[]
	)
		

	response = client.post(
		"/tasks",
		json={
			"title": "Test Task",
			"description": "This is a test task",
			"created_by_id": 1
		}
	)

	assert response.status_code == status.HTTP_200_OK
	assert response.json() == {
		"id": 1,
		"title": "Test Task",
		"description": "This is a test task",
		"created_by": {"id": 1, "username": "testuser"},
		"created_at": "2023-10-01T00:00:00Z",
		"completed": False,
		"priority": "baja",
		"due_date": None,
		"assigned_to": None,
		"comments": []
	}


def test_get_tasks_get_returns_200_on_success(client, mock_get_tasks_use_case):
	
	mock_get_tasks_use_case.return_value = GetTasksOutput(
		tasks=[
			TaskOutput(
				id=1,
				title="Test Task 1",
				description="This is a test task 1",
				created_by=User(email="testuser1", id=1, username="testuser1", role="user"),
				completed=False,
				priority="baja",
				created_at="2023-10-01T00:00:00Z",
				updated_at="2023-10-01T00:00:00Z",
				due_date=None,
				assigned_to=None,
				comments=[]
			),
			TaskOutput(
				id=2,
				title="Test Task 2",
				description="This is a test task 2",
				created_by=User(email="testuser2", id=2, username="testuser2", role="user"),
				completed=True,
				priority="alta",
				created_at="2023-10-02T00:00:00Z",
				updated_at="2023-10-01T00:00:00Z",
				due_date=None,
				assigned_to=None,
				comments=[]
			)
		],
		total=2,
		page=1,
		limit=10
	)

	response = client.get("/tasks")

	assert response.status_code == status.HTTP_200_OK
	assert response.json() == {
		"tasks": [
			{
				"id": 1,
				"title": "Test Task 1",
				"description": "This is a test task 1",
				"created_by": {"id": 1, "username": "testuser1"},
				"created_at": "2023-10-01T00:00:00Z",
				"updated_at": "2023-10-01T00:00:00Z",
				"completed": False,
				"priority": "baja",
				"due_date": None,
				"assigned_to": None,
				"comments": []
			},
			{
				"id": 2,
				"title": "Test Task 2",
				"description": "This is a test task 2",
				"created_by": {"id": 2, "username": "testuser2"},
				"created_at": "2023-10-02T00:00:00Z",
				"updated_at": "2023-10-01T00:00:00Z",
				"completed": True,
				"priority": "alta",
				"due_date": None,
				"assigned_to": None,
				"comments": []
			}
		],
		"total": 2,
		"page": 1,
		"limit": 10
	}

def test_get_tasks_get_returns_500_on_repository_exception(client, mock_get_tasks_use_case):
	
	mock_get_tasks_use_case.side_effect = RepositoryException()

	response = client.get("/tasks")

	assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
	assert response.json() == {
		"detail": "An error occurred in the repository."
	}


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
