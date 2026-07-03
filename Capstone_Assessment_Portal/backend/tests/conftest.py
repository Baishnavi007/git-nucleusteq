"""
Pytest fixtures for creating a FastAPI test client
"""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def client():
    """
    Returns a FastAPI TestClient object
    """
    with TestClient(app) as test_client:
        yield test_client