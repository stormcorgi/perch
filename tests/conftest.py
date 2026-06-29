"""generate fixtures"""
import os
import pytest
from perch.flask_app import create_app
from perch.db.connection import init_db, generate_session
from perch.db.update import update_actress, update_newfiles, update_tags, update_count


@pytest.fixture(name="app")
def fixture_app():
    """Create and configure a new app instance for each test.
    Must set FLASK_APP_ENV before create_app() so the app's
    internal current_session and all routes use the test DB."""
    os.environ["FLASK_APP_ENV"] = "testing"
    app = create_app()

    # Seed the test database via a dedicated session on the same DB file.
    # The app's routes use their own current_session (closure variable);
    # both point to the same SQLite file, so seeded data is visible.
    with app.app_context():
        db_path = app.config["DATABASE"]
        sess = generate_session(db_path)()
        update_actress(sess)
        update_newfiles(sess)
        update_tags(sess)
        update_count(sess)

    yield app


@pytest.fixture
def client(app):
    """Create and return app.test_client()"""
    return app.test_client()
