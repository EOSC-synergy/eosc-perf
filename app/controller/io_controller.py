"""
This module acts as a facade between view and model.
"""
import json
from re import match
from typing import List
from requests import get
from flask import session, redirect
from requests_html import HTMLSession
from .json_result_validator import JSONResultValidator
from .authenticator import authenticator, AuthenticateError
from .type_aliases import JSON
from ..model.facade import DatabaseFacade, facade
from ..model.data_types import Site, Report
# The parent url of docker hub projects, first for private second for docker certified.
docker_hub_url = {"certified": "https://hub.docker.com/r/",
                  "default": "https://hub.docker.com/_/"}
# For debugging skips the authentication process

class IOController:
    """This class acts as a facade between view and model, and validate user input.
    Attributes:
    _result_validator  (JSONResultValidator): The validator for an uploaded benchmark result."""

    def __init__(self):
        """Constructor generat a new instance of IOController.
        Args:
        data_base (DatabaseFacade): The facade used to interact with the model if left
                                    empty creates a new facade and there for a new database.
        """
        self._result_validator = JSONResultValidator()

    def authenticate(self):
        """Authenticate the current user."""
        if not self.is_authenticated():
            return redirect('/login')

    def submit_result(self, result_json: str, metadata: str) -> bool:
        """Submit a new benchmark result to the system if it is valid.
            Fails if the user isn't authenticated or the result json is in an invalid format.
        Args:
        result_json  (JSON): The benchmark result.
        metadata      (str): The metadata associated with the benchmark result.
        Returns:
        bool: If the benchmark was successfully added.
        """
        # Check if user is authenticated
        if self.is_authenticated():
            # Check if the result is in the correct format.
            if not self._result_validator.validate_json(result_json):
                raise ValueError("no valid result JSON")

            # if the user is not in the database, we must add them
            self.add_current_user_if_missing()
            # Try to add the result to the data base.
            return facade.add_result(result_json, metadata)
        return False

    def submit_benchmark(self, uploader_id: str, docker_name: str, comment: str,
                         check_for_page: bool = False) -> bool:
        """Submit a new Benchmark to the system.
        Args:
        uploader_id  (str): The id of the uploader.
        docker_name     (str): The name of the dockerhub reposetory and sub url.
                               So that https://hub.docker.com/_/[docker_name] or
                               https://hub.docker.com/_/[docker_name] results in a valid url.
        check_for_page (bool): Determines whether to control if the url corresponds to
                               an existing image on docker hub. Can lead to problems if
                               chromium isn't installed
                               and takes a considerable amount of time (5-10s).
        Returns:
        bool: If the benchmark was successfully submitted.
        """
        # Check if user is authenticated.
        if not self.is_authenticated():
            return False
        # Check for valid email address.
        # Check valid docker_hub_name.uploader_emailuploader_email
        if self._valid_docker_hub_name(docker_name, check_for_page):
            # Add to model.
            if facade.add_benchmark(docker_name=docker_name, uploader_id=uploader_id):
                return self.report(json.dumps({
                    'message': comment,
                    'type': 'benchmark',
                    'value': docker_name,
                    'uploader': uploader_id
                }))
        return False

    def submit_site(self, metadata_json: JSON) -> bool:
        """Submit a new site, will be aviable after getting approved.
        Args:
        metadata_json (JSON): A json formated str containing a 'short_name' and 'address' parameter
                              ,as well as maybe a 'name' parameter.
        Returns:
        bool: If the submission was successful.
        """
        if self.is_authenticated():
            # Crete new site.
            site = self._parse_site(metadata_json)
            json_str = '{ '+'"short_name" : "' + site.get_short_name() + \
                           '" , "address" : "' + site.get_address() + \
                           '" , "name" : "' + site.get_name() + \
                           '" , "description" : "' + site.get_description() + '" ' + '}'
            return facade.add_site(json_str)
        return False

    def submit_tag(self, tag: str) -> bool:
        """Submit a new tag
        Args:
        metadata_json (str): The submitted tag.
        Returns:
        bool: If the submission was successful.
        """
        if self.is_authenticated():
            return facade.add_tag(tag)
        return False

    def get_unapproved_sites(self) -> List[Site]:
        """If the current user is an admin provide a list of all unaproved sites.
        Args:
        Returns:
        List[Sites]: All unaproved sites, can be empty.
        """
        # Check if admin.
        if authenticator.is_admin():
            return self._unapproved_sites
        # User isn't admin.
        raise AuthenticateError(
            "The users attempting to get teh unapproved sites isn't an an admin.")

    def approve_site(self, site: Site = None, metadata_json: JSON = None) \
            -> bool:
        """If the current user is an admin, approve the given site.
        Args:
        site          (Site): The admin reviewed site getting add to the model.
        metadata_json (JSON): A json formated str containing a 'short_name' and 'address' parameter
                              ,as well as maybe a 'name' parameter. Gets used if site is left empty.
        Returns:
        bool: If process was successful.
        """

        # Check if user is allowed to approve.
        if authenticator.is_admin():
            # Decide whether to use site or metadata_json.
            site = [site, self._parse_site(metadata_json)][site is None]
            if not site is None:
                # Atm unnecessary step, but usefull in case the site got created not in
                # IOController or DatabaseFacade.
                json_str = '{ '+'"short_name" : "' + site.get_short_name() + \
                           '" , "address" : "' + site.get_address() + \
                           '" , "name" : "' + site.get_name() + \
                           '" , "description" : "' + site.get_description() + '" ' + '}'
                # Try to add to database.
                if facade.add_site(json_str):
                    # Successfully added, remove from _unapproved_sites.
                    for singel_site in self._unapproved_sites:
                        # one of the attributes enough in case a admin corrected eg. the addres.
                        if singel_site.get_short_name() is site.get_short_name() or \
                                singel_site.get_address() is site.get_address():
                            self._unapproved_sites.remove(singel_site)
                            break
                    return True
        return False

    def report(self, metadata: JSON) -> bool:
        """Add a Report to the model, and notify an admin about it.
        Args:
        metadata     (JSON): The metadata in json format, containing the
                             benchmark 'result_id' and the associated 'user_message'.
        Returns:
        bool: If the report was successfully added.
        """
        if self.is_authenticated():
            # Add to database.
            if facade.add_report(metadata):
                # TODO: notify admin, per email.
                return True
        return False

    def get_report(self, uuid: str) -> Report:
        """Get a report by UUID, require the user to be an admin.
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
        """Add the verdict to the model, if the verdict consents the report the associated
        benchmark gets deleted.
        Args:
            verdict (bool): The verdict; True when approving the reported item, False otherwise.
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
                if verdict:
                    if report.get_report_type() == Report.BENCHMARK:
                        report.get_benchmark().set_hidden(False)
                    elif report.get_report_type() == Report.SITE:
                        report.get_site().set_hidden(False)
            except DatabaseFacade.NotFoundError:
                # There is no report with given uuid.
                return False
            return True
        return False

    def add_current_user_if_missing(self):
        """Add the user from the current system as an uploader if they do not exist yet."""
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

    def _valid_docker_hub_name(self, docker_name: str, check_for_page: bool) -> bool:
        """Check if it is a valid docker hub name.
        Therefore controll the naming convention and if the corrensponding docker hub page,
        is existing.
        Args:
        docker_name      (str): The url to the docker hub page.
        check_for_page  (bool): Determines whether to control if the url corresponds to
                                an existing image on docker hub.
        Returns:
        bool: If it is a valid docker name.
        """
        # Distinguish between docker certified, and not docker certified.
        if "/" in docker_name:
            user_name, image_name = docker_name.split("/", 1)
            url_prefix = docker_hub_url['default']
            # controll valid docker id (https://docs.docker.com/docker-id/).
            if match(r'^([a-z]|[0,9]){4,30}\Z', user_name) is None:
                return False
        else:
            image_name = docker_name
            url_prefix = docker_hub_url['certified']
        url = url_prefix+docker_name
        # Controll the naming conventions (https://docs.docker.com/docker-hub/repos/).
        if not match(r'^([a-z]|[0,9]|[-,_]){2,255}\Z', image_name) is None:
            if not check_for_page:
                return True
            # Check if the page exists.
            try:
                get(url)
            except ConnectionError:
                return False
            # Load the http.
            else:
                htmlsession = HTMLSession()
                content = htmlsession.get(url)
                # Might install chromium.
                # Timeconsuming Step
                content.html.render()
                rendered_contend = content.html.search('<body{}/body>')
                # Exclude the default empty page on dockerhub.
                return not any(map(lambda x: 'data-testid="404page" alt="404 Route Not Found"'
                                   in x, rendered_contend))
        return False

    def _parse_site(self, metadata_json: JSON) -> Site:
        """Create a new site using a metadata json formated object.
        Args:
        metadata_json (JSON): A json formated str containing a 'short_name' and 'address' parameter
                              ,as well as maybe a 'name' parameter.
        Returns:
        Site: The new created Site object, is None if metadata_json doesn't
              contain the required parameters.
        """
        metadata = None
        try:
            metadata = json.loads(metadata_json)
        except json.JSONDecodeError:
            return None
        site = None
        # Helper function controlls that parameter is in metadata
        # and the associated value isn't empty.
        contained = lambda a: a in metadata and bool(a)
        # input validation
        if all(map(contained, ['short_name', 'address'])):
            # Create with or without name.
            if contained('name'):
                site = Site(metadata['short_name'],
                            metadata['address'], name=metadata['name'])
            else:
                site = Site(metadata['short_name'], metadata['address'])
            # add description if contaiend in metadata.
            if contained('description'):
                site.set_description(metadata['description'])
        return site

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
