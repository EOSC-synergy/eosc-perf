"""This module acts as a facade between the IOController and the EGI Check-In authentication system."""

import json
from os import urandom
from time import time
from typing import Optional
from urllib.request import urlopen
import requests
from aarc_g002_entitlement import Aarc_g002_entitlement, Aarc_g002_entitlement_Error

from flask import session
from authlib.integrations.flask_client import OAuth
from ..configuration import configuration
from ..model.facade import facade

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


class Authenticator:
    """A facade between IOController and the EGI Check-In authentication system.

    It integrates Open ID Connect into the web app.

    Attributes:
        oauth (OAuth): The used Flask OAuth registry for oauth clients.
        admin_entitlements (List[str]): If a user has one entitlement that is included in this list,
            they have admin rights.
        hostname (str): The hostname used for redirection after authentication.
        client_secret (str): The oauth client secret.
        scope (str): The scope used for registering the oauth client.
    """

    def __init__(self):
        self.oauth = None
        self.admin_entitlements = []
        self.hostname = None
        self.client_id = None
        self.client_secret = None
        self.scope = 'openid email profile eduperson_entitlement offline_access'
        self.conf_url = ""
        self.userinfo_url = ""

    def configure_authenticator(self, flask_app):
        """Set up OIDC authentication functionality for the web app.

        Args:
            flask_app (Flask): The flask app for which to set up OIDC functionality.
        """

        if len(configuration.get('oidc_client_secret_file')) == 0\
                or configuration.get('oidc_client_secret_file') == 'SET_ME':
            raise ValueError("Please configure OIDC client secret")
        self.client_secret = read_file_content(configuration.get('oidc_client_secret_file'))
        if self.client_secret is None or len(self.client_secret) == 0:
            raise ValueError("Invalid OIDC client secret file given")

        flask_app.secret_key = read_file_content(configuration.get('secret_key_file'))
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

        if configuration.get('debug'):
            self.admin_entitlements = configuration.get('debug_admin_entitlements')
            self.conf_url = CONFIGURATION_URL_DEBUG
            self.userinfo_url = USERINFO_URL_DEBUG
        else:
            self.admin_entitlements = configuration.get('admin_entitlements')
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
            self.__update_user_info()
        except KeyError:
            return False
        return True

    def is_admin(self) -> bool:
        """Check whether the current user has admin rights.

        Returns:
            bool: True if the user is an admin.
        """
        # skip auth check if configured in debug mode
        if configuration.get('debug') and configuration.get('debug-logged-in-is-admin') and self.is_authenticated():
            return True

        try:
            entitlements = session['user']['info']['eduperson_entitlement']
        except KeyError:
            return False
        for entitlement in entitlements:
            for required in self.admin_entitlements:
                try:
                    if self._match_entitlement(required, entitlement):
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
            params={'client_id': "eosc_perf",
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

    @staticmethod
    def __update_user_info():
        """Update saved email and name if current user is in db."""
        uid = session['user']['sub']
        try:
            uploader = facade.get_uploader(uid)
        except facade.NotFoundError:
            return
        email = session['user']['info']['email']
        name = session['user']['info']['name']
        uploader.set_email(email)
        uploader.set_name(name)


# single global instance
authenticator = Authenticator()


def configure_authenticator(app):
    """Configures the authenticator for given app and config."""
    authenticator.configure_authenticator(app)
