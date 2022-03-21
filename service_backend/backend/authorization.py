"""Authorization module."""
# Simplify code when Authlib V1.0 using:
# https://docs.authlib.org/en/latest/specs/rfc7662.html
#   #use-introspection-in-resource-server

from typing import Optional

from flaat.flask import Flaat
from flaat.requirements import HasAARCEntitlement
from flaat.user_infos import UserInfos
from flask import Flask
from flask_smorest import abort

from . import models

class Authorization(Flaat):
    """Monkeypatch flaat to solve lazy configuration
    https://github.com/indigo-dc/flaat/issues/32

    For more information see:
    https://flask.palletsprojects.com/en/2.0.x/extensiondev/#the-extension-code
    """

    def __init__(self, app=None):
        self.app: Optional[Flask] = app
        self.admin_entitlements: list = []
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        super().__init__()
        self.app = app

        self.set_trusted_OP_list(
            [
                "https://aai.egi.eu/oidc",
                "https://aai-demo.egi.eu/oidc",
                "https://aai-dev.egi.eu/oidc",
            ]
        )

        # Flaat timeout:
        timeout = app.config.get("FLAAT_TIMEOUT", 3)
        self.set_timeout(timeout)

        # verbosity:
        #     0: No output
        #     1: Errors
        #     2: More info, including token info
        #     3: Max
        verbosity = app.config.get("FLAAT_VERBOSITY", 0)
        self.set_verbosity(verbosity)

        # Required for using token introspection endpoint:
        client_id = app.config["OIDC_CLIENT_ID"]
        self.set_client_id(client_id)

        client_secret = app.config["OIDC_CLIENT_SECRET"]
        self.set_client_secret(client_secret)

        admin_entitlements = app.config["ADMIN_ENTITLEMENTS"]
        self.admin_entitlements = admin_entitlements

    def _requirement_auth_disabled(self):
        disabled = super()._requirement_auth_disabled()
        if self.app is not None:
            disabled = disabled or self.app.config["DISABLE_ADMIN_PROTECTION"]
        return disabled

    def get_admin_requirement(self):
        return HasAARCEntitlement(
            required=self.admin_entitlements, claim="eduperson_entitlement"
        )

    def admin_required(self, on_failure=None):
        """make view_func only available for admin users"""
        # the requirement is loaded lazily, so we can set eduperson_entitlements at runtime
        return self.requires(self.get_admin_requirement, on_failure=on_failure)

    def inject_object(self):
        """ inject kwarg "user" with the current user into a view function"""
        def _get_user(user_infos: UserInfos) -> models.User:
            user = models.User.get_user(user_infos)
            if user is None:
                error_msg = "User not registered"
                abort(401, messages={'error': error_msg})
            return user

        return super().inject_object(infos_to_user=_get_user, key="user")

    def inject_is_admin(self):
        """ inject boolean kwarg "is_admin" into a view function
        If no user info is available the view func will not be evaluated.
        """
        def _is_admin(user_infos: UserInfos):
            return self.get_admin_requirement().is_satisfied_by(user_infos)

        return super().inject_object(infos_to_user=_is_admin, key="is_admin", strict=True)
