
USER = str
"""Representation of a user to be authenticated or 
performing actions requiering authentication."""
JSON = str
"""Representation of a json formated string."""
class AuthenticateError(Exception):
        """Exception to signal a user isn't authenticated correctly."""
        pass