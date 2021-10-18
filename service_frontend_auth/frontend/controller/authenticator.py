"""This module exposes the Authenticator, which acts as an interface for the IOController to interact with the
EGI Check-In authentication system."""

import json
from os import urandom
from time import time
from typing import Optional
from urllib.request import urlopen

import requests
from aarc_g002_entitlement import Aarc_g002_entitlement, Aarc_g002_entitlement_Error
from authlib.integrations.flask_client import OAuth
from flask import session, Flask

from ..configuration import configuration

CONFIGURATION_URL_DEBUG = 'https://aai-dev.egi.eu/oidc/.well-known/openid-configuration'
CONFIGURATION_URL = 'https://aai.egi.eu/oidc/.well-known/openid-configuration'
USERINFO_URL_DEBUG = 'https://aai-dev.egi.eu/oidc/userinfo'
USERINFO_URL = 'https://aai.egi.eu/oidc/userinfo'


class AuthenticateError(Exception):
    """Exception to signal a user isn't authenticated correctly."""


def read_file_content(filename: str) -> Optional[str]:
    """Get the contents of a file.

    Returns:
        Optional[str]: The contents of the file as string, or None if the file could not be read.
    """
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except OSError:
        return None


class MockAuthenticator:
    def redirect_to_authentication(self):
        return None

    def is_authenticated(self) -> bool:
        return True

    def is_admin(self) -> bool:
        return True

    def logout(self) -> bool:
        return True

    def get_email(self) -> Optional[str]:
        return "user@example.com"

    def get_full_name(self) -> Optional[str]:
        return "Max Mustermann"

    def get_user_id(self) -> Optional[str]:
        return "a very unique individual :)"


