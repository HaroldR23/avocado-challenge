from use_cases.src.task.add_comments.input import AddCommentsInput
from domain.src.ports.repositories.exceptions import RepositoryException
from domain.src.ports.repositories import TaskRepository, CommentRepository
from use_cases.src.exceptions import TaskNotFoundError, EmptyCommentError
from domain.src.entities.comment import Comment

class AddCommentsToTask:
	def __init__(self, task_repository: TaskRepository, comment_repository: CommentRepository):
		self.task_repository = task_repository
		self.comment_repository = comment_repository

	def __call__(self, comment_input: AddCommentsInput):
		task = self.task_repository.get_by_id(task_id=comment_input.task_id)
		if not task:
			raise TaskNotFoundError(task_id=comment_input.task_id)

		if comment_input.content.strip() == "":
			raise EmptyCommentError()

		comment_to_add = Comment(content=comment_input.content, task_id=comment_input.task_id)
		try:
			self.comment_repository.create(comment=comment_to_add)
		except RepositoryException as e:
			raise e
