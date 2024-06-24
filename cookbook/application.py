#-------------------------------------------------------------------------------
# Application factory
#-------------------------------------------------------------------------------

import os
from pathlib import Path

from flask import Flask

from cookbook.config import Config

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

    from . import db
    db.init_app(app)

    from cookbook.main.views import blueprint as main
    app.register_blueprint(main)

    from cookbook.auth.views import blueprint as auth
    app.register_blueprint(auth)

    from cookbook.recipes.views import blueprint as recipes
    app.register_blueprint(recipes)

    return app
