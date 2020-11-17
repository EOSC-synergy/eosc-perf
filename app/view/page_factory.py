"""This module contains the factory classes generating the HTML pages."""
from os.path import isfile
from abc import abstractmethod
from typing import Any

import jinja2 as jj
from .type_aliases import HTML, JSON
from ..configuration import configuration
from ..controller.io_controller import controller

class PageFactory:

    """The PageFactory abstract class serves as a generator for pages.
    Attributes:
        _environment (jinja2.Environment): the environment to handle the combination of the final html file.
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

    def generate_page(self, template: str, args: Any = None, **jinja_args) -> HTML:
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
            jinja_args (kwargs): Extra arguments for the jinja template.
        Returns:
            HTML: The finished HTML page displaying the content and information.
        """
        template_content = self._environment.get_template(template)
        return template_content.render(
            content=self._generate_content(args),
            admin=controller.is_admin(),
            debug=configuration.get('debug'),
            im_link=configuration.get('infrastructure_href'),
            user_name=controller.get_full_name(),
            logged_in=controller.is_authenticated(),
            **jinja_args)

    @abstractmethod
    def _generate_content(self, args: Any) -> HTML:
        """(abstract) Pattern function to generate the content of a given page.

        Args:
            args (JSON): Parameters used by some childclasses to generate the
                right content.

        Returns:
            HTML: The Content part, consisting of JavaScript.
        """
