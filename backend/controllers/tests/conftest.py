import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, create_autospec
from controllers.src.create_app import create_app
from use_cases.src.task.create import CreateTaskUseCase

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

