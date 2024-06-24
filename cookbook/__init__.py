import os
from pathlib import Path

from flask import Flask, redirect, url_for

from config import Config

def create_app(config_class=Config):
    """Create and configure the flask application.
    """

    app = Flask(__name__, static_url_path=None)

    app.config.from_object(config_class)
    app.static_url_path = app.config['STATIC_FOLDER']
    app.static_folder = Path(app.root_path) / app.static_url_path

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
