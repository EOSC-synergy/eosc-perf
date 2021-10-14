"""This module acts as a facade between view and model."""
from typing import Optional, Callable, Any

from flask import redirect, Response

from .authenticator import AuthenticateError, Authenticator, MockAuthenticator


def _only_authenticated(message: str = "Not authenticated.") -> Callable[..., Any]:
    """Decorator helper for authentication.

    Args:
        message (str): Message to return if the user is not authenticated.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(self, *args, **kwargs) -> Callable[..., Any]:
            # use self because controller is not declared yet
            if not self.is_authenticated():
                raise AuthenticateError(message)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def _only_admin(function: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator helper for authentication.
    """

    def wrapper(self, *args, **kwargs) -> Callable[..., Any]:
        if not self.is_admin():
            raise AuthenticateError("Not an administrator.")
        return function(self, *args, **kwargs)

    return wrapper


class IOController:
    """This class acts as a middleman between view and model for actions that require input validation or
    authentication. This generally implies submitting new data or getting data exclusive to administrators.
    """

    def __init__(self):
        """Constructor: create a new instance of IOController."""
        self._authenticator: MockAuthenticator = MockAuthenticator()

    def load_authenticator(self, app):
        self._authenticator = Authenticator(app)

    def authenticate(self) -> Optional[Response]:
        """Authenticate the current user. Redirects user to '/login' which again redirects the user to EGI Check-In
        for authentication.

        Returns:
            Optional[Response]: A redirect to the login page, if necessary.
        """
        if not self.is_authenticated():
            return redirect('/login')

    @property
    def authenticator(self) -> MockAuthenticator:
        return self._authenticator

    def is_admin(self) -> bool:
        """Checks if current user has admin right, if one is logged on.

        Returns:
            bool: True if current user is admin.
        """
        return self._authenticator.is_admin()

    def is_authenticated(self) -> bool:
        """Check if the current user is authenticated.

        Returns:
            bool: True if the user is authenticated.
        """
        return self._authenticator.is_authenticated()


controller = IOController()
