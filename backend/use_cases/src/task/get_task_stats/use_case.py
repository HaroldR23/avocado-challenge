from domain.src.ports.repositories.exceptions import RepositoryException
from use_cases.src.task.get_task_stats.output import GetTaskStatsOutput
from use_cases.src.task.get_with_filters import GetTasksInput
from domain.src.ports.repositories import TaskRepository

class GetTaskStatsUseCase:
	def __init__(self, task_repository: TaskRepository):
		self.task_repository = task_repository

	def __call__(self) -> GetTaskStatsOutput:
		try:
			get_input_total_tasks = GetTasksInput(limit=100)
			get_input_completed_tasks = GetTasksInput(completed="completed", limit=100)
			total_tasks = self.task_repository.find_all_with_filters(**get_input_total_tasks.__dict__)[1]
			completed_tasks = self.task_repository.find_all_with_filters(**get_input_completed_tasks.__dict__)[1]
			completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

			return GetTaskStatsOutput(
				total_tasks=total_tasks,
				completed_tasks=completed_tasks,
				completion_rate=completion_rate
			)
		except RepositoryException as e:
			raise e
