'''This module acts as a facade between the IOController
and the EGI Check-In authentication system.
Provided is:
 - Authenticator'''

from time import time

from flask import redirect, session
from authlib.integrations.flask_client import OAuth

CONF_URL = 'https://aai-dev.egi.eu/oidc/.well-known/openid-configuration'

class Authenticator:
    """A fascade between IOController and the EGI Check-In authentication
       system. It integrates Open ID Connect into the web app."""

    def __init__(self):
        self.oauth = None

    def configure_authenticator(self, flask_app, config):
        """Sets up OIDC authentication functionality for the web app"""
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
                'scope': 'openid email profile'
            },
            secret=client_secret
        )

    def authenticate_user(self):
        """Redirects user to EGI Check-In for authentication"""
        redirect_uri = 'https://localhost/oidc-redirect'
        return self.oauth._clients["eosc-perf"].authorize_redirect(redirect_uri)

    def authentication_redirect(self):
        """Validates user authentication after login through EGI Check-In"""
        if self.is_authenticated():
            return 'Logged in successfully'
        return 'Login failed'

    def is_authenticated(self):
        """Checks if the current user is authenticated. Will return true
           if the user just logged in through EGI Check-In or if the user
           still has a token that is not expired."""
        if not self.__token_expired():
            return True
        try:
            token = self.oauth._clients['eosc-perf'].authorize_access_token()
            user = self.oauth._clients['eosc-perf'].parse_id_token(token)
            userinfo = self.oauth._clients['eosc-perf'].userinfo()
            session['user'] = user
            session['mail'] = userinfo['email']
        except KeyError:
            return False
        return True

    def get_email(self):
        """Returns the email address of the current user.
           If no user is logged in, an empty string is returned"""
        if not self.__token_expired():
            return session['mail']
        return ""

    def is_admin(self):
        """Checks wether the current user has admin rights"""
        # TODO: implement
        return False


def __token_expired():
    """Checks if the current user has a valid authentication token"""
    try:
        user = session['user']
    except KeyError:
        return True
    return user['exp'] < time()


def sign_out():
    """Signs out the current user"""
    session.pop('user', None)
    return redirect('/')

# single global instance
authenticator = Authenticator()

def configure_authenticator(app, config):
    authenticator.configure_authenticator(app, config)

    @app.route('/login')
    def authenticate_user():
        return authenticator.authenticate_user()

    @app.route('/oidc-redirect')
    def authentication_redirect():
        return authenticator.authentication_redirect()
