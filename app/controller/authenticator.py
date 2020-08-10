'''This module acts as a facade between the IOController
and the EGI Check-In authentication system.
Provided is:
 - Authenticator'''

from time import time

from flask import redirect, session
from flask.blueprints import Blueprint
from authlib.integrations.flask_client import OAuth
from ..model.facade import facade
from ..view.pages.helpers import info_redirect, error_redirect

CONF_URL = 'https://aai-dev.egi.eu/oidc/.well-known/openid-configuration'

class AuthenticateError(Exception):
    """Exception to signal a user isn't authenticated correctly."""
    pass

class Authenticator:
    """A fascade between IOController and the EGI Check-In authentication
       system. It integrates Open ID Connect into the web app."""

    def __init__(self):
        self.oauth = None
        self.admin_affiliations = []

    def configure_authenticator(self, flask_app, config):
        """Sets up OIDC authentication functionality for the web app"""
        if len(config['oidc_client_secret']) == 0:
            raise ValueError("missing openID client secret in configuration")
        client_secret = config['oidc_client_secret']

        flask_app.secret_key = '!secret'
        flask_app.config["EOSC-PERF_CLIENT_ID"] = 'eosc-perf'
        flask_app.config["EOSC-PERF_CLIENT_SECRET"] = client_secret

        self.oauth = OAuth(flask_app)
        self.oauth.register(
            name='eosc-perf',
            userinfo_endpoint='https://aai-dev.egi.eu/oidc/userinfo',
            server_metadata_url=CONF_URL,
            client_kwargs={
                'scope': 'openid email profile eduperson_scoped_affiliation'
            },
            secret=client_secret
        )
        if config['debug']:
            self.admin_affiliations = config['debug_admin_affiliations']
        else:
            self.admin_affiliations = config['admin_affiliations']

    def authenticate_user(self):
        """Redirects user to EGI Check-In for authentication"""
        redirect_uri = 'https://localhost/oidc-redirect'
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

    @staticmethod
    def _token_expired():
        """Checks if the current user has a valid authentication token"""
        try:
            user = session['user']
        except KeyError:
            return True
        return user['exp'] < time()

    @staticmethod
    def sign_out():
        """Signs out the current user"""
        session.pop('user', None)
        return redirect('/')

# single global instance
authenticator = Authenticator()
authenticator_blueprint = Blueprint('authenticator', __name__)

def configure_authenticator(app, config):
    """Configures the authenticator for given app and config"""
    authenticator.configure_authenticator(app, config)

@authenticator_blueprint.route('/login')
def authenticate_user():
    """"Authenticates user through authenticator singleton"""
    return authenticator.authenticate_user()

@authenticator_blueprint.route('/oidc-redirect')
def authentication_redirect():
    """"OIDC-Authentication redirect through authenticator singleton"""
    return authenticator.authentication_redirect()
