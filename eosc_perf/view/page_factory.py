"""This module contains the PageFactory base class used and extended by all other pages to generate the HTML pages.
"""
from abc import abstractmethod
from typing import Any, Tuple

import jinja2 as jj

from ..configuration import configuration
from ..controller.io_controller import controller
from ..utility.type_aliases import HTML, JSON


class PageFactory:
    """The PageFactory abstract class serves as a generator for pages. It fills in data used by the base template, which
    every other page template expands upon. This includes the navigation panel at the top, and the footer at the bottom.

    Attributes:
        _environment (jinja2.Environment): The jinja environment used to load the jinja templates.
    """

    _environment: jj.Environment

    def __init__(self, template: str):
        """Set up a new PageFactory.

        Args:
            template (str): Path to the template to use.
        """
        self._environment = jj.Environment(
            loader=jj.FileSystemLoader('templates/'),
            autoescape=jj.select_autoescape(['html', 'xml'])
        )
        self._template = template

    def generate_page(self, args: Any = None, **jinja_args) -> HTML:
        """Generate a HTML page from the input parameters not using the
        template provided in the class.

        Args:
            args (JSON): Parameters used by some child classes to generate the right content.
            jinja_args (kwargs): Extra arguments for the jinja template.
        Returns:
            HTML: The finished HTML page displaying the content and information.
        """
        template_content = self._environment.get_template(self._template)
        (content, extra_args) = self._generate_content(args)
        return template_content.render(
            content=content,
            admin=controller.is_admin(),
            debug=configuration.get('debug'),
            im_link=configuration.get('infrastructure_href'),
            user_name=controller.get_full_name(),
            logged_in=controller.is_authenticated(),
            support_email=configuration.get('support_email'),
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
