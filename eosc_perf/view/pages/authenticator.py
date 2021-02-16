from typing import Any, Dict, Tuple

from flask import Blueprint, Response

from eosc_perf.controller.authenticator import authenticator
from eosc_perf.utility.type_aliases import HTML
from eosc_perf.view.page_factory import PageFactory
from eosc_perf.view.pages.helpers import info_redirect, error_redirect

authenticator_blueprint = Blueprint('authenticator', __name__)


class RedirectFactory(PageFactory):
    """A factory to build the page redirecting to a url in cache."""

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return args, {}


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
        factory = RedirectFactory()
        page = factory.generate_page(template='redirect_return.html')
        return Response(page, mimetype='text/html')

    return error_redirect('Login failed')


@authenticator_blueprint.route('/logout')
def logout():
    """"Revoke current user's authentication."""
    if authenticator.logout():
        factory = RedirectFactory()
        page = factory.generate_page(template='redirect_return.html')
        return Response(page, mimetype='text/html')
    else:
        return info_redirect('There is no authenticated user to log out.')
