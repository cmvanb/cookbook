import os
from pathlib import Path
from textwrap import dedent


class Config:
    """ Configuration object for the Flask application.
    """

    TESTING: bool
    INSTANCE_PATH: str
    STATIC_FOLDER: str
    TEMPLATE_FOLDER: str
    SECRET_KEY: str
    DATABASE_PATH: str
    UPLOAD_FOLDER: str
    MAX_CONTENT_LENGTH: int

    def __init__(
        self,
        testing = None,
        instance_path = None,
        static_folder = None,
        template_folder = None,
        secret_key = None,
        database_path = None,
        upload_folder = None,
        max_content_length = None,
        ):
        """ Where no value is passed, the constructor will use a default value.
        """

        basedir = os.path.abspath(os.path.dirname(__file__))
        parentdir = Path(basedir).parent

        self.TESTING = testing \
            or False

        self.INSTANCE_PATH = instance_path \
            or os.path.join(parentdir, 'instance')

        self.STATIC_FOLDER = static_folder \
            or os.path.join(basedir, 'main/static')

        self.TEMPLATE_FOLDER = template_folder \
            or os.path.join(basedir, 'main/templates')

        self.SECRET_KEY = secret_key \
            or 'dev'

        self.DATABASE_PATH = database_path \
            or os.path.join(self.INSTANCE_PATH, 'cookbook.sqlite')

        self.UPLOAD_FOLDER = upload_folder \
            or os.path.join(self.STATIC_FOLDER, 'user_images')

        self.MAX_CONTENT_LENGTH = max_content_length \
            or 2 * 1000 * 1000


    def __str__(self):
        return dedent(f'''\
            INSTANCE_PATH      = {self.INSTANCE_PATH}
            STATIC_FOLDER      = {self.STATIC_FOLDER}
            TEMPLATE_FOLDER    = {self.TEMPLATE_FOLDER}
            SECRET_KEY         = {self.SECRET_KEY}
            DATABASE_PATH      = {self.DATABASE_PATH}
            UPLOAD_FOLDER      = {self.UPLOAD_FOLDER}
            MAX_CONTENT_LENGTH = {self.MAX_CONTENT_LENGTH}\
            ''')

    @staticmethod
    def from_env():
        """ Initialize with values from the environment.
        """

        return Config(
            testing            = os.environ.get('TESTING'),
            instance_path      = os.environ.get('INSTANCE_PATH'),
            static_folder      = os.environ.get('STATIC_FOLDER'),
            template_folder    = os.environ.get('TEMPLATE_FOLDER'),
            secret_key         = os.environ.get('SECRET_KEY'),
            database_path      = os.environ.get('DATABASE_PATH'),
            upload_folder      = os.environ.get('UPLOAD_FOLDER'),
            max_content_length = os.environ.get('MAX_CONTENT_LENGTH'),
            )
