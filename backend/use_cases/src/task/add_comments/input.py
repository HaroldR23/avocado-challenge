from dataclasses import dataclass

@dataclass
class AddCommentsInput:
    task_id: int
    content: str