class Authenticator(MockAuthenticator):
    """A middle-man between IOController and the EGI Check-In authentication system.

    It integrates Open ID Connect into the web app.

    Attributes:
        oauth (OAuth): The used Flask OAuth registry for oauth clients.
        admin_entitlement (str): If a user has this entitlement, they have admin rights.
        hostname (str): The hostname used for redirection after authentication.
        client_secret (str): The oauth client secret.
        scope (str): The scope used for registering the oauth client.
    """

    def __init__(self, flask_app):
        """Set up OIDC authentication functionality for the web app.

        Args:
            flask_app (Flask): The flask app for which to set up OIDC functionality.
        """
        self.oauth = None
        self.admin_entitlement = None
        self.hostname = None
        self.client_id = None
        self.client_secret = None
        self.scope = 'openid email profile eduperson_entitlement offline_access'
        self.conf_url = ""
        self.userinfo_url = ""

        if len(configuration.get('oidc_client_secret_file')) == 0 \
                or configuration.get('oidc_client_secret_file') == 'SET_ME':
            raise ValueError("Please configure OIDC client secret")
        self.client_secret = read_file_content(configuration.get('oidc_client_secret_file'))
        if self.client_secret is None or len(self.client_secret) == 0:
            raise ValueError("Invalid OIDC client secret file given")

        flask_app.secret_key = read_file_content(configuration.get('cookie_key_file'))
        # generate random temporary key if none is given
        if flask_app.secret_key is None or len(flask_app.secret_key) == 0:
            flask_app.secret_key = urandom(16)

        self.client_id = configuration.get('oidc_client_id')
        self.hostname = configuration.get('oidc_redirect_hostname')
        if len(self.client_id) == 0 or self.client_id == 'SET_ME':
            raise ValueError("Please configure the OIDC client id")
        if len(self.hostname) == 0 or self.hostname == 'SET_ME':
            raise ValueError("Please configure the domain")

        flask_app.config["EOSC_PERF_CLIENT_ID"] = self.client_id
        flask_app.config["EOSC_PERF_CLIENT_SECRET"] = self.client_secret

        self.admin_entitlement = configuration.get('admin_entitlement')

        if configuration.get('debug'):
            self.conf_url = CONFIGURATION_URL_DEBUG
            self.userinfo_url = USERINFO_URL_DEBUG
        else:
            self.conf_url = CONFIGURATION_URL
            self.userinfo_url = USERINFO_URL

        self.oauth = OAuth(flask_app)
        self.oauth.register(
            name='eosc_perf',
            userinfo_endpoint=self.userinfo_url,
            server_metadata_url=self.conf_url,
            client_kwargs={
                'scope': self.scope
            },
            secret=self.client_secret
        )

    def redirect_to_authentication(self):
        """Redirect user to EGI Check-In for authentication."""
        redirect_uri = 'https://' + self.hostname + '/oidc-redirect'
        return self.oauth.eosc_perf.authorize_redirect(redirect_uri)

    def is_authenticated(self) -> bool:
        """Check if the current user is authenticated.

        Returns:
            bool: True if logged in through EGI Check-In or token not expired.
        """
        if not self._token_expired():
            return True
        try:
            token = self.oauth.eosc_perf.authorize_access_token()
            user = self.oauth.eosc_perf.parse_id_token(token)
            userinfo = self.oauth.eosc_perf.userinfo()
            session['user'] = user
            session['user']['token'] = token
            session['user']['info'] = userinfo
        except KeyError:
            return False
        return True

    def get_user_info(self) -> Optional[dict]:
        if self.is_authenticated():
            try:
                token = session['user']['token']['access_token']
                email = session['user']['info']['email']
                name = session['user']['info']['name']
                admin = self.is_admin()
                return {"token": token, "email": email, "name": name, "admin": admin}
            except KeyError:
                return None
        return None

    def is_admin(self) -> bool:
        """Check whether the current user has admin rights.

        Returns:
            bool: True if the user is an admin.
        """
        # skip auth check if configured in debug mode
        if configuration.get('debug') and self.is_authenticated():
            return True

        try:
            entitlements = session['user']['info']['eduperson_entitlement']
        except KeyError:
            return False
        for entitlement in entitlements:
            try:
                if self._match_entitlement(self.admin_entitlement, entitlement):
                    return True
            except Aarc_g002_entitlement_Error:
                continue
        return False

    def logout(self) -> bool:
        """Sign out the current user.

        Returns:
            bool: True if logout successful
        """
        try:
            token = session['user']['info']
        except KeyError:
            return False
        endpoint = json.loads(urlopen(self.conf_url).read())["revocation_endpoint"]
        requests.post(
            endpoint,
            params={'token': token},
            headers={'content-type': 'application/x-www-form-urlencoded'})
        session.pop('user', None)
        return True

    def _refresh_token(self) -> bool:
        """Try to refresh token of current user.

        Returns:
            bool: True if refresh succeeds.
        """

        endpoint = json.loads(urlopen(self.conf_url).read())["token_endpoint"]
        try:
            refresh_token = session['user']['token']['refresh_token']
        except KeyError:
            self.logout()
            return False
        response = requests.post(
            endpoint,
            params={'client_id': "backend",
                    'client_secret': self.client_secret,
                    'grant_type': "refresh_token",
                    'refresh_token': refresh_token,
                    'scope': self.scope},
            headers={'content-type': 'application/x-www-form-urlencoded'})
        if response.status_code == 200:
            new_token = response.json()
            user = self.oauth.eosc_perf.parse_id_token(new_token)
            try:
                user['info'] = session['user']['info']
                user['token'] = new_token
                session['user'] = user
            except KeyError:
                self.logout()
                return False
            return True
        return False

    def _token_expired(self) -> bool:
        """Check if the current user has a valid authentication token.

        Returns:
            True if there is *no* valid token.
        """
        try:
            user = session['user']
        except KeyError:
            return True
        if user['exp'] < time():
            if not self._refresh_token():
                return False
            user = session['user']
        return user['exp'] < time()

    @staticmethod
    def _match_entitlement(required, actual) -> bool:
        """Match an AARC G002 entitlement.

        Returns:
            bool: True if the actual entitlements contain the required one.
        """
        required_entitlement = Aarc_g002_entitlement(required, strict=False)
        actual_entitlement = Aarc_g002_entitlement(actual)
        return required_entitlement.is_contained_in(actual_entitlement)

    def get_email(self) -> Optional[str]:
        try:
            return session['user']['info']['email']
        except KeyError:
            return None

    def get_full_name(self) -> Optional[str]:
        try:
            return session['user']['info']['name']
        except KeyError:
            return None

    def get_user_id(self) -> Optional[str]:
        try:
            return session['user']['sub']
        except KeyError:
            return None
