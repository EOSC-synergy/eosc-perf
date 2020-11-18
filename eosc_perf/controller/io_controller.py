"""This module acts as a facade between view and model."""
import json
import urllib.request
from json import JSONDecodeError
from typing import List, Union, Optional, Tuple
from urllib.error import URLError

from flask import session, redirect, Response

from .json_result_validator import JSONResultValidator
from .authenticator import authenticator, AuthenticateError
from .type_aliases import JSON
from ..model.facade import DatabaseFacade, facade
from ..model.data_types import Site, Report


class IOController:
    """This class acts as a facade between view and model and validates user input.
    Attributes:
        _result_validator (JSONResultValidator): The validator for uploaded benchmark results.
    """

    def __init__(self):
        """Constructor: create a new instance of IOController."""
        self._result_validator = JSONResultValidator()

    def authenticate(self) -> Optional[Response]:
        """Authenticate the current user. Redirects user to '/login' which again redirects the user to EGI Check-In
        for authentication.
        Returns:
            Optional[Response]: A redirect to the login page, if necessary.
        """
        if not self.is_authenticated():
            return redirect('/login')

    def submit_result(self, result_json: JSON, metadata: str) -> bool:
        """Submit a new benchmark result to the system.

        Fails if the user isn't authenticated or the result json is invalid.

        Args:
            result_json (JSON): The benchmark result to be uploaded.
            metadata (str): The metadata associated with the benchmark result.
        Returns:
            bool: True if the benchmark was successfully added.
        """
        if self.is_authenticated():
            if not self._result_validator.validate_json(result_json):
                raise ValueError("No valid result JSON")

            self._add_current_user_if_missing()
            return facade.add_result(result_json, metadata)

        raise AuthenticateError("Only authenticated users can submit results")

    def submit_benchmark(self, docker_name: str, comment: str) -> bool:
        """Submit a new benchmark to the system.

        Args:
            docker_name (str): The name of the dockerhub image.
            comment (str): Comment to add to benchmark submission.

        Returns:
            bool: True if the benchmark was successfully submitted.
        """
        if not self.is_authenticated():
            raise AuthenticateError("You need to be logged in to submit a benchmark.")

        if not self._valid_docker_hub_name(docker_name):
            raise RuntimeError("Could not verify {} as a valid docker hub name.".format(docker_name))

        self._add_current_user_if_missing()

        if not facade.add_benchmark(docker_name=docker_name, uploader_id=self.get_user_id()):
            raise RuntimeError("A benchmark with the given name was already submitted.")

        return self.report(json.dumps({
            'message': "New Benchmark. Submit comment: {}".format(comment),
            'type': 'benchmark',
            'value': docker_name,
            'uploader': self.get_user_id()
        }))

    def submit_site(self, short_name: str, address: str, name: str = None, description: str = None) -> bool:
        """Submit a new site to the system for review.
        Args:
            short_name (str): Machine-readable site identifier.
            address (str): Network address of the site.
            name (str): Human-readable name of the site.
            description (str): Human-readable description of the site.
        Returns:
            bool: True on success.
        """
        if not self.is_authenticated():
            raise AuthenticateError("You must be logged in to submit a site")
        self._add_current_user_if_missing()

        if short_name is None or len(short_name) == 0 or address is None or len(address) == 0:
            raise ValueError("invalid short_name or address")

        meta = {
            'short_name': short_name,
            'address': address
        }
        if name is not None:
            meta['name'] = name
        if description is not None:
            meta['description'] = description

        if not facade.add_site(json.dumps(meta)):
            return False

        message = "New Site. Short name: {}, address: {}".format(short_name, address)
        if name is not None:
            message += ", name: {}".format(name)
        if description is not None:
            message += ", description: {}".format(description)

        if not self.report(json.dumps({
            'message': message,
            'type': 'site',
            'value': short_name,
            'uploader': self.get_user_id()
        })):
            # delete site if submitting a report failed to avoid orphans
            facade.remove_site(short_name)
            return False
        return True

    def submit_tag(self, tag: str) -> bool:
        """Submit a new tag.
        Args:
            tag (str): The tag to be submitted.
        Returns:
            bool: True if the submission was successful.
        """
        if tag is None or len(tag) == 0:
            raise ValueError("invalid tag submitted")
        if not self.is_authenticated():
            raise AuthenticateError("You must be logged in to submit a tag")
        return facade.add_tag(tag)

    def get_site(self, short_name: str) -> Optional[Site]:
        """Get a single site by it's short name.
        Args:
           short_name (str): Short name of the site.
        Returns:
           Optional[Site]: The site with the given short name.
                 None if no site with given name is found.
        """
        try:
            site = facade.get_site(short_name)
        except facade.NotFoundError:
            site = None
        return site

    def remove_site(self, short_name: str) -> bool:
        """Remove a single site by it's short name.
        Args:
           short_name (str): Short name of the site.
        Returns:
           bool: True if removal was successful.
        """
        if self.is_authenticated():
            if self._site_result_amount(short_name) == 0:
                return facade.remove_site(short_name)
            else:
                raise RuntimeError("Only sites without results can be removed.")
        else:
            raise AuthenticateError("You need to be logged in to remove a site.")

    def report(self, metadata: JSON) -> bool:
        """Add a Report to the model and notify an admin about it.

        Args:
            metadata (JSON): The metadata in json format containing the benchmark 'result_id' and
                the associated 'user_message'.

        Returns:
            bool: True If the report was successfully added.
        """
        if self.is_authenticated():
            self._add_current_user_if_missing()
            # TODO: notify admin per email
            return facade.add_report(metadata)
        else:
            raise AuthenticateError("Must be logged in to submit a report")

    def get_report(self, uuid: str) -> Report:
        """Get a report by UUID. Requires the user to be an admin.
        Args:
            uuid (str): The unique identifier of the report.
        Returns:
            Report: The report.
        """
        if not authenticator.is_admin():
            raise AuthenticateError("User trying to view the reports isn't an admin.")
        return facade.get_report(uuid)

    def get_reports(self, only_unanswered: bool = False) -> List[Report]:
        """Provide a list of all reports, require the user to be an admin.

        Throws an AuthenticationError if authentication failed.

        Args:
            only_unanswered (bool): Whether to get all or only unanswered reports.
        Returns:
            List[Reports]: List containing requested reports.
        """
        if not authenticator.is_admin():
            raise AuthenticateError("User trying to view the reports isn't an admin.")
        return facade.get_reports(only_unanswered=only_unanswered)

    def process_report(self, verdict: bool, uuid: str) -> bool:
        """Set verdict of report with given uuid. If verdict is False, the item is hidden.
        Args:
            verdict (bool): The verdict; True makes the item visible, False hides it.
            uuid (str): The UUID of the judged report.
        Returns:
            bool: True if processing the report was successful.
        """
        if authenticator.is_admin():
            try:
                report = facade.get_report(uuid)
            except DatabaseFacade.NotFoundError:
                return False
            report.set_verdict(verdict)
            if report.get_report_type() == Report.BENCHMARK:
                report.get_benchmark().set_hidden(not verdict)
            elif report.get_report_type() == Report.SITE:
                report.get_site().set_hidden(not verdict)
            elif report.get_report_type() == Report.RESULT:
                report.get_result().set_hidden(not verdict)

            return True
        raise AuthenticateError("Only admins can process reports")

    def remove_result(self, uuid: str) -> bool:
        """Make a result invisible.
        Args:
            uuid (str): The uuid of the result.
        Returns:
            bool: True if the result was successfully hidden.
        """
        if not authenticator.is_admin():
            raise AuthenticateError("Only admins can remove results")
        try:
            result = facade.get_result(uuid)
        except DatabaseFacade.NotFoundError:
            return False
        result.set_hidden(True)
        return True

    def _add_current_user_if_missing(self):
        """Add the current user as an uploader if they do not exist yet."""
        if authenticator.is_authenticated():
            uid = self.get_user_id()
            try:
                facade.get_uploader(uid)
                return
            except facade.NotFoundError:
                email = self.get_email()
                name = self.get_full_name()
                facade.add_uploader(json.dumps({
                    'id': uid,
                    'email': email,
                    'name': name
                }))

    def _decompose_dockername(self, docker_name: str) -> Tuple[str, str, str]:
        """Helper to break a model-docker_name into a tuple.
        Args:
            docker_name (str): The docker identifier to decompose.
        Returns:
            Tuple[str, str, str]: A tuple containing the username, image name and tag name.
        """
        slash = docker_name.find('/')
        if slash == -1:
            # this should not have passed input validation
            pass
        username = docker_name[:slash]
        colon = docker_name.find(':')
        if colon == -1:
            image = docker_name[slash + 1:]
            tag = None
        else:
            image = docker_name[slash + 1:colon]
            tag = docker_name[colon + 1:]

        return username, image, tag

    def _build_dockerregistry_url(self, docker_name: str) -> str:
        """Helper function to build a link to the docker hub registry api.
        Returns:
            str: URL for the given image in the docker hub registry.
        """
        (username, image, tag) = self._decompose_dockername(docker_name)

        url = 'https://registry.hub.docker.com/v2/repositories/{}/{}'.format(username, image)
        return url

    def _build_dockerregistry_tag_url(self, docker_name: str) -> str:
        """Helper function to build a link to the docker hub registry api.
        Returns:
            str: URL for the list of tags associated with the given image name from the docker hub registry.
        """
        (username, image, tag) = self._decompose_dockername(docker_name)

        url = 'https://registry.hub.docker.com/v2/repositories/{}/{}/tags'.format(username, image)
        return url

    def _valid_docker_hub_name(self, docker_name: str) -> bool:
        """Check if a benchmark exists with the given name on docker hub.
        Args:
            docker_name (str): The name to be checked.
        Returns:
            bool: True if the image exists.
        """
        if docker_name is None or len(docker_name) == 0:
            return False
        try:
            dockerhub_content = urllib.request.urlopen(self._build_dockerregistry_url(docker_name)).read()
            (username, image, tag) = self._decompose_dockername(docker_name)
            meta = json.loads(dockerhub_content)
            if meta['is_private']:
                return False
            if tag is not None:
                # check tag as well
                dockerhub_tags = urllib.request.urlopen(self._build_dockerregistry_tag_url(docker_name)).read()
                tags = json.loads(dockerhub_tags)
                # search result with correct tag name
                for result in tags['results']:
                    if tag == result['name']:
                        return True
                return False
            return True
        except (URLError, JSONDecodeError):
            return False

    @staticmethod
    def _site_result_amount(short_name: str) -> int:
        """Get the number of results associated with a site.
        Args:
            short_name (str): The site to check.
        Result:
            int: The number of results linked to the specified site.
        """
        filters = {'filters': [
            {'type': 'site', 'value': short_name}
        ]}
        results = facade.query_results(json.dumps(filters))
        return len(results)

    @staticmethod
    def get_email() -> Optional[str]:
        """Get current user's unique identifier, if logged in.
        Returns:
           Optional[str]: The current user's email, or None if no user is logged in.
        """
        try:
            return session['user']['info']['email']
        except KeyError:
            return None

    @staticmethod
    def get_full_name() -> Optional[str]:
        """Get current user's full name, if logged in.
        Returns:
           Optional[str]: The current user's full name, or None if no user is logged in.
        """
        try:
            return session['user']['info']['name']
        except KeyError:
            return None

    @staticmethod
    def get_user_id() -> Optional[str]:
        """Get current user's unique identifier, if logged in.
        Returns:
           Optional[str]: The current user's unique identifier, or None if no user is logged in.
        """
        try:
            return session['user']['sub']
        except KeyError:
            return None

    @staticmethod
    def is_admin() -> bool:
        """Checks if current user has admin right, if one is logged on.
        Returns:
            bool: True if current user is admin.
        """
        return authenticator.is_admin()

    @staticmethod
    def is_authenticated() -> bool:
        """Check if the current user is authenticated.
        Returns:
            bool: True if the user is authenticated.
        """
        return authenticator.is_authenticated()


controller = IOController()
