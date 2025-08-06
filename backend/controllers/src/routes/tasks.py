from fastapi import APIRouter, Depends

from controllers.src.dtos.task_dtos import CreateTaskDTO, CreateTaskResponseDTO, CreatedByDTO, AssignedToDTO
from use_cases.src.task.create.use_case import CreateTaskUseCase
from use_cases.src.task.create.input import CreateTaskInput
from controllers.src.dependencies.tasks_dependencies import get_create_task_use_case

tasks_router = APIRouter()

@tasks_router.post("/tasks", tags=["Tasks"])
def create_task(
		task: CreateTaskDTO, 
		create_task_use_case: CreateTaskUseCase = Depends(get_create_task_use_case)
	):
		create_task_input = CreateTaskInput(
			**task.model_dump()
		)
		created_task = create_task_use_case(task_input=create_task_input)

		return CreateTaskResponseDTO(
				id=created_task.id,
				assigned_to=AssignedToDTO(
					id=created_task.assigned_to.id, 
					username=created_task.assigned_to.username
				) if created_task.assigned_to else None,
				comments=created_task.comments,
				created_at=created_task.created_at,
				completed=created_task.completed,
				description=created_task.description,
				due_date=created_task.due_date,
				priority=created_task.priority,
				title=created_task.title,
				created_by=CreatedByDTO(
					id=created_task.created_by.id,
					username=created_task.created_by.username
				)
		)
