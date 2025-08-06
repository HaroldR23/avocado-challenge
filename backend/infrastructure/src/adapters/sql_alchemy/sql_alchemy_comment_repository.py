from domain.src.ports.repositories import CommentRepository, RepositoryException
from domain.src.entities import Comment, Task, User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.src.adapters.sql_alchemy.models import Comment as CommentModel

class SQLAlchemyCommentRepository(CommentRepository):
	def __init__(self, session: Session):
		self.session = session

	def create(self, comment: Comment) -> Comment:
		try:
			comment_to_create = CommentModel(
				content=comment.content,
				task_id=comment.task_id,
			)
			self.session.add(comment_to_create)
			self.session.commit()
			self.session.refresh(comment_to_create)

			return Comment(
				id=comment_to_create.id,
				content=comment_to_create.content,
				task_id=comment_to_create.task_id,
			)
		except SQLAlchemyError as e:
			self.session.rollback()
			raise RepositoryException(f"Error creating comment: {e}") from e	
