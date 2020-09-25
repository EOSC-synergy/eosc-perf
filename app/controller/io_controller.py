"""
This module acts as a facade between view and model.
"""
import json
import urllib.request
from re import match
from typing import List
from flask import session, redirect
from .json_result_validator import JSONResultValidator
from .authenticator import authenticator, AuthenticateError
from .type_aliases import JSON
from ..model.facade import DatabaseFacade, facade
from ..model.data_types import Site, Report
# The parent url of docker hub projects, first for private second for docker certified.
docker_hub_url = {"certified": "https://hub.docker.com/r/",
                  "default": "https://hub.docker.com/_/"}

class IOController:
    """This class acts as a facade between view and model and validates user input.
    Attributes:
    _result_validator (JSONResultValidator): The validator for uploaded benchmark results."""

    def __init__(self):
        """Constructor: create a new instance of IOController."""
        self._result_validator = JSONResultValidator()

    def authenticate(self):
        """Authenticate the current user. Redirects user to '/login' which again redirects 
           the user to EGI Check-In for authentication."""
        if not self.is_authenticated():
            return redirect('/login')

    def submit_result(self, result_json: str, metadata: str) -> bool:
        """Submit a new benchmark result to the system.
           Fails if the user isn't authenticated or the result json is invalid.
        Args:
        result_json  (JSON): The benchmark result to be uploaded.
        metadata      (str): The metadata associated with the benchmark result.
        Returns:
        bool: True if the benchmark was successfully added, false otherwise.
        """
        # Check if user is authenticated
        if self.is_authenticated():
            # Check if the result is in the correct format.
            if not self._result_validator.validate_json(result_json):
                raise ValueError("no valid result JSON")

            # if the user is not in the database, we must add them
            self._add_current_user_if_missing()
            # Try to add the result to the data base.
            return facade.add_result(result_json, metadata)
        return False

    def submit_benchmark(self, docker_name: str, comment: str) -> bool:
        """Submit a new Benchmark to the system.
        Args:
        uploader_id  (str): The id of the uploader.
        docker_name     (str): The name of the dockerhub repository and sub url.
                               https://hub.docker.com/_/[docker_name] or
                               https://hub.docker.com/_/[docker_name] should be a valid url.
        check_for_page (bool): If true, it will be checked whether docker_name corresponds to
                               an existing image on docker hub. Can lead to problems if
                               chromium isn't installed and takes a considerable amount of time (5-10s).
        Returns:
        bool: True if the benchmark was successfully submitted, false othwe
        """
        # Check if user is authenticated.
        if not self.is_authenticated():
            raise RuntimeError("You need to be logged in to submit a benchmark.")
        if docker_name is None:
            raise ValueError("Docker name must not be None")
        # Check for valid email address.
        # Check valid docker_hub_name.uploader_emailuploader_email
        if self._valid_docker_hub_name(docker_name):
            self._add_current_user_if_missing()
            # Add to model.
            if facade.add_benchmark(docker_name=docker_name, uploader_id=self.get_user_id()):
                return self.report(json.dumps({
                    'message': "New Benchmark. Submit comment: {}".format(comment),
                    'type': 'benchmark',
                    'value': docker_name,
                    'uploader': self.get_user_id()
                }))
            else:
                raise RuntimeError("A benchmark with the given name was already submitted.")
        raise RuntimeError("Could not verify {} as a valid docker hub name.".format(docker_name))

    def submit_site(self, short_name: str, address: str, name: str = None, description: str = None) -> bool:
        """Submit a new site to the system for review.
        Args:
            short_name (str): site identifier
            address (str): network address of the site
            name (str): human-readable name of the site
            description (str): human-readable description of the site
        Returns:
            bool: True on success, false othwerwise.
        """
        if not self.is_authenticated():
            return False
        self._add_current_user_if_missing()

        if short_name is None:
            raise ValueError("Short name must not be None")
        if address is None:
            raise ValueError("Address name must not be None")

        meta = {
            'short_name': short_name,
            'address': address
        }
        if name is not None:
            meta['name'] = name
        if description is not None:
            meta['description'] = description

        if facade.add_site(json.dumps(meta)):
            message = "New Site. Short name: {}, address: {}".format(short_name, address)
            if name is not None:
                message += ", name: {}".format(name)
            if description is not None:
                message += ", description: {}".format(description)
            return self.report(json.dumps({
                    'message': message,
                    'type': 'site',
                    'value': short_name,
                    'uploader': self.get_user_id()
                }))
        return False


    def submit_tag(self, tag: str) -> bool:
        """Submit a new tag
        Args:
        metadata_json (str): The tag to be submitted.
        Returns:
        bool: True if the submission was successful, false otherwise.
        """
        if tag is None:
            raise ValueError("Tag must not be None")
        if self.is_authenticated():
            return facade.add_tag(tag)
        return False

    def get_site(self, short_name) -> Site:
        """Get a single site by it's short name.
           Args:
           short_name (str): short name of a site
           Returns:
           Site: The site with the given short name.
                 None if no site with given name is found."""
        try:
            site = facade.get_site(short_name)
        except facade.NotFoundError:
            site = None
        return site

    def remove_site(self, short_name) -> bool:
        """Removes a single site by it's short name.
           Args:
           short_name (str): short name of a site
           Returns:
           bool: True if removal was successful, false otherwise"""
        if self.is_authenticated():
            if self._site_result_amount(short_name) == 0:
                return facade.remove_site(short_name)
            else:
                raise RuntimeError("Only sites without results can be removed.")
        else:
            raise RuntimeError("You need to be logged in to remove a site.")

    def report(self, metadata: JSON) -> bool:
        """Add a Report to the model and notify an admin about it.
        Args:
        metadata     (JSON): The metadata in json format containing the
                             benchmark 'result_id' and the associated 'user_message'.
        Returns:
        bool: True If the report was successfully added, false otherwise
        """
        if self.is_authenticated():
            # if the user is not in the database, add them
            self._add_current_user_if_missing()
            # Add to database.
            # TODO: notify admin per email
            return facade.add_report(metadata)
        else:
            raise RuntimeError("Must be logged in to submit a report")

    def get_report(self, uuid: str) -> Report:
        """Get a report by UUID. Requires the user to be an admin.
        Args:
            uuid (str): The unique identifier for the report.
        Returns:
            List[Reports]: The report.
        """
        if authenticator.is_admin():
            return facade.get_report(uuid)
        raise AuthenticateError("User trying to view the reports isn't an admin.")

    def get_reports(self, only_unanswered: bool = False) -> List[Report]:
        """Provide a list of all reports, require the user to be an admin.
        Args:
        only_unanswered (bool): Whether all or only the unanswered, reports get provided.
        Returns:
        List[Reports]: List of all the requested reports, throws an AuthenticationError if
                       the authentication failed."""
        if authenticator.is_admin():
            return facade.get_reports(only_unanswered=only_unanswered)
        raise AuthenticateError(
            "User trying to view the reports isn't an admin.")

    def process_report(self, verdict: bool, uuid: str) -> bool:
        """Add verdict to report with given uuid. If verdict is False, the item with given uuid
           will stay hidden or become hidden.
        Args:
            verdict (bool): The verdict; True when approving the reported item, which means
                            it stays/becomes visible. If false, the reported item will
                            stay/become hidden.
            uuid (str): The uuid of the judged report.
        Returns:
            bool: If the process was successful.
        """
        # Check if user is admin.
        if authenticator.is_admin():
            # Set the verdict.
            try:
                report = facade.get_report(uuid)
                # Set the verdict status.
                report.set_verdict(verdict)
                # for benchmarks and sites: hidden only when added,
                # visible after 'review' == report
                if report.get_report_type() == Report.BENCHMARK:
                    report.get_benchmark().set_hidden(not verdict)
                elif report.get_report_type() == Report.SITE:
                    report.get_site().set_hidden(not verdict)
                elif report.get_report_type() == Report.RESULT:
                    report.get_result().set_hidden(not verdict)
            except DatabaseFacade.NotFoundError:
                # There is no report with given uuid.
                return False
            return True
        return False

    def remove_result(self, uuid:str):
        """Make a result invisible.
        Args:
            uuid (str): The uuid of the result.
        Resturns:
            bool: If the process was successfull."""
        if authenticator.is_admin():
            try:
                result = facade.get_result(uuid)
                result.set_hidden(True)
            except DatabaseFacade.NotFoundError:
                # There is no result with given uuid.
                return False
            return True
        return False
    
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

    def _decompose_dockername(self, docker_name):
        """Helper to break a model-docker_name into a tuple."""
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

        return (username, image, tag)

    def _build_dockerregistry_url(self, docker_name):
        """Helper function to build a link to the docker hub registry api."""
        (username, image, tag) = self._decompose_dockername(docker_name)

        url = 'https://registry.hub.docker.com/v2/repositories/{}/{}'.format(username, image)
        return url

    def _build_dockerregistry_tag_url(self, docker_name):
        """Helper function to build a link to the docker hub registry api."""
        (username, image, tag) = self._decompose_dockername(docker_name)

        url = 'https://registry.hub.docker.com/v2/repositories/{}/{}/tags'.format(username, image)
        return url

    def _valid_docker_hub_name(self, docker_name: str) -> bool:
        """Check if a benchmark exists with the given name on dockerhub.
        Args:
            docker_name      (str): The name to be checked.
        Returns:
            bool: True if the image exists.
        """
        try:
            dockerhub_content = urllib.request.urlopen(
                self._build_dockerregistry_url(docker_name)).read()
            (username, image, tag) = self._decompose_dockername(docker_name)
            json.loads(dockerhub_content)
            if not tag is None:
                # check tag as well
                dockerhub_tags = urllib.request.urlopen(
                    self._build_dockerregistry_tag_url(docker_name)).read()
                tags = json.loads(dockerhub_tags)
                # search result with correct tagname
                for result in tags['results']:
                    if tag == result['name']:
                        return True
                return False
            return True
        except:
            return False

    @staticmethod
    def _site_result_amount(short_name):
        filters = {'filters': [
            {'type': 'site', 'value': short_name}
        ]}
        results = facade.query_results(json.dumps(filters))
        return len(results)

    @staticmethod
    def get_email():
        """Get current user's unique identifier, if logged in.
           Returns:
           Id: The urrent user's email.
               Is None if no user is logged in."""
        try:
            return session['user']['info']['email']
        except KeyError:
            return None

    @staticmethod
    def get_full_name():
        """Get current user's full name, if logged in.
           Returns:
           Name: The urrent user's full name.
                 Is None if no user is logged in."""
        try:
            return session['user']['info']['name']
        except KeyError:
            return None

    @staticmethod
    def get_user_id() -> str:
        """Get current user's unique identifier, if logged in.
           Returns:
           Id: The urrent user's unique identifier.
               Is None if no user is logged in."""
        try:
            return session['user']['sub']
        except KeyError:
            return None

    @staticmethod
    def is_admin() -> bool:
        """Checks if current user has admin right, if one is logged on.
           Returns: True if current user is admin, otherwise False."""
        return authenticator.is_admin()

    @staticmethod
    def is_authenticated() -> bool:
        """Check if the current user is authenticated."""
        return authenticator.is_authenticated()

controller = IOController()
