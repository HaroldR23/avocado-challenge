from dataclasses import dataclass, field
from typing import Optional

from domain.src.entities.user import User


@dataclass
class CreateTaskOutput:
    title: str
    description: str
    created_by: User
    completed: bool 
    priority: Optional[str]
    created_at: str
    id: Optional[int] = None
    due_date: Optional[str] = None
    assigned_to: Optional[User] = None
    comments: list = field(default_factory=list)
