import os
import pytest
from myapp.app import create_app
from myapp.config import TestingConfig


@pytest.fixture(scope="session")
def app():
    """Create a Flask test app for the whole session."""
    os.environ.setdefault("OPENWEATHER_API_KEY", "test-key")
    app = create_app(TestingConfig)
    return app


@pytest.fixture
def client(app):
    """Provide a Flask test client for requests."""
    return app.test_client()
