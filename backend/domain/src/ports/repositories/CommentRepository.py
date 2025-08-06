from abc import ABC, abstractmethod

from domain.src.entities.comment import Comment


class CommentRepository(ABC):
    @abstractmethod
    def create(self, comment: Comment) -> Comment:
        ...
