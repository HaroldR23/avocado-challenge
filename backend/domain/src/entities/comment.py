from dataclasses import dataclass
from typing import Optional


@dataclass
class Comment:
    id: int
    content: str
    task_id: int
