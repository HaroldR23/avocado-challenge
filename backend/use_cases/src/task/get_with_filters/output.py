from dataclasses import dataclass, field
from typing import Optional, List

from domain.src.entities.user import User

@dataclass
class TaskOutput:
    title: str
    description: str
    created_by: User
    updated_at: str
    created_at: str
    id: Optional[int] = None
    comments: List[str] = field(default_factory=list)
    completed: bool = False
    priority: Optional[str] = None
    due_date: Optional[str] = None
    assigned_to: Optional[User] = None


@dataclass
class GetTasksOutput:
    tasks: List[TaskOutput] = field(default_factory=list)
    total: int = 0
    page: int = 1
    limit: int = 10
