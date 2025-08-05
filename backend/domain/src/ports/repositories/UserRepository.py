from abc import ABC, abstractmethod
from domain.src.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        ...
