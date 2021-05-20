"""This module acts as a facade between view and model."""
import json
import urllib.request
from json import JSONDecodeError
from typing import List, Optional, Callable, Any
from urllib.error import URLError

from flask import session, redirect, Response

from eosc_perf.utility.type_aliases import JSON
from .authenticator import authenticator, AuthenticateError
from .json_result_validator import JSONResultValidator
from .report_mailer import ReportMailer
from ..model.data_types import Report, SiteFlavor, UUID
from ..model.facade import DatabaseFacade, facade
from ..utility.dockerhub import decompose_dockername, build_dockerregistry_url, build_dockerregistry_tag_url


def _only_authenticated(message: str = "Not authenticated.") -> Callable[..., Any]:
    """Decorator helper for authentication.

    Args:
        message (str): Message to return if the user is not authenticated.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(self, *args, **kwargs) -> Callable[..., Any]:
            # use self because controller is not declared yet
            if not self.is_authenticated():
                raise AuthenticateError(message)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def _only_admin(function: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator helper for authentication.
    """

    def wrapper(self, *args, **kwargs) -> Callable[..., Any]:
        if not self.is_admin():
            raise AuthenticateError("Not an administrator.")
        return function(self, *args, **kwargs)

    return wrapper


class IOController:
    """This class acts as a middleman between view and model for actions that require input validation or
    authentication. This generally implies submitting new data or getting data exclusive to administrators.

    Attributes:
        _result_validator (JSONResultValidator): The validator for uploaded benchmark results.
    """

    def __init__(self):
        """Constructor: create a new instance of IOController."""
        self._result_validator = JSONResultValidator()
        self._report_mailer = ReportMailer()

    def authenticate(self) -> Optional[Response]:
        """Authenticate the current user. Redirects user to '/login' which again redirects the user to EGI Check-In
        for authentication.

        Returns:
            Optional[Response]: A redirect to the login page, if necessary.
        """
        if not self.is_authenticated():
            return redirect('/login')

    @_only_authenticated(message="Only authenticated users can submit results")
    def submit_result(self, result_json: JSON, uploader: str, benchmark_name: str, site: str, flavor: str,
                      tags: List[str] = []) -> bool:
        """Submit a new benchmark result to the system.

        Fails if the user isn't authenticated or the result json is invalid.

        Args:
            result_json (JSON): The benchmark result to be uploaded.
            uploader (str): The id of the uploader that submitted the result.
            benchmark_name (str): The identifier of the benchmark that was run.
            site (str): The id of the site this was run on.
            flavor (str): The virtual machine flavor this was run on.
            tags (List[str]): A list of user-created tags to associated this result to.
        Returns:
            bool: True if the benchmark was successfully added.
        """
        try:
            benchmark = facade.get_benchmark(benchmark_name)
        except facade.NotFoundError:
            raise ValueError("Unknown benchmark")

        template = benchmark.get_template() if benchmark.has_template() else None

        if not self._result_validator.validate_json(result_json, template):
            raise ValueError("No valid result JSON")

        self._add_current_user_if_missing()
        return facade.add_result(result_json, uploader, site, benchmark_name, flavor, tags)

    @_only_authenticated(message="You need to be logged in to submit a benchmark.")
    def submit_benchmark(self, docker_name: str, comment: str, template: Optional[JSON] = None) -> bool:
        """Submit a new benchmark to the system.

        Args:
            docker_name (str): The name of the dockerhub image.
            comment (str): Comment to add to benchmark submission.
            template (JSON): Optional JSON template for benchmark results.
        Returns:
            bool: True if the benchmark was successfully submitted.
        """
        if not self._valid_docker_hub_name(docker_name):
            raise RuntimeError("Could not verify '{}' as a valid docker hub name.".format(docker_name))

        self._add_current_user_if_missing()

        if template is not None and not self._result_validator.validate_json(template, skip_keycheck=True):
            raise ValueError("Template is not valid JSON")

        if not facade.add_benchmark(docker_name=docker_name, uploader_id=self.get_user_id(), description=comment,
                                    template=template):
            raise RuntimeError("A benchmark with the given name was already submitted.")

        # if user is an admin, skip review process
        # if self.is_admin():
        #    facade.get_benchmark(docker_name=docker_name).set_hidden(False)
        #    return True

        message = "New benchmark, docker identifier: {}".format(docker_name)
        if comment is not None and len(comment) > 0:
            message += ", description: {}".format(comment)

        return self.report(Report.BENCHMARK, docker_name, message, self.get_user_id())

    @_only_authenticated(message="You must be logged in to submit a site")
    def submit_site(self, identifier: str, address: str, name: str = None, description: str = None) -> bool:
        """Submit a new site to the system for review.

        Args:
            identifier (str): Machine-readable site identifier.
            address (str): Network address of the site.
            name (str): Human-readable name of the site.
            description (str): Human-readable description of the site.
        Returns:
            bool: True on success.
        """
        self._add_current_user_if_missing()

        if identifier is None or len(identifier) == 0 or address is None or len(address) == 0:
            raise ValueError("invalid identifier or address")

        if not facade.add_site(identifier, address, description=description, full_name=name):
            return False

        message = "New site, identifier: {}, address: {}".format(identifier, address)
        if name is not None:
            message += ", full name: {}".format(name)
        if description is not None:
            message += ", description: {}".format(description)

        if not self.report(Report.SITE, identifier, message, self.get_user_id()):
            # delete site if submitting a report failed to avoid orphans
            facade.remove_site(identifier)
            return False

        site = facade.get_site(identifier)
        default_flavor: SiteFlavor = SiteFlavor("unknown", site)
        site.add_flavor(default_flavor)

        return True

    @_only_authenticated("You must be logged in to submit a tag.")
    def submit_tag(self, tag: str) -> bool:
        """Submit a new tag.

        Args:
            tag (str): The tag to be submitted.
        Returns:
            bool: True if the submission was successful.
        """
        if tag is None or len(tag) == 0:
            raise ValueError("invalid tag submitted")
        return facade.add_tag(tag)

    @_only_authenticated(message="You must be logged in to submit a site flavor.")
    def submit_flavor(self, name: str, description: str, site_identifier: str) -> Optional[str]:
        """Submit a new site flavor.

        Args:
            name (str) - The name of the flavor.
            description (str) - The description of the flavor.
            site_identifier (str) - The identifier of the site the flavor belongs to.
        Returns:
            Optional[str] - The UUID of the new flavor if successful, None on error.
        """
        success, uuid = facade.add_flavor(name, description, site_identifier)
        return uuid if success else None

    @_only_admin
    def remove_site(self, identifier: str) -> bool:
        """Remove a single site by it's short name.

        Args:
           identifier (str): Short name of the site.
        Returns:
           bool: True if removal was successful.
        """
        if self._site_result_amount(identifier) == 0:
            return facade.remove_site(identifier)
        else:
            raise RuntimeError("Only sites without results can be removed.")

    @_only_authenticated("You must be logged in to submit a report.")
    def report(self, report_type: int, target, message: str, uploader: str) -> bool:
        """Add a Report to the model and notify an admin about it.

        Args:
            report_type (int): What is being reported.
            target (UUID): The item being report.
            message (str): An explanation of the report.
            uploader (str): The identifier of the uploader.
        Returns:
            bool: True If the report was successfully added.
        """
        self._add_current_user_if_missing()
        types = {
            Report.RESULT: 'result',
            Report.SITE: 'site',
            Report.BENCHMARK: 'benchmark'
        }
        if facade.add_report(json.dumps({
            'type': types[report_type],
            'value': target,
            'message': message,
            'uploader': uploader
        })):
            self._report_mailer.mail_entry(report_type, message)
            return True
        return False

    @_only_admin
    def get_report(self, uuid: str) -> Report:
        """Get a report by UUID. Requires the user to be an admin.

        Args:
            uuid (str): The unique identifier of the report.
        Returns:
            Report: The report.
        """
        return facade.get_report(uuid)

    @_only_admin
    def get_reports(self, only_unanswered: bool = False) -> List[Report]:
        """Provide a list of all reports, require the user to be an admin.

        Throws an AuthenticationError if authentication failed.

        Args:
            only_unanswered (bool): Whether to get all or only unanswered reports.
        Returns:
            List[Reports]: List containing requested reports.
        """
        return facade.get_reports(only_unanswered=only_unanswered)

    @_only_admin
    def process_report(self, verdict: bool, uuid: str) -> bool:
        """Set verdict of report with given uuid. If verdict is False, the item is hidden.

        Args:
            verdict (bool): The verdict; True makes the item visible, False hides it.
            uuid (str): The UUID of the judged report.
        Returns:
            bool: True if processing the report was successful.
        """
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

    @_only_admin
    def remove_result(self, uuid: str) -> bool:
        """Make a result invisible.

        Args:
            uuid (str): The uuid of the result.
        Returns:
            bool: True if the result was successfully hidden.
        """
        try:
            result = facade.get_result(uuid)
        except DatabaseFacade.NotFoundError:
            return False
        result.set_hidden(True)
        return True

    @_only_admin
    def update_flavor(self, uuid: str, name: str, description: str) -> bool:
        """Update a site flavor's details.

        Args:
            uuid (str) - The UUID of the flavor.
            name (str) - The new name to set.
            description (str) - The new description to set.
        """
        try:
            flavor = facade.get_site_flavor(uuid)
        except facade.NotFoundError:
            return False
        flavor.set_name(name)
        flavor.set_description(description)
        return True

    # @_only_authenticated
    def _add_current_user_if_missing(self):
        """Add the current user as an uploader if they do not exist yet."""
        uid = self.get_user_id()
        try:
            facade.get_uploader(uid)
        except facade.NotFoundError:
            facade.add_uploader(uid, self.get_full_name(), self.get_email())

    @staticmethod
    def _valid_docker_hub_name(docker_name: str) -> bool:
        """Check if a benchmark exists with the given name on docker hub.

        Args:
            docker_name (str): The name to be checked.
        Returns:
            bool: True if the image exists.
        """
        if docker_name is None or len(docker_name) == 0:
            return False
        try:
            dockerhub_content = urllib.request.urlopen(build_dockerregistry_url(docker_name)).read()
            (username, image, tag) = decompose_dockername(docker_name)
            meta = json.loads(dockerhub_content)
            if meta['is_private']:
                return False
            if tag is not None:
                # check tag as well
                dockerhub_tags = urllib.request.urlopen(build_dockerregistry_tag_url(docker_name)).read()
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
    def _site_result_amount(identifier: str) -> int:
        """Get the number of results associated with a site.

        Args:
            identifier (str): The site to check.
        Result:
            int: The number of results linked to the specified site.
        """
        filters = {'filters': [
            {'type': 'site', 'value': identifier}
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
