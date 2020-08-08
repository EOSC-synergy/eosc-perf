'''This module acts as a facade between the IOController
and the EGI Check-In authentication system'''

from time import time

from flask import url_for, redirect, session
from authlib.integrations.flask_client import OAuth

CONF_URL = "https://aai-dev.egi.eu/oidc/.well-known/openid-configuration"

def authenticator(app):
    """Sets up OIDC authentication functionality for the web app"""

    app.secret_key = '!secret'
    app.config["EOSC-PERF_CLIENT_ID"] = "eosc-perf"
    app.config["EOSC-PERF_CLIENT_SECRET"] = "UV0xI-uY9Hd-Z12Nc9gGNvajwpHdXtiYPAAbqASfsWqR9esSGj3jRZkLZO0-ndfoHAgYSEUD-OM5wivNwCIXyw"

    oauth = OAuth(app)
    oauth.register(
        name="eosc-perf",
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        },
        secret="UV0xI-uY9Hd-Z12Nc9gGNvajwpHdXtiYPAAbqASfsWqR9esSGj3jRZkLZO0-ndfoHAgYSEUD-OM5wivNwCIXyw"
    )

    @app.route('/login')
    def authenticate_user():
        """Redirects user to EGI Check-In for authentication"""
        redirect_uri = "https://localhost" + url_for('authentication_redirect', _external=False)
        return oauth._clients["eosc-perf"].authorize_redirect(redirect_uri)

    @app.route('/oidc-redirect')
    def authentication_redirect():
        """Validates user authentication after login through EGI Check-In"""
        if is_authenticated():
            return "Logged in successfully"
        else:
            return "Login failed"

    def is_authenticated():
        """Checks if the current user is authenticated. Will return true
           if the user just logged in through EGI Check-In or if the user
           still has a token that is not expired."""
        if not __token_expired():
            return True
        try:
            token = oauth._clients["eosc-perf"].authorize_access_token()
            user = oauth._clients["eosc-perf"].parse_id_token(token)
            session['user'] = user
        except KeyError:
            return False
        return True

    def sign_out():
        """Signs out the current user"""
        session.pop('user', None)
        return redirect('/')

    def __token_expired():
        """Checks if the current user has a non-expired authentication token"""
        try:
            user = session['user']
            print(user)
            return user['exp'] < time()
        except KeyError:
            return True

    def is_admin():
        """Checks wether the current user has admin rights"""
        # TODO: implement
        return False
