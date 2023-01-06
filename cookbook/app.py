import os

from flask import Flask, redirect, url_for

def create_app(test_config=None):

    # Create and configure the app.
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'cookbook.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.static_folder, 'user_images'),
        MAX_CONTENT_LENGTH=2 * 1000 * 1000,
        )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # This is the base route.
    @app.route('/')
    def index():
        # TODO: Return a nice splash page instead of redirecting.
        return redirect(url_for('auth.login'))

    from . import db
    db.init_app(app)

    from cookbook.auth.views import blueprint as auth
    app.register_blueprint(auth)

    from cookbook.recipes.views import blueprint as recipes
    app.register_blueprint(recipes)

    return app

