"""This module contains the factroyclasses generating the HTMLpages.
    Provided are:
        -
    
"""
import jinja2 as jj
from os.path import isfile
from .type_aliases import HTML, JSON

class PageFactory:

    """The PageFactory abstract class serves as a generator for pages.
    Members
    ------
    environment: jinja2.Environment
        the environment to handel thc combination of the final html file.
    """
    environment: jj.Environment

    def __init__(self):
        """constructor initials the enviroment."""
        environment = jj.Environment(
            loader=jj.FileSystemLoader('templates/'),
            autoescape=jj.select_autoescape(['html', 'xml'])
        )
        template = None
        pass

    def generate_page(self, args: JSON, template: HTML = None, info: str = None) -> HTML:
        """generate a HTML page from the inputparameters not using the template provided in the class.
        Parameters
        ------
        args: JSON
            Parameters used by some childclasses to generate the right content.
        template: HTML
            A template can be used instead of the default should contain variables for content and info,
            doesn't change the template lasting,
            can be left empty.
        info: str
            Information displayed on the returned HTML page # todo may contain extra html formating,
            doesn't change the info lasting,
            can be left empty.
        Returns
        ------
        : HTML
            The finished HTML page displaying the content and information.
        """

        if not template is None:
            # todo
            a = 1
        if not info is None:
            # todo
            a=2
        
        # todo
        return ""
    
    def _generate_content(self, args: JSON) -> HTML:
        """(abstract) patten function to generate the content of a given page.
        Parameters
        ------
        args: JSON
            Parameters used by some childclasses to generate the right content.
        """
        return

    def set_template(self, template: HTML):
        """change the default template to the input template.
        Parameters
        ------
        template: HTML
            The new template for this instance of PageFactory.
            Eather template as String or the filepath in view/template/s."""
        if isfile("template/"+template):
            self.template = self.environment.get_template(template)
        else:
            self.template = self.environment.from_string(template)
        pass

    def set_content(self, content: str):
        """set the content to the input content.
        Parameters
        ------
        content: str 
            New content for this instance of PageFactory"""
        # todo
        pass

    def set_info(self, info: str):
        """(abstract) change the default info into the input info.
        Parameters
        ------
        info: str
            The new info of this instance of PageFactory, may contain HTML formating."""
        # todo
        pass
