from dataclasses import dataclass

@dataclass
class GetTaskStatsOutput:
    total_tasks: int
    completed_tasks: int
    completion_rate: float
