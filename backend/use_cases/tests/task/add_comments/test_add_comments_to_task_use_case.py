import pytest

from domain.src.entities import Comment
from use_cases.src.exceptions import TaskNotFoundError, EmptyCommentError
from domain.src.ports.repositories.exceptions import RepositoryException

def test_add_comment_to_task_raises_repository_exception_when_repository_fails(
    mock_task_repository,
    mock_comment_repository,
    mock_task,
    mock_comment,
    add_comments_use_case
):
    
    mock_task_repository.get_by_id.return_value = mock_task
    mock_comment_repository.create.side_effect = RepositoryException("Repository error")

    with pytest.raises(RepositoryException, match="Repository error"):
        add_comments_use_case(comment_input=mock_comment)
    mock_comment_repository.create.assert_called_once()
    mock_task_repository.get_by_id.assert_called_once_with(task_id=mock_comment.task_id)


def test_add_comment_to_task_raises_task_not_found_error_when_task_does_not_exist(
    mock_task_repository,
    add_comments_use_case,
    mock_comment
):
    
    mock_task_repository.get_by_id.return_value = None

    with pytest.raises(TaskNotFoundError, match="Task with ID 1 not found."):
        add_comments_use_case(comment_input=mock_comment)

    mock_task_repository.get_by_id.assert_called_once_with(task_id=mock_comment.task_id)

def test_add_comment_to_task_raises_empty_comment_error_when_content_is_empty(
    mock_task_repository,
    add_comments_use_case,
    mock_task
):
    
    mock_task_repository.get_by_id.return_value = mock_task
    mock_comment = Comment(content="    ", task_id=1)

    with pytest.raises(EmptyCommentError, match="Comment content cannot be empty."):
        add_comments_use_case(comment_input=mock_comment)

    mock_task_repository.get_by_id.assert_called_once_with(task_id=mock_comment.task_id)


def test_add_comment_to_task_success(
    mock_task_repository,
    add_comments_use_case,
    mock_comment_repository,
    mock_task,
    mock_comment
):
    
    mock_task_repository.get_by_id.return_value = mock_task
    mock_comment_repository.create.return_value = mock_comment
 
    add_comments_use_case(comment_input=mock_comment)

    mock_task_repository.get_by_id.assert_called_once_with(task_id=mock_comment.task_id)
    mock_comment_repository.create.assert_called_once_with(comment=mock_comment)
