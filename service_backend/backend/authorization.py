"""Authorization module."""
# Simplify code when Authlib V1.0 using https://docs.authlib.org/en/latest/specs/rfc7662.html#use-introspection-in-resource-server

from functools import wraps
from flaat import Flaat
from flask import current_app, request


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
        self.set_cache_lifetime(120)  # seconds; default is 300
        self.set_trusted_OP_list([
            'https://aai-dev.egi.eu/oidc'
        ])

        # flaat.set_trusted_OP_file('/etc/oidc-agent/issuer.config')
        # flaat.set_OP_hint("helmholtz")
        # flaat.set_OP_hint("google")
        self.set_timeout(3)

        # verbosity:
        #     0: No output
        #     1: Errors
        #     2: More info, including token info
        #     3: Max
        self.set_verbosity(0)
        # flaat.set_verify_tls(True)

        # Required for using token introspection endpoint:
        client_id = app.config['EGI_CLIENT_ID']
        self.set_client_id(client_id)

        client_secret = app.config['EGI_CLIENT_SECRET']
        self.set_client_secret(client_secret)

        admin_entitlements = app.config['ADMIN_ENTITLEMENTS']
        self.admin_entitlements = admin_entitlements

    def valid_user(self):
        """Function to evaluate the validity of the user login"""
        if current_app.config['DISABLE_AUTHENTICATION']:
            current_app.logger.warning(f"AUTHENTICATION is disabled")
            return True

        try:
            all_info = self._get_all_info_from_request(request)
            current_app.logger.debug(f"request info: {all_info}")
            return all_info is not None

        except Exception as e:
            current_app.logger.error('Error validating user', exc_info=e)
            return False

    def login_required(self, on_failure=None):
        """Decorator to enforce a valid login.
        Optional on_failure is a function that will be invoked if there was no valid user detected.
        Useful for redirecting to some login page"""
        def wrapper(view_func):
            @wraps(view_func)
            def decorated(*args, **kwargs):
                if self.valid_user():
                    current_app.logger.debug(f"User accepted")
                    return self._wrap_async_call(view_func, *args, **kwargs)
                elif on_failure:
                    return self._return_formatter_wf(on_failure(self.get_last_error()), 401)
                else:
                    alert = f"No valid authentication: {self.get_last_error()}"
                    return self._return_formatter_wf(alert, 401)
            return decorated
        return wrapper

    def valid_admin(self, match='all'):
        """Function to evaluate the validity of the user as admin"""
        if current_app.config['DISABLE_ADMIN_PROTECTION']:
            current_app.logger.warning(f"ADMIN validation is disabled")
            return True

        try:
            claim = 'eduperson_assurance'
            all_info = self._get_all_info_from_request(request)
            current_app.logger.debug(f"request info: {all_info}")

            group = self.admin_entitlements
            req_group_list = group if isinstance(group, list) else [group]

            # copy entries from incoming claim
            (avail_group_entries, user_message) = self._get_entitlements_from_claim(
                all_info, claim)
            if not avail_group_entries:
                raise Exception(user_message)

            required = self._determine_number_of_required_matches(
                match, req_group_list)
            if not required:
                raise Exception("Error interpreting 'match' parameter")

            # now we do the actual checking
            matches = 0
            for entry in avail_group_entries:
                for g in req_group_list:
                    if entry == g:
                        matches += 1
            current_app.logger.debug(f"found {matches} of {required} matches")
            return matches >= required

        except Exception as e:
            current_app.logger.error('Error validating admin', exc_info=e)
            return False

    def admin_required(self, on_failure=None):
        """Decorator to enforce a valid admin.
        on_failure is a function that will be invoked if there was no valid user detected.
        Useful for redirecting to some login page"""
        def wrapper(view_func):
            @wraps(view_func)
            def decorated(*args, **kwargs):
                if self.valid_admin():
                    current_app.logger.debug(f"Admin accepted")
                    return self._wrap_async_call(view_func, *args, **kwargs)
                elif on_failure:
                    alert = 'You are not authorized'
                    return self._return_formatter_wf(on_failure(alert), 403)
                else:
                    alert = 'You are not authorized'
                    return self._return_formatter_wf(alert, 403)
            return self.login_required()(decorated)
        return wrapper
