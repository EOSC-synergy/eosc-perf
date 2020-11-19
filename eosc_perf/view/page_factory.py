"""This module contains the factory classes generating the HTML pages."""
from abc import abstractmethod
from typing import Any, Tuple

import jinja2 as jj

from eosc_perf.utility.type_aliases import HTML, JSON
from ..configuration import configuration
from ..controller.io_controller import controller


class PageFactory:
    """The PageFactory abstract class serves as a generator for pages.
    Attributes:
        _environment (jinja2.Environment): the environment to handle the combination of the final html file.
    """

    _environment: jj.Environment

    def __init__(self):
        """Set up a new PageFactory."""
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
            template (str): The filename of the template to use.
            args (JSON): Parameters used by some child classes to generate the right content.
            jinja_args (kwargs): Extra arguments for the jinja template.
        Returns:
            HTML: The finished HTML page displaying the content and information.
        """
        template_content = self._environment.get_template(template)
        (content, extra_args) = self._generate_content(args)
        return template_content.render(
            content=content,
            admin=controller.is_admin(),
            debug=configuration.get('debug'),
            im_link=configuration.get('infrastructure_href'),
            user_name=controller.get_full_name(),
            logged_in=controller.is_authenticated(),
            **extra_args,
            **jinja_args)

    @abstractmethod
    def _generate_content(self, args: Any) -> Tuple[HTML, Any]:
        """Pattern function to generate the content of a given page.

        Args:
            args (JSON): Parameters used by child classes to generate the right content.
        Returns:
            Tuple[HTML, Any]: A tuple containing page content to fill in and extra arguments for Jinja.
        """
