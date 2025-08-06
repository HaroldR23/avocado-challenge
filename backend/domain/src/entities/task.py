from domain.src.entities.comment import Comment
from domain.src.entities.user import User

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    title: str
    description: str
    created_by: User
    updated_at: str
    created_at: str
    comments: list[Comment] = field(default_factory=list)
    completed: bool = False
    id: Optional[int] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    assigned_to: Optional[User] = None
