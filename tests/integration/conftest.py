import os

import pytest
import requests
from requests.auth import HTTPBasicAuth


@pytest.fixture(scope='session')
def endpoint():
    return os.environ['GEN3_ENDPOINT']


@pytest.fixture(scope='session')
def client_id():
    return os.environ['GEN3_CLIENT_ID']


@pytest.fixture(scope='session')
def client_secret():
    return os.environ['GEN3_CLIENT_SECRET']


# session: the fixture is destroyed at the end of the test session.
@pytest.fixture(scope='session')
def access_token(endpoint, client_id, client_secret):
    """See https://github.com/uc-cdis/fence/blob/master/README.md#register-an-oauth-client-for-a-client-credentials-flow"""
    fence_url = f"{endpoint}/user/oauth2/token?grant_type=client_credentials"
    basic = HTTPBasicAuth(client_id, client_secret)
    response = requests.post(fence_url, data={'scope': "openid user data"}, auth=basic)
    assert response.status_code == 200, response.text
    return response.json()['access_token']

# response = response.json
# assert "access_token" in response
# assert "expires_in" in response
# assert response.get("token_type") == "Bearer"
