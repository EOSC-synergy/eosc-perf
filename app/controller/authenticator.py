'''This module acts as a facade between the IOController
and the EGI Check-In authentication system'''

from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth

DEFAULT_AUTH_URL = ""
CONF_URL = "https://aai-dev.egi.eu/oidc/.well-known/openid-configuration"

def authenticator(app):
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
        redirect_uri = "https://localhost" + url_for('is_authenticated', _external=False)
        return oauth._clients["eosc-perf"].authorize_redirect(redirect_uri)

    @app.route('/oidc-redirect')
    def is_authenticated():
        token = oauth._clients["eosc-perf"].authorize_access_token()
        user = oauth._clients["eosc-perf"].parse_id_token(token)
        session['user'] = user
        return redirect('/')

    def sign_out(self):
        session.pop('user', None)
        return redirect('/')

    def is_admin(self):
        # TODO: implement
        return False

    def get_auth_url(self):
        return self.auth_url

    def _set_token(self):
        # TODO: implement
        self.token = None

    def _val_token(self):
        # TODO: implement
        return False
