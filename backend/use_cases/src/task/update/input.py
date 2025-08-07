from dataclasses import dataclass
from typing import Optional


@dataclass
class UpdateTaskInput:
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    assigned_to_id: Optional[int] = None
