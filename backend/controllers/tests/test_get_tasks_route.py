from fastapi import status

from domain.src.entities.user import User
from use_cases.src.task.get_with_filters import GetTasksOutput, TaskOutput
from domain.src.ports.repositories.exceptions import RepositoryException

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
