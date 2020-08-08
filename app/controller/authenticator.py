'''This module acts as a facade between the IOController
and the EGI Check-In authentication system.
Provided is:
 - Authenticator'''

from time import time

from flask import url_for, redirect, session
from authlib.integrations.flask_client import OAuth

CONF_URL = "https://aai-dev.egi.eu/oidc/.well-known/openid-configuration"

class Authenticator:
    """A fascade between IOController and the EGI Check-In authentication 
       system. It integrates Open ID Connect into the web app."""

    def __init__(self):
        self.oauth = None

    def configure_authenticator(self, flask_app):
        """Sets up OIDC authentication functionality for the web app"""

        flask_app.secret_key = '!secret'
        flask_app.config["EOSC-PERF_CLIENT_ID"] = "eosc-perf"
        flask_app.config["EOSC-PERF_CLIENT_SECRET"] = "UV0xI-uY9Hd-Z12Nc9gGNvajwpHdXtiYPAAbqASfsWqR9esSGj3jRZkLZO0-ndfoHAgYSEUD-OM5wivNwCIXyw"

        self.oauth = OAuth(flask_app)
        self.oauth.register(
            name="eosc-perf",
            server_metadata_url=CONF_URL,
            client_kwargs={
                'scope': 'openid email profile'
            },
            secret="UV0xI-uY9Hd-Z12Nc9gGNvajwpHdXtiYPAAbqASfsWqR9esSGj3jRZkLZO0-ndfoHAgYSEUD-OM5wivNwCIXyw"
        )

    def authenticate_user(self, redirect_uri):
        """Redirects user to EGI Check-In for authentication"""
        return self.oauth._clients["eosc-perf"].authorize_redirect(redirect_uri)

    def authentication_redirect(self):
        """Validates user authentication after login through EGI Check-In"""
        if self.is_authenticated():
            return "Logged in successfully"
        else:
            return "Login failed"

    def is_authenticated(self):
        """Checks if the current user is authenticated. Will return true
           if the user just logged in through EGI Check-In or if the user
           still has a token that is not expired."""
        if not self.__token_expired():
            return True
        try:
            token = self.oauth._clients["eosc-perf"].authorize_access_token()
            user = self.oauth._clients["eosc-perf"].parse_id_token(token)
            session['user'] = user
        except KeyError:
            return False
        return True

    def sign_out(self):
        """Signs out the current user"""
        session.pop('user', None)
        return redirect('/')

    def __token_expired(self):
        """Checks if the current user has a valid authentication token"""
        try:
            user = session['user']
            print(user)
            return user['exp'] < time()
        except KeyError:
            return True

    def is_admin(self):
        """Checks wether the current user has admin rights"""
        # TODO: implement
        return False

# single global instance
authenticator = Authenticator()

def configure_authenticator(app):
    authenticator.configure_authenticator(app)

    @app.route("/login")
    def authenticate_user():
        redirect_uri = "https://localhost" \
                       + url_for('authentication_redirect', _external=False)
        return authenticator.authenticate_user(redirect_uri)

    @app.route("/oidc-redirect")
    def authentication_redirect():
        return authenticator.authentication_redirect()