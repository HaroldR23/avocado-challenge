from fastapi import APIRouter, Depends, Query

from use_cases.src.task.delete.use_case import DeleteTaskUseCase
from controllers.src.dtos.task_dtos import (
	CreateTaskDTO, 
	CreateTaskResponseDTO, 
	CreatedByDTO, 
	AssignedToDTO,
	DeleteTaskResponseDTO, 
	GetTasksInputDTO,
	GetTasksResponseDTO, 
	GetTaskResponseDTO,
	AddCommentsInputDTO,
	AddCommentsResponseDTO
)
from use_cases.src.task.create.use_case import CreateTaskUseCase, CreateTaskInput
from use_cases.src.task.get_with_filters.use_case import GetTasksUseCase, GetTasksInput
from use_cases.src.task.add_comments.use_case import AddCommentsToTaskUseCase, AddCommentsInput
from controllers.src.dependencies.tasks_dependencies import (
	get_create_task_use_case, 
	get_get_tasks_use_case, 
	get_delete_task_use_case,
	get_add_comment_to_task_use_case
)

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

@tasks_router.get("/tasks", tags=["Tasks"])
def get_tasks(
		input_data: GetTasksInputDTO = Depends(),
		get_tasks_use_case: GetTasksUseCase = Depends(get_get_tasks_use_case)
	):

		get_tasks_input = GetTasksInput(
			completed=input_data.status,
			priority=input_data.priority,
			assigned_to_id=input_data.assigned_to_id,
			created_by_id=input_data.created_by_id,
			due_date_before=input_data.due_date_before,
			due_date_after=input_data.due_date_after,
			page=input_data.page,
			limit=input_data.limit,
			order=input_data.order
		)

		tasks = get_tasks_use_case(get_tasks_input)

		return GetTasksResponseDTO(
			tasks=[GetTaskResponseDTO(
				assigned_to=AssignedToDTO(
					id=task.assigned_to.id, 
					username=task.assigned_to.username
				) if task.assigned_to else None,
				comments=task.comments,
				created_at=task.created_at,
				created_by=CreatedByDTO(
					id=task.created_by.id,
					username=task.created_by.username
				),
				completed=task.completed,
				description=task.description,
				due_date=task.due_date,
				id=task.id,
				priority=task.priority,
				title=task.title,
				updated_at=task.updated_at
			) for task in tasks.tasks],
			total=tasks.total,
			page=tasks.page,
			limit=tasks.limit
		)

@tasks_router.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(
	task_id: int, 
	delete_task_use_case: DeleteTaskUseCase = Depends(get_delete_task_use_case)
):
    delete_task_use_case(task_id=task_id)
    return DeleteTaskResponseDTO()

@tasks_router.post("/tasks/{task_id}/comments", tags=["Tasks"])
def add_comment_to_task(
		task_id: int, 
		add_comments_input: AddCommentsInputDTO, 
		add_comment_to_task_use_case: AddCommentsToTaskUseCase = Depends(get_add_comment_to_task_use_case)
	):
		comment_input = AddCommentsInput(
			task_id=task_id,
			content=add_comments_input.content
		)
		add_comment_to_task_use_case(comment_input=comment_input)
		return AddCommentsResponseDTO()
