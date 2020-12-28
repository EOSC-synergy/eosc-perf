from flask import Blueprint

from eosc_perf.controller.authenticator import authenticator
from eosc_perf.view.pages.helpers import info_redirect, error_redirect

authenticator_blueprint = Blueprint('authenticator', __name__)


def configure_authenticator(app):
    """Configures the authenticator for given app and config."""
    authenticator.configure_authenticator(app)


@authenticator_blueprint.route('/login')
def authenticate_user():
    """"Authenticates user through authenticator singleton."""
    return authenticator.authenticate_user()


@authenticator_blueprint.route('/oidc-redirect')
def authentication_redirect():
    """"OIDC-Authentication redirect through authenticator singleton."""
    if authenticator.is_authenticated():
        return info_redirect('Logged in successfully')
    return error_redirect('Login failed')


@authenticator_blueprint.route('/logout')
def logout():
    """"Revoke current user's authentication."""
    if authenticator.logout():
        return info_redirect('Logged out')
    else:
        return info_redirect('There is no authenticated user to log out.')

