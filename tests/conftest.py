import pytest
import json

from starlette.testclient import TestClient

from app.main import create_app


@pytest.fixture
def api():
    return TestClient(create_app())


