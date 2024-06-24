import os
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') \
        or 'dev'

    DATABASE = os.environ.get('DATABASE_URI') \
        or Path(basedir) / 'instance/cookbook.sqlite'

    STATIC_FOLDER = os.environ.get('STATIC_FOLDER') \
        or Path(basedir) / 'static'

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') \
        or Path(STATIC_FOLDER) / 'user_images'

    MAX_CONTENT_LENGTH = 2 * 1000 * 1000
