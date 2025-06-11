import os
import pytest
from demo import create_app, db
from demo.models import User

@pytest.fixture
def app(tmp_path):
    # configure app to use temporary database
    test_db = tmp_path / "test.db"
    flask_app = create_app()
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{test_db}"

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_create_user(client):
    response = client.post('/users', json={'name': 'Test'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test'
    # ensure user stored
    response = client.get('/users')
    users = response.get_json()['users']
    assert any(u['name'] == 'Test' for u in users)
