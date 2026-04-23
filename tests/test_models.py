from app.models import User
from app.call.services import generate_room_code

def test_password_hashing(app):
    with app.app_context():
        u = User(username='test', email='t@t.com')
        u.set_password('mypassword')
        assert u.check_password('mypassword') is True
        assert u.check_password('wrongpassword') is False

def test_token_generation(app, test_user):
    with app.app_context():
        from extensions import db
        from app.models import User
        u = db.session.get(User, test_user.id)
        token = u.get_token()
        assert token is not None
        assert len(token) == 32
        assert User.check_token(token) is not None

def test_room_code_format():
    code = generate_room_code()
    parts = code.split('-')
    assert len(parts) == 2
    assert len(parts[0]) == 4
    assert len(parts[1]) == 4