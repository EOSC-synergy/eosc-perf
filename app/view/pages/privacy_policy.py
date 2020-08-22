"""This module contains the factory to generate the privacy policy page.
Provided is:
 - PrivacyPolicyFactory
"""

from flask import Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

class PrivacyPolicyFactory(PageFactory):
    """A factory to build privacy policy pages."""

    def __init__(self):
        super(PrivacyPolicyFactory, self).__init__()
        with open('templates/privacy_policy.html') as file:
            self.set_template(file.read())

    def _generate_content(self, args: JSON) -> HTML:
        pass

privacy_blueprint = Blueprint('privacy-policy-factory', __name__)

@privacy_blueprint.route('/privacy')
def privacy_page():
    """HTTP endpoint for the privacy policy page"""
    factory = PrivacyPolicyFactory()
    return Response(factory.generate_page('{}'), mimetype='text/html')
