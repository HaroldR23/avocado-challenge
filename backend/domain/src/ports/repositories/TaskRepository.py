from abc import ABC, abstractmethod
from typing import Optional

from domain.src.entities.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> Task:
        ...
    
    @abstractmethod
    def find_all_with_filters(
        self,
        completed: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to_id: Optional[int] = None,
        created_by_id: Optional[int] = None,
        due_date_before: Optional[str] = None,
        due_date_after: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
        order: str = "desc"
    ) -> tuple[list[Task], int]:
        ...

    def delete(self, task_id: int) -> Optional[Task]:
        ...
