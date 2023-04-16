"""generate fixtures"""
import pytest

from perch.db.connection import init_db
# import perch.config
from perch.flask_app import create_app

# from perch import config



@pytest.fixture(name="app")
def fixture_app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.from_object("perch.config.Testing")

    # create the database and load test data
    with app.app_context():
        init_db(app.config["DATABASE"])

    app.post("/admin", data=dict(task="update_db"), follow_redirects=True)

    yield app


@pytest.fixture
def client(app):
    """Create and return app.test_client()"""
    return app.test_client()
