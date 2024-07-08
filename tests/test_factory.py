from cookbook.application import create_app
from cookbook.config import Config

def test_config():
    assert not create_app().testing

    app_config = Config(testing=True)
    assert create_app(app_config).testing
