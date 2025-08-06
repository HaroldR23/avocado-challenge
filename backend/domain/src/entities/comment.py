from dataclasses import dataclass
from typing import Optional


@dataclass
class Comment:
    content: str
    task_id: int
    id: Optional[int] = None

