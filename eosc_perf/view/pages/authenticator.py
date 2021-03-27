"""This submodule contains endpoints for authentication redirections.

Exposed endpoints:
    /login         - Authorization redirect for login.
    /oidc-redirect - Return endpoint after the identity provider authenticated the user.
    /logout        - Endpoint to log out the user.
"""

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


@authenticator_blueprint.route('/login')
def authenticate_user():
    """"Authenticates user through authenticator singleton."""
    return authenticator.redirect_to_authentication()


@authenticator_blueprint.route('/oidc-redirect')
def authentication_redirect():
    """"OIDC-Authentication redirect through authenticator singleton."""
    if authenticator.is_authenticated():
        factory = RedirectFactory()
        page = factory.generate_page(template='redirect_return.jinja2.html')
        return Response(page, mimetype='text/html')

    return error_redirect('Login failed')


@authenticator_blueprint.route('/logout')
def logout():
    """"Revoke current user's authentication."""
    authenticator.logout()
    factory = RedirectFactory()
    page = factory.generate_page(template='redirect_return.jinja2.html')
    return Response(page, mimetype='text/html')
