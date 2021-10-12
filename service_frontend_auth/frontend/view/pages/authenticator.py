"""This submodule contains endpoints for authentication redirections.

Exposed endpoints:
 - /login - Authorization redirect for login.
 - /oidc-redirect - Return endpoint after the identity provider authenticated the user.
 - /whoami - Get information about current user
 - /logout - Endpoint to log out the user.
"""

import json

from flask import Blueprint, Response, redirect
from frontend.controller.io_controller import controller

authenticator_blueprint = Blueprint('authenticator', __name__)


@authenticator_blueprint.route('/auth/login')
def authenticate_user():
    """"Authenticates user through authenticator singleton."""
    return controller.authenticator.redirect_to_authentication()


@authenticator_blueprint.route('/auth/oidc-redirect')
def authentication_redirect():
    """"OIDC-Authentication redirect through authenticator singleton."""
    if controller.is_authenticated():
        # TODO: return to where you were?
        return redirect("/", code=302)

    return Response("{}", mimetype='application/json', status=401)


@authenticator_blueprint.route('/auth/whoami')
def who_am_i():
    """"""
    data = controller.authenticator.get_user_info()
    if data is None:
        return Response("{}", mimetype="application/json", status=404)
    return Response(json.dumps(data), mimetype='application/json')


@authenticator_blueprint.route('/auth/logout')
def logout():
    """"Revoke current user's authentication."""
    controller.authenticator.logout()
    return Response("{}", mimetype='application/json', status=204)
