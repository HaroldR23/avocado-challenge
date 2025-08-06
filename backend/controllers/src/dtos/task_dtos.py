from typing import Optional
from pydantic import BaseModel

class CreateTaskDTO(BaseModel):
    title: str
    description: str
    created_by_id: int
    priority: Optional[str] = None
    due_date: Optional[str] = None
    assigned_to_id: Optional[int] = None

class CreatedByDTO(BaseModel):
    id: int
    username: str

class AssignedToDTO(CreatedByDTO):
    ...

class CreateTaskResponseDTO(BaseModel):
    id: int
    title: str
    description: str
    created_by: CreatedByDTO
    completed: bool
    priority: Optional[str] = None
    created_at: str
    due_date: Optional[str] = None
    assigned_to: Optional[AssignedToDTO] = None
    comments: list = []
