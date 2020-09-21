"""This module contains the factory to generate the Upload instructions
Provided is:
 - UploadInstructionFactory
"""

from flask import Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

class UploadInstructionFactory(PageFactory):
    """A factory to build privacy policy pages."""

    def __init__(self):
        super(UploadInstructionFactory, self).__init__()
        with open('templates/upload_instruction.html') as file:
            self.set_template(file.read())

    def _generate_content(self, args: JSON) -> HTML:
        pass

upload_instructions_blueprint = Blueprint('upload-instructions-factory', __name__)

@upload_instructions_blueprint.route('/instructions')
def privacy_page():
    """HTTP endpoint for the upload instructions page."""
    print("============================================yay")
    factory = UploadInstructionFactory()
    return Response(factory.generate_page('{}'), mimetype='text/html')
