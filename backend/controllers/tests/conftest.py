import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from use_cases.src.task.delete.use_case import DeleteTaskUseCase
from controllers.src.create_app import create_app
from use_cases.src.task.create import CreateTaskUseCase
from use_cases.src.task.get_with_filters import GetTasksUseCase

app = create_app()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_task_use_case() -> CreateTaskUseCase:
    mock = MagicMock(spec=CreateTaskUseCase)
    return mock 

@pytest.fixture(autouse=True)
def override_dependency(mock_task_use_case):
    from controllers.src.dependencies.tasks_dependencies import get_create_task_use_case
    app.dependency_overrides[get_create_task_use_case] = lambda: mock_task_use_case
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def mock_get_tasks_use_case() -> GetTasksUseCase:
    mock = MagicMock(spec=GetTasksUseCase)
    return mock

@pytest.fixture(autouse=True)
def override_get_tasks_dependency(mock_get_tasks_use_case):
    from controllers.src.dependencies.tasks_dependencies import get_get_tasks_use_case
    app.dependency_overrides[get_get_tasks_use_case] = lambda: mock_get_tasks_use_case
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def mock_delete_task_use_case():
    mock = MagicMock(spec=GetTasksUseCase)
    return mock

@pytest.fixture(autouse=True)
def override_delete_task_dependency(mock_delete_task_use_case):
    from controllers.src.dependencies.tasks_dependencies import get_delete_task_use_case
    app.dependency_overrides[get_delete_task_use_case] = lambda: mock_delete_task_use_case
    yield
    app.dependency_overrides.clear()
