"""generate fixtures"""

import os
import tempfile
import pytest
from perch import create_app

SAMPLE_LIB = "./tests/sample.library"
SAMPLE_DB_PATH = 'sqlite:///tests/test.db'


@pytest.fixture(name="app")
def fixture_app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app(
        {"TESTING": True, "DATABASE": db_path, "LIB_PATH": SAMPLE_LIB})

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create and return app.test_client()"""
    return app.test_client()
