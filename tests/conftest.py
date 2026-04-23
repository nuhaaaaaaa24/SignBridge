import pytest
from app import create_app
from extensions import db
from app.models import User, Room

@pytest.fixture
def app():
    app = create_app()

    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'MAIL_SERVER': None
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        if app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:':
            db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):  # 'app' arg ensures its context is active — don't open another one
    user = User(username='testuser', email='test@test.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_room(app, test_user):  # same here — no new app_context needed
    room = Room(room_code='TEST-1234', owner_id=test_user.id)
    db.session.add(room)
    db.session.commit()
    return room