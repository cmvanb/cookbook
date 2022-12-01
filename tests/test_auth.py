import pytest
from flask import g, session
from cookbook.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        '/auth/register', data = { 'email': 'a@gmail.com', 'password': 'a', 'display_name': 'A' }
    )
    assert response.headers['Location'] == '/auth/login'

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE email = 'a@gmail.com'",
        ).fetchone() is not None


@pytest.mark.parametrize(('email', 'password', 'display_name', 'message'), (
    ('', '', '', b'Email is required.'),
    ('', 'a', 'A', b'Email is required.'),
    ('a@gmail.com', '', 'A', b'Password is required.'),
    ('a@gmail.com', 'a', '', b'Display name is required.'),
    ('test@gmail.com', 'test', 'Test', b'already registered'),
    ('a', 'a', 'A', b'The email address is not valid.'),
))
def test_register_validate_input(client, email, password, display_name, message):
    response = client.post(
        '/auth/register',
        data = { 'email': email, 'password': password, 'display_name': display_name }
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200

    response = auth.login()
    assert response.headers['Location'] == '/recipes'

    with client:
        client.get('/recipes')
        assert session['user_id'] == 1
        assert g.user['email'] == 'test@gmail.com'


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('a@gmail.com', 'test', b'Incorrect email.'),
    ('test@gmail.com', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


