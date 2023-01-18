#-------------------------------------------------------------------------------
# Recipes tests
#-------------------------------------------------------------------------------

import io
import os
import pytest

from pathlib import Path

from cookbook.db import get_db

# Data generators for testing.
#-------------------------------------------------------------------------------
def image_data(
    image_bytes = b'bla bla bla', 
    image_file_name = 'cool.jpg'):
    return (io.BytesIO(image_bytes), image_file_name)

def recipe_data(
    title = 'different recipe', 
    author = 'oliver jameson',
    description = 'dot dot dot',
    source_url = 'http://google.com',
    image = 'default',
    servings = 1, 
    prep_time = 4,
    cook_time = 8,
    ingredients = 'six\nfive\nfour',
    instructions = 'new instructions'
    ):
    # NOTE: Hack because we can't use this function as a default value.
    if image == 'default':
        image = image_data()
    return {
        'title': title,
        'author': author,
        'description': description,
        'source_url': source_url,
        'image': image,
        'servings': servings,
        'prep_time': prep_time,
        'cook_time': cook_time,
        'ingredients': ingredients,
        'instructions': instructions,
    }

# Test index route.
#-------------------------------------------------------------------------------
def test_index(client, auth):
    response = client.get('/recipes', follow_redirects=True)
    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()

    response = client.get('/recipes')
    assert b'Log Out' in response.data
    assert b'test recipe' in response.data
    assert b'user_images/whatever.jpg' in response.data
    assert b'href=\'/recipes/add\'' in response.data
    assert b'href=\'/recipes/view/1\'' in response.data

# Authentication is required.
#-------------------------------------------------------------------------------
@pytest.mark.parametrize('path', (
    '/recipes/add',
    '/recipes/edit/1',
    '/recipes/delete/1',
    ))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == '/auth/login'

# Unauthenticated access is prevented.
#-------------------------------------------------------------------------------
def test_data_privacy(app, client, auth):
    with app.app_context():
        db = get_db()
        db.execute('UPDATE recipe SET user_id = 2 WHERE id = 1')
        db.commit()

    auth.login()

    # Current user can't access other user's recipe.
    assert client.post('/recipes/edit/1', data=recipe_data()).status_code == 404
    assert client.post('/recipes/delete/1').status_code == 404
    assert client.get('/recipes/view/1').status_code == 404

    # Current user doesn't see other user's view link.
    assert b'href=\'/recipes/view/1\'' not in client.get('/').data

# Recipes must exist to be operated on.
#-------------------------------------------------------------------------------
def test_exists_required(client, auth):
    auth.login()
    response = client.post('/recipes/delete/2')
    assert response.status_code == 404
    assert b'Recipe id 2 not found' in response.data

    response = client.post('/recipes/edit/2', data=recipe_data())
    assert response.status_code == 404
    assert b'Recipe id 2 not found' in response.data

# Recipes must be added to the database.
#-------------------------------------------------------------------------------
def test_add(client, auth, app):
    auth.login()
    assert client.get('/recipes/add').status_code == 200

    response = client.post('/recipes/add', data=recipe_data())
    assert response.headers['Location'] == '/recipes/view/2'

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM recipe').fetchone()[0]
        assert count == 2

# Recipes must be viewable.
#-------------------------------------------------------------------------------
def test_view(client, auth, app):
    auth.login()

    response = client.get('/recipes/view/1')
    assert response.status_code == 200
    assert b'1tbsp nonsense' in response.data

# Recipes must be edited in the database.
#-------------------------------------------------------------------------------
def test_edit(client, auth, app):
    auth.login()
    assert client.get('/recipes/edit/1').status_code == 200

    client.post('/recipes/edit/1', data=recipe_data())

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM recipe WHERE id = 1').fetchone()
        assert post['title'] == 'different recipe'

# Recipes must be validated when added or edited.
#-------------------------------------------------------------------------------
@pytest.mark.parametrize('path', (
    '/recipes/add',
    '/recipes/edit/1',
    ))
def test_add_edit_validate(client, auth, path):
    auth.login()
    recipe = recipe_data(title='')

    response = client.post(path, data=recipe)
    assert b'Title is required.' in response.data

    recipe = recipe_data(author='')
    response = client.post(path, data=recipe)
    assert b'Author is required.' in response.data

    recipe = recipe_data(description='')
    response = client.post(path, data=recipe)
    assert b'Description is required.' in response.data

    recipe = recipe_data(source_url='')
    response = client.post(path, data=recipe)
    assert b'Source URL is required.' in response.data

    recipe = recipe_data(image=image_data(image_file_name=''))
    response = client.post(path, data=recipe)
    assert b'Image is required.' in response.data

    recipe = recipe_data(image=image_data(image_file_name='uhoh.exe'))
    response = client.post(path, data=recipe)
    assert b'Image not allowed.' in response.data

    recipe = recipe_data(servings='')
    response = client.post(path, data=recipe)
    assert b'Servings is required.' in response.data

    recipe = recipe_data(prep_time='')
    response = client.post(path, data=recipe)
    assert b'Prep Time is required.' in response.data

    recipe = recipe_data(cook_time='')
    response = client.post(path, data=recipe)
    assert b'Cook Time is required.' in response.data

    recipe = recipe_data(ingredients='')
    response = client.post(path, data=recipe)
    assert b'Ingredients is required.' in response.data

    recipe = recipe_data(instructions='')
    response = client.post(path, data=recipe)
    assert b'Instructions is required.' in response.data

# Recipes must be deletable.
#-------------------------------------------------------------------------------

# NOTE: Do we need this?
user_images = Path(__file__).parent / 'user_images'

def test_delete(client, auth, app):
    # assert os.path.exists(os.path.join(user_images, 'whatever.jpg'))

    auth.login()
    response = client.post('/recipes/delete/1')
    assert response.headers['Location'] == '/recipes'

    with app.app_context():
        db = get_db()
        recipe = db.execute('SELECT * FROM recipe WHERE id = 1').fetchone()
        assert recipe is None

    # TODO: Test whether associated image is deleted.

    # assert not os.path.exists(os.path.join(user_images, 'whatever.jpg'))

