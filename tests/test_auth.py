import pytest
from flask import g, session
from cookbook.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        '/auth/register', data = { 'email': 'a@example.com', 'password': 'a', 'display_name': 'A' }
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE email = 'a@example.com'",
        ).fetchone() is not None


@pytest.mark.parametrize(('email', 'password', 'display_name', 'message'), (
    ('', '', '', b'Email is required.'),
    ('', 'a', 'A', b'Email is required.'),
    ('a@example.com', '', 'A', b'Password is required.'),
    ('a@example.com', 'a', '', b'Display name is required.'),
    ('test@example.com', 'test', 'Test', b'already registered'),
))
def test_register_validate_input(client, email, password, display_name, message):
    response = client.post(
        '/auth/register',
        data = { 'email': email, 'password': password, 'display_name': display_name }
    )
    assert message in response.data
