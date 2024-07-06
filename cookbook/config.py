import os
from pathlib import Path


class Config:
    def __init__(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        parentdir = Path(basedir).parent

        self.INSTANCE_PATH = os.environ.get('INSTANCE_PATH') \
            or os.path.join(parentdir, 'instance')

        self.STATIC_FOLDER = os.environ.get('STATIC_FOLDER') \
            or os.path.join(basedir, 'main/static')

        self.TEMPLATE_FOLDER = os.environ.get('TEMPLATE_FOLDER') \
            or os.path.join(basedir, 'main/templates')

        self.SECRET_KEY = os.environ.get('SECRET_KEY') \
            or 'dev'

        self.DATABASE_URI = os.environ.get('DATABASE_URI') \
            or os.path.join(self.INSTANCE_PATH, 'cookbook.sqlite')

        self.UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') \
            or os.path.join(self.STATIC_FOLDER, 'user_images')

        self.MAX_CONTENT_LENGTH = 2 * 1000 * 1000

    def __str__(self):
        return f'''
            INSTANCE_PATH      = {self.INSTANCE_PATH}
            STATIC_FOLDER      = {self.STATIC_FOLDER}
            TEMPLATE_FOLDER    = {self.TEMPLATE_FOLDER}
            SECRET_KEY         = {self.SECRET_KEY}
            DATABASE_URI       = {self.DATABASE_URI}
            UPLOAD_FOLDER      = {self.UPLOAD_FOLDER}
            MAX_CONTENT_LENGTH = {self.MAX_CONTENT_LENGTH}
            '''
