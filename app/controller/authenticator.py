'''This module acts as a facade between the IOController
and the EGI Check-In authentication system.
Provided is:
 - Authenticator'''

import json
from time import time
from urllib.request import urlopen
import requests

from flask import session
from flask.blueprints import Blueprint
from authlib.integrations.flask_client import OAuth
from ..configuration import configuration
from ..model.facade import facade
from ..view.pages.helpers import info_redirect, error_redirect


CONF_URL = 'https://aai-dev.egi.eu/oidc/.well-known/openid-configuration'

class AuthenticateError(Exception):
    """Exception to signal a user isn't authenticated correctly."""

class Authenticator:
    """A fascade between IOController and the EGI Check-In authentication
       system. It integrates Open ID Connect into the web app."""

    def __init__(self):
        self.oauth = None
        self.admin_affiliations = []
        self.hostname = None
        self.client_secret = None
        self.scope = 'openid email profile eduperson_scoped_affiliation offline_access'

    def configure_authenticator(self, flask_app):
        """Sets up OIDC authentication functionality for the web app"""
        if len(configuration.get('oidc_client_secret')) == 0:
            raise ValueError("missing openID client secret in configuration")
        self.client_secret = configuration.get('oidc_client_secret')

        flask_app.secret_key = '!secret'
        flask_app.config["EOSC-PERF_CLIENT_ID"] = 'eosc-perf'
        flask_app.config["EOSC-PERF_CLIENT_SECRET"] = self.client_secret

        self.oauth = OAuth(flask_app)
        self.hostname = configuration.get('oidc_redirect_hostname')
        self.oauth.register(
            name='eosc-perf',
            userinfo_endpoint='https://aai-dev.egi.eu/oidc/userinfo',
            server_metadata_url=CONF_URL,
            client_kwargs={
                'scope': self.scope
            },
            secret=self.client_secret
        )

        if configuration.get('debug'):
            self.admin_affiliations = configuration.get('debug_admin_affiliations')
        else:
            self.admin_affiliations = configuration.get('admin_affiliations')

    def authenticate_user(self):
        """Redirects user to EGI Check-In for authentication"""
        redirect_uri = 'https://' + self.hostname + '/oidc-redirect'
        return self.oauth._clients["eosc-perf"].authorize_redirect(redirect_uri)

    def authentication_redirect(self):
        """Validates user authentication after login through EGI Check-In"""
        if self.is_authenticated():
            return info_redirect('Logged in successfully')
        return error_redirect('Login failed')

    def is_authenticated(self):
        """Checks if the current user is authenticated. Will return true
           if the user just logged in through EGI Check-In or if the user
           still has a token that is not expired."""
        if not self._token_expired():
            return True
        try:
            token = self.oauth._clients['eosc-perf'].authorize_access_token()
            user = self.oauth._clients['eosc-perf'].parse_id_token(token)
            userinfo = self.oauth._clients['eosc-perf'].userinfo()
            session['user'] = user
            session['user']['token'] = token
            session['user']['info'] = userinfo
            self.__update_user_info()
        except KeyError:
            return False
        return True

    def is_admin(self):
        """Checks wether the current user has admin rights"""
        try:
            affiliations = session['user']['info']['edu_person_scoped_affiliations']
        except KeyError:
            return False
        return any(aff in affiliations for aff in self.admin_affiliations)

    def logout(self):
        """Signs out the current user"""
        try:
            token = session['user']['info']
        except KeyError:
            return False
        endpoint = json.loads(urlopen(CONF_URL).read())["revocation_endpoint"]
        requests.post(
            endpoint,
            params={'token': token},
            headers={'content-type': 'application/x-www-form-urlencoded'})
        session.pop('user', None)
        return True

    def _refresh_token(self):
        """Tries to refresh token of current user.
           Returns True if refresh succeeds, False otherwise."""
        endpoint = json.loads(urlopen(CONF_URL).read())["token_endpoint"]
        try:
            refresh_token = session['user']['token']['refresh_token']
        except KeyError:
            self.logout()
            return False
        response = requests.post(
            endpoint,
            params={'client_id': "eosc-perf",
                    'client_secret': self.client_secret,
                    'grant_type': "refresh_token",
                    'refresh_token': refresh_token,
                    'scope': self.scope},
            headers={'content-type': 'application/x-www-form-urlencoded'})
        new_token = response.json()
        user = self.oauth._clients['eosc-perf'].parse_id_token(new_token)
        user['info'] = session['user']['info']
        user['token'] = new_token
        session['user'] = user
        return response.status_code == 200

    def _token_expired(self):
        """Checks if the current user has a valid authentication token"""
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
    def __update_user_info():
        """If current user is in db, saved email and name are updated"""
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

authenticator_blueprint = Blueprint('authenticator', __name__)

def configure_authenticator(app):
    """Configures the authenticator for given app and config"""
    authenticator.configure_authenticator(app)

@authenticator_blueprint.route('/login')
def authenticate_user():
    """"Authenticates user through authenticator singleton"""
    return authenticator.authenticate_user()

@authenticator_blueprint.route('/oidc-redirect')
def authentication_redirect():
    """"OIDC-Authentication redirect through authenticator singleton"""
    return authenticator.authentication_redirect()

@authenticator_blueprint.route('/logout')
def logout():
    """"Revoke current user's authentication"""
    if authenticator.logout():
        return info_redirect('Logged out')
    else:
        return info_redirect('There is no authenticated user to log out.')
