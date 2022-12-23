import logging

import pytest
from flask import request
import requests
import requests_mock

from aced_queries.auth import Gen3SessionAuth, NO_AUTH_ON_FLASK_REQUEST, NO_FLASK_REQUEST


def test_session_auth_ok(app, token):
    """Test Gen3SessionAuth, ensure it reads incoming auth from flask request and insert it on outgoing requests."""
    assert app, "No configured app"
    with app.test_request_context('/', headers={'Authorization': f'bearer {token}'}):
        assert request, "Could not access default request"
        assert 'Authorization' in request.headers, "Missing Authorization header"

        # ensure that auth can read the flask incoming request
        auth = Gen3SessionAuth()
        assert auth._access_token, "Should have an access token"
        assert auth.endpoint == 'http://foo', "Should deduce endpoint from token"

        with requests_mock.mock() as m:
            # dummy server
            dummy_response = 'dummy response'
            m.get('http://foo/bar', text=dummy_response)
            # make a request
            _ = requests.get('http://foo/bar', auth=auth)
            # check response
            assert len(m.request_history) == 1, "Expected 1 request in history"
            authorized_request = m.request_history[0]
            assert 'Authorization' in authorized_request.headers
            auth_header = authorized_request.headers['Authorization']
            assert token in auth_header


def test_session_auth_fail_flask_no_auth(app, caplog):
    """Test Gen3SessionAuth, ensure it reads incoming auth from flask request and insert it on outgoing requests."""
    with app.test_request_context('/'):
        assert request, "Could not access default request"
        # ensure that auth can read the flask incoming request
        with pytest.raises(NotImplementedError):
            _ = Gen3SessionAuth()
        assert NO_AUTH_ON_FLASK_REQUEST in caplog.messages


def test_session_auth_fail_no_flask(caplog):
    """Test Gen3SessionAuth, ensure it reads incoming auth from flask request and insert it on outgoing requests."""
    with pytest.raises(NotImplementedError):
        _ = Gen3SessionAuth()
    assert NO_FLASK_REQUEST in caplog.messages


def test_session_auth_ok_token(token):
    """Test Gen3SessionAuth, ensure it reads incoming auth from flask request and insert it on outgoing requests."""
    _ = Gen3SessionAuth(access_token=token)


def test_session_auth_ok_token_debug(caplog, token):
    """Test Gen3SessionAuth, ensure it reads incoming auth from flask request and insert it on outgoing requests."""
    caplog.set_level(logging.DEBUG)
    _ = Gen3SessionAuth(access_token=token, endpoint='http://foobar', debug=True)
    assert len([m for m in caplog.messages if '_access_token' in m]) > 0, caplog.messages
