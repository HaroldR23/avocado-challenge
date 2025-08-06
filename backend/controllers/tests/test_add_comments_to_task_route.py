from fastapi import status

from use_cases.src.exceptions.task_exceptions import TaskNotFoundError
from use_cases.src.exceptions.comment_exceptions import EmptyCommentError
from domain.src.ports.repositories.exceptions import RepositoryException

def test_add_comments_to_task_returns_200_on_success(client, mock_add_comments_use_case):
    mock_add_comments_use_case.return_value = None

    response = client.post(
        "/tasks/1/comments",
        json={
            "content": "This is a test comment",
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Comment added successfully"
    }
    
def test_add_comments_to_task_raises_404_on_not_found_task(client, mock_add_comments_use_case):
	mock_add_comments_use_case.side_effect = TaskNotFoundError(task_id=1)

	response = client.post(
		"/tasks/1/comments",
		json={
			"content": "This is a test comment",
		}
	)

	assert response.status_code == status.HTTP_404_NOT_FOUND
	assert response.json() == {
		"detail": "Task with ID 1 not found.",
		"task_id": 1
	}
      
def test_add_comments_to_task_raises_500_on_repository_exception(client, mock_add_comments_use_case):
	mock_add_comments_use_case.side_effect = RepositoryException()

	response = client.post(
		"/tasks/1/comments",
		json={
			"content": "This is a test comment",
		}
	)

	assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
	assert response.json() == {
		"detail": "An error occurred in the repository."
	}

def test_add_comments_to_task_raises_400_on_empty_content(client, mock_add_comments_use_case):
	mock_add_comments_use_case.side_effect = EmptyCommentError()

	response = client.post(
		"/tasks/1/comments",
		json={
			"content": " "
		}
	)

	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert response.json() == {
		"detail": "Comment content cannot be empty."
	}
