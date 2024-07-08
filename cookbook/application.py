#-------------------------------------------------------------------------------
# Application factory
#-------------------------------------------------------------------------------

import os

from flask import Flask

from cookbook.config import Config

def create_app(config=None):
    """Create and configure the flask application.
    """

    config = config or Config.from_env_or_default()

    print(config)

    app = Flask(
        __name__,
        instance_path=config.INSTANCE_PATH,
        static_folder=config.STATIC_FOLDER,
        template_folder=config.TEMPLATE_FOLDER,
        static_url_path=None,
    )
    app.config.from_object(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from cookbook import db
    db.init_app(app)

    from cookbook.main.views import blueprint as main
    app.register_blueprint(main)

    from cookbook.auth.views import blueprint as auth
    app.register_blueprint(auth)

    from cookbook.recipes.views import blueprint as recipes
    app.register_blueprint(recipes)

    return app
