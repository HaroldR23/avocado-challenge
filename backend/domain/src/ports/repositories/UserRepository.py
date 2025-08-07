from abc import ABC, abstractmethod
from domain.src.entities.user import User
from typing import Optional

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        ...
