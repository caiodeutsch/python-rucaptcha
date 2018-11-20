import os
import tempfile

import pytest

from WebRucaptcha import app
from WebRucaptcha.dbconnect import Database

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        Database().creating_tables()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    print(rv)
    assert 1==1