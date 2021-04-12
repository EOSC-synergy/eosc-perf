# -*- coding: utf-8 -*-
"""Authorization module."""
# Simplify code when Authlib V1.0 using https://docs.authlib.org/en/latest/specs/rfc7662.html#use-introspection-in-resource-server

from .extensions import flaat
from .settings import Configuration


flaat.set_web_framework('flask')
flaat.set_cache_lifetime(120)  # seconds; default is 300
flaat.set_trusted_OP_list([
    'https://aai-dev.egi.eu/oidc'
])
# flaat.set_trusted_OP_file('/etc/oidc-agent/issuer.config')
# flaat.set_OP_hint("helmholtz")
# flaat.set_OP_hint("google")
flaat.set_timeout(3)


# verbosity:
#     0: No output
#     1: Errors
#     2: More info, including token info
#     3: Max
flaat.set_verbosity(0)
# flaat.set_verify_tls(True)


# Required for using token introspection endpoint:
flaat.set_client_id(Configuration.EGI_CLIENT_ID)
flaat.set_client_secret(Configuration.EGI_CLIENT_SECRET)


# Decorators collected from flaat
group_required = flaat.group_required
login_required = flaat.login_required

def admin_required(**kwargs):
    """Decorator to define admin requirements"""
    return group_required(
        group=[Configuration.ADMIN_ASSURANCE],
        claim='eduperson_assurance', **kwargs)
