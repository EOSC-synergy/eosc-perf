"""This module contains the factroyclasses generating the HTMLpages.
Provided are:
 - PageFactory
"""
from os.path import isfile
from abc import abstractmethod
import jinja2 as jj
from .type_aliases import HTML, JSON

class PageFactory:

    """The PageFactory abstract class serves as a generator for pages.
    Members
    ------
    _environment: jinja2.Environment
        the environment to handel the combination of the final html file.
    template: jinja2.Template
        the template used for the combination of the final html file.
    content: str
        the content parsed into the final html file.
        consisting of java script code.
    info: HTML
        the default information displayed of the final html page
    """

    _environment: jj.Environment

    def __init__(self):
        """constructor initialises the environment."""
        self._environment = jj.Environment(
            loader=jj.FileSystemLoader('templates/'),
            autoescape=jj.select_autoescape(['html', 'xml'])
        )
        self._template = None
        self._content = None
        self._info = None

    def generate_page(self, args: JSON, template: HTML = None, info: str = None) -> HTML:
        """Generate a HTML page from the input parameters not using the
        template provided in the class.

        Args:
            args (JSON): Parameters used by some child classes to generate
                the right content.
            template (HTML): A template can be used instead of the default
                should contain variables for content and info,
                doesn't change the template lasting,
                can be left empty.
            info (str): Information displayed on the returned HTML page
                # todo may contain extra html formatting,
                doesn't change the info lasting,
                can be left empty.
        Returns:
            HTML: The finished HTML page displaying the content and information.
        """
        template_tmp = self._template
        info_tmp = self._info
        if not template is None:
            template_tmp = jj.Template(template)
        if not info is None:
            info_tmp = info
        if self._content is None:
            return template_tmp.render(
                info=info_tmp,
                content=self._generate_content(args))
        return template_tmp.render(info=info_tmp, content=self._content)

    @abstractmethod
    def _generate_content(self, args: JSON) -> HTML:
        """(abstract) Pattern function to generate the content of a given page.

        Args:
            args (JSON): Parameters used by some childclasses to generate the
                right content.

        Returns:
            HTML: The Content part, consisting of JavaScript.
        """

    def set_template(self, template: HTML):
        """Change the default template to the input template.

        Args:
            template (HTML): The new template for this instance of PageFactory.
                Either template as String or the filepath in view/template/s.
                doesn't validate format.
        """
        if isfile("template/"+template):
            self._template = self._environment.get_template(template)
        else:
            self._template = self._environment.from_string(template)

    def set_content(self, content: str):
        """Set the content to the input content.

        Args:
            content (str): New content for this instance of PageFactory.
        """
        self._content = content

    def set_info(self, info: str):
        """(abstract) Change the default info into the input info.

        Args:
            info (str): The new info of this instance of PageFactory, may
                contain HTML formatting.
                is not checking if it is valid html syntax
        """
        self._info = info


#Can be deleted but maby helpful constructor for concrete Factory
# implementation
#class DummyFactory(PageFactory):
#    def __init__(self):
#        super().__init__()
#        self._template = self._environment.get_template("dummy.html")
#        self._info = "some nights i get up"
#        pass
#    def set_info(self, info;str) {
#        print("heureka it works")
#        super.set_info(info)
#    }
