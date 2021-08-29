# type: ignore
import os
from contextlib import contextmanager

import pytest
from flask_migrate import upgrade

from app import db, get_env, TESTING, metadata, app


@pytest.fixture(scope="session")
def connection():
    assert get_env() == TESTING
    with app.app_context():
        upgrade(directory=os.path.join(app.root_path, "migrations"))
    return db.engine.connect()


@pytest.fixture(scope="function", autouse=True)
def clean_session(connection):
    transaction = connection.begin()
    try:
        yield
    finally:
        for table in reversed(metadata.sorted_tables):
            connection.execute(table.delete())
        transaction.commit()


@contextmanager
def logged_in_client(user):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user_id"] = user.id
        yield client
