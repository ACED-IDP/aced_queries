import logging

import flask
import requests
from gen3.auth import endpoint_from_token

NO_AUTH_ON_FLASK_REQUEST = 'Gen3SessionAuth: No access_token provided and no Authorization in flask request'
NO_FLASK_REQUEST = 'Gen3SessionAuth No flask request'


class Gen3SessionAuth(requests.auth.AuthBase):
    """
    An Auth helper based on access token, reads token from incoming flask request.
    """

    def __init__(self, access_token=None, endpoint=None, debug=False):
        """
        endpoint
        """
        self.logger = logging.getLogger(__name__)

        self.endpoint = None
        if endpoint:
            self.endpoint = endpoint

        if debug:
            self.logger.setLevel(logging.DEBUG)
        if access_token:
            self._access_token = access_token
        elif not flask.request:
            self.logger.error(NO_FLASK_REQUEST)
            raise NotImplementedError(NO_FLASK_REQUEST)
        elif 'Authorization' not in flask.request.headers:
            self.logger.error(NO_AUTH_ON_FLASK_REQUEST)
            raise NotImplementedError(NO_AUTH_ON_FLASK_REQUEST)
        else:
            authorization_parts = flask.request.headers['Authorization'].split(' ')
            assert len(
                authorization_parts) == 2, f"Gen3SessionAuth expected bearer token {flask.request.headers['Authorization']}"
            self._access_token = authorization_parts[-1]
        if not endpoint:
            self.endpoint = endpoint_from_token(self._access_token)
        self.logger.debug(f"Gen3SessionAuth _access_token {self._access_token} endpoint {self.endpoint}")

    def __call__(self, request_):
        """Adds authorization header to the request
        This gets called by the python.requests package on outbound requests
        so that authentication can be added.
        Args:
            request_ (object): The incoming request object
        """
        request_.headers["Authorization"] = "bearer " + self._access_token
        return request_
