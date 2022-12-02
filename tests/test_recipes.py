import pytest
import io
from cookbook.db import get_db


def test_index(client, auth):
    response = client.get('/recipes', follow_redirects=True)
    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()

    response = client.get('/recipes')
    assert b'Log Out' in response.data
    assert b'test recipe' in response.data
    assert b'user_images/whatever' in response.data
    assert b'href=\'/recipes/add\'' in response.data
    assert b'href=\'/recipes/view/1\'' in response.data


# TODO: Test view route.


# TODO: Test edit route once implemented.
@pytest.mark.parametrize('path', (
    '/recipes/add',
    # '/recipes/edit/1',
    '/recipes/delete/1',
    ))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == '/auth/login'


def test_author_required(app, client, auth):
    # Change the post author to another user.
    with app.app_context():
        db = get_db()
        db.execute('UPDATE recipe SET user_id = 2 WHERE id = 1')
        db.commit()

    auth.login()

    # Current user can't modify other user's recipe.
    # TODO: Test edit route once implemented.
    # assert client.post('/recipes/edit/1').status_code == 404
    assert client.post('/recipes/delete/1').status_code == 404

    # Current user doesn't see other user's view link.
    assert b'href=\'/recipes/view/1\'' not in client.get('/').data


# TODO: Test edit route once implemented.
@pytest.mark.parametrize('path', (
    # '/recipes/edit/2',
    '/recipes/delete/2',
    ))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_add(client, auth, app):
    auth.login()
    assert client.get('/recipes/add').status_code == 200

    response = client.post('/recipes/add', data={
        'title': 'new recipe',
        'author': 'oliver jameson',
        'description': 'description',
        'source_url': 'http://example.com',
        'image': (io.BytesIO(b"some initial text data"), 'whatever.jpg'),
        'servings': 2,
        'prep_time': 5,
        'cook_time': 10,
        'ingredients': 'one\ntwo\nthree',
        'instructions': 'instructions go here',
    })
    assert response.headers['Location'] == '/recipes/view/2'

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM recipe').fetchone()[0]
        assert count == 2


# TODO: Implement this test once edit route is implemented.
# def test_edit(client, auth, app):
#     auth.login()
#     assert client.get('/recipes/edit/1').status_code == 200
#
#     client.post('/recipes/edit/1', data={
#         'title': 'updated recipe',
#         'author': 'oliver jameson',
#         'description': 'description',
#         'source_url': 'http://example.com',
#         'image': (io.BytesIO(b"some initial text data"), 'whatever.jpg')
#         'servings': 2,
#         'prep_time': 5,
#         'cook_time': 10,
#         'instructions': 'instructions go here',
#     })
#
#     with app.app_context():
#         db = get_db()
#         post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
#         assert post['title'] == 'updated'


@pytest.mark.parametrize('path', (
    '/recipes/add',
    # '/recipes/edit/1',
    ))
def test_add_edit_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={
        'title': '',
        'author': 'oliver jameson',
        'description': 'description',
        'source_url': 'http://example.com',
        'image': (io.BytesIO(b"some initial text data"), 'whatever.jpg'),
        'servings': 2,
        'prep_time': 5,
        'cook_time': 10,
        'ingredients': 'one\ntwo\nthree',
        'instructions': 'instructions go here',
        })
    assert b'Title is required.' in response.data



