from domain.src.ports.repositories.UserRepository import UserRepository
from domain.src.entities.user import User
from infrastructure.src.adapters.sql_alchemy.models import User as UserModel
from domain.src.ports.repositories import RepositoryException

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class SQLAlchemyUserRepository(UserRepository):
	def __init__(self, session: Session):
		self.session = session

	def find_by_id(self, user_id: int):
		try:
			user = self.session.query(UserModel).filter(UserModel.id == user_id).one_or_none()
			if not user:
				return None

			return User(
				id=user.id,
				username=user.username,
				email=user.email,
				role=user.role.name
			)
		except SQLAlchemyError as e:
			self.session.rollback()
			raise RepositoryException(f"Error finding user by ID {user_id}: {e}") from e
