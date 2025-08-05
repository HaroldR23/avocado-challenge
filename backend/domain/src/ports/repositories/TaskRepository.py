from abc import ABC, abstractmethod
from domain.src.entities.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> Task:
        ...
    