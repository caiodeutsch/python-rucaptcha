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

"""
Page response tests
"""
def test_index_page(client):

    response = client.get('/')
    
    assert response.status_code in (200, 301)

    response = client.get('index')
    
    assert response.status_code in (200, 301)

def test_invisible_captcha_page(client):

    response = client.get('invisible-recaptcha')
    
    assert response.status_code in (200, 301)

"""
API tests
"""

def test_image_captcha_api(client):

    response = client.get('api/?captcha_type=get_common_captcha')
    
    assert response.status_code in (200, 301)

    assert response.json.get('captcha_src')
