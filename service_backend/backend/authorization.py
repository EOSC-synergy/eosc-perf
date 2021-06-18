"""Authorization module."""
# Simplify code when Authlib V1.0 using https://docs.authlib.org/en/latest/specs/rfc7662.html#use-introspection-in-resource-server

from .extensions import flaat


# Decorators collected from flaat
def group_required(*args, **kwargs):
    return flaat.group_required(*args, **kwargs)


def login_required(*args, **kwargs):
    return flaat.login_required(*args, **kwargs)


def admin_required(**kwargs):
    """Decorator to define admin requirements"""
    return group_required(
        group=[flaat.admin_assurance],
        claim='eduperson_assurance', **kwargs)
