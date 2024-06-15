import os
from pathlib import Path

from flask import Flask, redirect, url_for

def create_app(test_config=None):
    """Create and configure the flask application.
    """

    app = Flask(__name__, instance_relative_config=True)

    assert app.static_folder is not None, 'Static folder must be configured.'

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=Path(app.instance_path) / Path('cookbook.sqlite'),
        UPLOAD_FOLDER=Path(app.static_folder) / Path('user_images'),
        MAX_CONTENT_LENGTH=2 * 1000 * 1000,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        # TODO: Render a nice splash page instead of redirecting.
        return redirect(url_for('auth.login'))

    from cookbook import db
    db.init_app(app)

    from cookbook.auth.views import blueprint as auth
    app.register_blueprint(auth)

    from cookbook.recipes.views import blueprint as recipes
    app.register_blueprint(recipes)

    return app
