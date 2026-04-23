def test_register(client):
    response = client.post('/register', data={
        'username': 'Nuharilwan',
        'email': 'nuha@gmail.com',
        'password': 'Nuharilwan@24',
        'password2': 'Nuharilwan@24'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_login(client, test_user):
    response = client.post('/login', data={
        'username': 'Nuharilwan',
        'password': 'Nuharilwan@24'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_login_wrong_password(client, test_user):
    response = client.post('/login', data={
        'username': 'Nuharilwan',
        'password': 'Nuharilwan@11'
    }, follow_redirects=True)
    assert b'Invalid username or password' in response.data

from app.main.forms import ContactForm


def test_contact_form_valid():
    form = ContactForm(
        data={
            "name": "Nuha",
            "email": "nuha@gmail.com",
            "subject": "Hello",
            "message": "This is a valid message body"
        }
    )
    assert form.validate() is True


def test_contact_form_missing_name(app):
    with app.app_context():
        form = ContactForm(data={
            "name": "",
            "email": "nuha@gmail.com",
            "subject": "Hello",
            "message": "This is a valid message body"
        })

        assert form.validate() is False


def test_contact_form_valid(app):
    with app.test_request_context():
        form = ContactForm(data={
            "name": "Nuha",
            "email": "nuha@gmail.com",
            "subject": "Hello",
            "message": "This is a valid message body"
        })
        assert form.validate()


def test_contact_form_short_message(app):
    with app.app_context():
        form = ContactForm(data={
            "name": "Nuha",
            "email": "nuha@gmail.com",
            "subject": "Hello",
            "message": "short"
        }
    )
    assert form.validate() is False


def test_contact_form_missing_subject(app):
    with app.app_context():
        form = ContactForm(
            data={
                "name": "Nuha",
                "email": "nuha@gmail.com",
                "subject": "",
                "message": "This is a valid message body"
            })
    assert form.validate() is False

def test_logout(client, test_user):
    client.post('/login', data={
        'username': 'Nuharilwan',
        'password': 'Nuharilwan@24'
    })
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
