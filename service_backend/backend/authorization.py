"""Authorization module."""
# Simplify code when Authlib V1.0 using:
# https://docs.authlib.org/en/latest/specs/rfc7662.html
#   #use-introspection-in-resource-server

from functools import wraps

from flaat import Flaat, tokentools
from flask import current_app, request
from flask_smorest import abort

from . import models


class Authorization(Flaat):
    """Monkeypatch flaat to solve lazy configuration
    https://github.com/indigo-dc/flaat/issues/32

    For more information see:
    https://flask.palletsprojects.com/en/2.0.x/extensiondev/#the-extension-code
    """

    def __init__(self, app=None):
        self.app = app
        self.admin_entitlements = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        super().__init__()

        self.set_web_framework('flask')
        self.set_trusted_OP_list([
            'https://aai-dev.egi.eu/oidc'
        ])

        # Flaat timeout:
        timeout = app.config.get('FLAAT_TIMEOUT', 3)
        self.set_timeout(timeout)

        # verbosity:
        #     0: No output
        #     1: Errors
        #     2: More info, including token info
        #     3: Max
        verbosity = app.config.get('FLAAT_VERBOSITY', 0)
        self.set_verbosity(verbosity)

        # TLS verification:
        verify_tls = app.config.get('VERIFY_TLS', False)
        self.set_verify_tls(verify_tls)

        # Required for using token introspection endpoint:
        client_id = app.config['OIDC_CLIENT_ID']
        self.set_client_id(client_id)

        client_secret = app.config['OIDC_CLIENT_SECRET']
        self.set_client_secret(client_secret)

        admin_entitlements = app.config['ADMIN_ENTITLEMENTS']
        self.admin_entitlements = admin_entitlements

    def current_tokeninfo(self):
        """Returns the token information from the current request.

        :return: Token information.
        :rtype: dict or None
        """
        token = tokentools.get_access_token_from_request(request)
        info = tokentools.get_accesstoken_info(token)
        return info['body'] if 'body' in info else None

    def current_userinfo(self):
        """Returns the token user info from the introspection endpoint.

        :return: User introspection endpoint information.
        :rtype: dict or None
        """
        token = tokentools.get_access_token_from_request(request)
        user_info = self.get_info_from_introspection_endpoints(token)
        return user_info

    def valid_token(self):
        """Function to evaluate the validity of the user login"""
        try:
            all_info = self._get_all_info_from_request(request)
            current_app.logger.debug(f"request info: {all_info}")
            return all_info is not None

        except Exception as e:
            current_app.logger.error('Error validating user', exc_info=e)
            return False

    def token_required(self, on_failure=None):
        """Decorator to enforce a valid login.
        Optional on_failure is called if no valid user detected.
        Useful for redirecting to some login page"""
        def wrapper(view_func):
            @wraps(view_func)
            def decorated(*args, **kwargs):
                if self.valid_token():
                    current_app.logger.debug("Token accepted")
                    return self._wrap_async_call(view_func, *args, **kwargs)
                elif on_failure:
                    failure = on_failure(self.get_last_error())
                    return self._return_formatter_wf(failure, 401)
                else:
                    alert = f"No valid authentication: {self.get_last_error()}"
                    abort(401, message=alert)
            return decorated
        return wrapper

    def valid_user(self):
        """Function to evaluate the validity of the user login"""
        user = models.User.current_user()
        if not user:
            current_app.logger.error("User not registered")
            return False
        else:
            current_app.logger.debug(f"User info: {user}")
            return True

    def login_required(self, on_failure=None):
        """Decorator to enforce a valid login.
        Optional on_failure is called if no valid user detected.
        Useful for redirecting to some login page"""
        def wrapper(view_func):
            @wraps(view_func)
            def decorated(*args, **kwargs):
                if self.valid_user():
                    current_app.logger.debug("User accepted")
                    return self._wrap_async_call(view_func, *args, **kwargs)
                elif on_failure:
                    failure = on_failure(self.get_last_error())
                    return self._return_formatter_wf(failure, 403)
                else:
                    abort(403, messages={'user': "Not registered"})
            return self.token_required()(decorated)
        return wrapper

    def valid_admin(self, match='all'):
        """Function to evaluate the validity of the user as admin"""
        if current_app.config['DISABLE_ADMIN_PROTECTION']:
            current_app.logger.warning("ADMIN validation is disabled")
            return True

        try:
            claim = 'eduperson_assurance'
            all_info = self._get_all_info_from_request(request)
            current_app.logger.debug(f"request info: {all_info}")

            group = self.admin_entitlements
            req_glist = group if isinstance(group, list) else [group]

            # copy entries from incoming claim
            (g_entries, user_msg) = self._get_entitlements_from_claim(
                all_info, claim)
            if not g_entries:
                raise Exception(user_msg)

            required = self._determine_number_of_required_matches(
                match, req_glist)
            if not required:
                raise Exception("Error interpreting 'match' parameter")

            # now we do the actual checking
            matches = 0
            for entry in g_entries:
                for g in req_glist:
                    if entry == g:
                        matches += 1
            current_app.logger.debug(f"found {matches} of {required} matches")
            return matches >= required

        except Exception as e:
            current_app.logger.error('Error validating admin', exc_info=e)
            return False

    def admin_required(self, on_failure=None):
        """Decorator to enforce a valid admin.
        Optional on_failure is called if no valid admin detected.
        Useful for redirecting to some login page"""
        def wrapper(view_func):
            @wraps(view_func)
            def decorated(*args, **kwargs):
                if self.valid_admin():
                    current_app.logger.debug("Admin accepted")
                    return self._wrap_async_call(view_func, *args, **kwargs)
                elif on_failure:
                    alert = 'You are not authorized'
                    return self._return_formatter_wf(on_failure(alert), 403)
                else:
                    alert = 'You are not authorized'
                    return self._return_formatter_wf(alert, 403)
            return self.login_required()(decorated)
        return wrapper
