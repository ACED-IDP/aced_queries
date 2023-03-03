import jwt as jwt
import pytest
from flask import Flask


def _create_app():
    app = Flask('dummy-dash-app')

    app.url_map.strict_slashes = False

    @app.route('/')
    def hello_world():
        return '<p>Hello, World!</p>'

    return app


@pytest.fixture(scope='module')
def app():
    """
    Application fixture.
    """
    app = _create_app()

    app.app_context().push()

    return app


@pytest.fixture()
def token():
    """Dummy jwt token"""
    return jwt.encode({"some": "payload", "iss": "http://foo"}, key="dummy")
