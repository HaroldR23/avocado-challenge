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
    title: str
    description: str
    created_by: CreatedByDTO
    completed: bool
    id: Optional[int] = None
    priority: Optional[str] = None
    created_at: str
    due_date: Optional[str] = None
    assigned_to: Optional[AssignedToDTO] = None
    comments: list = []


class GetTaskResponseDTO(BaseModel):
    id: Optional[int]
    title: str
    description: str
    created_by: CreatedByDTO
    completed: bool
    priority: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None
    due_date: Optional[str] = None
    assigned_to: Optional[AssignedToDTO] = None
    comments: list = []

class GetTasksResponseDTO(BaseModel):
    tasks: list[GetTaskResponseDTO]
    total: int
    page: int
    limit: int

class GetTasksInputDTO(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to_id: Optional[int] = None
    created_by_id: Optional[int] = None
    due_date_before: Optional[str] = None
    due_date_after: Optional[str] = None
    page: int = 1
    limit: int = 10
    order: str = "desc"


class DeleteTaskResponseDTO(BaseModel):
    message: str = "Task deleted successfully"

class AddCommentsInputDTO(BaseModel):
    content: str

class AddCommentsResponseDTO(BaseModel):
    message: str = "Comment added successfully"

class GetTaskStatsResponseDTO(BaseModel):
    total_tasks: int
    completed_tasks: int
    completion_rate: float
