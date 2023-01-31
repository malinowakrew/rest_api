import pytest
from app import create_app
import json

app = create_app()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'
    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.mark.webtest
def test_addition(client):
    with app.app_context():
        question = "/ticket/addition"
        data = {"title": "Something is not working",
                "description": "I have no idea what is happening",
                "severity": "high"}
        response = client.post(question, json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'new'


@pytest.mark.webtest
def test_read(client):
    with app.app_context():
        question = f"/ticket/"
        response = client.get(f'{question}')
    assert response.status_code == 200
