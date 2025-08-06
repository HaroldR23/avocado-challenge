from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateTaskInput:
    title: str
    description: str
    created_by_id: int
    priority: Optional[str] = None
    due_date: Optional[str] = None
    assigned_to_id: Optional[int] = None
