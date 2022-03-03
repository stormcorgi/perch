"""generate fixtures"""

import sys
import os
import pytest
import tempfile
from perch import create_app

sys.path.append(os.path.abspath(os.path.dirname(
    os.path.abspath(__file__)) + "/../app/"))

SAMPLE_LIB = "./tests/sample.library"
SAMPLE_DB_PATH = 'sqlite:///tests/test.db'


@pytest.fixture(name="app")
def fixture_app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    # with app.app_context():
    #     init_db()
    #     get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()
