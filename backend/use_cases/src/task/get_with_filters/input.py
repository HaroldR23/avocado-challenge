from dataclasses import dataclass
import datetime
from typing import Optional, Union

@dataclass
class GetTasksInput:
	completed: Optional[str] = None
	priority: Optional[str] = None
	due_date_before: Optional[str] = None
	due_date_after: Optional[str] = None
	assigned_to_id: Optional[int] = None
	created_by_id: Optional[int] = None
	page: int = 1
	limit: int = 10
	order: str = "desc"
